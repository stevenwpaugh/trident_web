from django.db import models

class MatchType(models.Model):
    """
    Table that lists names of match and base types
    """
    name = models.CharField(max_length=10,unique=True)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name
        

class Genome(models.Model): 
    genome_ver = models.CharField(max_length=20, unique=True) # In results
    genome_genus = models.CharField(max_length=20)
    genome_species = models.CharField(max_length=20)
    description = models.TextField(null=True)

    def __unicode__(self):
        rep = "%s %s (%s)" % (self.genome_genus, self.genome_species, self.genome_ver)
        return rep

class MicroRNA(models.Model):
    chromosome = models.CharField(max_length=2)# gff file, field 1
    is_primary_transcript = models.BooleanField()# parsed from gff file, field 3
    genomic_mir_start = models.PositiveIntegerField()# gff file filed 4
    genomic_mir_end = models.PositiveIntegerField()# gff file filed 4
    is_on_positive_strand = models.BooleanField()# parsed from gff file, column 8
    mirbase_id = models.CharField(max_length=20,unique=True)# ID field in gff column 9
    mirbase_acc = models.CharField(max_length=20)# accession_number field in gff column 9
    mirbase_name = models.CharField(max_length=20)# Name field in gff column 9
    mirbase_derives_from = models.CharField(max_length=20,null=True)# dervives_from field in gff column 9
    mirbase_seq = models.CharField(max_length=100,null=True)# Parse from mature.fa and hairpin.fa
    genome = models.ForeignKey(Genome)
    
class Results(models.Model):
    chunkid = models.CharField(max_length=3)# parse from reference_id (field 2)
    chromosome = models.CharField(max_length=2)# parse from reference_id (field 1)
    hit_genomic_start = models.IntegerField()# ref_coords[0]
    hit_genomic_end = models.IntegerField()# ref_coords[1]
    hit_score = models.PositiveIntegerField()# score
    hit_energy = models.FloatField()# energy 
    hit_mir_start = models.PositiveIntegerField()# query_coords[0]
    hit_mir_end = models.PositiveIntegerField()# query_coords[1]
    query_seq = models.CharField(max_length=100)# query_seq
    ref_seq = models.CharField(max_length=100)# reference_seq
    hit_string = models.CharField(max_length=100)# match_seq
    is_parallel = models.BooleanField()# orientation = parallel
    match_type = models.ForeignKey(MatchType, related_name='results_match_type')# match_type (direct, indirect)
    base_type = models.ForeignKey(MatchType, related_name='results_base_type')# base_type (pyrimidine, purine)
    microrna = models.CharField(max_length=100)# query_id
    # microrna = models.ForeignKey(MicroRNA)# query_id
    genome = models.ForeignKey(Genome)# parse reference_id, 7-th field

    def gff(self):
        retval = "chr%s\t" % self.chromosome
        retval += ".\t"
        retval += "%s\t" % self.base_type.name
        retval += "%d\t%d\t" % (self.hit_genomic_start, self.hit_genomic_end)
        retval += "%d\t" % self.hit_score
        if self.match_type.name == "indirect":
            retval += "-\t"
        else:
            retval += "+\t"
        retval += ".\t"# phase. Has no meaning in this context.
        retval += "Name=%s;Energy=%f;Chr=%s;GenomeStartPos=%s" % (self.microrna, self.hit_energy, self.chromosome, self.hit_genomic_start)

        return retval
        

class AffymetrixID(models.Model):
    probe_set_id = models.CharField(max_length=50)
    gene_symbol = models.CharField(max_length=50)
    chromosome =  models.CharField(max_length=2)
    probe_start =  models.IntegerField()
    probe_end =  models.IntegerField()
    genome = models.ForeignKey(Genome)
    

#class Genes(models.Model):
#    genome = models.ForeignKey(Genome)
#    affymetricids = models.ManyToMany(AffymetrixID)


def insert_score(score):

    def error_msg(err_msg):
        from sys import stderr
        stderr.write(err_msg)
        stderr.write("\n")

    ref_id_tokens = score['reference_id'].split('|')
    chunkid = ref_id_tokens[1]
    chromosome = ref_id_tokens[0]
    if chromosome.find("chr") > -1:
        chromosome = chromosome.replace("chr","")
    (hit_genomic_start, hit_genomic_end) =  (score['ref_start'], score['ref_end'])
    hit_score = int(float(score['score']))
    hit_energy = score['energy']
    (hit_mir_start, hit_mir_end) =  score['query_coords'].split(' ')
    query_seq = score['query_seq']
    ref_seq = score['reference_seq']
    hit_string = score['match_seq']
    hit_energy = score['energy']
    (hit_mir_start, hit_mir_end) = score['query_coords'].split(' ')
    query_seq = score['query_seq']
    ref_seq = score['reference_seq']
    hit_string = score['match_seq']
    is_parallel = (score['orientation'].strip() == 'parallel')
    microrna = score['query_id']
    
    # Look up match type and base type. If they are not in the table,
    # add them and tag their description to indicate that they were
    # added by this function.
    match_type = MatchType.objects.filter(name=score['match_type']) # direct, indirect
    if len(match_type) == 0:
        match_type = MatchType(name=score['match_type'],description='Added by import_score')
        match_type.save()
    else:
        match_type = match_type[0]
        
    base_type = MatchType.objects.filter(name=score['base_type']) # pyrimidine, purine
    if len(base_type) == 0:
        base_type = MatchType(name=score['base_type'],description='Added by import_score')
        base_type.save()
    else:
        base_type = base_type[0]

    genome_tokens = score['reference_id'].split('|')
    if len(genome_tokens) < 6:
        error_msg("Reference data is missing the genome version information.\nReference Data: %s" % score['reference_id'])
        exit(1)
    else:
        genome_version = genome_tokens[6]
    genome = Genome.objects.filter(genome_ver = genome_version)
    if len(genome) != 1:
        error_msg("Genome, '%s', has not yet been loaded into the database." % genome_version)
        return False
    
    r = Results(chunkid = chunkid, chromosome = chromosome, hit_genomic_start = hit_genomic_start, hit_genomic_end = hit_genomic_end, hit_score = hit_score, hit_energy = hit_energy, hit_mir_start = hit_mir_start, hit_mir_end = hit_mir_end, query_seq = query_seq, ref_seq = ref_seq, hit_string = hit_string, is_parallel = is_parallel, match_type = match_type, base_type = base_type, microrna = microrna, genome = genome[0])
    r.save()
    
    return True


