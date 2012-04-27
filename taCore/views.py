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


@login_required
def teach_aid(request, coursename):
    course = get_object_or_404(Course, name=coursename)
    students = []
    for cls in course.classes.all():
        for stu in cls.student_set.all():
            students.append(stu)
    appraisals = []
    for stu in students:
        appra = get_object_or_404(Appraisal, student=stu)
        comments = [cmt for cmt in appra.comment.all()]
        res = {
            'stu_name': stu.user.firstname,
            'appr_counter': appra.appr_counter,
            'excellence_counter': appra.excellence_counter,
            'good_counter': appra.good_counter,
            'bad_counter': appra.bad_counter,
            'last_appr': appra.last_appr,
            'slug': appra.slug,
        }
        appraisals.append(res)

    variables = RequestContext（request, {
            'appraisals': appraisals,
    })
    return render_to_response('taCore/teach_aid.html', variables)

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
    
