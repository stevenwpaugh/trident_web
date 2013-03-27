#!/usr/bin/env python

def import_scores(file, verbose = False):
    import tridentdb.models
    from trident import parser
    from hashlib import md5
    
    ignore_counter = 0
    result_hashes = []
    p = parser.Parser(file)
    for score in p:
        s = parser.str_score(score)
        hash = md5(s).digest()
        if hash in result_hashes:
            if verbose:
                print("Ignoring duplicate entry: {0}".format(s))
            ignore_counter += 1
            continue
        result_hashes.append(hash)
        if verbose:
            print(s)
        tridentdb.models.insert_score(score)

    if ignore_counter:
        print("Ignored {0} duplicate entries".format(ignore_counter))
        

def import_gff(file, genome_version):
    """
    Parses a gff file and populates the MicroRNA table.
    
    If the Mirbase ID section is misformed, it prints the line and continues
    through the file.
    """
    
    from tridentdb import models
    import re
    from django.db.utils import DatabaseError
    
    if genome_version == None:
        print("Genome Version is needed for loading a gff file.")
        return

    genomes = models.Genome.objects.filter(genome_ver = genome_version)
    if len(genomes) == 0:
        print("Unknown Genome Version: %s" % genome_version)
        return
        
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
        chromosome = info[0].replace("chr","")
        is_primary_transcript = (info[2] == 'miRNA_primary_transcript')
        genomic_mir_start = info[3]
        genomic_mir_end = info[4]
        is_on_positive_strand = (info[6] == '+')
        
        mirbase_id = mirbase_acc = mirbase_name = mirbase_derives_from = None
        mirbase = info[8].split(';')
        for tag in mirbase:
            (name,val) = tag.split('=')
            if name == "ID":
                mirbase_id = val
            elif name == "accession_number":
                mirbase_acc = val
            elif name == "Name":
                mirbase_name = val
            elif name == "derives_from":
                mirbase_derives_from = val
            else:
                print("Unknown Mirbase tag: \"%s\"" % name)
                continue

        mirna = models.MicroRNA(chromosome=chromosome, is_primary_transcript = is_primary_transcript, genomic_mir_start = genomic_mir_start, genomic_mir_end = genomic_mir_end, is_on_positive_strand = is_on_positive_strand, mirbase_id = mirbase_id, mirbase_acc = mirbase_acc, mirbase_name = mirbase_name, mirbase_derives_from = mirbase_derives_from, genome = genomes[0] )
        
        try:
            mirna.save()
        except DatabaseError as de:
            from sys import stderr
            stderr.write("Error loading GFF line: {0}\n".format(line))
            raise de
        ##end of import_gff

def load_file(filename, file_type, genome_version = None, verbose = False):
    with open(filename,'r') as file:
        if file_type == 'gff':
            import_gff(file, genome_version,verbose)
        elif file_type == 'score':
            import_scores(file,verbose)
        else:
            print("%s is not yet implemented" % file_type)

        
if __name__ == "__main__":
    from sys import argv
    from getopt import getopt
    from trident import parser
    
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ple.settings")

    from django.core.management import execute_from_command_line

    short_opts =  'g:'
    long_opts = ['verbose']
    (optlist, args) = getopt(argv[1:],short_opts, long_opts)


    verbose = False
    genome_version = None

    file_types = ['gff', 'mirna', 'dna', 'score']
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

    load_file(filename,file_type, genome_version, verbose)
