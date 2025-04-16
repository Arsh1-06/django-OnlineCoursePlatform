from django.contrib import admin
from .models import Course, Student, Category

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'cname', 'fee', 'duration')  

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'qualification', 'enrolled_courses')
    
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

admin.site.register(Course, CourseAdmin) 
admin.site.register(Student, StudentAdmin)
admin.site.register(Category, CategoryAdmin)
