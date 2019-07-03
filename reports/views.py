from django.views.generic import View
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from sms_handler.SmsParser import SmsParser
import json
from .models import *
from .models import Outreach
from party.models import *
from location.models import *
from health_activity.models import *
from participation.models import *
from datetime import date
from datetime import datetime, timezone, timedelta
import dateutil.parser
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from operator import itemgetter
import numpy as np
from .algorithms import *
from braces.views import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
def get_organisations():
    organisations = Organization.objects.all()
    return organisations

class DashboardView(LoginRequiredMixin, View):

    template_name = "pages/report_dashboard.html"

    def get(self, request, *args, **kwargs):
        today = datetime.now(timezone.utc).date()
        week = today - timedelta(days=7)
        month = today - timedelta(days=30)
        today_count = PatientHA.objects.filter(sent_date=today).count()
        week_count = PatientHA.objects.filter(sent_date__gte=week).count()
        month_count = PatientHA.objects.filter(sent_date__gte=month).count()
        return render_to_response(
            self.template_name,
            {"today_count":today_count, "week_count":week_count, "month_count":month_count},
            context_instance=RequestContext(request)
        )


class SmsOutreachChart(LoginRequiredMixin, View):

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
        outreach_ids = json.loads(request.POST.get("outreaches","[]"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        source = request.POST.get("source","-1")
        results = []
        if len(outreach_ids)>0:

            outreaches = Outreach.objects.filter(id__in=outreach_ids)
        else:
            outreaches = Outreach.objects.all()

        for outreach in outreaches:
            single_node = {}
            
            single_node["name"] = outreach.name
            if source == "-1":
                sms_date_counts_unordered = outreach.patient_has.filter(sent_date__gte=start_date,sent_date__lte=end_date).values('sent_date').annotate(count=Count('id'))
            else:
                sms_date_counts_unordered = outreach.patient_has.filter(sent_date__gte=start_date,sent_date__lte=end_date, source=int(source)).values('sent_date').annotate(count=Count('id'))
            data_points = []
            group_dates = sorted(sms_date_counts_unordered, key=itemgetter('sent_date'))
            for date_count in group_dates:
                data_point = {}
                data_point["date"] = date_count["sent_date"].isoformat()
                data_point["value"] = date_count["count"]
                data_points.append(data_point)
            single_node["data_points"] = data_points
            results.append(single_node)
        return HttpResponse(json.dumps(results))


class SmsOutreachTable(LoginRequiredMixin, View):

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
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SmsOutreachTable, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        outreach_ids = json.loads(request.POST.get("outreaches","[]"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        source = request.POST.get("source","-1")
        results = []
        if len(outreach_ids)>0:

            outreaches = Outreach.objects.filter(id__in=outreach_ids)
        else:
            outreaches = Outreach.objects.all()
        sn = 1
        for outreach in outreaches:
            single_node = {}
            if source == "-1":
                count = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date).count()
            else:
                count = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date,source=int(source)).count()
            single_node["outreach"] = outreach.name
            single_node["count"] = count
            single_node["sn"] = sn
            results.append(single_node)
            sn = sn+1

        return HttpResponse(json.dumps(results))

class LagReporting(LoginRequiredMixin, View):

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
        today = datetime.now(timezone.utc).date()
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
        

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LagReporting, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        plot_type = request.POST.get("type","district")
        value = request.POST.get("value")
        lag_input = int(request.POST.get("lag"))


        lag_count_day = np.zeros((250,7))

        upper_limit = np.zeros(250)
        lower_limit = np.zeros(250)
        central = np.zeros(250)



        if plot_type == "institution":
            outreach = Outreach.objects.get(id=value)
            has = outreach.patient_has.all()
        else:
            vdc = VDC.objects.get(id=value)
            has = vdc.patient_has.all()

        for ha in has:
            lag_time = ha.sent_date-ha.visit_date
            lag_day = lag_time.days

            

            if lag_day <= lag_input:
                epi_week = self.get_epidemiological_week(ha.visit_date)

                if epi_week > -1:
                    lag_count_day[epi_week][(ha.visit_date.weekday()+1)%7] = lag_count_day[epi_week][(ha.visit_date.weekday()+1)%7] + 1

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

class PatientsVisitTable(LoginRequiredMixin, View):

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
        outreach_ids = json.loads(request.POST.get("outreaches","[]"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        # print start_date, end_date
        results = []
        if len(outreach_ids) > 0:
            outreaches = Outreach.objects.filter(id__in=outreach_ids)
            has = PatientHA.objects.filter(outreach__in=outreaches,sent_date__gte=start_date,sent_date__lte=end_date).order_by("-sent_date")[:200]
        else:
            has = PatientHA.objects.filter(sent_date__gte=start_date,sent_date__lte=end_date).order_by("-sent_date")[:200]
            
        for ha in has:
            data_point = {}
            data_point["visit_date"] = ha.visit_date.isoformat()
            data_point["submitted_date"] = ha.sent_date.isoformat()
            data_point["district"] = ha.district.name
            data_point["patient_id"] = ha.patient_id
            data_point["sex"] = "Male" if ha.gender == "M" else "Female"
            age = float(ha.age)
            if age < 1:
                age = age * 12 
                age = str(int(age)) + " Months"
            else:
                age = str(int(age)) + " Years"
            data_point["age"] = age
            data_point["diagnosis"] = ha.icd.name
            results.append(data_point)

        # print results
        return HttpResponse(json.dumps(results))

class TimeSeries(LoginRequiredMixin, View):

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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TimeSeries, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        outreach = request.POST.get("outreach","-1")
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        group = request.POST.get("group","-1")
        icd = request.POST.get("icd","-1")
        district = request.POST.get("district","-1")
        vdc = request.POST.get("vdc","-1")
        gender = request.POST.get("gender","-1")
        age_group = request.POST.get("age_group","-1")
        algorithm = int(request.POST.get("algorithm","1"))

        query = {}
        if group != "-1":
            query["group__id"] = group

        if icd != "-1":
            query["icd__id"] = icd

        if district != "-1":
            query["district__id"] = district

        if vdc != "-1":
            query["vdc__id"] = vdc

        if gender != "-1":
            query["gender"] = gender

        if age_group != "-1":
            age_group = int(age_group)
            if age_group == 1:
                min_age = 0
                max_age = 4
            if age_group == 2:
                min_age = 5
                max_age = 14
            if age_group == 3:
                min_age = 15
                max_age = 49
            if age_group == 4:
                min_age = 50
                max_age = 64
            if age_group == 5:
                min_age = 65
                max_age = 1000
            query["age__gte"] = min_age
            query["age__lte"] = max_age



        if outreach != "-1":
            # outreach = Outreach.objects.filter(id=outreach)
            query["outreach__id"] = outreach
        diff_time = end_date - start_date
        diff_days = diff_time.days

        time_inputs = []
        event_dates = []
        print(query)
        for i in range(diff_days):
            current_date = start_date + timedelta(days=i)
            query["visit_date"] = current_date
            event_dates.append(current_date.isoformat())
            count = PatientHA.objects.filter(**query).count()
            time_inputs.append(count)
            print(count)
        # print len(calculateC2(inp)[0]), len(inp)
        print("algorithm",algorithm)
        if algorithm == 1:
            output = calculateC1(time_inputs)[0]
        if algorithm == 2:
            output = calculateC2(time_inputs)[0]
        if algorithm == 3:
            output = calculateC3(time_inputs)[0]
        # print(calculateC2(time_inputs)[0])
        result = {"labels":event_dates, "values":output}
        return HttpResponse(json.dumps(result))


class DetailTable(LoginRequiredMixin, View):

    template_name = "pages/detail_table.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailTable, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        outreach = request.POST.get("outreach","-1")
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        group = request.POST.get("group","-1")
        icd = request.POST.get("icd","-1")
        district = request.POST.get("district","-1")
        vdc = request.POST.get("vdc","-1")
        gender = request.POST.get("gender","-1")
        age_group = request.POST.get("age_group","-1")
        algorithm = int(request.POST.get("algorithm","1"))

        query = {}
        if group != "-1":
            query["group__id"] = group

        if icd != "-1":
            query["icd__id"] = icd

        if district != "-1":
            query["district__id"] = district

        if vdc != "-1":
            query["vdc__id"] = vdc

        if gender != "-1":
            query["gender"] = gender

        if age_group != "-1":
            age_group = int(age_group)
            if age_group == 1:
                min_age = 0
                max_age = 4
            if age_group == 2:
                min_age = 5
                max_age = 14
            if age_group == 3:
                min_age = 15
                max_age = 49
            if age_group == 4:
                min_age = 50
                max_age = 64
            if age_group == 5:
                min_age = 65
                max_age = 1000
            query["age__gte"] = min_age
            query["age__lte"] = max_age



        if outreach != "-1":
            # outreach = Outreach.objects.filter(id=outreach)
            query["outreach__id"] = outreach
        diff_time = end_date - start_date
        diff_days = diff_time.days

        time_inputs = []
        event_dates = []
        print(query)
        for i in range(diff_days):
            current_date = start_date + timedelta(days=i)
            query["visit_date"] = current_date
            event_dates.append(current_date.isoformat())
            count = PatientHA.objects.filter(**query).count()
            time_inputs.append(count)
            print(count)
        # print len(calculateC2(inp)[0]), len(inp)
        print("algorithm",algorithm)
        if algorithm == 1:
            output = calculateC1(time_inputs)[0]
        if algorithm == 2:
            output = calculateC2(time_inputs)[0]
        if algorithm == 3:
            output = calculateC3(time_inputs)[0]
        # print(calculateC2(time_inputs)[0])
        result = {"labels":event_dates, "values":output, "input":time_inputs}
        return HttpResponse(json.dumps(result))


class MappingView(LoginRequiredMixin, View):
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MappingView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        outreach = request.POST.get("outreach")
        icd = request.POST.get("icd")
        group = request.POST.get("group")
        district_name = request.POST.get("district")

        query = {}
        query["visit_date__gte"] = start_date
        query["visit_date__lte"] = end_date
        if outreach != "-1":
            query["outreach__id"] = outreach
        if icd != "-1":
            query["icd__id"] = icd
        if group != "-1":
            query["group__id"] = group
        district = District.objects.get(name__icontains=district_name.lower())

        query["district"] = district

        has = PatientHA.objects.filter(**query).values('vdc__vdc_code').annotate(count=Count('id'))

        result = {}
        for ha in has:
            result[ha["vdc__vdc_code"]] = ha["count"]

        return HttpResponse(json.dumps(result))

class MorbidityReport(LoginRequiredMixin, View):

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
        outreach_id = int(request.POST.get("outreach"))
        start_date = dateutil.parser.parse(request.POST.get("start_date"))
        end_date = dateutil.parser.parse(request.POST.get("end_date"))
        
        results = []
        
        outreach = Outreach.objects.get(id=outreach_id)
        groups = Group.objects.all()
        count = 1
        for group in groups:
            icds = ICD.objects.filter(morbidity_code=group.group_code)
            icd_results = []
            for icd in icds:
                total = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd).count()
                if total == 0:
                    continue
                male_count = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, gender="M").count()
                female_count = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, gender="F").count()
                age_group1 = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, age__lte=4).count()
                age_group2 = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, age__gt=4, age__lte=14).count()
                age_group3 = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, age__gt=14, age__lte=49).count()
                age_group4 = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, age__gt=49, age__lte=65).count()
                age_group5 = outreach.patient_has.filter(visit_date__gte=start_date, visit_date__lte=end_date, icd=icd, age__gt=65).count()
                result = {
                    "sn" : count,
                    "icd_code":icd.icd_code,
                    "disease_name":icd.name,
                    "male_count":male_count,
                    "female_count":female_count,
                    "age_group":[age_group1,age_group2, age_group3, age_group4, age_group5],
                    "total":total
                }
                count = count + 1
        

                icd_results.append(result)
            result = {"group_name":group.name, "results":icd_results}
            results.append(result)
         

        return HttpResponse(json.dumps(results))

class DataQualityView(LoginRequiredMixin, View):

    template_name = "pages/data_quality_view.html"

    def get(self, request, *args, **kwargs):
        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )