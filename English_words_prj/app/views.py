import csv

from django.shortcuts import render,redirect


from .forms import *
from .models import *

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, FormView, CreateView
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseNotFound, JsonResponse

from django.contrib import messages
import random

## For import/export
from tablib import Dataset
import json
from openpyxl import Workbook

## For users
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
### Create your views here.

def index(requset):
    return render(requset,'app/index.html')




class WordsFormView(View):

    def get(self,request):

        form_for_word = WordsFrom(request.GET,request=request)
        # form_for_word = WordsFrom()


        form_for_categorie = ModelCatsWordsForm()

        return render(request,'app/appendwords.html',context={'form':form_for_word,'form_for_categorie':form_for_categorie})
    def post(self,request):

        if self.request.POST.get('form-type') == 'form_for_word':
            form_for_word = WordsFrom(request.POST)
            if form_for_word.is_valid():
                word_form = form_for_word.save(commit=False)
                word_form.author = User.objects.get(username=request.user.username)
                word_form.save()
                messages.info(request, "Слово создано!",fail_silently=True)
                return HttpResponseRedirect('appendwords')
            return render(request,'app/appendwords.html',context={'form':form_for_word})
        elif self.request.POST.get('form-type') == 'form_for_categorie':
            form_for_categorie = ModelCatsWordsForm(request.POST)
            if form_for_categorie.is_valid():
                word_form = form_for_categorie.save(commit=False)
                # word_form.author = User.objects.get(user=request.user.username)
                word_form.author = User.objects.get(username=request.user.username)
                word_form.save()
                messages.info(request, "Категория создана!", fail_silently=True)
                return HttpResponseRedirect('appendwords')
            return render(request, 'app/appendwords.html', context={'form_for_categorie': form_for_categorie})


def check_eng_words(request):
    # words = ModelWords.objects.values_list() #'eng_name'
    # words = ModelWords.objects.filter(cat_id=1) # between all objects by 'cat_id'
    # words = ModelWords.objects.get(id=1) #  one object from group by 'id'
    if request.user.is_authenticated:
        words = ModelWords.objects.filter(author=request.user.id)
    else:
        words = []
    if len(words) == 0:
        return render(request,'app/error/havenotwords.html')
    random_word = random.choice(words)
    word = { 'rus_name': random_word.rus_name,'eng_name': random_word.eng_name   }
    # print(word)
    if request.method == 'POST':
        form = CheckWordsFrom(request.POST)
        if form.is_valid():
            # print(words)
            # print(form.cleaned_data)
            if word['eng_name'] == form.cleaned_data['eng_name']:
                messages.info(request, "True", fail_silently=True)
            else:
                messages.info(request, "Wrong", fail_silently=True)
    else:
        form = CheckWordsFrom()

    return render(request,'app/checkwords.html',{'form':form,'word':word})



class DoneView(TemplateView):
    template_name = 'app/done.html'

class ListWords(ListView,FormView):
    template_name = 'app/list.html'
    model = ModelWords
    form_class = FormatExportForm
    paginate_by = 10
    context_object_name = 'list_of_words'

    def get_queryset(self):
        # return ModelWords.objects.order_by('-id')
        return ModelWords.objects.filter(author=self.request.user.id)



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['cats'] = ModelCatsWords.objects.all()
        context['cats'] = ModelCatsWords.objects.filter(author=self.request.user.id)
        return context


class ListWordsCategory(ListView):
    model = ModelWords
    paginate_by = 10
    template_name = 'app/list.html'
    context_object_name = 'list_of_words'
    allow_empty = False

    def get_queryset(self):
        return ModelWords.objects.filter(cat_id=self.kwargs['cat_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['list_of_words'][0].cat)
        context['cat_selected'] = context['list_of_words'][0].cat_id
        context['cats']  = ModelCatsWords.objects.all()
        return context

def delete(request, id_word):
    word = ModelWords.objects.get(id=id_word)
    word.delete()
    return redirect('list')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')






def simple_export(request):
    objs = ModelWords.objects.all()
    # dataset = Dataset()
    format = request.POST.get('format')
    if format == 'xlsx':
        response = HttpResponse(content_type=f'{format}')
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Words"

        # Add headers
        headers = ['Russian', 'English']
        ws.append(headers)
        # Add data from the model
        for item in objs:
            ws.append([item.rus_name, item.eng_name])
        # Save the workbook to the HttpResponse
        wb.save(response)
        return response

    elif format == 'csv':
        response = HttpResponse(content_type=f'{format}')
        data = csv.writer(response)
        data.writerow(['Russian', 'English'])
        data.writerows(objs.values_list('rus_name', 'eng_name'))
        response['Content-Disposition'] = f'attachment; filename=words.{format}'
        return response
    elif format == 'json':
        json_data = json.dumps(list(objs.values('rus_name', 'eng_name')), ensure_ascii=False)
        response = HttpResponse(json_data, content_type=f'{format}')
        response['Content-Disposition'] = f'attachment; filename=words.{format}'
        return response


def simple_upload(request):
    try:
        if request.method == 'POST':
            dataset = Dataset()
            new_modelwords = request.FILES['myfile']
            if not new_modelwords.name.endswith('xlsx'):
                messages.error(request,'wrong format') # MESSAGE
                return HttpResponse('wrong format') # DELETE IT
            else:
                imported_data = dataset.load(new_modelwords.read(), format='xlsx')
                # print(imported_data)
                for data in imported_data:
                    print(data[0],data[1])
                    ModelWords.objects.create(
                            rus_name = data[0],
                            eng_name = data[1],)
                messages.success(request, 'Data is imported') # MESSAGE
    except Exception as E:
        #     print(E)
        messages.error(request, 'Error')  # MESSAGE

    return render(request, 'app/importform.html')


## РЕГИСТРАЦИЯ пользователей
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list')
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'app/login.html'
    def get_success_url(self):
        return reverse_lazy('list')

def logout_user(request):
    logout(request)
    return redirect('login')