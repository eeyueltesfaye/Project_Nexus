from django.contrib import admin
from .models import JobCategory, Job, JobApplication, SavedJob


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    fields = ['applicant', 'status', 'resume', 'applied_at']
    readonly_fields = ['applied_at']
    autocomplete_fields = ['applicant']
    classes = ['collapse']

    def has_change_permission(self, request, obj=None):
        # Only admin or recruiters can edit
        return request.user.role in ['ADMIN', 'RECRUITER']

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['ADMIN', 'RECRUITER']


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'job_type', 'status', 'posted_by', 'posted_at']
    list_filter = ['job_type', 'status', 'category', 'location']
    search_fields = ['title', 'company_name', 'industry']
    readonly_fields = ['view_count', 'posted_at']
    autocomplete_fields = ['category', 'posted_by']
    ordering = ['-posted_at']
    inlines = [JobApplicationInline]
    list_select_related = ('category', 'posted_by')

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'ADMIN':
            return True
        if obj and obj.posted_by == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant_email', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__email', 'applicant__first_name', 'applicant__last_name']
    autocomplete_fields = ['job', 'applicant']
    ordering = ['-applied_at']
    list_select_related = ('job', 'applicant')

    @admin.display(description='Applicant Email')
    def applicant_email(self, obj):
        return obj.applicant.email

    actions = ['mark_reviewed']

    @admin.action(description='Mark selected applications as Reviewed')
    def mark_reviewed(self, request, queryset):
        queryset.update(status='REVIEWED')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'job', 'saved_at']
    search_fields = ['user__email', 'job__title']
    autocomplete_fields = ['user', 'job']
    ordering = ['-saved_at']

    @admin.display(description='User Email')
    def user_email(self, obj):
        return obj.user.email
