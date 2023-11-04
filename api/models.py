from djongo import models
from datetime import datetime

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=30)
    enrollment_no = models.BigIntegerField()
    branch = models.CharField(max_length=10)
    semester = models.IntegerField()
    password = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=20, null=True)
    image = models.CharField(max_length=500, null=True)


class Attendance(models.Model):
    enrollment_no = models.BigIntegerField()
    date = models.DateField(null=True)
    semester = models.IntegerField(null=True)
    branch = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=10, default="Absent")
    subject_code = models.IntegerField()

class Session(models.Model):
    session_id = models.BigIntegerField()
    faculty_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=150, null=True)
    ip = models.CharField(max_length=50, null=True)


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    employee_id = models.IntegerField()
    branch = models.CharField(max_length=20)
    password = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=20)
    image = models.CharField(max_length=500, null=True)
    subjects = models.TextField(null=True, blank=True)

    def set_subjects(self, subjects_list):
        self.subjects = ','.join(subjects_list)

    def get_subjects(self):
        return self.subjects.split(',') if self.subjects else []

    def _str_(self):
        return self.name 