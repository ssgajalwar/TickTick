# yourappname/views.py
# demoapp/views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from .forms import  LeaveApplyForm, AdminRegistrationForm, StudentRegistrationForm, TeacherRegistrationForm,StudentAssignForm,CreateCourseForm,CreateSubjectForm,LecturesForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .decorator import allowed_users
from .models import Course,Subject,Student,RecordAttendance,Lectures,QrCodeLog
from .utils import unslugify
from datetime import date
from django.utils import timezone
from django.http import JsonResponse
from django.core.serializers import serialize
from .logic import *
import json
import geocoder
from geopy.geocoders import Nominatim

student_group, created = Group.objects.get_or_create(name='student')
admin_group, created = Group.objects.get_or_create(name='admin')
teacher_group, created = Group.objects.get_or_create(name='teacher')

backend='django.contrib.auth.backends.ModelBackend'

today_date = timezone.now().date()

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        print('user:',user)
        print('user authenticated',user.is_authenticated)
        print(user.groups)
        print(user.groups.all())
        if user.is_authenticated:
            if user.groups.filter(name='student').exists():
                return '/demoapp/student/'
            elif user.groups.filter(name='admin').exists():
                return '/demoapp/appadmin/'

            elif user.groups.filter(name='teacher').exists():
                return '/demoapp/teacher/'

        # Default redirect if no specific role is matched
        return '/default-redirect/'

    # You can override other methods if needed
def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        print(request.POST)
        print(form.is_valid(),'hello')
        if form.is_valid():

            username=form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                print("admin username is already taken")
                return render(request, 'registration/admin_registration.html', {'form': form})
            admin_user = User.objects.create_user(username=username, password=form.cleaned_data['password2'])
            admin_user.groups.add(admin_group)    
            print(admin_group.user_set.all())
            print('group added')
            # user = form.save()
            print('saved successfully')
            # login(request, user,backend=backend)
            return redirect('/demoapp/appadmin')
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration/admin_registration.html', {'form': form})

def student_registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        print(request.POST)
        print(form.is_valid(),'hello')
        if form.is_valid():

            username=form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                print("student username is already taken")
                return render(request, 'registration/student_registration.html', {'form': form})

            student_user = User.objects.create_user(username=username, password=form.cleaned_data['password2'])
            student_user.groups.add(student_group)
            print(student_group.user_set.all())
            print('group added')
            # user = form.save()
            print('saved successfully')
            # login(request, user,backend=backend)
            return redirect('/demoapp/appadmin/assignstudent/')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/student_registration.html', {'form': form})

def teacher_registration(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        print(request.POST)
        print(form.is_valid(),'hello')
        if form.is_valid():

            username=form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                print("teacher name is already taken")
                return render(request, 'registration/teacher_registration.html', {'form': form})
            
            teacher_user = User.objects.create_user(username=username, password=form.cleaned_data['password2'])
            teacher_user.groups.add(teacher_group)
            print(teacher_group.user_set.all())
            print('group added')
            # user = form.save()
            print('saved successfully')
            # login(request, user,backend=backend)
            return redirect('/demoapp/teacher')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'registration/teacher_registration.html', {'form': form})

@require_http_methods(["GET", "POST"])
@login_required(login_url='/demoapp/login/appadmin/')  # Specify your admin login URL
@allowed_users(allowed_roles=['admin'])
def admin_dashboard(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    subjects =  Subject.objects.all()
    return render(request, 'admin_dashboard.html', {
        'username': request.user.username,
        'students':students,
        'courses':courses,
        'subjects':subjects
        })

@require_http_methods(["GET", "POST"])
@login_required(login_url='/demoapp/login/student/')  # Specify your student login URL
@allowed_users(allowed_roles=['student'])
def student_dashboard(request):
    messages.info(request, f"Hello {request.user.username}, your role is student")
    return render(request, 'student_dashboard.html', {'username': request.user.username})

@require_http_methods(["GET", "POST"])
@login_required(login_url='/demoapp/login/teacher/')  # Specify your teacher login URL
@allowed_users(allowed_roles=['teacher'])
def teacher_dashboard(request):
    messages.info(request, f"Hello {request.user.username}, your role is teacher")
    return render(request, 'teacher_dashboard.html', {'username': request.user.username})

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def addcourse(request):
    print(request.method)
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'success_msg.html')
    form = CreateCourseForm()

    return render(request,'forms/addcourse.html',{
        'form':form
    })

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def addsubject(request):
    print(request.method)
    if request.method == 'POST':
        form = CreateSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'success_msg.html')
    form = CreateSubjectForm()
    return render(request,'forms/addsubject.html',{
        'form':form
    })

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def assignstudent(request):
    print(request.method)
    if request.method == 'POST':
        form = StudentAssignForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()    
            return redirect('/demoapp/appadmin/success')

    form = StudentAssignForm()
    return render(request,'forms/assignstudent.html',{
        'form':form
    })

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def courseDetail(request,course_name):
    print(unslugify(course_name))
    for_course = Course.objects.filter(course_name=course_name.upper()).first()

    data = Lectures.objects.filter(start=today_date,course=for_course)
    print(data)
    # data = Subject.objects.filter(course_id__course_name=course_name.upper()).values('subject_name').distinct()
    print(Subject.objects.filter(course_id__course_name='Btech'))
    return render(request,'coursedetail.html',{
        'data':data,
        'course_id':course_name
    })
@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def generateqr(request,course_name,subject_name):
    print(request.method)
    present_student = RecordAttendance.objects.all()
    if request.method == "POST":
        print("POST")
    else:    
        print(course_name)
        print(subject_name)

    return render(request,'generateqr.html',{
        'course_name':course_name,
        'subject_name':subject_name,
        'present_student':present_student,
        'present_length':len(present_student)
    })

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def allstudent(request,course_name):
    print("Show All Students for"+course_name)
    for_course = Course.objects.filter(course_name=course_name.upper()).first()
    allstudent_list = Student.objects.filter(course=for_course)
    return render(request,'allstudent.html',{
        'student_list':allstudent_list,
        'student_length':len(allstudent_list),
        'course_id':course_name

    })


@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def courseDashboard(request,course_name):
    print("Show All Students for"+course_name)
    for_course = Course.objects.filter(course_name=course_name.upper()).first()
    allstudent_list = Student.objects.filter(course=for_course)
    subject_list = Subject.objects.filter(course_id=for_course)
    print(subject_list)
    return render(request,'course_dashboard.html',{
        'student_list':allstudent_list,
        'student_length':len(allstudent_list),
        'course_id':course_name,
        'subject_list':json.dumps(list(subject_list.values()))

    })


@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def presentStudent(request,course_name):
    print("Show All Students for"+course_name)
    for_course = Course.objects.filter(course_name=course_name.upper()).first()
    # presentStudent = RecordAttendance.objects.all(course=for_course)
    
    records_today = RecordAttendance.objects.filter(date=today_date,course=for_course)
    unique_subjects = RecordAttendance.objects.filter(date=today_date,course=for_course).values_list('subject', flat=True).distinct()
    print(records_today)
    print(unique_subjects)
    return render(request,'presentStudent.html',{
        'present_student':records_today,
        'present_length':len(records_today),
        'course_id':course_name,
        'subject_list':unique_subjects
    })


@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def calender(request,course_name):
    print("Show Calender for"+course_name)
    for_course = Course.objects.filter(course_name=course_name.upper()).first()
    allstudent_list = Student.objects.filter(course=for_course)
    print(unslugify(course_name))
    data = Subject.objects.filter(course_id__course_name=for_course).values('subject_name').distinct()
    print(data,'-----')
    # data = Subject.objects.filter(course_id__course_name=course_name.upper()).values('subject_name').distinct()
    return render(request,'calender.html',{
        'subject_list':[item['subject_name'] for item in data],
        'student_list':allstudent_list,
        'student_length':len(allstudent_list),
        'course_id':course_name
    })

@login_required(login_url='/demoapp/login/student/')
@allowed_users(allowed_roles=['student'])
def markattendance(request,course_name,subject_name,code):
    # print(request.user)
    # print(course_name,subject_name,code,request.user.username)
    location = geocoder.ip('me')
    geolocator = Nominatim(user_agent="geoapiExercises")
    qrlocation = geolocator.reverse((request.GET.get('lat'), request.GET.get('lang')))
    user_city = location.city
    qr_location_city = qrlocation.raw.get('address', {}).get('city')

    # print(user_city)
    # print(qr_location_city)
    student = Student.objects.get(user=request.user.id)
    roll_no = student.roll_no
    code_exist = QrCodeLog.objects.filter(subject=subject_name).exists()
    print(code_exist)
    if code_exist:
        getcode =  QrCodeLog.objects.get(subject=subject_name)
        if getcode.code == code:
            # Check if a person with the given roll number and subject name exists for today
            roll_exist = RecordAttendance.objects.filter(rollno=roll_no, date=today_date).exists()
            subject_exist = RecordAttendance.objects.filter(subject=subject_name, date=today_date).exists()

            # If you want to check if both exist
            person_exist = RecordAttendance.objects.filter(rollno=roll_no, subject=subject_name, date=today_date).exists()
            print(roll_exist,subject_exist)
            print(person_exist)
            if person_exist:
                return HttpResponse("Attendance Already Existed: "+request.user.username)
            form = RecordAttendance(
                username=User.objects.get(username=request.user.username),
                rollno=roll_no,  # Assuming rollno is stored in the user's profile
                date=date.today(),
                attendance_status=True,
                course=Course.objects.get(course_name=course_name.upper()),
                subject=subject_name,
                longitude=request.GET.get('lang'),
                latitude=request.GET.get('lat')
            )
            # print(request.user.profile.roll_no)
            form.save()
            return HttpResponse("Attendance Marked Successfully for : "+request.user.username)

    # subject_obj = QrCodeLog.objects.all()
    # print(subject_obj)
    # print(subject_obj.code,code)

    # print(roll_no)
    # print(request.user.id)

    # details = course_name,subject_name,code
    return HttpResponse("Qr Code Expired : "+request.user.username)



@login_required()
def user_logout(request):
    logout(request)
    return redirect('/demoapp/hello') 

def hello(request):
    # print(User.objects.all())
    # print(Group.objects.all())
    return render(request,'hello.html')



def map(request):
    # Example usage
    latitude = 37.7749  # Example latitude
    longitude = -122.4194  # Example longitude

    location = get_location(latitude, longitude)
    print("Location:", location)

    return render(request,'map.html')


def leaveApply(request):
    form = LeaveApplyForm()

    return render(request,'student_dashboard.html',{
        'form': form
    })

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def holiday(request,course_name):

    return render(request,'holiday.html',{
        'course_id':course_name
    })

@login_required(login_url='/demoapp/login/appadmin/')
@allowed_users(allowed_roles=['admin'])
def holiday(request,course_name):

    return render(request,'holiday.html',{
        'course_id':course_name
    })


def forum(request,course_name):

    return render(request,'forum.html',{
        'course_id':course_name
    })

def lectures(request,course_name):
    if request.method == 'POST':
        # print(title=request.POST.get('title'))
        form = LecturesForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            print("Saved data")
        # data = Lectures.objects.all()
        # serialized_data = [{'title': obj.title, 'start': obj.start, 'end':obj.end} for obj in data]
        # Lectures.objects.create()
        return HttpResponse("Lecture added successfully")
            
    else:    
        for_course = Course.objects.filter(course_name=course_name.upper()).first()
        data = Lectures.objects.filter(course=for_course)
        print(data)
        serialized_data = []
        # serialized_data = [{'title': obj.title, 'start': obj.start, 'end':obj.end} for obj in data]
        for i in data:
            # print(i.title, i.start, i.end,i.course)
            # print(type(str(i.title))) 
            # print(i.course , course_name.upper())
            print("passed")
            temp = {'title':str(i.title), 'start': str(i.start), 'end':str(i.end)}
            serialized_data.append(temp)
            
            # print(subject_name)
        # Return JSON response
        return JsonResponse(serialized_data, safe=False)


def addLectures(request,course_name):
    form = LecturesForm(request.POST)
    # Return JSON response
    return render(request,'addlectures.html',{
        'form':form,
        'course_id':course_name
    })

def success(request):
    return render(request,'success.html',{
        # 'course_id':'course_name'
    })

def qrcodeLog(request,course_name,subject_name,code):
    subject_exists = QrCodeLog.objects.filter(subject=subject_name).exists()
    # if subject name already exist then ubdate otherwise create new
    if subject_exists:
        subject_obj = QrCodeLog.objects.get(subject=subject_name)
        subject_obj.code = code
        subject_obj.save()
        print('update')
    else:
        #create new object      
        obj = QrCodeLog.objects.create(code=code,course=course_name,subject=subject_name)
        obj.save()
    return HttpResponse('received')