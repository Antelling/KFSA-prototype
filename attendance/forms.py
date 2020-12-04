from django import forms
from . import models

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        exclude = ["user"]
