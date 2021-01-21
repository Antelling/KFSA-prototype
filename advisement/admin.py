from django.contrib import admin

# Register your models here.
from . import models
@admin.register(models.Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    pass
