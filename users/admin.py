from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile, RoleRequest
from jobs.models import JobApplication, SavedJob
from django.contrib.auth.models import Permission
from django.utils import timezone


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['codename', 'name']
    list_display = ['name', 'codename', 'content_type']
    list_filter = ['content_type']


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ['profile_completed']
    classes = ['collapse']


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    fields = ('job', 'status', 'applied_at')
    readonly_fields = ('applied_at',)
    show_change_link = True
    autocomplete_fields = ['job']
    classes = ['collapse']

    def has_change_permission(self, request, obj=None):
        return request.user.role in ['ADMIN', 'JOB_SEEKER']

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['ADMIN', 'JOB_SEEKER']


class SavedJobInline(admin.TabularInline):
    model = SavedJob
    extra = 0
    fields = ('job', 'saved_at')
    readonly_fields = ('saved_at',)
    show_change_link = True
    autocomplete_fields = ['job']
    classes = ['collapse']

    def has_change_permission(self, request, obj=None):
        return request.user.role in ['ADMIN', 'JOB_SEEKER']

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['ADMIN', 'JOB_SEEKER']


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    autocomplete_fields = ['groups', 'user_permissions']
    readonly_fields = ['last_login']

    inlines = [ProfileInline, JobApplicationInline, SavedJobInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

    def get_fieldsets(self, request, obj=None):
        if request.user.role == 'ADMIN':
            return super().get_fieldsets(request, obj)
        # restrict fields for non-admin users
        return (
            (None, {'fields': ('email', 'password')}),
            (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'country', 'profile_completed')
    search_fields = ('user__email', 'phone_number', 'country')
    list_filter = ('gender', 'country', 'profile_completed')
    autocomplete_fields = ['user']
    readonly_fields = ['profile_completed']
    classes = ['collapse']

# users/admin.py

from .models import RoleRequest

@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_role', 'approved', 'reviewed', 'requested_at', 'reviewed_at')
    list_filter = ('approved', 'reviewed', 'requested_role')
    search_fields = ('user__email',)
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for req in queryset.filter(reviewed=False):
            user = req.user
            user.role = req.requested_role
            user.save()

            req.approved = True
            req.reviewed = True
            req.reviewed_at = timezone.now()
            req.save()

        self.message_user(request, "Selected requests have been approved and users updated.")
