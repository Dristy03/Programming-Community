from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin


# Register your models here.

# custom design for Admin panel
class AccountAdmin(UserAdmin):
    # what you want to show in admin panel for users
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'role')

    # search parameters
    search_fields = ('email', 'first_name',)
    readonly_fields = ('date_joined', 'last_login')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'date_joined', 'role','password1', 'password2'),
        }),
    )
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
