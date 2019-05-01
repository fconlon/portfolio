from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    return redirect('/allowance/home/')

def userhome(request):
    if request.user.is_authenticated:
        return render(request, 'allowance/home.html')
    else:
        return redirect('/allowance/login/')