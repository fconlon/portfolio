from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'allowance'
urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('home/', views.userhome, name='home')
]
