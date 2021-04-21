from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import ChecksheetInstance, Advisee, ChecksheetTemplate
from accounts.models import Faculty
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os, json
from . import render_program
from .forms import AddChecksheet, AddAdvisee
from accounts.forms import PermissionSelect


"""homepage of the advisement system. Kind of dumb since advisement is the only system. """
def home(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("set_perm"))

    students = Advisee.objects.filter(advisors__in=[faculty])
    zipped = []
    for student in students:
        try:
            most_recent_advisement = ChecksheetInstance.objects.filter(advisee=student).order_by('-created_at')[0]
        except IndexError:
            most_recent_advisement = None
        zipped.append([student, most_recent_advisement, ", ".join([f.user.username for f in student.advisors.all()])])

    return render(request, 'advisement/adv_home.html', {'student_adv_pairs': zipped, 'faculty': faculty})



def add_advisement(request, advisee):
    advisee = Advisee.objects.get(pk=advisee)
    faculty = Faculty.objects.get(user=request.user)

    #check if there is already an advisement record for this user
    try:
        prev_adv = ChecksheetInstance.objects.filter(advisee=advisee).order_by("-pk")[0]
        data = prev_adv.data
    except IndexError:
        data = ""

    #create a new advisement recor_sessiond
    new_advisement = ChecksheetInstance(template=advisee.checksheet, advisee=advisee, advisor=faculty,
                                        data=data)
    new_advisement.save()

    #redirect to the edit view so reloading this page does not create duplicate records
    edit_url = reverse(new_edit_advisement, args=(new_advisement.pk,))
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
        past_advisements = ChecksheetInstance.objects.filter(advisee=advisement.advisee).exclude(id=advisement.id)\
            .order_by('-created_at')
        program = advisement.template.data
        html = render_program.render(json.loads(program), advisement.template.name)
        return render(request, "advisement/advisement.html", {'html': html, 'advisement': advisement, "editable": True, "record": past_advisements})


def view_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)
    past_advisements = ChecksheetInstance.objects.filter(advisee=advisement.advisee).exclude(id=advisement.id) \
        .order_by('-created_at')
    program = advisement.template.data
    html = render_program.render(json.loads(program), advisement.template.name)
    return render(request, "advisement/advisement.html",
                  {'html': html, 'advisement': advisement, "editable": False, "record": past_advisements})

def new_edit_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)
    if request.method == "POST":
        payload = request.POST.get("payload")
        payload = json.loads(payload)
        advisement.data = json.dumps(payload['serialization'])
        advisement.notes = payload['notes']
        advisement.save()
        return HttpResponse("save successful")
    else:
        past_advisements = ChecksheetInstance.objects.filter(advisee=advisement.advisee).exclude(id=advisement.id) \
            .order_by('-created_at')
        program = json.loads(advisement.template.data)
        return render(request, "checksheets/editor.html", {"program": program, 'advisement': advisement, "editable": False,
                                                            "record": past_advisements })

def new_view_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)
    past_advisements = ChecksheetInstance.objects.filter(advisee=advisement.advisee).order_by('-created_at')
    program = json.loads(advisement.template.data)
    return render(request, "checksheets/view_record.html", {"program": program, 'advisement': advisement, "editable": False,
                                                       "record": past_advisements })

def checksheet_listing(request):
    checksheets = ChecksheetTemplate.objects.all()
    for checksheet in checksheets:
        students = Advisee.objects.filter(checksheet=checksheet)
        if len(students.all()) > 0:
            checksheet.used = True
    return render(request, "advisement/checksheet_listing.html", {"checksheets": checksheets})

def add_checksheet(request):
    if request.method == "POST":
        form = AddChecksheet(request.POST)
        if form.is_valid():
            try:
                json.loads(form.cleaned_data["data"])

                #make sure the name is unique
                duplicates = ChecksheetTemplate.objects.filter(name=form.cleaned_data["name"]).delete()

                #save the new template
                form.save()

                #return the rendered HTML for the preview
                return HttpResponse("saved")
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
    zipped = []
    for advisee in advisees:
        try:
            most_recent_advisement = ChecksheetInstance.objects.filter(advisee=advisee).order_by('-created_at')[0]
        except IndexError:
            most_recent_advisement = None
        zipped.append([advisee, most_recent_advisement, ", ".join([f.user.username for f in advisee.advisors.all()])])
    return render(request, "advisement/list_advisees.html", {'advisee_pairs': zipped})


def edit_advisee(request, advisee):
    student = Advisee.objects.get(pk=advisee)
    if request.method == "POST":
        form = AddAdvisee(request.POST)
        if form.is_valid():
            student.name = request.POST.get("name")
            student.id_number = request.POST.get("id_number")
            student.advisors.set(request.POST.get("advisors"))
            student.checksheet = ChecksheetTemplate.objects.get(pk=request.POST.get("checksheet"))
            student.save()
            return HttpResponseRedirect(reverse("advisee_list"))
    else:
        form = AddAdvisee(initial={'name':student.name,
                                   'id_number':student.id_number,
                                   'advisors':student.advisors.all,
                                   'checksheet':student.checksheet
                                   })
        # form = AddAdvisee()
        return render(request, "advisement/edit_advisee.html", {"form": form})


def faculty_list(request):
    advisors = Faculty.objects.all()
    return render(request, "advisement/list_faculty.html", {'advisors': advisors})


def edit_faculty(request, faculty):
    advisor = Faculty.objects.get(pk=faculty)
    if request.method == "POST":
        advisor.can_advise = request.POST.get("can_advise")=="on"
        advisor.can_upload_checksheets = request.POST.get("can_upload_checksheets")=="on"
        advisor.can_add_students = request.POST.get("can_add_students")=="on"
        advisor.can_assign_students = request.POST.get("can_assign_students")=="on"
        advisor.can_manage_students = request.POST.get("can_manage_students")=="on"
        advisor.can_manage_faculty = request.POST.get("can_manage_faculty")=="on"
        advisor.save()
        return HttpResponseRedirect(reverse("faculty_list"))
    else:
        form = PermissionSelect(initial={'can_advise':advisor.can_advise,
                                         'can_upload_checksheets':advisor.can_upload_checksheets,
                                         'can_add_students':advisor.can_add_students,
                                         'can_assign_students':advisor.can_assign_students,
                                         'can_manage_students':advisor.can_manage_students,
                                         'can_manage_faculty':advisor.can_manage_faculty
                                         })
        return render(request, "advisement/edit_faculty.html", {"form": form})

def delete_checksheet(request):
    name = request.POST.get("name")
    checksheet = ChecksheetTemplate.objects.get(name=name)
    students = Advisee.objects.filter(checksheet=checksheet)
    hmm = len(students.all())
    if len(students.all()) > 0:
        return HttpResponse("cannot delete this checksheet, it has students using it. ")
    else:
        checksheet.delete()
        return HttpResponseRedirect(reverse("list_checksheets"))

def view_template(request, template):
    template = ChecksheetTemplate.objects.get(pk=template)
    program = json.loads(template.data)
    return render(request, "checksheets/view_template.html", {"program": program, "template": template})
