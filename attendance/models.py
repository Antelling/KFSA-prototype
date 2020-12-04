from django.db import models
from .utils import AttTypes

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User')

class Enrollment(models.Model):
    student_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course)

class Session(models.Model):
    date = models.DateTimeField()
    course = models.ForeignKey(Course)

class Attendance(models.Model):
    enrollment = models.ForeignKey(Enrollment)
    session = models.ForeignKey(Session)
    type = models.IntegerField(choices=AttTypes.choices(), default=AttTypes.absent)