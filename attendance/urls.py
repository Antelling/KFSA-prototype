from django.urls import path

from django.views.generic.base import TemplateView
from .views import AddStudentView

urlpatterns = [
    path('', TemplateView.as_view(template_name='attendance/att_home.html'), name='att_home'),
    path('add_course/', AddStudentView.as_view(), name="add_course")
]


