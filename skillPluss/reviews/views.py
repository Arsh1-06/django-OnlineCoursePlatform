from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Student
from .models import Review
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    # Check if user is enrolled
    try:
        student = Student.objects.get(email=request.user.email)
        if course not in student.courses.all():
            messages.error(request, "You must be enrolled in the course to leave a review.")
            return redirect('courses:course_detail', course_id=course_id)
    except Student.DoesNotExist:
        messages.error(request, "You must be enrolled in the course to leave a review.")
        return redirect('courses:course_detail', course_id=course_id)
    
    # Check if user already has a review
    if Review.objects.filter(course=course, student=student).exists():
        messages.error(request, "You have already reviewed this course. You can edit your existing review.")
        return redirect('courses:course_detail', course_id=course_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            messages.error(request, "Both rating and comment are required.")
            return render(request, 'reviews/add_review.html', {'course': course})
        
        Review.objects.create(
            course=course,
            student=student,
            rating=rating,
            review=comment
        )
        messages.success(request, "Your review has been added successfully!")
        return redirect('courses:course_detail', course_id=course_id)
    
    return render(request, 'reviews/add_review.html', {'course': course})

@login_required
def edit_review(request, course_id, review_id):
    course = get_object_or_404(Course, course_id=course_id)
    student = get_object_or_404(Student, email=request.user.email)
    review = get_object_or_404(Review, id=review_id, student=student, course=course)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            messages.error(request, "Both rating and comment are required.")
            return render(request, 'reviews/edit_review.html', {
                'course': course,
                'review': review
            })
        
        review.rating = rating
        review.review = comment
        review.save()
        
        messages.success(request, "Your review has been updated successfully!")
        return redirect('courses:course_detail', course_id=course_id)
    
    return render(request, 'reviews/edit_review.html', {
        'course': course,
        'review': review
    })

@login_required
def delete_review(request, course_id, review_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, email=request.user.email)
        review = get_object_or_404(Review, id=review_id, student=student, course_id=course_id)
        review.delete()
        messages.success(request, "Your review has been deleted successfully!")
    
    return redirect('courses:course_detail', course_id=course_id) 