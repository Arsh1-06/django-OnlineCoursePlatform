from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('about/', views.about, name='about'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/direct-enroll/', views.direct_enroll, name='direct_enroll'),
    path('course/<int:course_id>/rate/', views.rate_course, name='rate_course'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.view_lesson, name='view_lesson'),
    path('category/<int:category_id>/', views.category_courses, name='category_courses'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('pricing/', views.pricing, name='pricing'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/course/create/', views.create_course, name='create_course'),
    path('instructor/course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('instructor/course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('instructor/course/<int:course_id>/lessons/', views.manage_lessons, name='manage_lessons'),
    path('instructor/course/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('instructor/course/<int:course_id>/lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('instructor/course/<int:course_id>/lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('instructor/course/<int:course_id>/lessons/reorder/', views.reorder_lessons, name='reorder_lessons'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_user_profile, name='edit_profile'),
] 