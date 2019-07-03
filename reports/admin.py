from django.contrib import admin

from .models import (
    PatientHA
)


@admin.register(PatientHA)
class PatientHAAdmin(admin.ModelAdmin):
    pass

