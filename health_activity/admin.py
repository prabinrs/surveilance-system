from django.contrib import admin

from .models import (
    HealthActivity, ActivityRelationship, Observation,
    Case, Outbreak, Intervention, Referral
)


@admin.register(HealthActivity)
class HealthActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityRelationship)
class ActivityRelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Outbreak)
class OutbreakAdmin(admin.ModelAdmin):
    pass


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    pass


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass
