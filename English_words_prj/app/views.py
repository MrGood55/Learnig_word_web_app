from django.shortcuts import render,redirect
from .forms import *
from .models import *
# from .resources import *
from .admin import WordsResources
from django.urls import reverse_lazy

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView,FormView
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseNotFound, JsonResponse
# from django.core.paginator import Paginator
from django.contrib import messages
import random

## For import/export
from tablib import Dataset
import pandas as pd

### Create your views here.

def index(requset):
    return render(requset,'app/index.html')

class WordsFormView(View):
    def get(self,request):
        form = WordsFrom()

        return render(request,'app/appendwords.html',context={'form':form})
    def post(self,request):
        form = WordsFrom(request.POST)
        if form.is_valid():
            form.save()

            messages.info(request, "Задача создана!",fail_silently=True)
            return HttpResponseRedirect('appendwords')

        return render(request,'app/appendwords.html',context={'form':form})

# class CheckWordsFormView(View):
#     def get(self,request):
#         form = CheckWordsFrom()
#         words = ModelWords.objects.all()
#         return render(request,'app/checkwords.html',context={'form':form,'words':words})
#     def post(self,request):
#         form = WordsFrom(request.POST)
#         if form.is_valid():
#
#             messages.success(request, "Проверим!",fail_silently=True)
#             return HttpResponseRedirect('appendwords')
#
#         return render(request,'app/checkwords.html',context={'form':form})

def check_eng_words(request):
    # words = ModelWords.objects.values_list() #'eng_name'
    # words = ModelWords.objects.filter(cat_id=1) # between all objects by 'cat_id'
    # words = ModelWords.objects.get(id=1) #  one object from group by 'id'

    words = ModelWords.objects.all()
    print(len(words))
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
    def post(self, request, **kwargs):
        qs = self.get_queryset()
        dataset = Dataset()
        # print('qs is ',qs)
        # dataset = WordsResources().export(queryset=qs)
        # dataset = WordsResources().export()


        # print('dataset is ',dataset.csv)

        format =  request.POST.get('format')

        dataset = dataset.load(qs, format=format)
        for num, i in enumerate(dataset):
            print(num, i)

        if format == 'xls':
            # ds = dataset.xls
            ds = dataset.load(qs, format=format)
        elif format == 'csv':
            # ds = dataset.csv
            ds = dataset.load(qs, format=format)

        else:
            # ds = dataset.json
            ds = dataset.load(qs, format=format)

        response = HttpResponse(ds, content_type=f'{format}')
        response['Content-Disposition'] = f'attachment; filename=posts.{format}'
        return response

    def get_queryset(self):
        return ModelWords.objects.order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = ModelCatsWords.objects.all()
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



import time

# class SimpleExportWithResouces(ListView,FormView):
#     model = ModelWords
#     template_name = 'app/list.html'
#     form_class = FormatExportForm
#     def post(self, request, **kwargs):
#         qs = self.get_queryset()
#         dataset = WordsResources().export(qs)
#
#         format =  request.POST.get('format')
#         if format == 'xls':
#             ds = dataset.xls
#         elif format == 'csv':
#             ds = dataset.csv
#         else:
#             ds = dataset.json
#         response = HttpResponse(ds, content_type=f'{format}')
#         response['Content-Disposition'] = f'attachment; filename=posts.{format}'
#         return response
def simple_export(request):
    try:
        start = time.time() #################################
        objs = ModelWords.objects.all()
        data = []
        for obj in objs:
            data.append({
                'rus_name': obj.rus_name,
                'eng_name': obj.rus_name,
                'cat': obj.cat
            })
            pd.DataFrame(data).to_excel('output.xlsx')
        end = time.time()
        print(end - start)
    except:
        messages.success(request, 'Data is downloaded')  # MESSAGE
    # return redirect('list')
    return JsonResponse({
        'status' : 200
    })
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