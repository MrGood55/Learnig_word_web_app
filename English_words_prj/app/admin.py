from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


from import_export import resources


class WordsResources(resources.ModelResource):
    class Meta:
        model = ModelWords
        # fields = ('id', 'name', 'price',)
        # export_order = ()
        fields = '__all__'
# Register your models here.

# admin.site.register(ModelWords)
# admin.site.register(ModelCatsWords)
@admin.register(ModelCatsWords)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('name','author')
@admin.register(ModelWords)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('rus_name', 'eng_name','cat','author')