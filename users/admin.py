from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'created_at', 'is_active')
    # list_filter = ('role',)

    fieldsets = (
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'mobile', 'email', 'password','city','state','country','zipcode','address_1','address_2','house_or_building','road_or_area','landmark')}),
        (_('Permissions'), {'fields': ('is_admin', 'is_staff', 'is_active', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('mobile',)
    filter_horizontal = ('groups',)
    readonly_fields = ('created_at',)

