from django.views.generic import View
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from sms_handler.SmsParser import SmsParser
import json
from .models import *
from party.models import *
from location.models import *
from health_activity.models import *
from participation.models import *
from datetime import date
from datetime import datetime, timezone
import dateutil.parser
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from operator import itemgetter
import numpy as np

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
def get_organisations():
    organisations = Organization.objects.all()
    return organisations

class DashboardView(View):

    template_name = "pages/report_dashboard.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )


class SmsOutreachChart(View):

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        return parameters



    template_name = "pages/sms_outreach_chart.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SmsOutreachChart, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        # date_range = json.loads(request.POST.get("daterange",{}))
        outreaches = json.loads(request.POST.get("outreaches","[]"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        results = []

        if len(outreaches) > 0:
            parties = Party.objects.filter(party_identifier__in=outreaches)
        else:
            organizations = Organization.objects.all()
            parties = []
            for organization in organizations:
                parties.append(organization.party)
        for party in parties:
            single_node = {}
            # party = Party.objects.get(id=int(outreach))
            sms_date_counts_unordered = ActorParticipation.objects.filter(actor_type_code="sms", party=party, start_datetime__gt=start_date, start_datetime__lt=end_date).extra({'datetime':"date(start_datetime)"}).values('datetime').annotate(count=Count('id'))

            single_node["name"] = Organization.objects.get(party=party).organization_name
            data_points = []
            sms_date_counts= sorted(sms_date_counts_unordered, key=itemgetter('datetime'))

            for sms_date_count in sms_date_counts:
                data_point = {}
                data_point["date"] = sms_date_count["datetime"].isoformat()
                data_point["value"] = sms_date_count["count"]
                data_points.append(data_point)
            single_node["data_points"] = data_points
            results.append(single_node)
        print(results)
        return HttpResponse(json.dumps(results))


class SmsOutreachTable(View):

    template_name = "pages/sms_outreach_table.html"

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        return parameters

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )

class LagReporting(View):

    template_name = "pages/lag_reporting.html"

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        districts = District.objects.all()
        parameters["districts"] = districts
        parameters["lags"] = [1,5,7,15,20]
        return parameters

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )
    def get_epidemiological_week(self,event_datetime):
        today = datetime.now(timezone.utc)
        time_diff = today - event_datetime
        days_diff = time_diff.days
        total_days = days_diff - (today.weekday()+1)%7
        total_weeks = int(total_days/7)
        week_index = 249-total_weeks
        return week_index

    def get_mad(self,weeks):
        upper = []
        median_list = []
        lower = []

        for week in weeks:
            median = np.median(week)
            mad = abs(week-median)
            mad_median = np.median(mad)
            mad_median_multiplied = 1.4826 * mad_median
            upper_limit = median + 2*mad_median_multiplied
            lower_limit = median - 2*mad_median_multiplied
            upper.append(upper_limit)
            lower.append(lower_limit)
            median_list.append(median)

        result ={"central":median_list,"upper":upper,"lower":lower}

        return result
        
    def post(self, request, *args, **kwargs):

        plot_type = request.POST.get("type","district")
        value = request.POST.get("value")
        lag_input = int(request.POST.get("lag"))


        lag_count_day = np.zeros((250,7))

        upper_limit = np.zeros(250)
        lower_limit = np.zeros(250)
        central = np.zeros(250)

        if plot_type == "institution":
            outreach_party = Party.objects.get(party_identifier=value)
            actor_partnerships = ActorParticipation.objects.filter(party=outreach_party,actor_type_code="symptom")
            for actor_partnership in actor_partnerships:
                health_realtionship = ActivityRelationship.objects.get(activity_main=actor_partnership.activity,activity_relationship_type_code="sms")

                critical_time = health_realtionship.activity_main.activity_critical_datetime
                submitted_time = health_realtionship.activity_sub.activity_critical_datetime
                lag_time = submitted_time - critical_time
                lag_day = lag_time.days
                print(lag_day)

                if lag_day <= lag_input:
                    epi_week = self.get_epidemiological_week(critical_time)

                    if epi_week > -1:
                        lag_count_day[epi_week][(critical_time.weekday()+1)%7] = lag_count_day[epi_week][(critical_time.weekday()+1)%7] + 1


        else:
            physical_locations = PhysicalLocation.objects.filter(vdc_code=value)
            location_list = [ph_loc.location for ph_loc in physical_locations]

            party_location_relationships = PartyLocationParticipation.objects.filter(location__in=location_list)
            parties = [rel.party for rel in party_location_relationships]


            # outreach_party = Party.objects.get(party_identifier=value)
            target_partnerships = TargetParticipation.objects.filter(party__in=parties,target_type_code="symptom")
            for target_partnership in target_partnerships:
                health_realtionship = ActivityRelationship.objects.get(activity_main=target_partnership.activity,activity_relationship_type_code="sms")

                critical_time = health_realtionship.activity_main.activity_critical_datetime
                submitted_time = health_realtionship.activity_sub.activity_critical_datetime
                lag_time = submitted_time - critical_time
                lag_day = lag_time.days

                if lag_day <= lag_input:
                    epi_week = self.get_epidemiological_week(critical_time)

                    if epi_week > -1:
                        lag_count_day[epi_week][(critical_time.weekday()+1)%7] = lag_count_day[epi_week][(critical_time.weekday()+1)%7] + 1
                    
        mad = self.get_mad(lag_count_day)
        upper_limit = mad.get("upper")
        lower_limit = mad.get("lower")
        central = mad.get("central")

        parameters = {}
        parameters["upper_limit"] = list(upper_limit)
        parameters["lower_limit"] = list(lower_limit)
        parameters["central"] = list(central)

        # parameters["lag_counts"] = lag_count_day
        return HttpResponse(json.dumps(parameters))

class PatientsVisitTable(View):

    template_name = "pages/patients_visit_table.html"

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        return parameters

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientsVisitTable, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        # date_range = json.loads(request.POST.get("daterange",{}))
        outreaches = json.loads(request.POST.get("outreaches","[]"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        # print start_date, end_date
        results = []

        if len(outreaches) == 0:
            check_ups = ActorParticipation.objects.filter(actor_type_code="diagnosis", start_datetime__gt=start_date, start_datetime__lt=end_date).order_by("-start_datetime")[:200]
        else:
            party_list = []

            for outreach in outreaches:
                # single_node = {}
                party = Party.objects.get(id=int(outreach))
                party_list.append(party)
            
            check_ups = ActorParticipation.objects.filter(actor_type_code="diagnosis",party__in=party_list, start_datetime__gt=start_date, start_datetime__lt=end_date).order_by("-start_datetime")[:200]

         
        for checkup in check_ups:
            # print checkup.start_datetime
            data_point = {}
            data_point["visit_date"] = checkup.start_datetime.isoformat()
            main_activity = ActivityRelationship.objects.get(activity_sub=checkup.activity).activity_main
            sms_activity = ActivityRelationship.objects.get(activity_main=main_activity,activity_relationship_type_code="sms").activity_sub

            patient_party = TargetParticipation.objects.get(activity=main_activity).party


            data_point["submitted_date"] = sms_activity.activity_critical_datetime.isoformat()
            individual = Individual.objects.get(party=patient_party)
            patient_location = PartyLocationParticipation.objects.get(party=patient_party).location
            physical_location = PhysicalLocation.objects.get(location=patient_location)
            patient_district = District.objects.get(district_code=physical_location.district_code)

            data_point["district"] = patient_district.name
            data_point["patient_id"] = patient_party.party_identifier
            data_point["sex"] = "Male" if individual.sex_code == "M" else "Female"
            days = (dateutil.parser.parse(datetime.now().isoformat()+"+05:45") - individual.birth_date).days
            if days>365:
                age_text = str(int(days/365)) + " years"
            else:
                age_text = str(int(days/30)) + " months"
            data_point["age"] = age_text
            observation = Observation.objects.get(activity=checkup.activity)
            icd = ICD.objects.get(icd_code=observation.observation_value)
            data_point["diagnosis"] = icd.name
            results.append(data_point)

        # print results
        return HttpResponse(json.dumps(results))

class TimeSeries(View):

    template_name = "pages/time_series.html"

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        districts = District.objects.all()
        parameters["districts"] = districts
        # parameters["lags"] = [1,5,7,15,20]
        morbidities = Morbidity.objects.all()
        parameters["morbidities"] = morbidities
        return parameters


    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):
        outreaches = json.loads(request.POST.get("outreaches","[]"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        # diagnosis_group = 
        # diagonosis = 
        # district_code = 
        # vdc_code = 
        # sex = 
        # age_group = 
        
        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )


class DetailTable(View):

    template_name = "pages/detail_table.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )

class MappingView(View):
    template_name = "pages/mapping.html"

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        districts = District.objects.all()
        parameters["districts"] = districts
        # parameters["lags"] = [1,5,7,15,20]
        morbidities = Morbidity.objects.all()
        parameters["morbidities"] = morbidities
        return parameters


    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )

class MorbidityReport(View):

    template_name = "pages/morbidity_report.html"

    def get_context(self):
        parameters = {}
        organizations = Organization.objects.all()
        parameters["organizations"] = organizations
        return parameters


    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            self.get_context(),
            context_instance=RequestContext(request)
        )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MorbidityReport, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        outreach = request.POST.get("outreach")
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))


        
class DataQualityView(View):

    template_name = "pages/data_quality_view.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )