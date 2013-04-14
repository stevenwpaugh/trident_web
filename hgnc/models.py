from django.db import models

class hgncsymbols(models.Model):
    hgnc_id = models.PositiveIntegerField()
    approved_symbol = models.CharField()
    approved_name = models.CharField()
    status = models.CharField()
    previous_symbols = models.CharField()
    previous_names = models.CharField()
    synonyms = models.CharField()
    chromosome = models.CharField()
    accession_numbers = models.CharField()
    refseq_ids = models.CharField()
