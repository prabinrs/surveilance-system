from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import *

class CronSetting(models.Model):

    # Attributes:
    server_url = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    project_name = models.CharField(max_length=100, blank=True)
    last_submission_time = models.DateTimeField()

    # Meta and Strings:
    class Meta:
        verbose_name = _("CronSetting")
        verbose_name_plural = _("CronSetting")

    def __str__(self):
        return self.server_url
