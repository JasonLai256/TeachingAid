from django.contrib import admin

from taCore.models import *


class DegreeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'college')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('title', 'college', 'user')
    list_filter = ('user',)
    ordering = ('title',)
    search_field = ('tltle',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'college', 'speciality')
    
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AppraisalAdmin(admin.ModelAdmin):
    list_display = ('slug', 'course', 'student')

admin.site.register(Degree, DegreeAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Appraisal, AppraisalAdmin)
