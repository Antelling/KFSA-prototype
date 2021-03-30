from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.ChecksheetInstance)
class ChecksheetInstanceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ChecksheetTemplate)
class ChecksheetTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Advisee)
class AdviseeAdmin(admin.ModelAdmin):
    pass
