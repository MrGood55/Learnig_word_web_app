from django.db import models
from django.urls import reverse

# Create your models here.


class ModelWords(models.Model):
    # categorie = models.CharField(max_length=40,default='Раздел')
    rus_name = models.CharField(max_length=40,default='Слово')
    eng_name = models.CharField(max_length=40,default='Word')
    cat = models.ForeignKey('ModelCatsWords', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.rus_name

class ModelCatsWords(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel')