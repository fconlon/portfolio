from django.shortcuts import render, redirect
#from django.http import HttpResponse
from allowance.models import ParentToChildren, ChildToParents
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