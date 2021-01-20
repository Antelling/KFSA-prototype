from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Advisor
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import CreateAdvisorStudentPair

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
    except MultipleObjectsReturned:
        advisors = Advisor.objects.filter(user=request.user)
        advisors.delete()
        return HttpResponse("numerous advisement records returned, deleted them all")
    except ObjectDoesNotExist:
        advisor = Advisor.objects.create(user=request.user)
        advisor.save()
        return HttpResponse("created new advisor for this user.")
    return render(request, 'advisement/adv_home.html', {'students': advisor.students.all()})
