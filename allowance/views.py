from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from allowance.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.utils import IntegrityError
from decimal import Decimal
from json import dumps

# Create your views here.
def index(request):
    #need to add site homepage
    return redirect('/allowance/home/')

def userhome(request):
    #refactor this using ajax requests in the components
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
    childHist = { 'data' : [] }
    key = 1
    uname = request.POST['username']
    histList = History.objects.filter(uname=uname)
    for item in histList:
        childHist['data'].append({
            'reason': item.reason,
            'date': item.date,
            'transaction': item.transaction
        })
        key += 1
    return JsonResponse(childHist)

def addChild(request):
    uname = request.user.username
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    childUname = request.POST['username']
    childPassword = request.POST['password']

    try:
        newChild = User.objects.create_user(childUname, first_name=firstName,
                    last_name=lastName, password=childPassword)
    except IntegrityError:
        return JsonResponse({})

    AllowanceUserInfo.objects.create(user=newChild, is_parent=False, balance=0.0)

    existingChild = ParentToChildren.objects.filter(parent=request.user.username)[0].child
    qs = ParentToChildren.objects.filter(child=existingChild)

    for record in qs:
        ParentToChildren.objects.create(parent=record.parent, child=newChild)
        u = User.objects.get(username=record.parent)
        ChildToParents.objects.create(child=childUname, parent=u)

    return JsonResponse({ 'success': True })

def removeChild(request):
    uname = request.POST['username']
    try:
        user = User.objects.get(username=uname)
        user.delete()
    except User.DoesNotExist:
        return JsonResponse({})

    return JsonResponse({ 'success': True })

def changePassword(request):
    uname = request.user.username
    pw = request.POST['old_password']
    user = authenticate(username=uname, password=pw)
    if user:
        form = PasswordChangeForm(user, data=request.POST)
        form.full_clean()
        form.save()
        update_session_auth_hash(request, user)
        return JsonResponse({ 'success': True })
    else:
        return JsonResponse({})