from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="faculty_identity")
    can_advise = models.BooleanField()
    can_upload_checksheets = models.BooleanField()
    can_add_students = models.BooleanField()
    can_assign_students = models.BooleanField()
    can_manage_students = models.BooleanField()
    can_manage_faculty = models.BooleanField()

    def __str__(self):
        return "Faculty< " + self.user.username + " >"
