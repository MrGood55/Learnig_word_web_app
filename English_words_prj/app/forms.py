from django import forms
from .models import ModelWords

FORMAT_CHOICES = {
    ('xls','xls'),
    ('csv','csv'),
    ('json','json')
}
class WordsFrom(forms.ModelForm):
    class Meta:
        model = ModelWords
        fields = '__all__'
        labels = {
            'categorie' : 'Раздел',
            'rus_name' : 'Слово на русском',
            'eng_name' : 'Слово на английском',
        }
class CheckWordsFrom(forms.Form):
    eng_name = forms.CharField(label='',max_length=100,empty_value='word is ..',strip=True,
                               widget=forms.TextInput(attrs={'class':"""form-control 
                                                                       border border-primary 
                                                                       overflow-x-scroll w-100""",
                                'placeholder':"word"}))


class FormatExportForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES,widget=forms.Select(attrs={'class':'form-select'}))

