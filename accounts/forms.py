from django import forms

class AddStudentForm(forms.Form):
    name = forms.CharField(label='Student Name', max_length=100)
    id = forms.CharField(label="Student ID Number", max_length=100)


class PermissionSelect(forms.Form):
    can_advise = forms.BooleanField(required=False)
    can_upload_checksheets = forms.BooleanField(required=False)
    can_add_students = forms.BooleanField(required=False)
    can_assign_students = forms.BooleanField(required=False)
    can_manage_students = forms.BooleanField(required=False)
    can_manage_faculty = forms.BooleanField(required=False)
