# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render
# from django.contrib.admin.views.decorators import staff_member_required
# from django.db.models import Sum
# from datetime import date

# from core.models import CustomUser, Course, Enrollment, Application, RoleApprovalLog, SiteAnalytics, CourseStats

# @staff_member_required
# def admin_dashboard(request):
#     # ----------------
#     # Users
#     # ----------------
#     total_users = CustomUser.objects.count()
#     active_users = CustomUser.objects.filter(is_active=True).count()
#     superusers = CustomUser.objects.filter(is_superuser=True).count()
#     admins = CustomUser.objects.filter(is_admin=True).count()
#     moderators = CustomUser.objects.filter(is_moderator=True).count()
#     tutors = CustomUser.objects.filter(is_tutor=True).count()
#     all_users = CustomUser.objects.all().order_by('-date_joined')  # for table

#     # ----------------
#     # Courses
#     # ----------------
#     total_courses = Course.objects.count()
#     published_courses = Course.objects.filter(is_published=True).count()
#     all_courses = Course.objects.all().order_by('-created_at')

#     # ----------------
#     # Enrollments & Certificates
#     # ----------------
#     total_enrollments = Enrollment.objects.count()
#     completed_enrollments = Enrollment.objects.filter(progress=100).count()
#     total_certificates = CourseStats.objects.aggregate(total_completions=Sum('completions'))['total_completions'] or 0

#     # ----------------
#     # Applications
#     # ----------------
#     pending_applications = Application.objects.filter(status='pending').count()
#     approved_applications = Application.objects.filter(status='approved').count()
#     rejected_applications = Application.objects.filter(status='rejected').count()
#     all_applications = Application.objects.all().order_by('-submitted_at')

#     # ----------------
#     # Analytics
#     # ----------------
#     today_metrics = SiteAnalytics.objects.filter(date=date.today()).first()

#     context = {
#         # Summary Cards
#         'total_users': total_users,
#         'active_users': active_users,
#         'superusers': superusers,
#         'admins': admins,
#         'moderators': moderators,
#         'tutors': tutors,
#         'total_courses': total_courses,
#         'published_courses': published_courses,
#         'total_enrollments': total_enrollments,
#         'completed_enrollments': completed_enrollments,
#         'total_certificates': total_certificates,
#         'pending_applications': pending_applications,
#         'approved_applications': approved_applications,
#         'rejected_applications': rejected_applications,
#         'today_metrics': today_metrics,

#         # Detailed lists
#         'all_users': all_users,
#         'all_courses': all_courses,
#         'all_applications': all_applications,
#     }

#     return render(request, 'admin/custom_dashboard.html', context)


# # ----------------
# # Hook custom dashboard into Django admin
# # ----------------
# original_get_urls = admin.site.get_urls

# def get_urls():
#     custom_urls = [
#         path('dashboard/', admin_dashboard, name='admin-dashboard'),
#     ]
#     return custom_urls + original_get_urls()

# admin.site.get_urls = get_urls