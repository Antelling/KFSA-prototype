from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Advisor, Student, ChecksheetInstance
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os, json
from . import render_program

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

    #get or create student record
    try:
        student = Student.objects.get(user=user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(f"../../add_major/{user.pk}") #FIXME: replace relative redirect with named reference

    advisement_sessions = ChecksheetInstance.objects.filter(student=student)
    return render(request, "advisement/student_overview.html", {"student": student, "advisements": advisement_sessions})


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
    #gather the student and advisor objects
    student_user = User.objects.get(pk=student)
    student = Student.objects.get(user=student_user)
    advisor = Advisor.objects.get(user=request.user)

    #check if there is already an advisement record for this user
    try:
        prev_adv = ChecksheetInstance.objects.filter(student=student).order_by("-pk")[0]
        data = prev_adv.data
    except IndexError:
        data = ""

    #create a new advisement record
    new_advisement = ChecksheetInstance(template_filename=student.template_filename, student=student, advisor=advisor,
                                        data=data)
    new_advisement.save()

    #redirect to the edit view so reloading this page does not create duplicate records
    edit_url = reverse(edit_advisement, args=(new_advisement.pk,))
    return HttpResponseRedirect(edit_url)


def edit_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)
    if request.method == "POST":
        advisement.data = request.POST.get("serialization")
        advisement.notes = request.POST.get("notes")
        advisement.save()
        return HttpResponse("save successful")
    else:
        # render a checksheet to html
        program = open(os.path.join(os.getcwd(), "advisement/checksheet_templates",
                                    advisement.template_filename), "r").read()
        html = render_program.render(json.loads(program),
                                     str(advisement.template_filename.split(".")[0]).replace("_", " "))
        return render(request, "advisement/advisement.html", {'html': html, 'advisement': advisement, "editable": True})


def view_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)
    program = open(os.path.join(os.getcwd(), "advisement/checksheet_templates",
                                advisement.template_filename), "r").read()
    html = render_program.render(json.loads(program),
                                 str(advisement.template_filename.split(".")[0]).replace("_", " "))
    return render(request, "advisement/advisement.html", {'html': html, 'advisement': advisement, "editable": False})
