from django.db import models

class ImportException(Exception):
    pass

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
    browser_name = models.CharField(max_length=16, null=True, blank=True)
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
    chunkid = models.CharField(max_length=6)# parse from reference_id (field 2)
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
        
    def dict(self,interp = None):
        result_dict = {}
        result_dict['microrna'] = self.microrna
        result_dict['chromosome'] = self.chromosome
        result_dict['hit_genomic_start'] = self.hit_genomic_start
        result_dict['hit_genomic_end'] = self.hit_genomic_end
        result_dict['base_type'] = self.base_type.__unicode__()
        result_dict['hit_score'] = self.hit_score
        result_dict['hit_energy'] = self.hit_energy
        result_dict['query_seq'] = self.query_seq
        result_dict['hit_string'] = self.hit_string
        result_dict['ref_seq'] = self.ref_seq
        result_dict['match_type'] = self.match_type.__unicode__()
        result_dict['genome'] = self.genome.__unicode__()
    
        if interp:
            from trident.classify import get_grade
            if not hasattr(interp,"__call__"):
                from trident import TridentException
                raise TridentException("Interpolator object is not callable")
            result_dict["grade"] = get_grade(interp({'query_id': self.microrna, 'energy': self.hit_energy,'score': self.hit_score})) # Supplying the necessary fields for the inerpolator as a dict (instead of full trident score dict)
    
        return result_dict

class AffymetrixID(models.Model):
    probe_set_id = models.CharField(max_length=50)
    gene_symbol = models.CharField(max_length=50)
    chromosome =  models.CharField(max_length=2)
    probe_start =  models.IntegerField()
    probe_end =  models.IntegerField()
    genome = models.ForeignKey(Genome)
    

class Genes(models.Model):
    name = models.CharField(max_length=32) # Symbolic name, not scientific name
    genomic_start = models.PositiveIntegerField()
    genomic_end = models.PositiveIntegerField()
    is_on_positive_strand = models.BooleanField()
    chromosome = models.CharField(max_length=2)
    db_xref = models.CharField(max_length=100) # Comma separated list
    synonyms = models.CharField(max_length=300)
    genome = models.ForeignKey(Genome)

def insert_score(score):
    from django.db.utils import DatabaseError
    import trident.parser as TP

    def error_msg(err_msg):
        from sys import stderr
        stderr.write(err_msg)
        stderr.write("\n")

    if not score:
        return

    ref_id_tokens = TP.get_reference(score)
    chunkid = ref_id_tokens['chunk']
    chromosome = ref_id_tokens['chromosome']
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
        raise ImportException("Genome, '{0}', has not yet been loaded into the database.\nHit: {1}".format(genome_version,score))
    
    r = Results(chunkid = chunkid, chromosome = chromosome, hit_genomic_start = hit_genomic_start, hit_genomic_end = hit_genomic_end, hit_score = hit_score, hit_energy = hit_energy, hit_mir_start = hit_mir_start, hit_mir_end = hit_mir_end, query_seq = query_seq, ref_seq = ref_seq, hit_string = hit_string, is_parallel = is_parallel, match_type = match_type, base_type = base_type, microrna = microrna, genome = genome[0])

    try:
        r.save()
    except DatabaseError as de:
        from sys import stderr
        stderr.write("Error loading score line: {0}\n".format(score))
        raise de

    
    return True


