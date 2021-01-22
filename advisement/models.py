from django.db import models
from django.contrib.auth.models import User

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

class ChecksheetInstance(models.Model):
    template_filename = models.CharField(max_length=400)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    data = models.TextField()
    date = models.DateTimeField(auto_now=True)
    notes = models.TextField()
