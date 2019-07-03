from django.db import models
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):

    # Attributes:
    location_identifier = models.CharField(max_length=100, blank=True)
    location_setting_code = models.CharField(max_length=60, blank=True)
    location_type_code = models.CharField(max_length=60, blank=True)
    location_status_code = models.CharField(max_length=60, blank=True)
    current_status_effective_date = models.DateField(blank=True, null=True)
    location_narrative_text = models.TextField(blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.location_identifier + ' ' + self.location_status_code


class LocationRelationship(models.Model):

    # Relations:
    location = models.ForeignKey(Location, blank=True, null=True)

    # Attributes:
    location_relationship_datetime_range = models.CharField(
        max_length=100, blank=True)
    location_relationship_type_code = models.CharField(
        max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Location Relationship")
        verbose_name_plural = _("Location Relationships")

    def __str__(self):
        return self.location_relationship_type_code


class PostalLocation(models.Model):

    # Relations:
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE,
        blank=True, null=True
    )

    # Attributes:
    street_address = models.CharField(max_length=200, blank=True)
    address_direction = models.TextField(blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Postal Location")
        verbose_name_plural = _("Postal Locations")

    def __str__(self):
        return self.street_address


class TelecommunicationLocation(models.Model):

    # Relations:
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE,
        blank=True, null=True
    )

    # Attributes:
    personal_identification_number = models.CharField(max_length=100,
                                                      blank=True)
    time_zone = models.CharField(max_length=100, blank=True)
    electronic_address = models.IntegerField(null=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Telecommunication Location")
        verbose_name_plural = _("Telecommunication Locations")

    def __str__(self):
        return self.personal_identification_number


class PhysicalLocation(models.Model):

    # Relations:
    location = models.ForeignKey(Location, blank=True, null=True)
    # Attributes:
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    district_code = models.CharField(max_length=200, blank=True)
    vdc_code = models.CharField(max_length=200, blank=True)
    ward_no = models.CharField(max_length=200, blank=True)
    location_name = models.CharField(max_length=200, blank=True)
    property_location = models.TextField(blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Physical Location")
        verbose_name_plural = _("Physical Locations")

    def __str__(self):
        return self.location_name


class District(models.Model):

    # Relations:
    district_code = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)


    # Meta and Strings:
    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return self.name


class VDC(models.Model):

    # Relations:
    vdc_code = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    district_code = models.CharField(max_length=200, blank=True)
    layer = models.TextField(blank=True)


    # Meta and Strings:
    class Meta:
        verbose_name = _("VDC")
        verbose_name_plural = _("VDCs")

    def __str__(self):
        return self.name