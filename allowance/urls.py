from django.urls import path
from . import views

app_name = 'allowance'
urlpatterns = [
    path('', views.index, name='index'),
]
