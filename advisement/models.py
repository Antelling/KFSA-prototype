from django.db import models
from django.contrib.auth.models import User
from accounts.models import Faculty
from django.core.signing import Signer
from django.urls import reverse
import urllib

class ChecksheetTemplate(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    data_file = models.TextField()

    def __str__(self):
        return self.name

class Advisee(models.Model):
    name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=10)
    advisors = models.ManyToManyField(Faculty)
    checksheet = models.ForeignKey(ChecksheetTemplate, on_delete=models.PROTECT)
    signer = Signer(sep='/', salt='advisement.Advisee')

    def get_absolute_url(self):
        signed_pk = self.signer.sign(self.pk)
        url_sign = urllib.parse.quote_plus(signed_pk)
        print("")
        return reverse('viewtranscript', kwargs={'signed_pk': url_sign})

    def __str__(self):
        return "Advisee<" + self.name + ">"

class ChecksheetInstance(models.Model):
    template = models.ForeignKey(ChecksheetTemplate, on_delete=models.PROTECT)
    advisee = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    data = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "ChecksheetInstance<" + str(self.pk) + ", advisor: " + self.advisor.user.username + ", student: " + self.advisee.name \
              + ">"

