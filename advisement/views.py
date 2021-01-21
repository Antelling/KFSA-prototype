from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Advisor, Student
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.urls import reverse

from .forms import CreateAdvisorStudentPair, StudentChecksheetSelect

def add_advisee(request):
    if request.method == "POST":
        form = CreateAdvisorStudentPair(request.POST)
        if form.is_valid():
            advisor = Advisor.objects.get(user=request.user)
            students = form.cleaned_data.get("students")
            advisor.students.clear()
            for student in students:
                advisor.students.add(student)
            advisor.save()
            return HttpResponseRedirect("/advisement/")
    else:
        try:
            advisor = Advisor.objects.get(user=request.user)
            print(advisor)
            # form = CreateAdvisorStudentPair(advisor.students.all())
            form = CreateAdvisorStudentPair() #TODO: make form auto-fill with existing info
        except ObjectDoesNotExist:
            form = CreateAdvisorStudentPair()

    return render(request, 'advisement/add_adv_student_pair.html', {'form': form})


def home(request):
    try:
        advisor = Advisor.objects.get(user=request.user)
        print(advisor.students.all())
    except MultipleObjectsReturned:  #TODO: remove these development safeguard cases
        advisors = Advisor.objects.filter(user=request.user)
        advisors.delete()
        return HttpResponse("numerous advisement records returned, deleted them all")
    except ObjectDoesNotExist:
        advisor = Advisor.objects.create(user=request.user)
        advisor.save()
        return HttpResponse("created new advisor for this user.")
    return render(request, 'advisement/adv_home.html', {'students': advisor.students.all()})


def student_overview(request, student):
    user = User.objects.get(pk=student)
    try:
        student = Student.objects.get(user=user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(f"../../add_major/{user.pk}") #FIXME: replace relative redirect with named reference
    return render(request, "advisement/student_overview.html", {"student": student})

def add_major(request, student):
    student_user = User.objects.get(pk=student)
    if request.method == "POST":
        form = StudentChecksheetSelect(request.POST)
        if form.is_valid():
            student = Student(user=student_user, template_filename=form.cleaned_data.get("choice"))
            student.save()
            return HttpResponseRedirect(f"../../add_advisement/{student_user.pk}/") #FIXME: bad relative hardcoding

        else:
            return HttpResponse("error saving major")
    else:
        form = StudentChecksheetSelect()
        return render(request, "advisement/add_major.html", {"form": form})

def add_advisement(request, student):
    student_user = User.objects.get(pk=student)
    student = Student.objects.get(user=student_user)
    return HttpResponse(f"making an advisement record for {student_user.username}. Major is {student.template_filename}")
