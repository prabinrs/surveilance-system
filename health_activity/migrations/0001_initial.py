# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-10 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('activity_relationship_type_code', models.CharField(blank=True, max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Activity Relationships',
                'verbose_name': 'Activity Relationship',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_method_code', models.CharField(blank=True, max_length=60)),
                ('detection_method_code', models.CharField(blank=True, max_length=60)),
                ('transmission_mode_code', models.CharField(blank=True, max_length=60)),
                ('disease_imported_code', models.CharField(blank=True, max_length=60)),
                ('etiologic_status_code', models.CharField(blank=True, max_length=60)),
                ('classification_status_code', models.CharField(blank=True, max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Cases',
                'verbose_name': 'Case',
            },
        ),
        migrations.CreateModel(
            name='HealthActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_indentifier', models.CharField(blank=True, max_length=100)),
                ('activity_descriptive_text', models.TextField(blank=True)),
                ('activity_status_code', models.CharField(blank=True, max_length=60)),
                ('activity_mood_code', models.CharField(blank=True, max_length=60)),
                ('activity_type_code', models.CharField(blank=True, max_length=60)),
                ('activity_method_code', models.CharField(blank=True, max_length=60)),
                ('subject_site_code', models.CharField(blank=True, max_length=60)),
                ('interpretation_code', models.CharField(blank=True, max_length=60)),
                ('confidentiality_code', models.CharField(blank=True, max_length=60)),
                ('priority_code', models.CharField(blank=True, max_length=60)),
                ('activity_datetime', models.DateTimeField(blank=True, null=True)),
                ('activity_critical_datetime', models.DateTimeField(blank=True, null=True)),
                ('max_repetition_number', models.IntegerField(null=True)),
                ('notification_reason_code', models.CharField(blank=True, max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Health Activities',
                'verbose_name': 'Health Activity',
            },
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intervention_reason_code', models.CharField(blank=True, max_length=60)),
                ('intervention_form_code', models.CharField(blank=True, max_length=60)),
                ('intervention_route_code', models.CharField(blank=True, max_length=60)),
                ('intervention_quantity', models.IntegerField(null=True)),
                ('strength_quantity', models.IntegerField(null=True)),
                ('rate_quantity', models.IntegerField(null=True)),
                ('activity', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health_activity.HealthActivity')),
            ],
            options={
                'verbose_name_plural': 'Interventions',
                'verbose_name': 'Intervention',
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_type_code', models.CharField(blank=True, max_length=60)),
                ('observation_value', models.CharField(blank=True, max_length=60)),
                ('derivation_expression_text', models.CharField(blank=True, max_length=100)),
                ('activity', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health_activity.HealthActivity')),
            ],
            options={
                'verbose_name_plural': 'Observations',
                'verbose_name': 'Observation',
            },
        ),
        migrations.CreateModel(
            name='Outbreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outbreak_jurisdictional_extent_code', models.CharField(blank=True, max_length=60)),
                ('outbreak_peak_date', models.DateField(blank=True, null=True)),
                ('outbreak_time_range', models.CharField(blank=True, max_length=100)),
                ('case', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health_activity.Case')),
            ],
            options={
                'verbose_name_plural': 'Outbreaks',
                'verbose_name': 'Outbreak',
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_reason', models.TextField(blank=True)),
                ('referral_description', models.TextField(blank=True)),
                ('activity', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='health_activity.HealthActivity')),
            ],
            options={
                'verbose_name_plural': 'Referrals',
                'verbose_name': 'Referral',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='observation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='health_activity.Observation'),
        ),
        migrations.AddField(
            model_name='activityrelationship',
            name='activity_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_relation', to='health_activity.HealthActivity'),
        ),
        migrations.AddField(
            model_name='activityrelationship',
            name='activity_sub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_relation_sub', to='health_activity.HealthActivity'),
        ),
    ]