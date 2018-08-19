from django.shortcuts import render
from titanic.models import Survivors
HRATIO = .003
# Create your views here.
def index(request):
    return render(request, 'titanic/index.html', build_titanic_context(''))

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
        for fltr in filters.split():
            if fltr == 'firstclass':
                value[0] = value[0].filter(pclass__exact=1)
            elif fltr == 'secondclass':
                value[0] = value[0].filter(pclass__exact=2)
            elif fltr == 'thirdclass':
                value[0] = value[0].filter(plcass__exact=3)
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
                value[0] = value[0].filter(age__gte=18).exclude(age__exact='')
        value.append(value[0].count() * HRATIO)
        value.append(value[1]/2)

    #add together appropriate cyl heights
    ctxt['scf'][2] += ctxt['fcf'][1]
    ctxt['tcf'][2] += ctxt['fcf'][1] + ctxt['scf'][1]
    ctxt['scm'][2] += ctxt['fcm'][1]
    ctxt['tcm'][2] += ctxt['fcm'][1] + ctxt['scm'][1]
    ctxt['scl'][2] += ctxt['fcl'][1]
    ctxt['tcl'][2] += ctxt['fcl'][1] + ctxt['scl'][1]
    ctxt['scd'][2] += ctxt['fcd'][1]
    ctxt['tcd'][2] += ctxt['fcd'][1] + ctxt['scd'][1]
    ctxt['scc'][2] += ctxt['fcc'][1]
    ctxt['tcc'][2] += ctxt['fcc'][1] + ctxt['scc'][1]
    ctxt['sca'][2] += ctxt['fca'][1]
    ctxt['tca'][2] += ctxt['fca'][1] + ctxt['sca'][1]

    return ctxt

