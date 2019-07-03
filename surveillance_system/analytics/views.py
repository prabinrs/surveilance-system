from django.views.generic import View
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
import json



class AnalyticsHome(View):
    template_name = 'analytics/home.html'

    def get(self, request, *args, **kwargs):
    	return render(request,self.template_name, {})
