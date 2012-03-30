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


@login_required
def course_page(request, course_name):
    pass


@login_required
def student_page(request, stuid):
    student = get_object_or_404(User, username=stuid)
    stuinfo = student.student_set.all()[0]
    courses = stuinfo.course_set.all()
    
    variables = RequestContext(request, {
            'username': student.first_name,
            'stuid': student.username,
            'courses': courses,
            'info': stuinfo
            })
    return render_to_response('taCore/student_page.html', variables)


@login_required
def teather_page(request, username):
    teather = get_object_or_404(User, username=username)
    tchinfo = teather.teacher_set.all()[0]
    class_info = tchinfo.leading_class

    variables = RequestContext(request, {
            'username': teather.first_name,
            'info': tchinfo,
            })
    return render_to_response('taCore/teacher_page.html', variables)

