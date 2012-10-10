from drresults.models import *
from django.contrib import admin

admin.site.register(geic50)
admin.site.register(gemeth)
admin.site.register(gemir)
#class ResultsAdmin(admin.ModelAdmin):
#	search_fields = ['hit_genomic_start']
#	#list_filter = ['hit_genomic_start']
#admin.site.register(Results,ResultsAdmin)
#admin.site.register(AffymetrixID)
