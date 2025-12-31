# from django.urls import path
# from core import views

# urlpatterns = [
#     # ---------------------------
#     # Health Check
#     # ---------------------------
#     path("ping", views.ping, name="ping"),


#     # ---------------------------
#     # Authentication
#     # ---------------------------
#     path("login", views.login_view, name="login_user"),
#     path("logout", views.logout_view, name="logout_user"),
#     path("refresh", views.refresh_view, name="refresh_token"),
#     path("csrf/", views.get_csrf, name="csrf"),


#     # ---------------------------
#     # User Management
#     # ---------------------------
#     path("register", views.register_user, name="register_user"),
#     path("user", views.user_view, name="current_user"),
#     path("users/me", views.user_view, name="current_user_profile"),
#     path("current-user/", views.current_user, name="current-user"),


#     # ---------------------------
#     # Applications / Roles / Admin
#     # ---------------------------
#     path("apply/role", views.apply_role),
#     path("applications", views.list_applications),
#     path("applications/<uuid:app_id>/review", views.review_application),
#     path("admin/set-roles", views.set_user_roles),


#     # ---------------------------
#     # Analytics
#     # ---------------------------
#     path("admin/analytics/site", views.site_analytics),
#     path("admin/analytics/courses/<uuid:course_id>", views.course_stats),


#     # ---------------------------
#     # Email Verification
#     # ---------------------------
#     path("email/send-code", views.send_verification_code),
#     path("email/verify", views.verify_code),


#     # ---------------------------
#     # Notifications
#     # ---------------------------
#     path("notifications", views.list_notifications),
#     path("notifications/<uuid:notif_id>/read", views.mark_notification_read),


#     # ---------------------------
#     # Tutor / Course Management
#     # ---------------------------
#     # Public
#     path("courses/categories/", views.list_categories, name="list-categories"),
#     path("courses", views.list_courses, name="list-all-courses"),
#     path("courses/<uuid:course_id>", views.get_course, name="get_course"),
#     path("courses/featured/", views.random_featured_courses, name="featured-courses"),

#     # Tutor-specific
#     path("tutor/courses", views.tutor_course_list, name="list-my-courses"),
#     path("tutor/courses/create", views.create_course, name="create-course"),
#     path('tutor/courses/<uuid:course_id>', views.tutor_course_detail, name='tutor-course-detail'),

#     # Optionally, other tutor course actions
#     path("tutor/course/<uuid:id>/update/", views.tutor_course_update, name="tutor-course-update"),
#     path("tutor/course/<uuid:id>/delete/", views.tutor_course_delete, name="tutor-course-delete"),
#     path("tutor/courses/deleted", views.tutor_deleted_courses, 
#          name="tutor-deleted-courses"),
#     path("tutor/courses/<uuid:course_id>/restore", views.restore_course, 
#          name="tutor-course-restore"),

#     path("tutor/courses/<uuid:course_id>/lessons/add", views.add_lesson),
#     path("tutor/lessons/<uuid:lesson_id>/update", views.update_lesson),
#     path("tutor/lessons/<uuid:lesson_id>/delete", views.delete_lesson),
#     path("tutor/media/upload", views.upload_media),

#     # Modules
#     path("tutor/courses/<uuid:course_id>/modules/add", views.add_module, name="add-module"),
#     path("tutor/courses/<uuid:course_id>/modules/<uuid:module_id>", views.get_course_module,
#             name="get-module"),
#     path("tutor/courses/<uuid:course_id>/modules", views.list_course_modules, 
#             name="list-course-modules"),

#     path("tutor/courses/<uuid:course_id>/modules/<uuid:module_id>/update", views.update_module, name="update-module"),
#     path("tutor/courses/<uuid:course_id>/modules/<uuid:module_id>/delete", views.delete_module, name="delete-module"),
    

#     # Tutor Service and Control
#     path("tutor/dashboard-stats", views.tutor_dashboard_stats, name="tutor-dashboard-stats"),
#     path("tutor/students/", views.tutor_students, name="tutor-students-list"),
#     path('tutor/earnings/', views.tutor_earnings, name='tutor-earnings'),


#     # ---------------------------
#     # Student
#     # ---------------------------
#     path("courses", views.list_courses),
#     path("courses/<uuid:course_id>", views.course_detail),
#     path("lessons/<uuid:lesson_id>", views.lesson_detail),
#     path("courses/<uuid:course_id>/enroll", views.enroll_course),
#     path("my-enrollments", views.my_enrollments),


#     # ---------------------------
#     # Progress Tracking
#     # ---------------------------
#     path("enrollments/<uuid:enrollment_id>/lessons/<uuid:lesson_id>/complete", views.complete_lesson),
#     path("enrollments/<uuid:enrollment_id>/progress", views.view_progress),


#     # ---------------------------
#     # Certificates
#     # ---------------------------
#     path("enrollments/<uuid:enrollment_id>/certificate", views.issue_certificate),


#     # ---------------------------
#     # Admin Views
#     # ---------------------------
#     path("admin/overview-stats", views.admin_overview_stats, name="admin_overview_stats"),
#     path("admin/users", views.admin_users_list, name="admin_list_users"),
#     path("admin/courses", views.admin_list_courses, name="admin_list_courses"),
#     path("admin/courses/<uuid:course_id>", views.admin_delete_course, name="admin_delete_course"),
#     path("admin/settings", views.admin_settings, name="admin-settings"),
# ]