import os
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

def get_checksheet_options():
    options = os.listdir(os.path.join(os.getcwd(), "advisement/checksheet_templates"))
    return [(opt, opt.replace("_", " ").replace(".json", "")) for opt in options]

class StudentChecksheetSelect(forms.Form):
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=get_checksheet_options())
