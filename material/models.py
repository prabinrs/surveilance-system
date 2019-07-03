from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import Location
from party.models import Party


class Material(models.Model):

    # Attributes:
    material_identifier = models.CharField(max_length=100, blank=True)
    material_name = models.CharField(max_length=100, blank=True)
    material_type_code = models.CharField(max_length=60, blank=True)
    material_description = models.TextField(blank=True)
    material_datetime_range = models.CharField(max_length=100, blank=True)
    handling_code = models.CharField(max_length=60, blank=True)
    danger_code = models.CharField(max_length=60, blank=True)
    source_site_code = models.CharField(max_length=60, blank=True)
    material_quantity = models.IntegerField(null=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.material_identifier + ' ' + self.material_name


class MaterialRelationship(models.Model):

    # Relations:
    material = models.ForeignKey(Material, blank=True, null=True)

    # Attributes:
    material_relationship_type_code = models.CharField(
        max_length=60, blank=True)
    material_relationship_datetime_range = models.CharField(
        max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Material Relationship")
        verbose_name_plural = _("Material Relationships")

    def __str__(self):
        return self.material_relationship_type_code


class MaterialLocationParticipation(models.Model):

    # Relations:
    material = models.ForeignKey(Material, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    # Attributes:
    participation_datetime_range = models.CharField(max_length=100, blank=True)
    participation_type_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Material Location Participation")
        verbose_name_plural = _("Material Location Participations")

    def __str__(self):
        return self.participation_type_code


class MaterialResponsibility(models.Model):

    # Relations:
    material = models.ForeignKey(Material, blank=True, null=True)
    party = models.ForeignKey(Party, blank=True, null=True)

    # Attributes:
    responsibility_datetime_range = models.CharField(
        max_length=100, blank=True)
    responsibility_type_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Material Responsibility")
        verbose_name_plural = _("Material Responsibilities")

    def __str__(self):
        return self.responsibility_type_code
