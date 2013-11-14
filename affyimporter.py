#!/usr/bin/env python

def import_affyanno(file):
	from affyannodb import models
    	for line in file:
		info = line.split('\t')
		probe_set_id = info[0]
		gene_symbol = info[1]
		chr = info[2]
		genomic_start = info[3]
		genomic_end = info[4]	
	        affyanno = models.expression(probe_set_id=probe_set_id, gene_symbol=gene_symbol, chr=chr, genomic_start=genomic_start, genomic_end=genomic_end, na_ver="na31")
		affyanno.save()	

def load_file(filename):
    with open(filename,'r') as file:
        import_affyanno(file)
        
if __name__ == "__main__":
    import sys
    from sys import argv
    from getopt import getopt
    
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trident_web.settings")
    from django.db import models
    from django.core.management import execute_from_command_line
    filename = sys.argv[1]
    load_file(filename)
