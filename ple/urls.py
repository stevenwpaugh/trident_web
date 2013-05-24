from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from tridentdb.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from ple.views import secure_required
from ple.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    
    #This line shows how to redirect to https site when we have a SSL cert
    #url(r'^$', secure_required(login_required(direct_to_template)), {'template': 'index.html'}),
    
    url(r'^about/', 'direct_to_template', {'template': 'about.html'}),
    url(r'^api/', direct_to_template, {'template': 'api.html'}),
    #url(r'^tools/', direct_to_template, {'template': 'tools.html'}),
    url(r'^download/linux', 'direct_to_template', {'template': 'downloadlinux.html'}),
    url(r'^download/', 'direct_to_template', {'template': 'download.html'}),
    url(r'^accounts/', include('registration.urls')),
    url(r'^jbrowse/','direct_to_template',{'template': 'jbrowse.html'}),
    #url(r'^json','direct_to_template',{'template': 'test.json'}),
)

urlpatterns += patterns('',
    url(r'^browse', 'ple.views.browse'),
    url(r'^gene/(?P<gene_symbol>\S+)/$', 'ple.views.genedetail'),
    url(r'^tools/$', 'ple.sequence_submission.ple_me'),
    url(r'^tools/(?P<mirna>\S+)/(?P<dna>\S+)/$','ple.sequence_submission.ple_them'),
    url(r'^search/(?P<query>\S+)/$','ple.site_search.site_search_restapi'),
    url(r'^search/$', 'ple.site_search.site_search'),
   url(r'^detail/(?P<microrna_id>\S+)/chr(?P<chr>\S+)/(?P<start_pos>\S+)/$', 'ple.views.resultdetail'), # Added this URL to be more flexible with chromosome labels.
   url(r'^detail/(?P<microrna_id>\S+)/(?P<chr>\S+)/(?P<start_pos>\S+)/$', 'ple.views.resultdetail'),
   url(r'^result/(?P<microrna_id>\S+)/$', 'ple.views.result'),	
   url(r'^detail/(?P<microrna_id>\S+)/$', 'ple.views.micrornadetail'),
   url(r'^json/(?P<search_string>\S+)/(?P<chromosome>\S+)/(?P<start_pos>\S+)/$', 'ple.views.jsondetail_chr_start'),
   url(r'^json/(?P<search_string>\S+)/(?P<chromosome>\S+)/$', 'ple.views.jsondetail_chr'),
   url(r'^json/(?P<search_string>\S+)/$', 'ple.views.jsondetail'),
	#url(r'^ple/', 'ple.sequence_submission.ple_me', name='home'),   
   url(r'^detail2/(?P<microrna_id>\S+)/(?P<chr>\S+)/(?P<start_pos>\S+)/$', 'ple.views.resultdetailold'),
    # url(r'^ple/', include('ple.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/$','polls.views.index'),
    url(r'^polls/(?P<poll_id>\d+)/$','polls.views.detail'),
    url(r'^polls/a/(?P<msg>\S+)/$','polls.views.msg'),
    (r'^profiles/', include('profiles.urls')),

)


