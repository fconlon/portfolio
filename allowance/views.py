from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from allowance.models import ParentToChildren, ChildToParents, History
from django.contrib.auth.models import User
from decimal import Decimal
from json import dumps

# Create your views here.
def index(request):
    return redirect('/allowance/home/')

def userhome(request):
    if request.user.is_authenticated:
        userDict = {
            'userName' : request.user.username,
            'firstName' : request.user.first_name,
            'lastName' : request.user.last_name
        }
        ctxt = {'userDict' : dumps(userDict)}
        if request.user.allowanceuserinfo.is_parent:
            qs = ParentToChildren.objects.filter(parent=request.user.username)
            childrenDict = {}
            for tup in qs:
                childrenDict[tup.child.username] = {
                    'firstName' : tup.child.first_name,
                    'lastName' : tup.child.last_name,
                    'balance' : str(tup.child.allowanceuserinfo.balance)
                }
            ctxt['childrenDict'] = dumps(childrenDict)
        else:
            qs = ChildToParents.objects.filter(child=request.user.username)
            ctxt['parents'] = qs
        return render(request, 'allowance/home.html', ctxt)
    else:
        return redirect('/allowance/login/')

def updateBalance(request):
    uname = request.POST['username']
    reason = request.POST['rsn']
    amount = Decimal(request.POST['amt'])
    u = User.objects.get(username=uname)
    if request.POST['type'] == 'Withdraw':
        u.allowanceuserinfo.balance -= amount
        History.objects.create(uname=uname, reason=reason, transaction=-amount)
    else:
        u.allowanceuserinfo.balance += amount
        History.objects.create(uname=uname, reason=reason, transaction=amount)
    u.allowanceuserinfo.save()
    return HttpResponse('Success')

def childHistory(request):
    childHist = {}
    key = 1
    uname = request.POST['username']
    histList = History.objects.filter(uname=uname)
    for item in histList:
        childHist[key] = {
            'reason': item.reason,
            'date': item.date,
            'transation': item.transaction
        }
        key += 1
    return JsonResponse(childHist)