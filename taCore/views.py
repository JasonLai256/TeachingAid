from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

from taCore.forms import *
from taCore.models import *



def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main')
    else:
        return HttpResponseRedirect('/login')


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def main_page(request):
    # shared_bookmarks = SharedBookmark.objects.order_by('-date')[:10]
    # variables = RequestContext(request, {
    #         'shared_bookmarks': shared_bookmarks
    # })
    return render_to_response('taCore/main.html')


