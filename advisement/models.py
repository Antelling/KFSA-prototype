from django.db import models
from django.contrib.auth.models import User


class ChecksheetInstance(models.Model):
    template_filename = models.CharField(max_length=400)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=500)
    date = models.DateTimeField()

class Advisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="identity")
    students = models.ManyToManyField(User)

    def __str__(self):
        return "Advisor< " + self.user.username + " >"
