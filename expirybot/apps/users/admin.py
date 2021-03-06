from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    UserProfile, EmailAddressOwnershipProof, KeyOwnershipProof,
    SearchResultForKeysByEmail
)


@admin.register(SearchResultForKeysByEmail)
class SearchResultForKeysByEmailAdmin(admin.ModelAdmin):
    list_display = (
        'datetime',
        'email_address',
        'num_fingerprints',
    )

    search_fields = (
        'email_address__email_address',
        'key_fingerprints',
    )

    readonly_fields = (
        'email_address',
    )

    def num_fingerprints(self, instance):
        return len(instance.key_fingerprints)


@admin.register(EmailAddressOwnershipProof)
class EmailAddressOwnershipProofAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'profile')

    search_fields = (
        'email_address__email_address',
        'profile__user__username',
    )


@admin.register(KeyOwnershipProof)
class KeyOwnershipProofAdmin(admin.ModelAdmin):
    list_display = (
        'pgp_key',
        'profile',
        'created_at',
    )

    readonly_fields = (
        'pgp_key',
        'profile',
        'created_at',
    )

    search_fields = (
        'pgp_key__fingerprint',
        'profile__user__username',
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'created_at',
        'welcome_email_sent_datetime',
        'receive_occasional_feedback_requests',
        'notify_product_updates',
        'notify_email_addresses',
    )

    list_filter = (
        'created_at',
        'updated_at',
        'welcome_email_sent_datetime',
        'receive_occasional_feedback_requests',
        'notify_product_updates',
        'notify_email_addresses',
    )


class ProofsInline(admin.StackedInline):
    model = EmailAddressOwnershipProof


class UserProfileInline(admin.StackedInline):
    # Define an inline admin descriptor for UserProfile model
    # which acts a bit like a singleton
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

    readonly_fields = (
        'uuid',
        'created_at',
        'updated_at'
    )

    inlines = (ProofsInline,)


class UserAdmin(BaseUserAdmin):
    # Define a new User admin
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
