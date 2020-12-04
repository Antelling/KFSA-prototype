from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import AddCourseForm
from . import models
# from django.apps.auth import User

class AddStudentView(CreateView):
    form_class = AddCourseForm
    success_url = reverse_lazy('../')
    template_name = 'attendance/add_course.html'


class AddStudentView(CreateView):
    model = models.Course
    form_class = AddCourseForm
    template_name = 'attendance/add_course.html'

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.user = UserProfile.objects.get(user=self.request.user)  # use your own profile here
    #     candidate.save()
    #     return HttpResponseRedirect(self.get_success_url())