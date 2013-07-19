from django import forms
from django.forms import widgets
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
import ple_interface
from tridentdb.models import *
from affyannodb.models import *
from hgnc.models import *
from django.contrib.auth.decorators import login_required

def get_species_choices():
    genomes = Genome.objects.filter(Q(status__isnull=True)|Q(status="")).all()
    genome_list = []
    for genome in genomes:
        genome_list.append( (genome.genome_ver,"{0} {1}".format(genome.genome_genus, genome.genome_species)))
    return forms.MultipleChoiceField(required=False, widget=widgets.CheckboxSelectMultiple(),choices=genome_list)

class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search_text'] = forms.CharField()
        self.fields['search_species'] = get_species_choices()


def perform_search(query, species = None):
    genes = None

    # Query genes. If species is H. sapiens, join with hgnc data
    where_stmt = " TRUE "
    if query:
        main_query = "select tridentdb_genes.*, hgnc_hgncsymbols.approved_name, hgnc_hgncsymbols.previous_symbols, tridentdb_genome.browser_name from tridentdb_genes left join hgnc_hgncsymbols on tridentdb_genes.name = hgnc_hgncsymbols.approved_symbol left join tridentdb_genome on tridentdb_genes.genome_id = tridentdb_genome.id"
        if species:
            genes = Genes.objects.raw("{0} where lower(name) like %s and tridentdb_genome.genome_ver like %s;".format(main_query), ["%{0}%".format(query), species[0]])
        else:
            genes = Genes.objects.raw("{0} where lower(name) like %s;".format(main_query), ["%{0}%".format(query)])

    # Query Mirna
    if species:
        from django.db.models import Q

        g = Genome.objects.get(genome_ver = species[0])
        q = Q(genome_id = g.id)
        for s in species[1:]:
            q = q | Q(genome_id = Genome.objects.get(genome_ver = s).id)
        mirnas = MicroRNA.objects.filter(mirbase_name__icontains=query).filter(q).order_by('mirbase_name')
    else:
        mirnas = MicroRNA.objects.filter(mirbase_name__icontains=query).order_by('mirbase_name')

    return render_to_response('search/search_output.html', {'genes': genes, "mirnas": mirnas})

#@login_required    
def site_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            userquery = form.cleaned_data['search_text']
            species_list = form.cleaned_data['search_species']
            return perform_search(userquery,species=species_list)
    else:
        form = SearchForm()
        
    return render_to_response('search/search_form.html', {'form': form}, context_instance=RequestContext(request))

#@login_required    
def site_search_restapi(request, query):
    if not query:
        return render_to_response('search/search_form.html', {'form': SearchForm()}, context_instance=RequestContext(request))
    return perform_search(query)
