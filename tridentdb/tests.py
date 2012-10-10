"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest

class TestInsert(unittest.TestCase):
    def test_match_type(self):
        import models
        mt = models.MatchType(name='fake_match',description='Match type for unit test')
        mt.save()
        
        self.assertNotEqual( len(models.MatchType.objects.filter(name='fake_match')),0)
        self.assertEqual( len(models.MatchType.objects.filter(name='fake_matchf')),0)

    def test_genome_uniqueness(self):
        import models
        gn = models.Genome(genome_ver='42',genome_genus='Felis',genome_species='Catus',description='endothermic quadruped, carnivorous by nature')
        gn.save()
        gn.save()
        self.assertEqual(1, len(models.Genome.objects.all()))
        
    def test_mirna(self):
        from models import MicroRNA, Genome
        original_size = len(Genome.objects.all())
        gn = Genome(genome_ver='12', genome_genus='Arabidopsis', genome_species='Lyrata',description='???')
        
        gn.save()
        self.assertEqual(original_size + 1,len(Genome.objects.all()))

        mirna = MicroRNA(chromosome='13', is_primary_transcript=True, genomic_mir_start=42, genomic_mir_end=92, is_on_positive_strand=True, mirbase_id='aly-miR4242', mirbase_acc='MIMAT0017931', mirbase_name='aly-miR4242', mirbase_derives_from='nothing', mirbase_seq='aaaguuaacuauggcauuccc', genome=gn)
        
        mirna.save()
        self.assertNotEqual(0,len(MicroRNA.objects.filter(mirbase_seq='aaaguuaacuauggcauuccc')))

    def test_score(self):
        from trident import parser
        from models import insert_score

        from os import getcwd
        with open('tridentdb/sample.score','r') as file:
            p = parser.Parser(file)
            for score in p:
                r = insert_score(score)
                print(r)

    def test_result_gff(self):
        from models import Results

        result1 = Results.objects.all()[0]
        self.assertIsNotNone(result)
        print(result1.gff())
