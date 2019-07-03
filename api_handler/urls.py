# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views
from . import load_map
from . import internet_message

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^sms/incoming$',
        view=views.SmsRequestHandler.as_view(),
        name='sms_handler'
    ),
    url(
        regex=r'^generate/data$',
        view=views.GenerateData.as_view(),
        name='generate_data'
    ),
    url(
        regex=r'^import/sms$',
        view=views.ImportSMSData.as_view(),
        name='import_sms'
    ),
    url(
        regex=r'^vdc-list/(?P<district_code>[-\w]+)/$',
        view=views.ListVDCs.as_view(),
        name='list_vdc'
    ),
    url(
        regex=r'^icd-list/(?P<morbidity_code>[-\w]+)/$',
        view=views.ListICDs.as_view(),
        name='list_icd'
    ),
    url(
        regex=r'^load-map$',
        view=load_map.SaveLayers.as_view(),
        name='load_map'
    ),
    url(
        regex=r'^vdc-layer/(?P<district_code>[-\w]+)/(?P<vdc_code>[-\w]+)/$',
        view=views.VDCJsonLayer.as_view(),
        name='vdc_layer'
    ),
    url(
        regex=r'^district-layer/(?P<district_name>[-\w]+)/$',
        view=views.DistrictLayer.as_view(),
        name='district_layer'
    ),
    url(
        regex=r'^submission$',
        view=internet_message.UploadHandler.as_view(),
        name='upload_handler'
    ),
    url(
        regex=r'^formList$',
        view=internet_message.FormList.as_view(),
        name='form_list'
    ),


]
