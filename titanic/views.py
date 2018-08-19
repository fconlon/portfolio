from django.shortcuts import render
from django.http import HttpResponse
from titanic.models import Survivors
from json import dumps

HRATIO = .003

def index(request):
    return render(request, 'titanic/index.html', build_titanic_context(''))

def fltrs(request):
    return HttpResponse(dumps(build_titanic_context(request.GET['q'])))

def build_titanic_context(filters):
    #initialize context
    ctxt = {
        'fc': [Survivors.objects.filter(pclass__exact=1)],
        'sc': [Survivors.objects.filter(pclass__exact=2)],
        'tc': [Survivors.objects.filter(pclass__exact=3)],
        'fcf': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='female')],
        'scf': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='female')],
        'tcf': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='female')],
        'fcm': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='male')],
        'scm': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='male')],
        'tcm': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='male')],
        'fcl': [Survivors.objects.filter(pclass__exact=1).filter(survived=True)],
        'scl': [Survivors.objects.filter(pclass__exact=2).filter(survived=True)],
        'tcl': [Survivors.objects.filter(pclass__exact=3).filter(survived=True)],
        'fcd': [Survivors.objects.filter(pclass__exact=1).filter(survived=False)],
        'scd': [Survivors.objects.filter(pclass__exact=2).filter(survived=False)],
        'tcd': [Survivors.objects.filter(pclass__exact=3).filter(survived=False)],
        'fcc': [Survivors.objects.filter(pclass__exact=1).filter(age__lt=18)],
        'scc': [Survivors.objects.filter(pclass__exact=2).filter(age__lt=18)],
        'tcc': [Survivors.objects.filter(pclass__exact=3).filter(age__lt=18)],
        'fca': [Survivors.objects.filter(pclass__exact=1).filter(age__gte=18)],
        'sca': [Survivors.objects.filter(pclass__exact=2).filter(age__gte=18)],
        'tca': [Survivors.objects.filter(pclass__exact=3).filter(age__gte=18)],
    }

    #add extra filters
    for (key, value) in ctxt.items():
        for fltr in filters.split('_'):
            if fltr == 'firstclass':
                value[0] = value[0].filter(pclass__exact=1)
            elif fltr == 'secondclass':
                value[0] = value[0].filter(pclass__exact=2)
            elif fltr == 'thirdclass':
                value[0] = value[0].filter(pclass__exact=3)
            elif fltr == 'female':
                value[0] = value[0].filter(sex__exact='female')
            elif fltr == 'male':
                value[0] = value[0].filter(sex__exact='male')
            elif fltr == 'lived':
                value[0] = value[0].filter(survived__exact=True)
            elif fltr == 'died':
                value[0] = value[0].filter(survived__exact=False)
            elif fltr == 'child':
                value[0] = value[0].filter(age__lt=18)
            elif fltr == 'adult':
                value[0] = value[0].filter(age__gte=18).extra(where=["age!=''"])
        value.append(round(value[0].count() * HRATIO, 4))
        value.append(round(value[1]/2, 4))
        value.pop(0)

    #add together appropriate cyl heights
    ctxt['scf'][1] += ctxt['fcf'][0]
    ctxt['tcf'][1] += ctxt['fcf'][0] + ctxt['scf'][0]
    ctxt['scm'][1] += ctxt['fcm'][0]
    ctxt['tcm'][1] += ctxt['fcm'][0] + ctxt['scm'][0]
    ctxt['scl'][1] += ctxt['fcl'][0]
    ctxt['tcl'][1] += ctxt['fcl'][0] + ctxt['scl'][0]
    ctxt['scd'][1] += ctxt['fcd'][0]
    ctxt['tcd'][1] += ctxt['fcd'][0] + ctxt['scd'][0]
    ctxt['scc'][1] += ctxt['fcc'][0]
    ctxt['tcc'][1] += ctxt['fcc'][0] + ctxt['scc'][0]
    ctxt['sca'][1] += ctxt['fca'][0]
    ctxt['tca'][1] += ctxt['fca'][0] + ctxt['sca'][0]

    return ctxt

