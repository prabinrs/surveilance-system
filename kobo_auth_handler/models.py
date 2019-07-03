from django.db import models


class KoboScrets(models.Model):
    client_id = models.CharField(max_length=100, blank=True)
    client_secret = models.CharField(max_length=100, blank=True)
    access_token = models.CharField(max_length=60, blank=True)
    material_description = models.TextField(blank=True)
    material_datetime_range = models.CharField(max_length=100, blank=True)
    handling_code = models.CharField(max_length=60, blank=True)
    danger_code = models.CharField(max_length=60, blank=True)
    source_site_code = models.CharField(max_length=60, blank=True)
    material_quantity = models.IntegerField(null=True)


class MaterialRelationship(models.Model):
    material_relationship_type_code = models.CharField(
        max_length=60, blank=True)
    material_relationship_datetime_range = models.CharField(
        max_length=100, blank=True)
    material = models.ForeignKey(Material, null=True)


class MaterialLocationParticipation(models.Model):
    participation_datetime_range = models.CharField(max_length=100, blank=True)
    participation_type_code = models.CharField(max_length=60, blank=True)
    material = models.ForeignKey(Material, null=True)
    location = models.ForeignKey(Location, null=True)


class MaterialResponsibility(models.Model):
    responsibility_datetime_range = models.CharField(
        max_length=100, blank=True)
    responsibility_type_code = models.CharField(max_length=60, blank=True)
    material = models.ForeignKey(Material, null=True)
    party = models.ForeignKey(Party, null=True)
