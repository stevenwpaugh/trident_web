from django.forms import widgets
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import ple_interface
from tridentdb.models import get_species_choices



default_nts = {'nt1': 'AAGACGGGAGGAAAGAAGGGAG', 'nt2': 'CTGCTAGCTACTGGGGGAAGAAGAGGGGGCAGAGCTGCTAGCTACT', 'long_format': False}

class SequenceForm(forms.Form):
    nt1 = forms.CharField(max_length=30,widget=forms.Textarea(attrs={'cols':30,'rows':10}))
    nt2 = forms.CharField(widget=forms.Textarea(attrs={'cols':30,'rows':10}))
    long_format = forms.BooleanField(required=False)
    genomes = forms.ChoiceField([("null", "No Species")] + get_species_choices().choices)
    use_miranda = forms.BooleanField(required=False)
    
def ple_to_resultlist(parser, browser_name=None, genome=None):
    from views import get_interpolator

    interp = get_interpolator()
    
    result_list = []
    for score in parser:
        if score is None:
            raise Exception("Error in trident output")
        score['microrna'] = ""
        score['chromosome'] = ""
        score['hit_genomic_start'] = score['ref_start']
        score['hit_genomic_end'] = score['ref_end']
        score['hit_score'] = score['score']
        score['hit_energy'] = score['energy']
        score['hit_string'] = score['match_seq']
        score['ref_seq'] = score['reference_seq']
        score['genome'] = ""
        if genome:
            score['genome'] = "Based on {0}".format(genome)
        if browser_name:
            if interp:
                from trident.classify import get_grade
                if not hasattr(interp,"__call__"):
                    from trident import TridentException
                    raise TridentException("Interpolator object is not callable")
                score["grade"] = get_grade(interp({'query_id': browser_name, 'energy': score['energy'], 'score': score['score']}))
        result_list.append(score)
        
    return result_list
 
#@login_required
def ple_them(request,mirna,dna):
    import trident.parser as TP
    from trident import FastaError
    form_dict = {"nt1": mirna, "nt2": dna, "long_format": 0, "use_miranda": 0}
    errormsg = None
    try:
        ple_output = ple_interface.run_ple(form_dict)
        parser = TP.Parser(ple_output)
        result_list = ple_to_resultlist(parser)
    except FastaError as fe:
        errormsg = fe.message
        result_list = []
    return render_to_response('resultdetail.html',{'latest_result_list': result_list, 'error_message': errormsg})
            
def json_ple_them(request,mirna,dna):
    from django.utils import simplejson
    import trident.parser as TP
    from trident import FastaError
    form_dict = {"nt1": mirna, "nt2": dna, "long_format": 0, "use_miranda": 0}
    errormsg = None
    try:
        ple_output = ple_interface.run_ple(form_dict)
        parser = TP.Parser(ple_output)
        result_list = ple_to_resultlist(parser)
    except FastaError as fe:
        errormsg = fe.message
        result_list = []
    return HttpResponse(simplejson.dumps({'latest_result_list': result_list, 'error_message': errormsg}))

#@login_required
def ple_me(request):
    if request.method == 'POST':
        form = SequenceForm(request.POST)
        if form.is_valid():
            import trident.parser as TP
            from trident import FastaError
            errormsg = None
            try:
                browser_name = None
                genome = None
                if "genomes" in form.cleaned_data and form.cleaned_data["genomes"]:
                    species = form.cleaned_data["genomes"]
                    if species != "null":
                        from tridentdb.models import Genome
                        g = Genome.objects.get(genome_ver = species)
                        genome = g.genome_ver
                        browser_name = g.browser_name
                ple_output = ple_interface.run_ple(form.cleaned_data)
                parser = TP.Parser(ple_output)
                result_list = ple_to_resultlist(parser, browser_name, genome)
                                     
            except FastaError as fe:
                errormsg = fe.message
                result_list = []
            return render_to_response('resultdetail.html',{'latest_result_list': result_list,'error_message': errormsg})
    else:
        form = SequenceForm(default_nts)
        
    return render_to_response('ple/sequence_form.html', {'form': form}, context_instance=RequestContext(request))
