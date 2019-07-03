from django.contrib import admin

from .models import (
    Party, PartyRelationship, PartyLocationParticipation,
    Individual, Person, NonPersonLivingOrganism,
    Organization, FormalOrganization, InformalOrganization
)


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    pass


@admin.register(PartyRelationship)
class PartyRelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(PartyLocationParticipation)
class PartyLocationParticipationAdmin(admin.ModelAdmin):
    pass


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(NonPersonLivingOrganism)
class NonPersonLivingOrganismAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(FormalOrganization)
class FormalOrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(InformalOrganization)
class InformalOrganizationAdmin(admin.ModelAdmin):
    pass
