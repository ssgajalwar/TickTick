# demoapp/models.py
from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields specific to the admin profile

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields specific to the student profile

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields specific to the teacher profile

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    subjects = models.ManyToManyField('Subject',blank=True)

    def __str__(self):
        return self.course_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username


class RecordAttendance(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    rollno = models.CharField(max_length=20)
    date = models.DateField()
    attendance_status = models.BooleanField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255,blank=True,)
    latitude = models.CharField(max_length=255,blank=True)
    def __str__(self):
        return f"{self.username} - {self.date}"
    
class Lectures(models.Model):
    title = models.ForeignKey('Subject', on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    duration = models.FloatField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title}"
    
class QrCodeLog(models.Model):
    code = models.CharField(max_length=255)
    course =  models.CharField(max_length=255)   
    subject = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.course}-{self.subject}"
    
class LeaveApply(models.Model):
    rollno = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()    
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.rollno}"