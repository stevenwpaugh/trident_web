from tridentdb.models import *
from django.contrib import admin

admin.site.register(TaxonomyGroup)
admin.site.register(Genome)
admin.site.register(MicroRNAGeneAssociation)
admin.site.register(MatchType)
class ResultsAdmin(admin.ModelAdmin):
	#search_fields = ['hit_genomic_start']
	#list_filter = ['hit_genomic_start']
        list_display = ('microrna', 'genome')
admin.site.register(Results,ResultsAdmin)
admin.site.register(AffymetrixID)

class MicroRNAAdmin(admin.ModelAdmin):
	list_display = ("mirbase_name", "chromosome", "genome")
admin.site.register(MicroRNA, MicroRNAAdmin)
