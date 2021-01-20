from django import forms
from . import models
from django.contrib.auth.models import User
from django.forms import TextInput

class CreateAdvisorStudentPair(forms.ModelForm):
    class Meta:
        model = models.Advisor
        fields = ['students']

    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
