

# Create your models here.
from django.db import models


import uuid



class Aktorius(models.Model):
    vardas_pavarde = models.CharField('Vardas pavarde', max_length=100)
    g_metai = models.IntegerField('Gimimo data')
    kinografija = models.TextField('Kino', max_length=2000, default='')

    def __str__(self):
        return f"{self.vardas_pavarde}"

class Filmas(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100)
    rodymo_data = models.IntegerField('Kada pasirode')
    aprasymas = models.TextField('Aprasymas', max_length=2000)
    aktoriusFK = models.ForeignKey(Aktorius, on_delete=models.SET_NULL, null=True, related_name='filmas_set')

    def __str__(self):
        return f"{self.pavadinimas}"
