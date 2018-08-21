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
        'cyls': {
            #class
            'fc': [Survivors.objects.filter(pclass__exact=1)],
            'sc': [Survivors.objects.filter(pclass__exact=2)],
            'tc': [Survivors.objects.filter(pclass__exact=3)],
            #female
            'fcf': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='female')],
            'scf': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='female')],
            'tcf': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='female')],
            #male
            'fcm': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='male')],
            'scm': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='male')],
            'tcm': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='male')],
            #lived
            'fcl': [Survivors.objects.filter(pclass__exact=1).filter(survived=True)],
            'scl': [Survivors.objects.filter(pclass__exact=2).filter(survived=True)],
            'tcl': [Survivors.objects.filter(pclass__exact=3).filter(survived=True)],
            #died
            'fcd': [Survivors.objects.filter(pclass__exact=1).filter(survived=False)],
            'scd': [Survivors.objects.filter(pclass__exact=2).filter(survived=False)],
            'tcd': [Survivors.objects.filter(pclass__exact=3).filter(survived=False)],
            #child
            'fcc': [Survivors.objects.filter(pclass__exact=1).filter(age__lt=18)],
            'scc': [Survivors.objects.filter(pclass__exact=2).filter(age__lt=18)],
            'tcc': [Survivors.objects.filter(pclass__exact=3).filter(age__lt=18)],
            #adult
            'fca': [Survivors.objects.filter(pclass__exact=1).filter(age__gte=18).extra(where=["age!=''"])],
            'sca': [Survivors.objects.filter(pclass__exact=2).filter(age__gte=18).extra(where=["age!=''"])],
            'tca': [Survivors.objects.filter(pclass__exact=3).filter(age__gte=18).extra(where=["age!=''"])],
        },
        'parab': {
            #first class
            'fcmp': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='male')],
            'fcfp': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='female')],
            #second class
            'scmp': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='male')],
            'scfp': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='female')],
            #third class
            'tcmp': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='male')],
            'tcfp': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='female')],
            #female lived
            'fcflp': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='female').filter(survived=True)],
            'scflp': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='female').filter(survived=True)],
            'tcflp': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='female').filter(survived=True)],
            #female died
            'fcfdp': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='female').filter(survived=False)],
            'scfdp': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='female').filter(survived=False)],
            'tcfdp': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='female').filter(survived=False)],
            #male lived
            'fcmlp': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='male').filter(survived=True)],
            'scmlp': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='male').filter(survived=True)],
            'tcmlp': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='male').filter(survived=True)],
            #male died
            'fcmdp': [Survivors.objects.filter(pclass__exact=1).filter(sex__exact='male').filter(survived=False)],
            'scmdp': [Survivors.objects.filter(pclass__exact=2).filter(sex__exact='male').filter(survived=False)],
            'tcmdp': [Survivors.objects.filter(pclass__exact=3).filter(sex__exact='male').filter(survived=False)],
            #child lived
            'fcclp': [Survivors.objects.filter(pclass__exact=1).filter(age__lt=18).filter(survived=True)],
            'scclp': [Survivors.objects.filter(pclass__exact=2).filter(age__lt=18).filter(survived=True)],
            'tcclp': [Survivors.objects.filter(pclass__exact=3).filter(age__lt=18).filter(survived=True)],
            #child died
            'fccdp': [Survivors.objects.filter(pclass__exact=1).filter(age__lt=18).filter(survived=False)],
            'sccdp': [Survivors.objects.filter(pclass__exact=2).filter(age__lt=18).filter(survived=False)],
            'tccdp': [Survivors.objects.filter(pclass__exact=3).filter(age__lt=18).filter(survived=False)],
            #adult lived
            'fcalp': [Survivors.objects.filter(pclass__exact=1).filter(age__gte=18).extra(where=["age!=''"]).filter(survived=True)],
            'scalp': [Survivors.objects.filter(pclass__exact=2).filter(age__gte=18).extra(where=["age!=''"]).filter(survived=True)],
            'tcalp': [Survivors.objects.filter(pclass__exact=3).filter(age__gte=18).extra(where=["age!=''"]).filter(survived=True)],
            #adult died
            'fcadp': [Survivors.objects.filter(pclass__exact=1).filter(age__gte=18).extra(where=["age!=''"]).filter(survived=False)],
            'scadp': [Survivors.objects.filter(pclass__exact=2).filter(age__gte=18).extra(where=["age!=''"]).filter(survived=False)],
            'tcadp': [Survivors.objects.filter(pclass__exact=3).filter(age__gte=18).extra(where=["age!=''"]).filter(survived=False)],
        },
        'text': {}
    }

    #fliter cylinders
    for (key, value) in ctxt['cyls'].items():
        for fltr in filters.split('_'):
            if fltr == 'First Class':
                value[0] = value[0].filter(pclass__exact=1)
            elif fltr == 'Second Class':
                value[0] = value[0].filter(pclass__exact=2)
            elif fltr == 'Third Class':
                value[0] = value[0].filter(pclass__exact=3)
            elif fltr == 'Female':
                value[0] = value[0].filter(sex__exact='female')
            elif fltr == 'Male':
                value[0] = value[0].filter(sex__exact='male')
            elif fltr == 'Lived':
                value[0] = value[0].filter(survived__exact=True)
            elif fltr == 'Died':
                value[0] = value[0].filter(survived__exact=False)
            elif fltr == 'Child':
                value[0] = value[0].filter(age__lt=18)
            elif fltr == 'Adult':
                value[0] = value[0].filter(age__gte=18).extra(where=["age!=''"])
        value.append(round(value[0].count() * HRATIO, 4))
        value.append(round(value[1]/2, 4))
        value.pop(0)

    #filter parabolas
    for (key, value) in ctxt['parab'].items():
        for fltr in filters.split('_'):
            if fltr == 'First Class':
                value[0] = value[0].filter(pclass__exact=1)
            elif fltr == 'Second Class':
                value[0] = value[0].filter(pclass__exact=2)
            elif fltr == 'Third Class':
                value[0] = value[0].filter(pclass__exact=3)
            elif fltr == 'Female':
                value[0] = value[0].filter(sex__exact='female')
            elif fltr == 'Male':
                value[0] = value[0].filter(sex__exact='male')
            elif fltr == 'Lived':
                value[0] = value[0].filter(survived__exact=True)
            elif fltr == 'Died':
                value[0] = value[0].filter(survived__exact=False)
            elif fltr == 'Child':
                value[0] = value[0].filter(age__lt=18)
            elif fltr == 'Adult':
                value[0] = value[0].filter(age__gte=18).extra(where=["age!=''"])
        value.append(round(value[0].count() * HRATIO, 4))
        value.pop(0)

    #calculate cyl y position heights
    #class
    ctxt['cyls']['scf'][1] += ctxt['cyls']['fcf'][0]
    ctxt['cyls']['tcf'][1] += ctxt['cyls']['fcf'][0] + ctxt['cyls']['scf'][0]
    ctxt['cyls']['scm'][1] += ctxt['cyls']['fcm'][0]
    ctxt['cyls']['tcm'][1] += ctxt['cyls']['fcm'][0] + ctxt['cyls']['scm'][0]
    #lived
    ctxt['cyls']['scl'][1] += ctxt['cyls']['fcl'][0]
    ctxt['cyls']['tcl'][1] += ctxt['cyls']['fcl'][0] + ctxt['cyls']['scl'][0]
    #died
    ctxt['cyls']['scd'][1] += ctxt['cyls']['fcd'][0]
    ctxt['cyls']['tcd'][1] += ctxt['cyls']['fcd'][0] + ctxt['cyls']['scd'][0]
    #child
    ctxt['cyls']['scc'][1] += ctxt['cyls']['fcc'][0]
    ctxt['cyls']['tcc'][1] += ctxt['cyls']['fcc'][0] + ctxt['cyls']['scc'][0]
    #adult
    ctxt['cyls']['sca'][1] += ctxt['cyls']['fca'][0]
    ctxt['cyls']['tca'][1] += ctxt['cyls']['fca'][0] + ctxt['cyls']['sca'][0]

    #calculate parabola bot heights
    #first class
    ctxt['parab']['fcmp'].append(0)
    ctxt['parab']['fcfp'].append(0)
    #second class
    ctxt['parab']['scmp'].append(0)
    ctxt['parab']['scfp'].append(0)
    #third class
    ctxt['parab']['tcmp'].append(0)
    ctxt['parab']['tcfp'].append(0)
    #female lived
    ctxt['parab']['fcflp'].append(0)
    ctxt['parab']['scflp'][0] += ctxt['parab']['fcflp'][0]
    ctxt['parab']['scflp'].append('fcflp')
    ctxt['parab']['tcflp'][0] += ctxt['parab']['scflp'][0]
    ctxt['parab']['tcflp'].append('scflp')
    #female died
    ctxt['parab']['fcfdp'].append(0)
    ctxt['parab']['scfdp'][0] += ctxt['parab']['fcfdp'][0]
    ctxt['parab']['scfdp'].append('fcfdp')
    ctxt['parab']['tcfdp'][0] += ctxt['parab']['scfdp'][0]
    ctxt['parab']['tcfdp'].append('scfdp')
    #male lived
    ctxt['parab']['fcmlp'].append(0)
    ctxt['parab']['scmlp'][0] += ctxt['parab']['fcmlp'][0]
    ctxt['parab']['scmlp'].append('fcmlp')
    ctxt['parab']['tcmlp'][0] += ctxt['parab']['scmlp'][0]
    ctxt['parab']['tcmlp'].append('scmlp')
    #male died
    ctxt['parab']['fcmdp'].append(0)
    ctxt['parab']['scmdp'][0] += ctxt['parab']['fcmdp'][0]
    ctxt['parab']['scmdp'].append('fcmdp')
    ctxt['parab']['tcmdp'][0] += ctxt['parab']['scmdp'][0]
    ctxt['parab']['tcmdp'].append('scmdp')
    #child lived
    ctxt['parab']['fcclp'].append(0)
    ctxt['parab']['scclp'][0] += ctxt['parab']['fcclp'][0]
    ctxt['parab']['scclp'].append('fcclp')
    ctxt['parab']['tcclp'][0] += ctxt['parab']['scclp'][0]
    ctxt['parab']['tcclp'].append('scclp')
    #child died
    ctxt['parab']['fccdp'].append(0)
    ctxt['parab']['sccdp'][0] += ctxt['parab']['fccdp'][0]
    ctxt['parab']['sccdp'].append('fccdp')
    ctxt['parab']['tccdp'][0] += ctxt['parab']['sccdp'][0]
    ctxt['parab']['tccdp'].append('sccdp')
    #adult lived
    ctxt['parab']['fcalp'].append(0)
    ctxt['parab']['scalp'][0] += ctxt['parab']['fcalp'][0]
    ctxt['parab']['scalp'].append('fcalp')
    ctxt['parab']['tcalp'][0] += ctxt['parab']['scalp'][0]
    ctxt['parab']['tcalp'].append('scalp')
    #adult died
    ctxt['parab']['fcadp'].append(0)
    ctxt['parab']['scadp'][0] += ctxt['parab']['fcadp'][0]
    ctxt['parab']['scadp'].append('fcadp')
    ctxt['parab']['tcadp'][0] += ctxt['parab']['scadp'][0]
    ctxt['parab']['tcadp'].append('scadp')

    #calculate cyl text label heights
    #class
    ctxt['text']['fct'] = ctxt['cyls']['fc'][0] + .15
    ctxt['text']['sct'] = ctxt['cyls']['sc'][0] + .15
    ctxt['text']['tct'] = ctxt['cyls']['tc'][0] + .15
    #sex
    ctxt['text']['ft'] = ctxt['cyls']['fcf'][0] + ctxt['cyls']['scf'][0] + ctxt['cyls']['tcf'][0] + .15
    ctxt['text']['mt'] = ctxt['cyls']['fcm'][0] + ctxt['cyls']['scm'][0] + ctxt['cyls']['tcm'][0] + .15
    #survived
    ctxt['text']['lt'] = ctxt['cyls']['fcl'][0] + ctxt['cyls']['scl'][0] + ctxt['cyls']['tcl'][0] + .15
    ctxt['text']['dt'] = ctxt['cyls']['fcd'][0] + ctxt['cyls']['scd'][0] + ctxt['cyls']['tcd'][0] + .15
    #age
    ctxt['text']['ct'] = ctxt['cyls']['fcc'][0] + ctxt['cyls']['scc'][0] + ctxt['cyls']['tcc'][0] + .15
    ctxt['text']['at'] = ctxt['cyls']['fca'][0] + ctxt['cyls']['sca'][0] + ctxt['cyls']['tca'][0] + .15


    return ctxt
