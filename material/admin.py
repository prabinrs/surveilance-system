from django.contrib import admin

from .models import (
    Material, MaterialRelationship,
    MaterialLocationParticipation, MaterialResponsibility
)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialRelationship)
class MaterialRelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialLocationParticipation)
class MaterialLocationParticipationAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialResponsibility)
class MaterialResponsibilityAdmin(admin.ModelAdmin):
    pass
