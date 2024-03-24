from django.contrib import admin
from .models import AdminProfile, StudentProfile, TeacherProfile,Course,Student,Subject,RecordAttendance,Lectures,QrCodeLog,LeaveApply
from django.contrib.auth.models import User 

admin.site.register(AdminProfile)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(RecordAttendance)
admin.site.register(Lectures)
admin.site.register(QrCodeLog)
admin.site.register(LeaveApply)
# admin.site.register(User)