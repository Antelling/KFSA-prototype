import os
from django import forms
from . import models
from accounts.models import Faculty
from django.contrib.auth.models import User
from django.forms import TextInput

def get_checksheet_options():
    options = os.listdir(os.path.join(os.getcwd(), "advisement/checksheet_templates"))
    return [(opt, opt.replace("_", " ").replace(".json", "")) for opt in options]

class StudentChecksheetSelect(forms.Form):
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=get_checksheet_options())

class AddChecksheet(forms.ModelForm):
    class Meta:
        model = models.ChecksheetTemplate
        fields = "__all__"

class AddAdvisee(forms.ModelForm):
    class Meta:
        model = models.Advisee
        fields = "__all__"

    advisors = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              queryset=Faculty.objects.filter(can_advise=True))

