from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import ChecksheetInstance, Advisee, ChecksheetTemplate
from accounts.models import Faculty
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os, json
from .forms import AddChecksheet, AddAdvisee
from accounts.forms import PermissionSelect
from django.core.signing import BadSignature
from django.http import Http404
import urllib

"""homepage of the advisement system. Kind of dumb since advisement is the only system. """
@login_required
def home(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
    except ObjectDoesNotExist:
        #return HttpResponseRedirect(reverse("set_perm"))
        fac = Faculty(user=request.user,
                      can_advise=False,
                      can_add_students=False,
                      can_assign_students=False,
                      can_manage_faculty=False,
                      can_manage_students=False,
                      can_upload_checksheets=False)
        fac.save()
        faculty = Faculty.objects.get(user=request.user)

    students = Advisee.objects.filter(advisors__in=[faculty])
    zipped = []
    for student in students:
        try:
            most_recent_advisement = ChecksheetInstance.objects.filter(advisee=student).order_by('-created_at')[0]
        except IndexError:
            most_recent_advisement = None
        zipped.append([student, most_recent_advisement, ", ".join([f.user.username for f in student.advisors.all()])])

    return render(request, 'advisement/adv_home.html', {'student_adv_pairs': zipped, 'faculty': faculty})


"""Create a new advisment record"""
@login_required
def add_advisement(request, advisee):
    advisee = Advisee.objects.get(pk=advisee)
    faculty = Faculty.objects.get(user=request.user)

    #check that user is an advisor
    if not faculty.can_advise:
        return HttpResponse("You are not an advisor.")

    #check that this advisee lists the faculty as an advisor
    if not faculty in advisee.advisors.all():
        return HttpResponse("You are not an advisor of this student.")

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

    #redirect to the edit view
    edit_url = reverse(edit_advisement, args=(new_advisement.pk,))
    return HttpResponseRedirect(edit_url)

"""Edit an advisement record"""
@login_required
def edit_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)

    #security checks
    advisee = advisement.advisee
    faculty = Faculty.objects.get(user=request.user)
    #check that user is an advisor
    if not faculty.can_advise:
        return HttpResponse("You are not an advisor.")
    #check that this advisee lists the faculty as an advisor
    if not faculty in advisee.advisors.all():
        return HttpResponse("You are not an advisor of this student.")

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
        with open(advisement.template.data_file, "r") as data_file:
            program = json.loads(data_file.read())
        return render(request, "checksheets/editor.html", {"program": program, 'advisement': advisement, "editable": False,
                                                            "record": past_advisements })
"""View an advisement record.
Only available to advisors of the record's advisee."""
@login_required
def view_advisement(request, advisement):
    advisement = ChecksheetInstance.objects.get(pk=advisement)

    #security checks
    advisee = advisement.advisee
    faculty = Faculty.objects.get(user=request.user)
    #check that user is an advisor
    if not faculty.can_advise:
        return HttpResponse("You are not an advisor.")
    #check that this advisee lists the faculty as an advisor
    if not faculty in advisee.advisors.all():
        return HttpResponse("You are not an advisor of this student.")

    past_advisements = ChecksheetInstance.objects.filter(advisee=advisement.advisee).order_by('-created_at')
    with open(advisement.template.data_file, "r") as data_file:
        program = json.loads(data_file.read())
    url = advisement.advisee.get_absolute_url()
    return render(request, "checksheets/view_record.html", {"program": program, 'advisement': advisement, "editable": False,
                                                       "share_url": url, "record": past_advisements })

"""List all the checksheets in the system, and determine wether or not any advisees list the checksheet as their 
program."""
@login_required
def checksheet_listing(request):
    checksheets = ChecksheetTemplate.objects.all()
    for checksheet in checksheets:
        students = Advisee.objects.filter(checksheet=checksheet)
        if len(students.all()) > 0:
            checksheet.used = True
    return render(request, "advisement/checksheet_listing.html", {"checksheets": checksheets})

"""Add a new checksheet to the system."""
@login_required
def add_checksheet(request):

    #security check
    faculty = Faculty.objects.get(user=request.user)
    if not faculty.can_upload_checksheets:
        return HttpResponse("You do not have permission to upload checksheets.")

    if request.method == "POST":
        form = AddChecksheet(request.POST)
        if form.is_valid():
            try:
                json.loads(form.cleaned_data["data"])

                #make sure the name is unique
                ChecksheetTemplate.objects.filter(name=form.cleaned_data["name"]).delete()

                #save the new template
                form.save()

                #return the rendered HTML for the preview
                return HttpResponse("saved")
            except Exception as e:
                return HttpResponse(str(e))
    else:
        form = AddChecksheet()
        return render(request, "advisement/upload_checksheet.html", {"checksheet": form})



"""Add a new advisee to the system."""
@login_required
def add_students(request):
    faculty = Faculty.objects.get(user=request.user)
    if not faculty.can_add_students:
        return HttpResponse("You do not have permission to add students.")

    if request.method == "POST":
        form = AddAdvisee(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("add_students"))
    else:
        form = AddAdvisee()
        return render(request, "advisement/add_advisee.html", {"form": form})


"""List all of the students in the system.
Used to manage student records."""
@login_required
def advisee_list(request):
    faculty = Faculty.objects.get(user=request.user)
    if not faculty.can_manage_students:
        return HttpResponse("You do not have permission to manage students.")
    advisees = Advisee.objects.all()
    zipped = []
    for advisee in advisees:
        try:
            most_recent_advisement = ChecksheetInstance.objects.filter(advisee=advisee).order_by('-created_at')[0]
        except IndexError:
            most_recent_advisement = None
        zipped.append([advisee, most_recent_advisement, ", ".join([f.user.username for f in advisee.advisors.all()])])
    return render(request, "advisement/list_advisees.html", {'advisee_pairs': zipped})


"""Edit an advisee record."""
def edit_advisee(request, advisee):
    faculty = Faculty.objects.get(user=request.user)
    if not faculty.can_manage_students:
        return HttpResponse("You do not have permission to manage students.")
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
        return render(request, "advisement/edit_advisee.html", {"form": form})


"""List all faculty in the system."""
@login_required
def faculty_list(request):
    faculty = Faculty.objects.get(user=request.user)
    if not faculty.can_manage_faculty:
        return HttpResponse("You do not have permission to manage faculty.")
    advisors = Faculty.objects.all()
    return render(request, "advisement/list_faculty.html", {'advisors': advisors})


"""Edit a faculty record"""
@login_required
def edit_faculty(request, faculty):
    user = Faculty.objects.get(user=request.user)
    if not user.can_manage_faculty:
        return HttpResponse("You do not have permission to manage faculty.")
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

"""delete a checksheet.
Only possible if checksheets do not have any students.
Checksheet parameter passed in via POST.
Called from form submission in list checksheets template."""
def delete_checksheet(request):
    #security check
    faculty = Faculty.objects.get(user=request.user)
    if not faculty.can_upload_checksheets:
        return HttpResponse("You do not have permission to manage programs.")

    name = request.POST.get("name")
    checksheet = ChecksheetTemplate.objects.get(name=name)

    #constraint check
    students = Advisee.objects.filter(checksheet=checksheet)
    if len(students.all()) > 0:
        return HttpResponse("cannot delete this checksheet, it has students using it. ")
    else:
        #delete and return to list checksheets
        checksheet.delete()
        return HttpResponseRedirect(reverse("list_checksheets"))


"""View a rendered program by itself, with no additional UI. Not linked to by anywhere in the app, but 
acessible via direct URL. Useful for checking that new program definitions have a correct and appealing rendered 
appearance."""
@login_required
def view_template(request, template):
    template = ChecksheetTemplate.objects.get(pk=template)
    with open(template.data_file, "r") as data_file:
        program = json.loads(data_file.read())
    return render(request, "checksheets/view_template.html", {"program": program, "template": template})

"""View a students transcript, accessed through the student's secret link. 
No login is required, so students can view their own transcript, once an advisor has shared the student's link. """
def viewtranscript(request, signed_pk):
    try:
        signature = urllib.parse.unquote_plus(signed_pk)
        pk = int(Advisee.signer.unsign(signature))
        advisee = Advisee.objects.get(pk=pk)
        past_advisements = ChecksheetInstance.objects.filter(advisee=advisee).order_by('-created_at')
        advisement = past_advisements[0]
        with open(past_advisements.latest('pk').template.data_file, "r") as data_file:
            program = json.loads(data_file.read())
        return render(request, "checksheets/student_view_record.html",
                      {"program": program, "editable": False, "advisement": advisement,
                       "record": past_advisements})
    except (BadSignature, Advisee.DoesNotExist):
        raise Http404('No Order matches the given query.')
