from django.db import models

class School(models.Model):
    city = models.CharField("City", max_length=100)
    zip = models.CharField("Zipcode", max_length=10)
    def __unicode__(self):
        return self.name + ' (' + self.city + ', ' + self.state + ')'
