from django.shortcuts import render, redirect
#from django.http import HttpResponse
from allowance.models import ParentToChildren, ChildToParents

# Create your views here.
def index(request):
    return redirect('/allowance/home/')

def userhome(request):
    if request.user.is_authenticated:
        ctxt = {}
        if request.user.allowanceuserinfo.is_parent:
            qs = ParentToChildren.objects.filter(parent=request.user.username)
            ctxt['children'] = qs
        else:
            qs = ChildToParents.objects.filter(child=request.user.username)
            ctxt['parents'] = qs
        return render(request, 'allowance/home.html', ctxt)
    else:
        return redirect('/allowance/login/')