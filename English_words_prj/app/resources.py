from import_export import resources
from .models import ModelWords

class WordsResources(resources.ModelResource):
    class Meta:
        model = ModelWords
        # fields = ('id', 'name', 'price',)
        # export_order = ()
        fields = '__all__'