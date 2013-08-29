from tridentdb.models import *
from django.contrib import admin

admin.site.register(TaxonomyGroup)
admin.site.register(Genome)
admin.site.register(MatchType)

class ResultsAdmin(admin.ModelAdmin):
	#search_fields = ['hit_genomic_start']
	#list_filter = ['hit_genomic_start']
        list_display = ('microrna', 'genome')
admin.site.register(Results,ResultsAdmin)
admin.site.register(AffymetrixID)

class GenesAdmin(admin.ModelAdmin):
    list_display = ("name", "genome")
admin.site.register(Genes, GenesAdmin)

class MicroRNAAdmin(admin.ModelAdmin):
	list_display = ("mirbase_name", "chromosome", "genome")
admin.site.register(MicroRNA, MicroRNAAdmin)

class MicroRNAGeneAssociationAdmin(admin.ModelAdmin):
	list_display = ("microrna", "gene")
admin.site.register(MicroRNAGeneAssociation, MicroRNAGeneAssociationAdmin)
