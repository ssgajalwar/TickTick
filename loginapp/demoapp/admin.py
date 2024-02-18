from django.contrib import admin
from .models import AdminProfile, StudentProfile, TeacherProfile,Course,Student,Subject

admin.site.register(AdminProfile)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Subject)
