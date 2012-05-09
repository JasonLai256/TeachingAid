# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

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
    variables = RequestContext(request, {})
    return render_to_response('taCore/main.html', variables)


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


@login_required
def teach_aid(request, courseid):
    query = request.GET.get('query')
    course = get_object_or_404(Course, id=courseid)
    students = []
    for cls in course.classes.all():
        for stu in cls.student_set.all():
            students.append(stu)
    appraisals = []
    for stu in students:
        slug = unicode(course.id) + '-' + stu.user.username
        try:
            appra = Appraisal.objects.get(slug=slug)
        except ObjectDoesNotExist:
            _create_appraisal(slug, course, stu)
        res = {
            'stu_name': stu.user.first_name,
            'stu_id': stu.user.username,
            'appr_counter': appra.appr_counter,
            'excellence_counter': appra.excellence_counter,
            'good_counter': appra.good_counter,
            'bad_counter': appra.bad_counter,
            'last_appr': appra.last_appr,
            'slug': appra.slug,
            'comments': appra.comment_set.all(),
        }
        appraisals.append(res)

    appraisals = _make_order(appraisals, query)

    variables = RequestContext(request, {
            'appraisals': appraisals,
            'amount': len(appraisals),
            'courseid': courseid,
            'coursename': course.name,
    })
    return render_to_response('taCore/teach_aid.html', variables)

def _create_appraisal(slug, course, stu):
    appr = Appraisal(slug=slug, course=course, student=stu)
    appr.save()

def _make_order(appraisals, query):
    if not query:
        pass
    elif query == "name":
        appraisals.sort(key=lambda e: e['stu_name'])
    elif query == "last-excellence":
        pass
    elif query == "last_good":
        pass
    elif query == "last_bad":
        pass
    elif query == "most-count":
        pass
    elif query == "most-excellence":
        pass
    elif query == "most-good":
        pass
    elif query == "most-bad":
        pass
    elif query == "no-count":
        pass
    elif query == "most-comment":
        pass
    elif query == "":
        pass
    elif query == "":
        pass
    return appraisals
    

@login_required
def appraisal_poll(request, slug):
    poll = request.POST['appraisal']
    appra = get_object_or_404(Appraisal, slug=slug)
    if poll == 'excellence':
        appra.excellence_counter += 1
        appra.last_appr = 'excellence'
    elif poll == 'good':
        appra.good_counter += 1
        appra.last_appr = 'good'
    elif poll == 'bad':
        appra.bad_counter += 1
        appra.last_appr = 'bad'
    else:
        pass

    appra.appr_counter += 1

    return redirect_to('')

@login_required    
def appraisal_comment(request, slug):
    cmt = request.POST['comment']
    cmt = Comment(comment=cmt)
    appra = get_object_or_404(Appraisal, slug=slug)
    
