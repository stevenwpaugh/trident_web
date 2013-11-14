from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from tridentdb.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from trident_web.views import secure_required
from trident_web.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^download/data/(?P<genome_ver>\S+)/$', 'trident_web.views.downloaddata'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    
    url(r'^about/', TemplateView.as_view(template_name='about.html')),
    url(r'^api/', TemplateView.as_view(template_name='api.html')),
    #url(r'^accounts/', include('registration.urls')),
    url(r'^download/linux', TemplateView.as_view(template_name='downloadlinux.html')),
    url(r'^download/python', RedirectView.as_view(url="ftp://trident.stjude.org/binaries/python")),
    url(r'^download/hadoop', RedirectView.as_view(url="ftp://trident.stjude.org/binaries/java")),
    url(r'^download/', TemplateView.as_view(template_name='download.html')),
)

urlpatterns += patterns('',
    url(r'^browse', 'trident_web.views.browse'),
    url(r'^genomes/(?P<id>\S+)/$', 'trident_web.views.genomedetail'),
    url(r'^genomes/', 'trident_web.views.genome_list'),
    url(r'^gene/(?P<species>\S+)/(?P<gene_symbol>\S+)/$', 'trident_web.views.genedetail'),
    url(r'^tools/$', 'trident_web.sequence_submission.ple_me'),
    url(r'^tools/(?P<mirna>\S+)/(?P<dna>\S+)/$','trident_web.sequence_submission.ple_them'),
    url(r'^tools_json/(?P<mirna>\S+)/(?P<dna>\S+)/$','trident_web.sequence_submission.json_ple_them'),
    url(r'^search/(?P<query>\S+)/$','trident_web.site_search.site_search_restapi'),
    url(r'^search/$', 'trident_web.site_search.site_search'),
   url(r'^detail/(?P<microrna_id>\S+)/chr(?P<chr>\S+)/(?P<start_pos>\S+)/$', 'trident_web.views.resultdetail'), # Added this URL to be more flexible with chromosome labels.
   url(r'^detail/(?P<microrna_id>\S+)/(?P<chr>\S+)/(?P<start_pos>\S+)/$', 'trident_web.views.resultdetail'),
   url(r'^result/(?P<microrna_id>\S+)/$', 'trident_web.views.result'),	
   url(r'^detail/(?P<microrna_id>\S+)/$', 'trident_web.views.micrornadetail'),
   url(r'^json/(?P<search_string>\S+)/chr(?P<chromosome>\S+)/(?P<start_pos>\S+)/$', 'trident_web.views.jsondetail_chr_start'), # Added this URL to be more flexible with chromosome labels.
   url(r'^json/(?P<search_string>\S+)/(?P<chromosome>\S+)/(?P<start_pos>\S+)/$', 'trident_web.views.jsondetail_chr_start'),
   url(r'^json/(?P<search_string>\S+)/chr(?P<chromosome>\S+)/$', 'trident_web.views.jsondetail_chr'), # Added this URL to be more flexible with chromosome labels.
   url(r'^json/(?P<search_string>\S+)/(?P<chromosome>\S+)/$', 'trident_web.views.jsondetail_chr'),
   url(r'^json/(?P<search_string>\S+)/$', 'trident_web.views.jsondetail'),
	
   url(r'^detail2/(?P<microrna_id>\S+)/(?P<chr>\S+)/(?P<start_pos>\S+)/$', 'trident_web.views.resultdetailold'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)


