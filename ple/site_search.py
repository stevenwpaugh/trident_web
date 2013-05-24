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

def perform_search(query):
    mirnas = MicroRNA.objects.filter(mirbase_name__icontains=query)
    genes = hgncsymbols.objects.filter(approved_symbol__icontains=query)
    return render_to_response('search/search_output.html', {'genes': genes, "mirnas": mirnas})

#@login_required    
def site_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            userquery = form.cleaned_data['search_text']
            return perform_search(userquery)
    else:
        form = SearchForm()
        
    return render_to_response('search/search_form.html', {'form': form}, context_instance=RequestContext(request))

#@login_required    
def site_search_restapi(request, query):
    if not query:
        return render_to_response('search/search_form.html', {'form': SearchForm()}, context_instance=RequestContext(request))
    return perform_search(query)
