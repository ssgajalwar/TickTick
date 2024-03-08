# yourappname/forms.py
from django.contrib.auth.models import User 
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Student, Course, Subject

class AdminLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

class StudentLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

class TeacherLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class StudentRegistrationForm(UserCreationForm):
    # roll_no = forms.CharField(max_length=20)
    # course = forms.ModelChoiceField(queryset=Course.objects.all())
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class StudentAssignForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'course','roll_no']  

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'subjects']        

class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'course_id']        
