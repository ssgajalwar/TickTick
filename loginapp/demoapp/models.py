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

    def __str__(self):
        return self.user.username
