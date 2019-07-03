# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.DashboardView.as_view(),
        name='dashboard'
    ),
    url(
        regex=r'^sms-outreach-chart/$',
        view=views.SmsOutreachChart.as_view(),
        name='sms_chart'
    ),
    url(
        regex=r'^sms-outreach-table/$',
        view=views.SmsOutreachTable.as_view(),
        name='sms_table'
    ),
    url(
        regex=r'^lag-report/$',
        view=views.LagReporting.as_view(),
        name='lag_report'
    ),
    url(
        regex=r'^patient-visit-table/$',
        view=views.PatientsVisitTable.as_view(),
        name='patients_table'
    ),
    url(
        regex=r'^time-series/$',
        view=views.TimeSeries.as_view(),
        name='time_series'
    ),
    url(
        regex=r'^data-quality/$',
        view=views.DataQualityView.as_view(),
        name='data_quality'
    ),
    url(
        regex=r'^detail-table/$',
        view=views.DetailTable.as_view(),
        name='detail_table'
    ),
    url(
        regex=r'^mapping/$',
        view=views.MappingView.as_view(),
        name='mapping'
    ),
    url(
        regex=r'^morbidity/$',
        view=views.MorbidityReport.as_view(),
        name='morbidity'
    ),
]
