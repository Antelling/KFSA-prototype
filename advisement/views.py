from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Advisor, Student, ChecksheetInstance, Advisee, ChecksheetTemplate
from accounts.models import Faculty
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os, json
from . import render_program
from .forms import CreateAdvisorStudentPair, StudentChecksheetSelect, AddChecksheet, AddAdvisee

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
        faculty = Faculty.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("set_perm"))

    students = Advisee.objects.filter(advisors__in=[faculty])
    return render(request, 'advisement/adv_home.html', {'students': students, 'faculty': faculty})


def advisee_overview(request, advisee):
    advisee = Advisee.objects.get(pk=advisee)
    advisement_sessions = ChecksheetInstance.objects.filter(advisee=advisee)
    return render(request, "advisement/student_overview.html", {"advisee": advisee, "advisements": advisement_sessions})


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


def add_advisement(request, advisee):
    advisee = Advisee.objects.get(pk=advisee)
    faculty = Faculty.objects.get(user=request.user)

    #check if there is already an advisement record for this user
    try:
        prev_adv = ChecksheetInstance.objects.filter(advisee=advisee).order_by("-pk")[0]
        data = prev_adv.data
    except IndexError:
        data = ""

    #create a new advisement record
    new_advisement = ChecksheetInstance(template=advisee.checksheet, advisee=advisee, advisor=faculty,
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
        program = advisement.template.data
        html = render_program.render(json.loads(program), advisement.template.name)
        return render(request, "advisement/advisement.html", {'html': html, 'advisement': advisement, "editable": True})


def view_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)
    program = advisement.template.data
    html = render_program.render(json.loads(program), advisement.template.name)
    return render(request, "advisement/advisement.html", {'html': html, 'advisement': advisement, "editable": False})


def checksheet_listing(request):
    checksheets = ChecksheetTemplate.objects.all()
    return render(request, "advisement/checksheet_listing.html", {"checksheets": checksheets})

def add_checksheet(request):
    if request.method == "POST":
        form = AddChecksheet(request.POST)
        if form.is_valid():
            try:
                html = render_program.render(json.loads(form.cleaned_data["data"]), form.cleaned_data["name"])

                #make sure the name is unique
                duplicates = ChecksheetTemplate.objects.filter(name=form.cleaned_data["name"]).delete()

                #save the new template
                form.save()

                #return the rendered HTML for the preview
                return HttpResponse(html)
            except Exception as e:
                return HttpResponse(str(e))
    else:
        form = AddChecksheet()
        return render(request, "advisement/upload_checksheet.html", {"checksheet": form})


def add_students(request):
    if request.method == "POST":
        form = AddAdvisee(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("add_students"))
    else:
        form = AddAdvisee()
        return render(request, "advisement/add_advisee.html", {"form": form})

def advisee_list(request):
    advisees = Advisee.objects.all()
    return render(request, "advisement/list_advisees.html", {'advisees': advisees})

def edit_advisee(request, advisee):
    if request.method == "POST":
        pass
    else:
        return HttpResponse("edit an advisee")
