from django.shortcuts import render
from titanic.models import Survivors

# Create your views here.
def index(request):
    firstclass = Survivors.objects.filter(pclass__exact=1)
    context = { 'firstclass': firstclass }
    return render(request, 'titanic/index.html', context)
