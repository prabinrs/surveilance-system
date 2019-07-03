from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import *

class Group(models.Model):

    # Attributes:
    group_code = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.name

class Outreach(models.Model):

    # Attributes:
    outreach_code = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Outreach")
        verbose_name_plural = _("Outreaches")

    def __str__(self):
        return self.name


class Morbidity(models.Model):

    # Attributes:
    morbidity_code = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Morbidity")
        verbose_name_plural = _("Morbidities")

    def __str__(self):
        return self.name



class ICD(models.Model):
    # Attributes:
    icd_code = models.CharField(max_length=100, blank=True)
    morbidity_code = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("ICD")
        verbose_name_plural = _("ICDs")

    def __str__(self):
        return self.name


class PatientHA(models.Model):
    st = models.DateTimeField()
    et = models.DateTimeField()
    visit_date = models.DateField()
    sent_date = models.DateField()
    outreach = models.ForeignKey(Outreach,related_name="patient_has")
    ha_provider_id = models.CharField(max_length=100,null=True, blank=True)
    patient_id = models.CharField(max_length=100,null=True, blank=True)
    age = models.CharField(max_length=100,null=True, blank=True)
    unit = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=100,null=True, blank=True)
    district = models.ForeignKey(District,null=True,related_name="patient_has")
    vdc = models.ForeignKey(VDC,related_name="patient_has")
    ward = models.IntegerField(null=True,)
    obs_k = models.CharField(max_length=100,null=True, blank=True)
    obs_l = models.CharField(max_length=100,null=True, blank=True)
    obs_m = models.CharField(max_length=100,null=True, blank=True)
    derived_n = models.CharField(max_length=100,null=True, blank=True)
    derived_o = models.CharField(max_length=100,null=True, blank=True)
    derived_p = models.CharField(max_length=100,null=True, blank=True)
    derived_q = models.CharField(max_length=100,null=True, blank=True)
    derived_r = models.CharField(max_length=100,null=True, blank=True)
    derived_s = models.CharField(max_length=100,null=True, blank=True)
    group = models.ForeignKey(Group,null=True,related_name="patient_has")
    icd = models.ForeignKey(ICD,null=True,related_name="patient_has")
    source = models.IntegerField(default=0)
