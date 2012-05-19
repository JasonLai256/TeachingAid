# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from taCore.forms import *
from taCore.models import *
from knowledge.models import Question



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
    user = request.user
    if user.teacher_set.count() != 0:
        identity = 't'
        t = Teacher.objects.get(user=user)
        courses = [c for c in t.course_set.all()]
        status = {
            'title': u'老师',
            'courses': courses,
            'info': t.descript,
        }
    elif user.student_set.count() != 0:
        identity = 's'
        s = Student.objects.get(user=user)
        status = {
            'title': u'同学',
            'stuid': s.user.username,
        }
    else:
        identity = 'm'
        status = {
            'title': '',
            }
        
    questions = Question.objects.can_view(request.user)[0:20]
        
    variables = RequestContext(request, {
            'identity': identity,
            'status': status,
            'questions': questions,
            'count': len(questions),
            })
    return render_to_response('taCore/main.html', variables)

@login_required
def teach_aid(request, courseid):
    query = request.GET.get('query')
    select = request.GET.get('select')
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
        comments = [comment for comment in appra.comment_set.all()]
        res = {
            'stu_name': stu.user.first_name,
            'stu_id': stu.user.username,
            'appr_counter': appra.appr_counter,
            'excellence_counter': appra.excellence_counter,
            'good_counter': appra.good_counter,
            'bad_counter': appra.bad_counter,
            'absent_counter': appra.absent_counter,
            'leave_counter': appra.leave_counter,
            'come_late_counter': appra.come_late_counter,
            'last_appr': appra.last_appr,
            'slug': appra.slug,
            'comments': comments,
        }
        appraisals.append(res)

    appraisals = _make_order(appraisals, query)
    group = _select_apprs(appraisals, select)

    variables = RequestContext(request, {
            'appraisals': appraisals,
            'amount': len(appraisals),
            'courseid': courseid,
            'coursename': course.name,
            'selected_group': group,
    })
    return render_to_response('taCore/teach_aid.html', variables)

def _create_appraisal(slug, course, stu):
    appr = Appraisal(slug=slug, course=course, student=stu)
    appr.save()

def _select_apprs(appraisals, select):
    """selector format is like 'query-number', `query` is the content for the
    select, `num` is the number of seleting appraisal.
    """
    if not select:
        return
    query, num = select.rsplit('-', 1)
    num = int(num)
    if query == 'random':
        from random import shuffle
        shuffle(appraisals)
        ret = appraisals[:num]
    else:
        ret = _make_order(appraisals, query)
        
    return ret

def _make_order(appraisals, query):
    apprs = None
    if not query:
        apprs = appraisals
    elif query == "name":
        apprs = sorted(appraisals,key=lambda e: e['stu_name'])
    elif query == "last-excellence":
        apprs = [a for a in appraisals if a['last_appr'] == 'excellence']
    elif query == "last-good":
        apprs = [a for a in appraisals if a['last_appr'] == 'good']
    elif query == "last-bad":
        apprs = [a for a in appraisals if a['last_appr'] == 'bad']
    elif query == "last-absent":
        apprs = [a for a in appraisals if a['last_appr'] == 'absent']
    elif query == "last-leave":
        apprs = [a for a in appraisals if a['last_appr'] == 'leave']
    elif query == "last-come-late":
        apprs = [a for a in appraisals if a['last_appr'] == 'come_late']
    elif query == "most-count":
        apprs = sorted(appraisals,key=lambda e: e['appr_counter'])
        apprs.reverse()
    elif query == "most-excellence":
        apprs = sorted(appraisals,key=lambda e: e['excellence_counter'])
        apprs.reverse()
    elif query == "most-good":
        apprs = sorted(appraisals,key=lambda e: e['good_counter'])
        apprs.reverse()
    elif query == "most-bad":
        apprs = sorted(appraisals,key=lambda e: e['bad_counter'])
        apprs.reverse()
    elif query == "most-absent":
        apprs = sorted(appraisals,key=lambda e: e['absent_counter'])
        apprs.reverse()
    elif query == "most-leave":
        apprs = sorted(appraisals,key=lambda e: e['leave_counter'])
        apprs.reverse()
    elif query == "most-come-late":
        apprs = sorted(appraisals,key=lambda e: e['come_late_counter'])
        apprs.reverse()
    elif query == "least-count":
        apprs = sorted(appraisals,key=lambda e: e['appr_counter'])
    elif query == "most-comment":
        apprs = sorted(appraisals,key=lambda e: len(e['comments']))
        apprs.reverse()
    else:
        apprs = appraisals
    return apprs
    

@login_required
def appraisal_poll(request, slug):
    poll = request.POST['appraisal']
    comm = request.POST['comment']
    
    appra = get_object_or_404(Appraisal, slug=slug)
    if poll == 'excellence':
        appra.excellence_counter += 1
    elif poll == 'good':
        appra.good_counter += 1
    elif poll == 'bad':
        appra.bad_counter += 1
    elif poll == 'absent':
        appra.absent_counter += 1
    elif poll == 'leave':
        appra.leave_counter += 1
    elif poll == 'come_late':
        appra.come_late_counter += 1
    else:
        raise ValidationError('invalid radio field name.')
    appra.last_appr = poll
    appra.appr_counter += 1
    appra.save()

    if comm:
        comment = Comment(comment=comm, appraisal=appra)
        comment.save()

    courseid = str(appra.course.id)
    return HttpResponseRedirect('/teach-aid/'+courseid)
    
