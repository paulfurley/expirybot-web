import datetime
import logging
import requests


from django.core.management.base import BaseCommand
# from django.db import transaction
from django.conf import settings
from django.utils import timezone

from expirybot.apps.blacklist.models import EmailAddress
from expirybot.apps.blacklist.utils import (
    record_bounce, delete_bounce_from_mailgun, parse_mailgun_date
)
from expirybot.apps.status.models import EventLatestOccurrence

LOG = logging.getLogger(__name__)



class Command(BaseCommand):
    help = ('Updates keys from the keyserver')

    def handle(self, *args, **options):
        sync_mailgun_suppressions()


def sync_mailgun_suppressions():
    for (email, unsubscribe_datetime) in get_unsubscribes():
        record_unsubscribe(email, unsubscribe_datetime)

    for (email, complain_datetime) in get_complaints():
        record_complaint(email, complain_datetime)

    for (email, bounce_datetime) in get_bounces():
        if record_bounce(email, bounce_datetime):
            delete_bounce_from_mailgun(email)

    EventLatestOccurrence.record_event('sync-mailgun-suppressions-succeeded')


def get_unsubscribes():
    return get_suppression('unsubscribes')


def get_complaints():
    return get_suppression('complaints')


def get_bounces():
    return get_suppression('bounces')


def get_suppression(type_):
    api_key = settings.MAILGUN_API_KEY
    if not api_key:
        raise RuntimeError('Bad Mailgun API key: {}'.format(api_key))

    url = 'https://api.mailgun.net/v3/{domain}/{type_}?limit=1000'.format(
        domain=settings.MAILGUN_DOMAIN, type_=type_
    )

    urls_processed = set()

    for _ in range(50):  # don't rely only on `break`
        response = requests.get(url, auth=('api', api_key))
        response.raise_for_status()

        for item in response.json()['items']:
            email = item['address']
            created_at = parse_mailgun_date(item['created_at'])

            yield email, created_at

        urls_processed.add(url)

        url = response.json()['paging']['next']  # Mailgun 'next' loop round :(
        if url in urls_processed:
            break


def record_unsubscribe(email, unsubscribed_at):
    obj, new = EmailAddress.objects.get_or_create(email_address=email)
    LOG.info("unsubscribe {} - {}".format(email, unsubscribed_at))

    if obj.unsubscribe_datetime:
        obj.unsubscribe_datetime = min(
            unsubscribed_at, obj.unsubscribe_datetime
        )
    else:
        obj.unsubscribe_datetime = unsubscribed_at

    obj.save()


def record_complaint(email, complain_datetime):
    obj, new = EmailAddress.objects.get_or_create(email_address=email)
    LOG.info("complain {} - {}".format(email, complain_datetime))

    if obj.complain_datetime:
        obj.complain_datetime = min(
            complain_datetime, obj.complain_datetime
        )
    else:
        obj.complain_datetime = complain_datetime

    obj.save()
