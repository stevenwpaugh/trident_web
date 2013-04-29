#!/usr/bin/env python

file_types = ['dna', 'genes', 'gff', 'hgnc', 'mirna', 'score']
def print_usage():
    print("Usage: importer [options] <file type> <filename>")
    print("Valid file types:")
    print(", ".join(file_types))


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

def import_genes(filename, chromosome, verbose = False):
    from gene_crawler import crawl_genes
    from tridentdb.models import Genes
    from django.db.utils import DatabaseError
    
    if not chromosome:
        raise Exception("Missing Chromosome information")

    genes = crawl_genes(filename)

    for gene in genes:
        if verbose:
            print("Importing {0}".format(gene.name))
        (start, end) = gene.get_coords()
        dbentry = Genes(name = gene.name, genomic_start = start, genomic_end = end,synonyms = gene.synonym, is_on_positive_strand = (gene.direction == "+"), chromosome = chromosome, db_xref = ",".join(gene.db_xref))
        try:
            dbentry.save()
        except DatabaseError as de:
            from sys import stderr
            from gene_crawler import write_gene
            stderr.write("Error loading gene:")
            write_gene(gene,stderr)
            raise de

def import_scores(file, verbose = False):
    import tridentdb.models
    from trident import parser
    from hashlib import md5
    
    ignore_counter = 0
    result_hashes = []
    p = parser.Parser(file)
    for score in p:
        if not score:
            continue # non-score lines in a file will produce this
        s = parser.str_score(score)
        hash = md5(s).digest()
        if hash in result_hashes:
            if verbose:
                print("Ignoring duplicate entry: {0}".format(s))
            ignore_counter += 1
            continue
        else:
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

def load_file(filename, file_type, genome_version = None, chromosome = None, verbose = False):
    if file_type == "genes":# this function does not want a file type
        import_genes(filename,chromosome,verbose)
    else:
        with open(filename,'r') as file:# these functions do want a file type
            if file_type == 'gff':
                import_gff(file, genome_version,verbose)
            elif file_type == 'score':
                import_scores(file,verbose)
            elif file_type == 'hgnc':
                next(file)
                import_hgnc(file)
            else:
                print("%s is not yet implemented" % file_type)

        
if __name__ == "__main__":
    from sys import argv
    from getopt import getopt
    from trident import parser
    
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ple.settings")

    from django.core.management import execute_from_command_line

    short_opts =  'c:g:h'
    long_opts = ["chromosome","genome","help",'verbose']
    (optlist, args) = getopt(argv[1:],short_opts, long_opts)


    verbose = False
    genome_version = None
    chromosome = None

    for (opt,optarg) in optlist:
        while opt[0] == '-':
            opt = opt[1:]
        while opt[:-1] == '=':
            opt = opt[:-1]
        if opt in ["c", "chromosome"]:
            chromosome = optarg
        elif opt in ['g', 'genome']:
            genome_version = optarg
        elif opt in ["h","help"]:
            print_usage()
            exit(0)
        elif opt == 'verbose':
            verbose = True
        else:
            from sys import stderr
            stderr.write("Unknown option '%s'" % opt)
            exit(1)
        
    if len(args) < 2:
        print_usage()
        exit(1)

    file_type = args[0]
    filename = args[1]

    load_file(filename,file_type, genome_version, chromosome, verbose)
