# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return HttpResponse("Yo, World!")

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)

def msg(request, msg):
    return render_to_response('ple/msg.html', {'msg': msg})
