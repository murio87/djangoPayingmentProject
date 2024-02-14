from django.contrib import admin
from .models import AccountPeople
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_admin', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(AccountPeople, AccountAdmin)
