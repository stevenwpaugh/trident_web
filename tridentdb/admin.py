from tridentdb.models import *
from django.contrib import admin

admin.site.register(Genome)
admin.site.register(MicroRNA)
admin.site.register(MatchType)
class ResultsAdmin(admin.ModelAdmin):
	search_fields = ['hit_genomic_start']
	#list_filter = ['hit_genomic_start']
admin.site.register(Results,ResultsAdmin)
admin.site.register(AffymetrixID)
