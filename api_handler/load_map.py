from django.views.generic import View
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from sms_handler.SmsParser import SmsParser
import json
from party.models import *
from location.models import *
from health_activity.models import *
from participation.models import *
from reports.models import *


class SaveLayers(View):
    def get(self, request, *args, **kwargs):
        with open('nepal.geojson') as data_file:    
            data = json.load(data_file)
            features = data.get("features")
            for feature in features:
                vdc_code = "".join(feature.get("properties").get("vdc_code").split()[-2:])
                dist_code = feature.get("properties").get("dist_code")
                vdc = VDC.objects.get(district_code=dist_code, vdc_code=vdc_code)
                vdc.layer = json.dumps(feature)
                vdc.save()
        return HttpResponse(len(data.get("features")))