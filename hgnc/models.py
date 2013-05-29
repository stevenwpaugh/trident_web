from django.db import models

def get_hgnc_genome():
    return "GRCh37.p5"

class hgncsymbols(models.Model):
    hgnc_id = models.PositiveIntegerField()
    approved_symbol = models.CharField(max_length=500)
    approved_name = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    previous_symbols = models.CharField(max_length=500)
    previous_names = models.CharField(max_length=500)
    synonyms = models.CharField(max_length=500)
    chromosome = models.CharField(max_length=500)
    accession_numbers = models.CharField(max_length=500)
    refseq_ids = models.CharField(max_length=500)
