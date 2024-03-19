from django.urls import path
from django.contrib.auth.views import LoginView
from .views import addLectures,lectures,presentStudent,calender,allstudent,markattendance,generateqr,courseDetail,assignstudent,addsubject,addcourse,CustomLoginView,admin_dashboard, student_dashboard, teacher_dashboard,hello,admin_registration,student_registration,teacher_registration,user_logout
from . import views
app_name = 'demoapp'

urlpatterns = [
    path('hello/',views.hello,name='hello'),
    path('appadmin/', views.admin_dashboard, name='admin_dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('login/appadmin/', CustomLoginView.as_view(template_name='appadmin_login.html'), name='admin_login'),
    path('login/student/', CustomLoginView.as_view(template_name='student_login.html'), name='student_login'),
    path('login/teacher/', CustomLoginView.as_view(template_name='teacher_login.html'), name='teacher_login'),
    path('admin/register/', admin_registration, name='admin_registration'),
    path('student/register/', student_registration, name='student_registration'),
    path('teacher/register/', teacher_registration, name='teacher_registration'),
    path('logout/', user_logout, name='user_logout'),
    path('appadmin/success/', views.success, name='success'),
    path('appadmin/addcourse/', addcourse, name='addcourse'),
    path('appadmin/addsubject/', addsubject, name='addsubject'),
    path('appadmin/assignstudent/', assignstudent, name='assignstudent'),

    path('appadmin/coursedetail/<slug:course_name>', courseDetail, name='coursedetail'),
    path('appadmin/coursedetail/dashboard/<slug:course_name>', views.courseDashboard, name='coursedashboard'),
    path('appadmin/coursedetail/holiday/<slug:course_name>', views.holiday, name='holiday'),
    path('appadmin/coursedetail/forum/<slug:course_name>', views.forum, name='forum'),
    path('appadmin/coursedetail/allstudent/<slug:course_name>', allstudent, name='allstudent'),
    path('appadmin/coursedetail/present/<slug:course_name>', presentStudent, name='presentStudent'),
    path('appadmin/coursedetail/calender/<slug:course_name>', calender, name='calender'),
    path('appadmin/coursedetail/lectures/<slug:course_name>', lectures, name='lectures'),
    path('appadmin/coursedetail/lectures/<slug:course_name>/addlecture', addLectures, name='addLectures'),
    path('appadmin/generateqr/<slug:course_name>/<slug:subject_name>', generateqr, name='generateqr'),
    path('appadmin/qrcodelog/<slug:course_name>/<slug:subject_name>/<slug:code>', views.qrcodeLog, name='qrcodelog'),

    path('student/markattendance/<slug:course_name>/<slug:subject_name>/<slug:code>',markattendance,name="markattendance")
#     # Add more URLs as needed
]
