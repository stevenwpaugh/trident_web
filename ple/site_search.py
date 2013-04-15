from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
import ple_interface
from tridentdb.models import *
from affyannodb.models import *
from hgnc.models import *
from django.contrib.auth.decorators import login_required

class SearchForm(forms.Form):
    search_text = forms.CharField()
#@login_required    
def site_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            userquery = request.POST['search_text']
            #userquery = form.search_interface.run_search(form.cleaned_data)
            #search_result_list = MicroRNA.objects.filter(mirbase_name__icontains=userquery)
	    #affy_result_list = expression.objects.filter(gene_symbol__icontains=userquery)
            genes = hgncsymbols.objects.filter(approved_symbol__icontains=userquery)
            #gene_dict = {}
            #for gene in genes:
            #    gene_dict[gene.approved_symbol] = gene
            return render_to_response('search/search_output.html', {'genes': genes})
    else:
        form = SearchForm()
        
    return render_to_response('search/search_form.html', {'form': form}, context_instance=RequestContext(request))
