import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import date
import uuid
from tinymce.models import HTMLField
from PIL import Image


import uuid

class Category(models.Model):
    name = models.CharField("Kategorija", max_length=25)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategorija"
        verbose_name_plural = "Kategorijos"


class Aktorius(models.Model):
    vardas_pavarde = models.CharField('Vardas pavarde', max_length=100)
    g_metai = models.IntegerField('Gimimo data')
    kinografija = HTMLField()
    nuotrauka = models.ImageField("Nuotrauka", upload_to="photo", null=True, blank=True)


    def __str__(self):
        return f"{self.vardas_pavarde}"

    class Meta:
        verbose_name = "Aktorius"
        verbose_name_plural = "Aktoriai"

    def display_filmai(self):
        return ', '.join(filmas.pavadinimas for filmas in self.filmas.all()[:3])

    def get_absolute_url(self):
        return reverse('aktorius-vienas', args=[str(self.id)])


class Filmas(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100)
    rating = models.FloatField(null=True, blank=True)
    rodymo_data = models.IntegerField('Rodomas nuo:')
    aprasymas = HTMLField()
    aktoriusFK = models.ForeignKey(Aktorius, on_delete=models.SET_NULL, null=True, related_name='filmas_set', verbose_name="Aktorius")
    category = models.ManyToManyField(Category, help_text="Išrinkite kategorija")
    cover = models.ImageField("Viršelis", upload_to="covers", null=True, blank=True)

    def __str__(self):
        return f"{self.pavadinimas}"
    def get_absolute_url(self):
        return reverse('filmas-vienas', args=[str(self.id)])

    class Meta:
        verbose_name = "Filmas"
        verbose_name_plural = "Filmai"


class FilmasInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    filmas = models.ForeignKey('Filmas', on_delete=models.CASCADE, related_name='filmasinstance_set')
    due_back = models.DateField('Bus prieinamas', null=True, blank=True)


    LOAN_STATUS = (
        ('gr', 'Grazinta'),
        ('pa', 'Paimta'),
        ('ga', 'Galima paimti'),
        ('re', 'Rezervuota')
    )

    status = models.CharField(
        max_length=2,
        choices=LOAN_STATUS,
        blank=True,
        default='ga',
        help_text='Kopijos statusas')


    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id}"


class Review(models.Model):
    review_date = models.DateTimeField(auto_now_add=True)
    rate_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    stars = models.IntegerField(choices=rate_choices)
    comment = models.TextField('Atsiliepimas', max_length=2000)
    movie = models.ForeignKey(Filmas, on_delete=models.CASCADE, related_name='filmasreview_set', blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.movie.pavadinimas} - {self.author}'

class AReview(models.Model):
    review_date = models.DateTimeField(auto_now_add=True)
    rate_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    stars = models.IntegerField(choices=rate_choices)
    comment = models.TextField('Atsiliepimas', max_length=2000)
    aktorius = models.ForeignKey(Filmas, on_delete=models.CASCADE, related_name='aktoriusreview_set', blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    nuotrauka = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} profilis"

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = "Profiliai"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if (img.height > 300) or (img.width > 300):
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
