import re

from django.core.exceptions import ValidationError
from django.db import models

from .cryptographic_key import CryptographicKey
from .mixins import ExpiryCalculationMixin


def validate_fingerprint(string):
    def validate_openpgp_v4_fingerprint(string):
        return bool(re.match('^[A-F0-9]{40}$', string))

    def validate_openpgp_v3_fingerprint(string):
        return bool(re.match('^[A-F0-9]{16}$', string))

    if not validate_openpgp_v4_fingerprint(string) \
            and not validate_openpgp_v3_fingerprint(string):
        raise ValidationError('Not an OpenPGP v3 or v4 fingerprint: {}'.format(
            string))


class PGPKey(CryptographicKey, ExpiryCalculationMixin):

    fingerprint = models.CharField(
        help_text=(
            "The 40-character key fingerprint without spaces."
        ),
        max_length=40,
        primary_key=True,
        validators=[
            validate_fingerprint,
        ],
    )

    last_synced = models.DateTimeField(null=True, blank=True)

    creation_date = models.DateField(null=True, blank=False)

    expiry_date = models.DateField(null=True, blank=True)

    revoked = models.BooleanField(default=False)

    @property
    def human_fingerprint(self):
        if len(self.fingerprint) == 40:
            return '{} {} {} {} {}  {} {} {} {} {}'.format(  # nbsp
                self.fingerprint[0:4],
                self.fingerprint[4:8],
                self.fingerprint[8:12],
                self.fingerprint[12:16],
                self.fingerprint[16:20],
                self.fingerprint[20:24],
                self.fingerprint[24:28],
                self.fingerprint[28:32],
                self.fingerprint[32:36],
                self.fingerprint[36:40]
            )
        else:
            return self.fingerprint

    def __str__(self):
        return self.zero_x_fingerprint

    @property
    def zero_x_fingerprint(self):
        return '0x{}'.format(self.fingerprint)

    @property
    def key_id(self):
        return '0x{}'.format(self.fingerprint[-16:])

    @property
    def uids_string(self):
        return ', '.join(str(uid) for uid in self.uids.all())

    @property
    def email_addresses(self):
        return list(filter(
            None,
            (uid.email_address for uid in self.uids.all())
        ))

    @property
    def uids(self):
        return self.uids_set.all()

    @property
    def subkeys(self):
        return self.subkeys_set.all()