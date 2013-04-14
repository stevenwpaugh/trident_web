#!/usr/bin/env python

def import_hgnc(file):
    from hgnc import models
    import re
    from django.db.utils import DatabaseError
        
    lineno = 1
    for line in file:
        print("Line Number: %d" % lineno)
        lineno += 1
        if len(line) == 0:
            continue
        line = line.strip()
        if line[0] == '#':
            continue
        info = line.split('\t')
        hgnc_id = info[0].replace("HGNC:","")
        approved_symbol = info[1]
        approved_name = info[2]
        status = info[3]
        previous_symbols = info[4]
        previous_names = info[5]
        synonyms = info[6]
        chromosome = info[7]
        accession_numbers = info[8]
        refseq_ids = info[9]

        hgncsymbols = models.hgncsymbols(hgnc_id=hgnc_id,approved_symbol=approved_symbol,approved_name=approved_name,status=status,previous_symbols=previous_symbols,previous_names=previous_names,synonyms=synonyms,chromosome=chromosome,accession_numbers=accession_numbers,refseq_ids=refseq_ids)
        
        try:
            hgncsymbols.save()
        except DatabaseError as de:
            from sys import stderr
            stderr.write("Error loading hgnc line: {0}\n".format(line))
            raise de
        ##end of import_hgnc

def load_file(filename, file_type, genome_version = None, chromosome = None, verbose = False):
    with open(filename,'r') as file:# these functions do want a file type
        if file_type == 'hgnc':
            import_hgnc(file)
        else:
            print("%s is not yet implemented" % file_type)

        
if __name__ == "__main__":
    from sys import argv
    from getopt import getopt
    
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ple.settings")

    from django.core.management import execute_from_command_line

    short_opts =  'g:'
    long_opts = ['verbose']
    (optlist, args) = getopt(argv[1:],short_opts, long_opts)


    verbose = False
    genome_version = None

    file_types = ['hgnc']
    for (opt,val) in optlist:
        while opt[0] == '-':
            opt = opt[1:]
        while opt[:-1] == '=':
            opt = opt[:-1]
        if opt == 'verbose':
            verbose = True
        elif opt in ['g', 'genome']:
            genome_version = val
        else:
            from sys import stderr
            stderr.write("Unknown option '%s'" % opt)
            exit(1)
        
    if len(args) < 2:
        print("Usage: importer [options] <file type> <filename>")
        exit(1)

    file_type = args[0]
    filename = args[1]
    chromosome = None
    if len(args) > 2:
        chromosome = args[2]

    load_file(filename,file_type, genome_version, chromosome, verbose)
