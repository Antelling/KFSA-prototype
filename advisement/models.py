from django.db import models
from django.contrib.auth.models import User
from accounts.models import Faculty

class Advisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="identity")
    students = models.ManyToManyField(User)

    def __str__(self):
        return "Advisor< " + self.user.username + " >"

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_identity")
    template_filename = models.CharField(max_length=400)

    def __str__(self):
        return "Student< " + self.user.username + " >"




class ChecksheetTemplate(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    data = models.TextField()

    def __str__(self):
        return self.name

class Advisee(models.Model):
    name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=10)
    advisors = models.ManyToManyField(Faculty)
    checksheet = models.ForeignKey(ChecksheetTemplate, on_delete=models.PROTECT)

class ChecksheetInstance(models.Model):
    template = models.ForeignKey(ChecksheetTemplate, on_delete=models.PROTECT)
    advisee = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    data = models.TextField()
    date = models.DateTimeField(auto_now=True)
    notes = models.TextField()

    def __str__(self):
        return "ChecksheetInstance<advisor: " + self.advisor.user.username + ", student: " + self.advisee.name \
              + ">"

