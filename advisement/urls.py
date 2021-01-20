from django.urls import path

from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='adv_home'),
    path('add_advisee/', views.add_advisee, name="add_advisee")
]


