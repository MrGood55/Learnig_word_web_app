from django import forms
from .models import ModelWords,ModelCatsWords
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

### Add your models here
FORMAT_CHOICES = {
    ('xlsx','xlsx'),
    ('csv','csv'),
    ('json','json')
}
class WordsFrom(forms.ModelForm):
    # cat =
    def __init__(self, *args, **kwargs):
        # author = kwargs.pop('user')

        super().__init__(*args, **kwargs)
        # self.fields['lists'].queryset = List.objects.filter(user=user)

        for visible in self.visible_fields():
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = ModelWords
        # fields =  '__all__'
        fields =  ['rus_name', 'eng_name','cat'] #'__all__'
        # exclude =  ['rus_name', 'eng_name','cat'] #'__all__'
        labels = {
            'categorie' : 'Раздел',
            'rus_name' : 'Слово на русском',
            'eng_name' : 'Слово на английском',
            'cat' : 'Категория'
        }
class ModelCatsWordsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Категория'

    class Meta:
        model = ModelCatsWords
        fields = ['name']
        labels = {
            'name': 'Категория'
        }

class CheckWordsFrom(forms.Form):
    eng_name = forms.CharField(label='',max_length=100,empty_value='word is ..',strip=True,
                               widget=forms.TextInput(attrs={'class':"""form-control 
                                                                       border border-primary 
                                                                       overflow-x-scroll w-100""",
                                'placeholder':"word"}))


class FormatExportForm(forms.Form):
    format = forms.ChoiceField(choices=FORMAT_CHOICES,widget=forms.Select(attrs={'class':'form-select'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

