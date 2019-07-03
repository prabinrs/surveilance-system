from django.db import models
from django.utils.translation import ugettext_lazy as _


class HealthActivity(models.Model):

    # Attributes:
    activity_indentifier = models.CharField(max_length=100, blank=True)
    activity_descriptive_text = models.TextField(blank=True)
    activity_status_code = models.CharField(max_length=60, blank=True)
    activity_mood_code = models.CharField(max_length=60, blank=True)
    activity_type_code = models.CharField(max_length=60, blank=True)
    activity_method_code = models.CharField(max_length=60, blank=True)
    subject_site_code = models.CharField(max_length=60, blank=True)
    interpretation_code = models.CharField(max_length=60, blank=True)
    confidentiality_code = models.CharField(max_length=60, blank=True)
    priority_code = models.CharField(max_length=60, blank=True)
    activity_datetime = models.DateTimeField(blank=True, null=True)
    activity_critical_datetime = models.DateTimeField(blank=True, null=True)
    max_repetition_number = models.IntegerField(null=True)
    notification_reason_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Health Activity")
        verbose_name_plural = _("Health Activities")

    def __str__(self):
        return "activity mood code : " + self.activity_mood_code + self.activity_indentifier + ' ' + self.activity_status_code


class ActivityRelationship(models.Model):
    # Relations:
    activity_main = models.ForeignKey(HealthActivity, null=True, blank=True, related_name="activity_relation")
    activity_sub = models.ForeignKey(HealthActivity, null=True, blank=True, related_name="activity_relation_sub")

    # Attributes:
    # activity_relationship_datetime_range = models.CharField(
    #     max_length=100, blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    activity_relationship_type_code = models.CharField(
        max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Activity Relationship")
        verbose_name_plural = _("Activity Relationships")

    def __str__(self):
        return self.activity_relationship_type_code


class Observation(models.Model):

    # Relations:
    activity = models.OneToOneField(
        HealthActivity, on_delete=models.CASCADE, null=True, blank=True)

    # Attributes:
    observation_type_code = models.CharField(max_length=60, blank=True)
    observation_value = models.CharField(max_length=60, blank=True)
    derivation_expression_text = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Observation")
        verbose_name_plural = _("Observations")

    def __str__(self):
        return self.observation_value


class Case(models.Model):

    # Relations:
    observation = models.OneToOneField(
        Observation, on_delete=models.CASCADE, null=True)

    # Attributes:
    confirmation_method_code = models.CharField(max_length=60, blank=True)
    detection_method_code = models.CharField(max_length=60, blank=True)
    transmission_mode_code = models.CharField(max_length=60, blank=True)
    disease_imported_code = models.CharField(max_length=60, blank=True)
    etiologic_status_code = models.CharField(max_length=60, blank=True)
    classification_status_code = models.CharField(max_length=60, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")

    def __str__(self):
        return self.confirmation_method_code + self.classification_status_code


class Outbreak(models.Model):

    # Relations:
    case = models.OneToOneField(
        Case, on_delete=models.CASCADE, blank=True, null=True)

    # Attributes:
    outbreak_jurisdictional_extent_code = models.CharField(
        max_length=60, blank=True)
    outbreak_peak_date = models.DateField(blank=True, null=True)
    outbreak_time_range = models.CharField(max_length=100, blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Outbreak")
        verbose_name_plural = _("Outbreaks")

    def __str__(self):
        return self.outbreak_jurisdictional_extent_code


class Intervention(models.Model):

    # Relations:
    activity = models.OneToOneField(
        HealthActivity, on_delete=models.CASCADE, blank=True, null=True)

    # Attributes:
    intervention_reason_code = models.CharField(max_length=60, blank=True)
    intervention_form_code = models.CharField(max_length=60, blank=True)
    intervention_route_code = models.CharField(max_length=60, blank=True)
    intervention_quantity = models.IntegerField(null=True)
    strength_quantity = models.IntegerField(null=True)
    rate_quantity = models.IntegerField(null=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Intervention")
        verbose_name_plural = _("Interventions")

    def __str__(self):
        return self.intervention_reason_code


class Referral(models.Model):

    # Relations:
    activity = models.OneToOneField(
        HealthActivity, on_delete=models.CASCADE,
        blank=True, null=True)

    # Attributes:
    referral_reason = models.TextField(blank=True)
    referral_description = models.TextField(blank=True)

    # Meta and Strings:
    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referrals")

    def __str__(self):
        return self.referral_reason
