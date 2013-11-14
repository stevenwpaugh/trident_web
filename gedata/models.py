from django.db import models

# Create your models here.

class Gedata(models.Model):
    pid = models.CharField(max_length=20)
    probe_set_id = models.CharField(max_length=20)
    value = models.FloatField()
    log = models.BooleanField()
    value_type = models.CharField(max_length=20)
    date = models.DateField() 
    def as_json(self):
        return dict(
            id=self.id, pid=self.pid, probe_set_id=self.probe_set_id,
            value=self.value, log=self.log,
            value_type=self.value_type, date=self.date.isoformat())

class Snplc50(models.Model):
        probe_set_id = models.CharField(max_length=20)
        totxv_fisher_p_b = models.FloatField(null=True, blank=True)
        totxv_fisher_0_1_b = models.IntegerField(null=True, blank=True)
        totxv_fisher_0_3_b = models.IntegerField(null=True, blank=True)
        totxv_fisher_1_1_b = models.IntegerField(null=True, blank=True)
        totxv_fisher_1_3_b = models.IntegerField(null=True, blank=True)
        totxv_fisher_2_1_b = models.IntegerField(null=True, blank=True)
        totxv_fisher_2_3_b = models.IntegerField(null=True, blank=True)
        totxv_snp_lm_p_b = models.FloatField(null=True, blank=True)
        totxv_snp_lm_stat_b = models.FloatField(null=True, blank=True)
        totxvi_fisher_p_b = models.FloatField(null=True, blank=True)
        totxvi_fisher_0_1_b = models.IntegerField(null=True, blank=True)
        totxvi_fisher_0_3_b = models.IntegerField(null=True, blank=True)
        totxvi_fisher_1_1_b = models.IntegerField(null=True, blank=True)
        totxvi_fisher_1_3_b = models.IntegerField(null=True, blank=True)
        totxvi_fisher_2_1_b = models.IntegerField(null=True, blank=True)
        totxvi_fisher_2_3_b = models.IntegerField(null=True, blank=True)
        totxvi_snp_lm_p_b = models.FloatField(null=True, blank=True)
        totxvi_snp_lm_stat_b = models.FloatField(null=True, blank=True)
        all_fisher_p_b = models.FloatField(null=True, blank=True)
        all_fisher_0_1_b = models.IntegerField(null=True, blank=True)
        all_fisher_0_3_b = models.IntegerField(null=True, blank=True)
        all_fisher_1_1_b = models.IntegerField(null=True, blank=True)
        all_fisher_1_3_b = models.IntegerField(null=True, blank=True)
        all_fisher_2_1_b = models.IntegerField(null=True, blank=True)
        all_fisher_2_3_b = models.IntegerField(null=True, blank=True)
        all_snp_lm_p_b = models.FloatField(null=True, blank=True)
        all_snp_lm_stat_b = models.FloatField(null=True, blank=True)
        cmh_meta = models.FloatField(null=True, blank=True)
        p_b = models.FloatField(null=True, blank=True)
        stat_b = models.FloatField(null=True, blank=True)
