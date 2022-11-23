from django.contrib import admin
from .models import NewUser, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email',)
    list_filter = ('email', 'is_active', 'is_staff', 'is_moderator')
    ordering = ('-start_date',)
    inlines = [UserProfileInline]
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff', 'is_moderator')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
