from django.contrib import admin

# Register your models here.
from .models import Advisor
@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    pass
