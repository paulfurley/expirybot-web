from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, EmailAddressOwnershipProof


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
