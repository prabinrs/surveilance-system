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
from datetime import date
import dateutil.parser
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from random import randint
import uuid
import requests
from lxml import etree as ET
import re
from .views import write_into_model

def get_server():
    return "https://kobo.humanitarianresponse.info"

def get_kc_server():
    return "https://kc.humanitarianresponse.info"

class FormList(View):

    def get(self, request, *args, **kwargs):
        # print(request.GET, request.POST, request.META)
        # return html
        # headers = {
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "Accept-Encoding":"gzip, deflate, sdch, br",
        # "Accept-Language":"en-US,en;q=0.8",
        # "Connection":"keep-alive",
        # "Host":"kobo.humanitarianresponse.info",
        # "Upgrade-Insecure-Requests":"1",
        # "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        # }
        # login_request = requests.get(get_server() + "/accounts/login/", headers=headers)
        # # print(login_request.content)
        # content = str(login_request.content)

        # token = content.split("csrfmiddlewaretoken")[-1].split("value=\\'")[1].split("\\'")[0]
        # # print(login_request.headers.get("Set-Cookie"))
        # print(token)
        # headers["Referer"] ="https://kobo.humanitarianresponse.info/accounts/login/"
        # headers["Cookie"] = login_request.headers.get("Set-Cookie")
        # data = {"username":"sujitmhj","password":"myp@$$w0rd","csrfmiddlewaretoken":token}
        # make_login = requests.post(get_server() + "/accounts/login/", data=data, headers=headers)
        # print(make_login.content)
        # headers1 = {}
        # print(make_login.headers.get("Set-Cookie"))
        # headers1["cookie"] = "__bm-hap_hKBcutrqRn9rEZDW=S2; kobonaut=4jyw8rvr1g7r7aq3gukbk5j403oqaxp7; csrftoken=fmUgElVVw0jSALNjWH3k4VpbmWURIVlj; _ga=GA1.2.581001116.1468663417; _gat=1" #make_login.headers.get("Set-Cookie")
        response = requests.get("https://kc.humanitarianresponse.info/api/v1/forms",auth=("sujitmhj","myp@$$w0rd"))
        ret_response = HttpResponse(response.content, content_type="text/xml; charset=utf-8")

        # ret_response["Content-Type"] = "text/xml;q=0.8; charset=utf-8"
        return ret_response

class UploadHandler(View):

    def get_xml_value(self,root,key):
        # key = "n"
        end_str_list = root.split("<"+key+">")
        end_str = end_str_list[-1]
        # print(end_str)
        if len(end_str_list) == 1:
            return None
        return end_str.split("</"+key+">")[0]


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadHandler, self).dispatch(request, *args, **kwargs)

    # send the user back to their own page after a successful update
    def post(self, request, *args, **kwargs):
        # print(request.FILES, request.GET)

        file = request.FILES["xml_submission_file"]
        data = str(file.read())
        print(data)
        # root = ET.fromstring(data)

        keys = ["st","et","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v"]
        dict_value = {}
        for key in keys:
            dict_value[key] = self.get_xml_value(data,key)

        # print(dict_value)
        write_into_model(dict_value, datetime.now(), None, 1)


        return HttpResponse("completed", status=201)
        # response["status"]

    def head(self, request, *args, **kwargs):
        # print(request.META, request)

        try:
                # print(request.META)
                response = HttpResponse(status=302)
                # return 
                import requests

                url1 = "https://kc.humanitarianresponse.info/submission/?deviceID="+request.GET.get("deviceID")
                # url2 = "http://localhost:8000/api/sms/incoming?deviceID=imei%3A869537020118189"
                headers = {'HTTP_CONNECTION': 'Keep-Alive',
                'HTTP_X_OPENROSA_VERSION': '1.0',
                'SERVER_PROTOCOL': 'HTTP/1.1'
                }
                a = requests.head(url1,headers=headers)
                # print(a.status_code)
                headers = a.headers
                headers["location"] = "http://192.168.1.11:8000/api/sms/incoming" #"headers["location"].replace("https://kobo.humanitarianresponse.info","http://192.168.1.11:8000/api/sms/incoming")
                for key in headers.keys():
                        response[key] = headers[key]
                return response
        except:
                url1 = "https://kobo.humanitarianresponse.info/accounts/login/"
                # url2 = "http://localhost:8000/api/sms/incoming?deviceID=imei%3A869537020118189"
                headers ={"cookie":request.META.get("HTTP_COOKIE")}
                # print("request-headers", request.META)
                import re
                regex = re.compile('^HTTP_')
                dict((regex.sub('', header), value) for (header, value) 
                       in request.META.items() if header.startswith('HTTP_'))
                a = requests.head(url1, headers=headers)
                print("second response", a.status_code)
                # print("headers",a.headers)
                headers = a.headers
                print("hhh", headers)
                headers["Set-Cookie"] = headers["Set-Cookie"].replace("Domain=.humanitarianresponse.info;","Domain=192.168.1.11:8000;")
                # headers["location"] = "http://192.168.1.11:8000/api/sms/incoming" #"headers["location"].replace("https://kobo.humanitarianresponse.info","http://192.168.1.11:8000/api/sms/incoming")
                response = HttpResponse(a.content,status=204)
                response["Set-Cookie"] = headers["Set-Cookie"]
                for key in headers.keys():
                        # print(key)
                        # if key=="Set-Cookie":
                        #         response[key] = headers[key].replace("Domain=.humanitarianresponse.info;","")
                        #         print("ss",headers[key])
                                
                        # else:
                        response[key] = headers[key]
                print("res",headers["Set-Cookie"])

                return response
