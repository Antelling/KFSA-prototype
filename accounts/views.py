from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import AddStudentForm, PermissionSelect
from django.http import HttpResponseRedirect
from .models import Faculty


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts_login')
    template_name = 'registration/signup.html'


class AddStudentView(generic.CreateView):
    form_class = AddStudentForm
    success_url = reverse_lazy('../')
    template_name = 'registration/add_student.html'
    
def set_permissions(request):
    if request.method == "POST":
        form = PermissionSelect(request.POST)
        if form.is_valid():
            fac = Faculty(user=request.user, **form.cleaned_data)
            fac.save()
            return HttpResponseRedirect(reverse_lazy("adv_home"))
    else:
        form = PermissionSelect()
        return render(request, 'registration/set_perm.html', {'form': form})


