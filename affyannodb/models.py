from django.db import models

class expression(models.Model):
    probe_set_id = models.CharField(max_length=50)
    gene_symbol = models.CharField(max_length=100)
    chr = models.CharField(max_length=5)
    genomic_start = models.PositiveIntegerField()# gff file filed 4
    genomic_end = models.PositiveIntegerField()# gff file filed 4
    na_ver = models.CharField(max_length=20)
