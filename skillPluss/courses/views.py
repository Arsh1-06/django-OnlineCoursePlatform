from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Course, Category, Lesson, Student, Rating, UserProfile, LessonResource, CompletedLesson
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    categories = Category.objects.all()[:8]  
    featured_courses = Course.objects.all().order_by('-created_at')[:8]  
    return render(request, 'courses/home.html', {
        'categories': categories,
        'featured_courses': featured_courses
    })

def course_list(request):
    courses = Course.objects.filter(instructor__isnull=False)  
    categories = Category.objects.all()
    

    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(cname__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)
    
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'user': request.user
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    ratings = Rating.objects.filter(course=course).order_by('-created_at')
    
    is_enrolled = False
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(email=request.user.email)
            is_enrolled = student.courses.filter(course_id=course.course_id).exists()
            
            print(f"User: {request.user.email}, Is Enrolled: {is_enrolled}")
            print(f"Student courses: {[c.course_id for c in student.courses.all()]}")
            print(f"Course ID: {course.course_id}")
            print(f"Student ID: {student.id}")
            print(f"Student name: {student.name}")
            print(f"Student email: {student.email}")
            print(f"Course name: {course.cname}")
            print(f"Course instructor: {course.instructor}")
            print(f"Course fee: {course.fee}")
            print(f"Course status: {course.status}")
            
            student.refresh_from_db()
            
            is_enrolled = student.courses.filter(course_id=course.course_id).exists()
            print(f"Enrollment status after refresh: {is_enrolled}")
            print(f"Student courses after refresh: {[c.course_id for c in student.courses.all()]}")
        except Student.DoesNotExist:
            print(f"Student does not exist for user: {request.user.email}")
            pass
    
    context = {
        'course': course,
        'ratings': ratings,
        'is_enrolled': is_enrolled
    }
    
    return render(request, 'courses/course_detail.html', context)

def category_courses(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_courses.html', {
        'category': category,
        'courses': courses
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    try:
        student = Student.objects.get(email=request.user.email)
        if course in student.courses.all():
            messages.warning(request, 'You are already enrolled in this course!')
            return redirect('courses:course_detail', course_id=course.course_id)
    except Student.DoesNotExist:
        student = Student.objects.create(
            email=request.user.email,
            name=request.user.get_full_name() or request.user.username,
            gender='O',  
            qualification=''  
        )
    
    if request.method == 'POST':
        if course.fee > 0:
            messages.info(request, f'Please complete the payment of ₹{course.fee} to access the course.')
            return render(request, 'courses/payment.html', {
                'course': course,
                'student': student
            })
        else:
            student.courses.add(course)
            student.refresh_from_db()
            messages.success(request, f'Successfully enrolled in {course.cname}!')
            return redirect('courses:course_detail', course_id=course.course_id)
    
    return render(request, 'courses/enroll.html', {'course': course})

def pricing(request):
    return render(request, 'courses/pricing.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('courses:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'courses/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'courses/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'courses/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'courses/register.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )
        
        profile = UserProfile.objects.create(
            user=user,
            role=role,
            bio=request.POST.get('bio', '')
        )
        
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
        
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('courses:home')
    
    return render(request, 'courses/register.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('courses:home')

@login_required
def instructor_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access the instructor dashboard.')
        return redirect('courses:login')
    
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'instructor':
        messages.error(request, 'You do not have instructor privileges.')
        return redirect('courses:home')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor/dashboard.html', {'courses': courses})

@login_required
def create_course(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to create a course.')
        return redirect('courses:login')
    
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'instructor':
        messages.error(request, 'You do not have instructor privileges.')
        return redirect('courses:home')
    
    if request.method == 'POST':
        try:
            course = Course.objects.create(
                instructor=request.user,
                cname=request.POST['cname'],
                description=request.POST['description'],
                category_id=request.POST['category'],
                fee=request.POST['fee'],
                level=request.POST['level'],
                status=request.POST['status'],
                requirements=request.POST['requirements'],
                what_you_will_learn=request.POST['what_you_will_learn']
            )
            
            if 'image' in request.FILES:
                course.image = request.FILES['image']
                course.save()
            
            messages.success(request, 'Course created successfully!')
            return redirect('courses:instructor_dashboard')
        except Exception as e:
            messages.error(request, f'Error creating course: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'courses/instructor/create_course.html', {'categories': categories})

@login_required
def manage_lessons(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'Access denied. You are not the instructor of this course.')
        return redirect('courses:home')
    
    lessons = course.lessons.all().order_by('order')
    return render(request, 'courses/instructor/manage_lessons.html', {
        'course': course,
        'lessons': lessons
    })

@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'Access denied. You are not the instructor of this course.')
        return redirect('courses:home')
    
    if request.method == 'POST':
        try:
            lesson = Lesson.objects.create(
                course=course,
                title=request.POST['title'],
                description=request.POST['description'],
                type=request.POST['type'],
                duration=request.POST['duration'],
                order=course.lessons.count() + 1
            )
            
            if lesson.type == 'video':
                lesson.video_url = request.POST['video_url']
            elif lesson.type == 'text':
                lesson.content = request.POST['text_content']
            elif lesson.type == 'quiz':
                lesson.content = request.POST['quiz_questions']
            elif lesson.type == 'assignment':
                lesson.content = request.POST['assignment_details']
            
            lesson.save()
            
            if 'resources' in request.FILES:
                for file in request.FILES.getlist('resources'):
                    LessonResource.objects.create(
                        lesson=lesson,
                        file=file,
                        filename=file.name
                    )
            
            messages.success(request, 'Lesson added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding lesson: {str(e)}')
    
    return redirect('courses:manage_lessons', course_id=course_id)

@login_required
def edit_lesson(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    
    if request.user != lesson.course.instructor:
        messages.error(request, 'Access denied. You are not the instructor of this course.')
        return redirect('courses:home')
    
    if request.method == 'POST':
        try:
            lesson.title = request.POST['title']
            lesson.description = request.POST['description']
            lesson.type = request.POST['type']
            lesson.duration = request.POST['duration']
            
            if lesson.type == 'video':
                lesson.video_url = request.POST['video_url']
            elif lesson.type == 'text':
                lesson.content = request.POST['text_content']
            elif lesson.type == 'quiz':
                lesson.content = request.POST['quiz_questions']
            elif lesson.type == 'assignment':
                lesson.content = request.POST['assignment_details']
            
            lesson.save()
            messages.success(request, 'Lesson updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating lesson: {str(e)}')
    
    return redirect('courses:manage_lessons', course_id=course_id)

@login_required
def delete_lesson(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    
    if request.user != lesson.course.instructor:
        messages.error(request, 'Access denied. You are not the instructor of this course.')
        return redirect('courses:home')
    
    if request.method == 'POST':
        try:
            lesson.delete()
            messages.success(request, 'Lesson deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting lesson: {str(e)}')
    
    return redirect('courses:manage_lessons', course_id=course_id)

@login_required
def reorder_lessons(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lesson_order = data.get('lesson_order', [])
            
            course = get_object_or_404(Course, course_id=course_id)
            if request.user != course.instructor:
                return JsonResponse({'error': 'Access denied'}, status=403)
            
            for index, lesson_id in enumerate(lesson_order, 1):
                Lesson.objects.filter(id=lesson_id, course=course).update(order=index)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def user_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view your profile.')
        return redirect('courses:login')
    
    user = request.user
    
    try:
        profile = user.userprofile
    except:
        profile = UserProfile.objects.create(
            user=user,
            role='student'
        )
    
    if profile.role == 'instructor':
        courses = Course.objects.filter(instructor=user)
        return render(request, 'courses/instructor/profile.html', {
            'user': user,
            'courses': courses
        })
    else:
        try:
            student = Student.objects.get(email=user.email)
        except Student.DoesNotExist:
            student = Student.objects.create(
                email=user.email,
                name=user.get_full_name() or user.username,
                gender='O',
                qualification=''
            )
        
        enrolled_courses = student.courses.all()
        
        for course in enrolled_courses:
            total_lessons = course.lessons.count()
            completed_lessons = student.completed_lessons.filter(lesson__course=course)
            completed_count = completed_lessons.count()
            
            course.total_lessons_count = total_lessons
            course.completed_lessons_count = completed_count
            course.progress_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
        
        return render(request, 'courses/student/profile.html', {
            'user': user,
            'enrolled_courses': enrolled_courses
        })

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'courses/categories/manage.html', {'categories': categories})

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            Category.objects.create(name=name, description=description)
            messages.success(request, 'Category added successfully!')
            return redirect('courses:manage_categories')
        else:
            messages.error(request, 'Category name is required.')
    
    return render(request, 'courses/categories/form.html', {'action': 'Add'})

@staff_member_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            category.name = name
            category.description = description
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('courses:manage_categories')
        else:
            messages.error(request, 'Category name is required.')
    
    return render(request, 'courses/categories/form.html', {
        'action': 'Edit',
        'category': category
    })

@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('courses:manage_categories')
    
    return render(request, 'courses/categories/delete.html', {'category': category})

@login_required
def edit_user_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to edit your profile.')
        return redirect('courses:login')
    
    user = request.user
    try:
        profile = user.userprofile
    except:
        profile = UserProfile.objects.create(
            user=user,
            role='student'
        )
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', user.email)
        user.save()
        
        profile.bio = request.POST.get('bio', '')
        
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('courses:profile')
    
    return render(request, 'courses/edit_profile.html', {
        'user': user,
        'profile': profile
    })

@login_required
def rate_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    try:
        student = Student.objects.get(email=request.user.email)
        if course not in student.courses.all():
            messages.error(request, 'You must be enrolled in the course to rate it.')
            return redirect('courses:course_detail', course_id=course_id)
    except Student.DoesNotExist:
        messages.error(request, 'You must be enrolled in the course to rate it.')
        return redirect('courses:course_detail', course_id=course_id)
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review = request.POST.get('review', '')
        
        if rating_value:
            rating, created = Rating.objects.get_or_create(
                course=course,
                student=student,
                defaults={
                    'rating': rating_value,
                    'review': review,
                    'email': request.user.email
                }
            )
            
            if not created:
                rating.rating = rating_value
                rating.review = review
                rating.save()
            
            messages.success(request, 'Thank you for rating this course!')
        else:
            messages.error(request, 'Please provide a rating.')
    
    return redirect('courses:course_detail', course_id=course_id)

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You do not have permission to edit this course.')
        return redirect('courses:instructor_dashboard')
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        cname = request.POST.get('cname')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        fee = request.POST.get('fee')
        duration = request.POST.get('duration')
        requirements = request.POST.get('requirements')
        what_you_will_learn = request.POST.get('what_you_will_learn')
        level = request.POST.get('level')
        status = request.POST.get('status')
        
        course.cname = cname
        course.description = description
        course.category_id = category_id
        course.fee = fee
        course.duration = duration
        course.requirements = requirements
        course.what_you_will_learn = what_you_will_learn
        course.level = level
        course.status = status
        
        if request.FILES.get('image'):
            if course.image:
                course.image.delete()
            course.image = request.FILES['image']
        
        try:
            course.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('courses:instructor_dashboard')
        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')
    
    return render(request, 'courses/instructor/edit_course.html', {
        'course': course,
        'categories': categories
    })

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You do not have permission to delete this course.')
        return redirect('courses:instructor_dashboard')
    
    if request.method == 'POST':
        try:
            if course.image:
                course.image.delete()
            
            course.delete()
            messages.success(request, 'Course deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting course: {str(e)}')
    
    return redirect('courses:instructor_dashboard')

@login_required
def view_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, course_id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    is_enrolled = False
    try:
        student = Student.objects.get(email=request.user.email)
        is_enrolled = student.courses.filter(course_id=course.course_id).exists()
        
        if not is_enrolled:
            messages.error(request, 'You must be enrolled in this course to access lessons.')
            return redirect('courses:course_detail', course_id=course_id)
            
        CompletedLesson.objects.get_or_create(student=student, lesson=lesson)
            
    except Student.DoesNotExist:
        messages.error(request, 'You must be enrolled in this course to access lessons.')
        return redirect('courses:course_detail', course_id=course_id)
    
    all_lessons = course.lessons.all().order_by('order')
    
    current_index = 0
    for i, l in enumerate(all_lessons):
        if l.id == lesson.id:
            current_index = i
            break
    
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'current_index': current_index
    })

@login_required
def direct_enroll(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    
    if request.method != 'POST':
        return redirect('courses:course_detail', course_id=course.course_id)
    
    try:
        student = Student.objects.get(email=request.user.email)
        if student.courses.filter(course_id=course.course_id).exists():
            messages.warning(request, 'You are already enrolled in this course!')
            return redirect('courses:course_detail', course_id=course.course_id)
    except Student.DoesNotExist:
        student = Student.objects.create(
            email=request.user.email,
            name=request.user.get_full_name() or request.user.username,
            gender='O',  
            qualification=''  
        )
    
    if course.fee > 0:
        if request.POST.get('payment_completed') == 'true':
            try:
                student.courses.add(course)
                student.save()
                
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'status': 'success',
                        'message': f'Successfully enrolled in {course.cname}!'
                    })
                
                messages.success(request, f'Successfully enrolled in {course.cname}!')
                return redirect('courses:course_detail', course_id=course.course_id)
            except Exception as e:
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=500)
                messages.error(request, f'Error enrolling in course: {str(e)}')
                return redirect('courses:course_detail', course_id=course.course_id)
        else:
            return render(request, 'courses/payment.html', {
                'course': course,
                'student': student
            })
    else:
        student.courses.add(course)
        messages.success(request, f'Successfully enrolled in {course.cname}!')
        return redirect('courses:course_detail', course_id=course.course_id)

def about(request):
    """
    View for the About Us page
    """
    return render(request, 'courses/about.html')

def help_support(request):
    """
    View for the combined help and support page.
    Handles both the FAQ display and contact form submission.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        topic = request.POST.get('topic')
        message = request.POST.get('message')
        
        messages.success(request, 'Your message has been sent. We will get back to you soon!')
        return redirect('courses:help_support')
        
    return render(request, 'courses/help_support.html')
