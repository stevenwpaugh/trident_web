from django.db import models
from django.db.models import Min, Max
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
from tridentdb.models import Results, MicroRNA,Genes
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
import re
from django.template import Context, loader
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ple_interface import *
from drresults.models import *
from local_settings import interpolator_filename

def index(request):
	return HttpResponse("Hello, World!")

def detail(request, microrna_id):
	latest_result_list = Results.objects.filter(microrna = microrna_id)[:20]
	query = ', '.join([p.query_seq for p in latest_result_list])
	match = ', '.join([p.hit_string for p in latest_result_list])
	ref = ', '.join([p.ref_seq for p in latest_result_list])
	output = "<pre>%s<br/>%s<br/>%s</pre>" % (query,match,ref)
	return HttpResponse(output)

def result(request, microrna_id):
        latest_result_list = Results.objects.filter(microrna = microrna_id)[:20]
        query = ', '.join([p.query_seq for p in latest_result_list])
        match = ', '.join([p.hit_string for p in latest_result_list])
        ref = ', '.join([p.ref_seq for p in latest_result_list])
        output = "<pre>%s<br/>%s<br/>%s</pre>" % (query,match,ref)
        return HttpResponse(output)

def resultdetailold(request, microrna_id, chr, start_pos):
	latest_result_list = Results.objects.filter(microrna = microrna_id)[:1000]
	myxmin = Results.objects.filter(pk__in=latest_result_list).aggregate(Min('hit_energy'))
	myxmax = Results.objects.filter(pk__in=latest_result_list).aggregate(Max('hit_energy'))
        myx = ', '.join(map(str, [p.hit_energy for p in latest_result_list]))
	myymin = Results.objects.filter(pk__in=latest_result_list).aggregate(Min('hit_score'))
	myymax = Results.objects.filter(pk__in=latest_result_list).aggregate(Max('hit_score'))
        myy = ', '.join(map(str, [p.hit_score for p in latest_result_list]))
        output = "var myx = [%s];\nvar myy = [%s];var myxmin = [%s]; var myxmax = [%s]; var myymin = [%s]; var myymax = [%s];" % (myx,myy,myxmin['hit_energy__min'],myxmax['hit_energy__max'], myymin['hit_score__min'], myymax['hit_score__max'])
        #output = "var myx = [%s];\nvar myy = [%s];" % (myx,myy)
        return HttpResponse(output)

def get_grade(log_value):
	if log_value <= -5:
		return 1
	elif log_value <= -4:
		return 2
	elif log_value <= -3:
		return 3
	elif log_value <= -2:
		return 4
	return 5

def result_to_dict(result):
	result_dict = {}
	result_dict['microrna'] = result.microrna
	result_dict['chromosome'] = result.chromosome
	result_dict['hit_genomic_start'] = result.hit_genomic_start
	result_dict['hit_genomic_end'] = result.hit_genomic_end
	result_dict['base_type'] = result.base_type.__unicode__()
	result_dict['hit_score'] = result.hit_score
	result_dict['hit_energy'] = result.hit_energy
	result_dict['query_seq'] = result.query_seq
	result_dict['hit_string'] = result.hit_string
	result_dict['ref_seq'] = result.ref_seq
	result_dict['match_type'] = result.match_type.__unicode__()
	result_dict['genome'] = result.genome.__unicode__()

	interp = get_interpolator()
	if interp:
		result_dict["grade"] = get_grade(interp(result.hit_energy,result.hit_score))
	
	return result_dict

def get_interpolator():
	import os.path as OP
	interp = None
	if interpolator_filename and OP.isfile(interpolator_filename):
		import pickle
		interp = pickle.load(open(interpolator_filename,"rb"))
		if interp:
			if not hasattr(interp,"__call__"):
				interp = None
	return interp

def resultdetail(request, microrna_id, chr, start_pos):
	interp = get_interpolator()
	
        latest_result_list = Results.objects.filter(microrna = microrna_id)
        latest_result_list = latest_result_list.filter(chromosome = chr)
        latest_result_list = latest_result_list.filter(hit_genomic_start = start_pos)
	t = loader.get_template('resultdetail.html')
	result_list = []
	for result in latest_result_list:
		result_dict = result_to_dict(result)
		if interp:
			result_dict['grade'] = get_grade(interp(result.hit_energy,result.hit_score))
		result_list.append(result_dict)
		
 	c = Context({
        	#'latest_result_list': latest_result_list,
		'latest_result_list': result_list
    	})
    	return HttpResponse(t.render(c))

def proberesultdetail(request, probe_set_id):
        latest_result_list = geic50.objects.filter(probe_set_id = probe_set_id)
	meth_result_list = gemeth.objects.filter(probe_set_id = probe_set_id)
        mir_result_list = gemir.objects.filter(probe_set_id = probe_set_id)
	t = loader.get_template('proberesultdetail.html')
        c = Context({
                'latest_result_list': latest_result_list,
                'meth_result_list': meth_result_list,
                'mir_result_list': mir_result_list
        })
        return HttpResponse(t.render(c))

#class PleForm(forms.Form):
#    nt1 = forms.CharField(max_length=100)
#    nt2 = forms.CharField()
#    sender = forms.EmailField()
#   cc_myself = forms.BooleanField(required=False)

#def pletool(request):
#        if request.method == 'POST':
#		form = PleForm(request.POST)
#		run_ple(form)
#		return HttpResponse("hello")
#	else:
#		form = PleForm()
#	return render(request, 'pleresult.html',{
#		'form': form,
#       })


def micrornadetail(request, microrna_id):
        latest_result_list = MicroRNA.objects.filter(mirbase_name = microrna_id)
        t = loader.get_template('micrornadetail.html')
        c = Context({
                'latest_result_list': latest_result_list,
        })
        return HttpResponse(t.render(c))



class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def jsondetail(request, search_string):
	from django.utils import simplejson
	mirna_list = MicroRNA.objects.filter(mirbase_name__icontains = search_string)

	json_array = []
	for res in mirna_list:
		num_results = Results.objects.filter(microrna = res.mirbase_name).count()
		json_dict = {}
		for key in ["mirbase_name","chromosome","genomic_mir_start","genomic_mir_end","is_primary_transcript","is_on_positive_strand","mirbase_seq","mirbase_id","mirbase_derives_from","genome_id"]:
			val = getattr(res,key)
			if val == None:
				continue
			json_dict[key] = val
		json_array.append({"mirna": json_dict, "num_results": num_results})
		
	
	return HttpResponse(simplejson.dumps({search_string: json_array}),mimetype="application/json")

def jsondetail_chr(request, search_string, chromosome):
	from django.utils import simplejson

	result_list = Results.objects.filter(microrna = search_string,chromosome = chromosome)
	json_dict = {"mirna": search_string, "chromosome": chromosome, "num_results": len(result_list)}
		
	return HttpResponse(simplejson.dumps({search_string: json_dict}),mimetype="application/json")

def jsondetail_chr_start(request, search_string, chromosome, start_pos):
	from django.utils import simplejson

	result_list = Results.objects.filter(microrna = search_string,chromosome = chromosome,hit_genomic_start = start_pos)
	json_dict = {"mirna": search_string, "chromosome": chromosome, "num_results": len(result_list)}
	result_array = []
	result_dict = None
	if result_list:
		for item in result_list:
			result_array.append(result_to_dict(item))
			result_dict = result_to_dict(item)

	return HttpResponse(simplejson.dumps({search_string: json_dict,"results": result_dict}),mimetype="application/json")

def genedetail(request, gene_symbol):
	genes = Genes.objects.filter(name = gene_symbol)
	gene_dict = {}

	
	for gene in genes:
		gene_dict[gene.name] = gene
	
	c = Context({'gene_list': gene_dict})
	t = loader.get_template("genedetail.html")
	return HttpResponse(t.render(c))
