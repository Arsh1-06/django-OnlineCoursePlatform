from django.contrib import admin
from .models import Course, Student, Category

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'cname', 'fee', 'duration')  # Display columns

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'qualification', 'enrolled_courses')
    
    # To display the gender as radio button
    radio_fields = {'gender': admin.VERTICAL}

    def enrolled_courses(self, obj):
        course_names = []
        for course in obj.courses.all():
            course_names.append(course.cname)
        return ", ".join(course_names)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Course, CourseAdmin)  # Register Course with CourseAdmin
admin.site.register(Student, StudentAdmin)  # Register Student with StudentAdmin
admin.site.register(Category, CategoryAdmin)
