from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('course/<int:course_id>/add/', views.add_review, name='add_review'),
    path('course/<int:course_id>/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('course/<int:course_id>/delete/<int:review_id>/', views.delete_review, name='delete_review'),
] 