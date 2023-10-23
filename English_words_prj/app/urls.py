"""
URL configuration for English_words_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [

    path('appendwords', views.WordsFormView.as_view(),name='appendwords'),
    path('checkwords', views.check_eng_words,name='checkwords'),
    path('done', views.DoneView.as_view(),name='done'),
    path('', views.ListWords.as_view(),name='list'),
    path('delete/<int:id_word>', views.delete,name='delete'),
    path('category/<int:cat_id>/', views.ListWordsCategory.as_view(), name='category'),
    path('import_export_words', views.simple_upload, name='import_export_words'),
    path('import_words', views.simple_upload, name='import_words'),
    path('export_words', views.simple_export, name='export_words'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),

]


