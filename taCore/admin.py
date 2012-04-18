from django.contrib import admin

from taCore.models import *


class DegreeAdmin(admin.ModelAdmin):
    pass

class CollegeAdmin(admin.ModelAdmin):
    pass

class SpecialityAdmin(admin.ModelAdmin):
    pass

class ClassAdmin(admin.ModelAdmin):
    pass

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('title', 'college', 'user')
    list_filter = ('user',)
    ordering = ('title',)
    search_field = ('tltle',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'college', 'speciality')
    
admin.site.register(Degree, DegreeAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
