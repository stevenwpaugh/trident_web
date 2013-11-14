from django.http import HttpResponse
from django.utils import simplejson
from django.template.response import TemplateResponse
from gedata.models import *
from django_datatables_view.base_datatable_view import BaseDatatableView

import json

def index(request):
    return TemplateResponse(request, 'index.html', {'entries': Gedata.objects.all()})       

def randomTest(request):
    resultset = Gedata.objects.all()
    results = [obj.as_json() for obj in resultset]
    return HttpResponse(json.dumps(results), mimetype="application/json")

def gedataTest(request, probesetid):
    resultset = Gedata.objects.filter(probe_set_id=probesetid)
    results = [obj.as_json() for obj in resultset]
    return HttpResponse(json.dumps(results), mimetype="application/json")

class OrderListJson(BaseDatatableView):
    columns = ['pid', 'probe_set_id', 'value']    
    order_columns = ['pid', 'probe_set_id', 'value']

    def get_initial_queryset(self):
        return Gedata.objects.all()

class OrderListJsonLC50SNP(BaseDatatableView):
    columns = ['probe_set_id', 'p_b']    
    order_columns = ['probe_set_id', 'p_b']

    def get_initial_queryset(self):
        return Snplc50.objects.all()


