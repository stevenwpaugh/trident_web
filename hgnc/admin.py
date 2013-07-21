from hgnc.models import *
from django.contrib import admin

class HGNCSymbolsAdmin(admin.ModelAdmin):
    list_display = ('approved_symbol', 'synonyms')

admin.site.register(hgncsymbols, HGNCSymbolsAdmin)

    
