# yourappname/forms.py
from django.contrib.auth.models import User 
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Student, Course, Subject,Lectures,LeaveApply

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

class LecturesForm(forms.ModelForm):
    class Meta:
        model = Lectures
        fields = ['title', 'start', 'end', 'duration','course']

    def __init__(self, *args, **kwargs):
        super(LecturesForm, self).__init__(*args, **kwargs)
        # Add the DateInput widget to the start and end fields

        subject_choices = Subject.objects.all().values_list('id', 'subject_name')
        self.fields['title'].choices = [(subject[0], subject[1]) for subject in subject_choices]        
        self.fields['start'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end'].widget = forms.DateInput(attrs={'type': 'date'})

class LeaveApplyForm(forms.ModelForm):
    class Meta:
        model = LeaveApply
        fields = ['rollno','start','end','course','reason']
    def __init__(self,*args,**kwargs):
        super(LecturesForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end'].widget = forms.DateInput(attrs={'type': 'date'})