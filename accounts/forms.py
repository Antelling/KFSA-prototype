from django import forms

class AddStudentForm(forms.Form):
    name = forms.CharField(label='Student Name', max_length=100)
    id = forms.CharField(label="Student ID Number", max_length=100)