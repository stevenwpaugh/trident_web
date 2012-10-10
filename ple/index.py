from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
import ple_interface

default_nts = {'nt1': 'UGAGGUAGUAAGUUGUAUUGUU', 'nt2': 'TCATCGATCGTCAAGAAAAGAAGAAAGAAGGAGATCATCGATCGTC', 'long_format': False}

class SequenceForm(forms.Form):
    nt1 = forms.CharField(max_length=30,widget=forms.Textarea(attrs={'cols':30,'rows':10}))
    nt2 = forms.CharField(widget=forms.Textarea(attrs={'cols':30,'rows':10}))
    long_format = forms.BooleanField(required=False)
    use_miranda = forms.BooleanField(required=False)
    
def index(request):
	return HttpResponse("Hello, World!")
