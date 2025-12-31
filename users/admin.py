# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _
# from core.models import (
#     CustomUser,
#     Course,
#     Lesson,
#     Enrollment,
#     LessonProgress,
#     Certificate,
#     Application,
#     RoleApprovalLog,
#     SiteAnalytics,
#     CourseStats,
#     Notification,
#     EmailVerification,
# )

# # ---------------------------
# # ADMIN ACTIONS
# # ---------------------------
# def ban_users(modeladmin, request, queryset):
#     queryset.update(is_active=False)
# ban_users.short_description = "Ban selected users (deactivate accounts)"

# def unban_users(modeladmin, request, queryset):
#     queryset.update(is_active=True)
# unban_users.short_description = "Unban selected users (activate accounts)"

# def make_student(modeladmin, request, queryset):
#     """
#     Appoint selected users as moderator (application-level).
#     Only superusers or existing admins can perform this action.
#     """
#     # Check if the requester is allowed
#     if not request.user.is_superuser and not getattr(request.user, "is_admin", False):
#         modeladmin.message_user(request, "You do not have permission to promote users.", level="error")
#         return

#     for user in queryset:
#         user.is_student = True
#         user.save()
#     modeladmin.message_user(request, "Selected users have been promoted to Student.")


# def revoke_student(modeladmin, request, queryset):
#     """Remove admin privileges"""
#     for user in queryset:
#         user.is_student = False
#         user.save()
# revoke_student.short_description = "Revoke Student privileges"

# def make_tutor(modeladmin, request, queryset):
#     """
#     Appoint selected users as moderator (application-level).
#     Only superusers or existing admins can perform this action.
#     """
#     # Check if the requester is allowed
#     if not request.user.is_superuser and not getattr(request.user, "is_admin", False):
#         modeladmin.message_user(request, "You do not have permission to promote users.", level="error")
#         return

#     for user in queryset:
#         user.is_tutor = True
#         user.save()
#     modeladmin.message_user(request, "Selected users have been promoted to tutor.")


# def revoke_tutor(modeladmin, request, queryset):
#     """Remove admin privileges"""
#     for user in queryset:
#         user.is_tutor = False
#         user.save()
# revoke_tutor.short_description = "Revoke Tutor privileges"

# def make_moderator(modeladmin, request, queryset):
#     """
#     Appoint selected users as moderator (application-level).
#     Only superusers or existing admins can perform this action.
#     """
#     # Check if the requester is allowed
#     if not request.user.is_superuser and not getattr(request.user, "is_admin", False):
#         modeladmin.message_user(request, "You do not have permission to promote users.", level="error")
#         return

#     for user in queryset:
#         user.is_moderator = True
#         user.save()
#     modeladmin.message_user(request, "Selected users have been promoted to moderator.")


# def revoke_moderator(modeladmin, request, queryset):
#     """Remove admin privileges"""
#     for user in queryset:
#         user.is_moderator = False
#         user.save()
# revoke_moderator.short_description = "Revoke Moderator privileges"

# def make_admin(modeladmin, request, queryset):
#     """
#     Appoint selected users as admin (application-level).
#     Only superusers or existing admins can perform this action.
#     """
#     # Check if the requester is allowed
#     if not request.user.is_superuser and not getattr(request.user, "is_admin", False):
#         modeladmin.message_user(request, "You do not have permission to promote users.", level="error")
#         return

#     for user in queryset:
#         user.is_admin = True
#         user.is_staff = True  # Ensure access to admin site
#         user.save()
#     modeladmin.message_user(request, "Selected users have been promoted to admin.")


# def revoke_admin(modeladmin, request, queryset):
#     """Remove admin privileges"""
#     for user in queryset:
#         user.is_admin = False
#         user.is_staff = False
#         user.save()
# revoke_admin.short_description = "Revoke Admin privileges"


# def approve_applications(modeladmin, request, queryset):
#     for app in queryset.filter(status='pending'):
#         app.status = 'approved'
#         app.save()
#         # Auto-create RoleApprovalLog
#         RoleApprovalLog.objects.create(
#             user=app.applicant,
#             role=app.role,
#             approved_by=request.user
#         )
# approve_applications.short_description = "Approve selected applications"


# def reject_applications(modeladmin, request, queryset):
#     queryset.filter(status='pending').update(status='rejected')
# reject_applications.short_description = "Reject selected applications"


# # ---------------------------
# # CUSTOM USER ADMIN
# # ---------------------------
# @admin.register(CustomUser)
# class CustomUserAdmin(BaseUserAdmin):
#     actions = [ban_users, unban_users, make_student, revoke_student, make_tutor, revoke_tutor, make_moderator, revoke_moderator, make_admin, revoke_admin]

#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'full_name', 'password', 'avatar')}),
#         (_('Roles & Permissions'), {'fields': (
#             'is_student', 'is_tutor', 'is_moderator', 'is_admin', 'is_staff', 'is_superuser')}),
#         (_('Status'), {'fields': ('is_active', 'is_email_verified')}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'username', 'email', 'full_name', 'password1', 'password2',
#                 'is_student', 'is_tutor', 'is_moderator', 'is_admin', 'is_staff', 'is_superuser'
#             )}
#         ),
#     )

#     list_display = ('username', 'email', 'full_name', 'is_student', 'is_tutor', 'is_moderator', 'is_admin', 'is_staff', 'is_superuser', 'is_active')
#     list_filter = ('is_student', 'is_tutor', 'is_moderator', 'is_admin', 'is_staff', 'is_superuser', 'is_active')
#     search_fields = ('username', 'email', 'full_name')
#     ordering = ('username',)
#     list_editable = ('is_active', 'is_admin')


# # ---------------------------
# # COURSE & LESSONS
# # ---------------------------
# class LessonInline(admin.TabularInline):
#     model = Lesson
#     extra = 0
#     fields = ('title', 'video_url', 'created_at', 'updated_at')
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     inlines = [LessonInline]
#     list_display = ('title', 'tutor', 'is_published', 'created_at', 'updated_at')
#     list_filter = ('is_published',)
#     search_fields = ('title', 'tutor__email', 'tutor__username')
#     ordering = ('-created_at',)


# # ---------------------------
# # ENROLLMENT & LESSON PROGRESS
# # ---------------------------
# class LessonProgressInline(admin.TabularInline):
#     model = LessonProgress
#     extra = 0
#     fields = ('lesson', 'completed', 'completed_at')
#     readonly_fields = ('completed_at',)

# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     inlines = [LessonProgressInline]
#     list_display = ('student', 'course', 'progress', 'enrolled_at')
#     search_fields = ('student__email', 'course__title')
#     ordering = ('-enrolled_at',)


# @admin.register(Certificate)
# class CertificateAdmin(admin.ModelAdmin):
#     list_display = ('enrollment', 'issued_at', 'file_url')
#     search_fields = ('enrollment__student__email', 'enrollment__course__title')
#     ordering = ('-issued_at',)


# # ---------------------------
# # APPLICATIONS & ROLE LOG
# # ---------------------------
# @admin.register(Application)
# class ApplicationAdmin(admin.ModelAdmin):
#     actions = [approve_applications, reject_applications]
#     list_display = ('applicant', 'role', 'status', 'reviewer', 'submitted_at', 'reviewed_at')
#     list_filter = ('role', 'status')
#     search_fields = ('applicant__email', 'reviewer__email')
#     ordering = ('-submitted_at',)


# @admin.register(RoleApprovalLog)
# class RoleApprovalLogAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role', 'approved_by', 'approved_at')
#     search_fields = ('user__email', 'approved_by__email')
#     ordering = ('-approved_at',)


# # ---------------------------
# # ANALYTICS & STATS
# # ---------------------------
# @admin.register(SiteAnalytics)
# class SiteAnalyticsAdmin(admin.ModelAdmin):
#     list_display = ('date', 'new_users', 'new_courses', 'new_enrollments')
#     ordering = ('-date',)


# @admin.register(CourseStats)
# class CourseStatsAdmin(admin.ModelAdmin):
#     list_display = ('course', 'date', 'enrollments', 'completions')
#     search_fields = ('course__title',)
#     ordering = ('-date',)


# # ---------------------------
# # NOTIFICATIONS
# # ---------------------------
# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'title', 'is_read', 'created_at')
#     list_filter = ('is_read',)
#     search_fields = ('user__email', 'title')
#     ordering = ('-created_at',)


# # ---------------------------
# # EMAIL VERIFICATIONS
# # ---------------------------
# @admin.register(EmailVerification)
# class EmailVerificationAdmin(admin.ModelAdmin):
#     list_display = ('email', 'code', 'used', 'created_at')
#     list_filter = ('used',)
#     search_fields = ('email', 'code')
#     ordering = ('-created_at',)