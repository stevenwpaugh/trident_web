from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import ple_interface

default_nts = {'nt1': 'UGAGGUAGUAAGUUGUAUUGUU', 'nt2': 'TCATCGATCGTCAAGAAAAGAAGAAAGAAGGAGATCATCGATCGTC', 'long_format': False}

class SequenceForm(forms.Form):
    nt1 = forms.CharField(max_length=30,widget=forms.Textarea(attrs={'cols':30,'rows':10}))
    nt2 = forms.CharField(widget=forms.Textarea(attrs={'cols':30,'rows':10}))
    long_format = forms.BooleanField(required=False)
    use_miranda = forms.BooleanField(required=False)
    
@login_required
def ple_me(request):
    if request.method == 'POST':
        form = SequenceForm(request.POST)
        if form.is_valid():
            import trident.parser as TP
            ple_output = ple_interface.run_ple(form.cleaned_data)
            parser = TP.Parser(ple_output)
            result_list = []
            for score in parser:
                score['microrna'] = ""
                score['chromosome'] = ""
                score['hit_genomic_start'] = score['ref_start']
                score['hit_genomic_end'] = score['ref_end']
                score['hit_score'] = score['score']
                score['hit_energy'] = score['energy']
                score['hit_string'] = score['match_seq']
                score['ref_seq'] = score['reference_seq']
                score['genome'] = ""
                result_list.append(score)
            return render_to_response('resultdetail.html',{'latest_result_list': result_list})
    else:
        form = SequenceForm(default_nts)
        
    return render_to_response('ple/sequence_form.html', {'form': form}, context_instance=RequestContext(request))
