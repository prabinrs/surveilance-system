from django.db import models
from django.utils.translation import ugettext_lazy as _

from health_activity.models import HealthActivity
from location.models import Location
from material.models import Material
from party.models import Party


class ActorParticipation(models.Model):

    # Relations:
    party = models.ForeignKey(Party, blank=True, null=True, related_name="actor_participations")
    activity = models.ForeignKey(HealthActivity, blank=True, null=True, related_name="actor_participations")

    # Attributes:
    actor_type_code = models.CharField(max_length=60, blank=True)
    # actor_time_range = models.CharField(max_length=100, blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Actor Participation")
        verbose_name_plural = _("Actor Participations")

    def __str__(self):
        return self.actor_type_code


class TargetParticipation(models.Model):

    # Relations:
    party = models.ForeignKey(Party, blank=True, null=True)
    activity = models.ForeignKey(HealthActivity, blank=True, null=True)
    material = models.ForeignKey(Material, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    # Attributes:
    target_type_code = models.CharField(max_length=60, blank=True)
    target_awareness_code = models.CharField(max_length=60, blank=True)
    # target_time_range = models.CharField(max_length=100, blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Target Participation")
        verbose_name_plural = _("Target Participations")

    def __str__(self):
        return self.target_type_code
