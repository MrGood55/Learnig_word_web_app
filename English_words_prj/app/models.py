from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class ModelWords(models.Model):
    class Meta:
        verbose_name = 'Words'
        verbose_name_plural = 'Words'
    rus_name = models.CharField(max_length=40)#,default='Слово'
    eng_name = models.CharField(max_length=40)#,default='Word'd
    cat = models.ForeignKey('ModelCatsWords', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return self.rus_name

class ModelCatsWords(models.Model):
    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=100, db_index=True)#default='Категория'
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})
class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel')