from django.urls import path
#from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'allowance'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.userhome, name='home'),
    path('update/', views.updateBalance, name='update'),
    path('childhistory/', views.childHistory, name="childhistory"),
    path('removechild/', views.removeChild, name="removechild"),
    path('addchild/', views.addChild, name="addChild"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
