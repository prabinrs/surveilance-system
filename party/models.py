from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import Location


class Party(models.Model):

    # Attributes:
    party_identifier = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Party")
        verbose_name_plural = _("Parties")

    def __str__(self):
        return self.party_identifier


class PartyRelationship(models.Model):

    # Relations:
    party_main = models.ForeignKey(Party, blank=True, null=True,related_name="party_relations")
    party_sub = models.ForeignKey(Party, blank=True, null=True,related_name="party_relations_sub")

    # Attributes:
    # party_relationship_datetime_range = models.CharField(
    #     max_length=100, blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    party_relationship_type_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Party Relationship")
        verbose_name_plural = _("Party Relationships")

    def __str__(self):
        return self.party_relationship_type_code


class PartyLocationParticipation(models.Model):

    # Relations:
    party = models.ForeignKey(Party, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    # Attributes:
    participation_datetime_range = models.CharField(max_length=100, blank=True)
    participation_type_code = models.CharField(max_length=60, blank=True)
    current_status_code = models.CharField(max_length=60, blank=True)
    current_status_effective_date = models.DateField(blank=True, null=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Party Location Participation")
        verbose_name_plural = _("Party Location Participations")

    def __str__(self):
        return self.participation_type_code


class Individual(models.Model):

    # Attributes:
    party = models.ForeignKey(
        Party,blank=True, null=True)

    # Attributes:
    birth_date = models.DateTimeField(blank=True, null=True)
    death_date = models.CharField(max_length=60, blank=True)
    sex_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Individual")
        verbose_name_plural = _("Individuals")

    def __str__(self):
        return self.party.party_identifier


class Person(models.Model):

    # Relations:
    individual = models.ForeignKey(
        Individual, on_delete=models.CASCADE,
        blank=True, null=True)

    # Attributes:
    person_name = models.CharField(max_length=200, blank=True)
    ethnicity_code = models.CharField(max_length=60, blank=True)
    race_code = models.CharField(max_length=60, blank=True)
    occupation_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return self.person_name


class NonPersonLivingOrganism(models.Model):

    # Relations:
    individual = models.OneToOneField(
        Individual, on_delete=models.CASCADE,
        blank=True, null=True)

    # Attributes:
    organism_name = models.CharField(max_length=200, blank=True)
    species_name = models.CharField(max_length=200, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Nonperson Living Organism")
        verbose_name_plural = _("Nonperson Living Organisms")

    def __str__(self):
        return self.organism_name


class Organization(models.Model):

    # Relations:
    party = models.OneToOneField(
        Party, on_delete=models.CASCADE,
        blank=True, null=True)

    # Attributes:
    organization_name = models.CharField(max_length=200, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.organization_name


class FormalOrganization(models.Model):

    # Relations:
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE,
        blank=True, null=True)

    # Attributes:
    industry_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Formal Organization")
        verbose_name_plural = _("Formal Organizations")

    def __str__(self):
        return self.industry_code + ' ' + self.organization.organization_name


class InformalOrganization(models.Model):

    # Relations:
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE,
        blank=True, null=True)

    # Attributes:
    group_type_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Informal Organization")
        verbose_name_plural = _("Informal Organizations")

    def __str__(self):
        return self.group_type_code + ' ' + self.organization.organization_name
