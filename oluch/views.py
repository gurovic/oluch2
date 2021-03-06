import os
import sys
import datetime

import zipfile
import rarfile

from django import forms
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.template import RequestContext

import oluch.settings as settings
from oluch.models import Submit, Problem, Contest
from oluch.forms import SubmitForm, UserInfoForm
from django.utils.translation import ugettext_lazy as _

IMAGE_EXTENSIONS = ['png', 'gif', 'jpeg', 'jpg']
rarfile.UNRAR_TOOL = '/usr/bin/unrar'
ARCHIVE_OBJECTS = {'zip': zipfile.ZipFile, 'rar': rarfile.RarFile}

def is_picture(submit_filename):
    pictures = []
    extension = submit_filename.split('.')[-1].lower()
    if extension in IMAGE_EXTENSIONS:
        is_picture = '1'
    elif extension in ARCHIVE_OBJECTS.keys():
        is_picture = '2'
        unzippath = os.path.join(settings.MEDIA_ROOT, submit_filename.split('.')[0])
        zipf = ARCHIVE_OBJECTS[extension](os.path.join(settings.MEDIA_ROOT, submit_filename), 'r')
        if not os.path.exists(unzippath):
            os.mkdir(unzippath)
            num = 10  # filenames will be 10.png, 11.jpg, 12.png etc
            for filename in zipf.namelist():
                submit_file_name = submit_filename.replace('\\', '/') 
                rel_path = submit_file_name[:submit_file_name.rfind('.')]
                file_content = zipf.open(filename, "r").read()
                new_filename = os.path.join(unzippath, str(num) + '.' + filename.split('.')[-1])

                fout = open(new_filename, "wb")
                fout.write(file_content)
                fout.close()

                pictures.append(rel_path + '/' + new_filename.split(os.sep)[-1])
                num += 1
        else:
            pictures = list(map(lambda x: submit_filename.split('.')[0] + '/' + x, os.listdir(unzippath)))
    else:
        is_picture = '0'

    return [is_picture, pictures]

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = 'a@aaa.ru'
            user = User.objects.create_user(username=username, password=password1, 
                                            email=email)
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.save()
            profile = user.userprofile
            profile.grade = form.cleaned_data['grade']
            profile.maxgrade = form.cleaned_data['maxgrade']
            profile.school = form.cleaned_data['school']
            profile.city = form.cleaned_data['city']
            profile.country = form.cleaned_data['country']
            profile.save()

            user = authenticate(username=username, password=password1)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect(reverse('contest_list'))
    else: # If not POST
        form = UserInfoForm()

    return render_to_response('olymp/register.html', {
        'form': form,
        },
                              context_instance=RequestContext(request)
                              )


def contest_list(request):
    jury = is_jury(request.user)
    all_contests = Contest.objects.all()
    return render(request, 'olymp/contest_list.html', 
                  {'contests': all_contests,
                   'jury': jury,
                   })


def user_submited_problems(user, contest):
    return Submit.objects.filter(author=user, problem__contest=contest).values_list('problem__id', 'problem__number', 'problem__title').order_by('problem__sort_order')

def user_not_submited_problems(user, contest):
    all = Problem.objects.filter(contest=contest).values_list('id', 'number', 'title')
    submited = set(user_submited_problems(user, contest))
    return [(item[0], item[1] + '. ' + item[2]) for item in all if item not in submited]

def user(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    if (not contest.accept_submits and 
        not contest.show_results and 
        not is_jury(request.user)):
        return HttpResponseRedirect(reverse('contest_list'))

    choices = user_not_submited_problems(request.user, contest_id)
    submited = user_submited_problems(request.user, contest_id)
    submits = Submit.objects.filter(author=request.user, 
                                    problem__contest__id = contest_id).order_by('problem')
    if request.method == 'POST':
        form = SubmitForm(choices, request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            new_submit = Submit(author=request.user, file=request.FILES['file'], problem=Problem.objects.get(id=int(form.cleaned_data['problem'])), final_mark=-2)
            new_submit.save()
        return HttpResponseRedirect(reverse('user', args = [contest_id]))
    elif choices:
        form = SubmitForm(choices)
        return render(request, 'olymp/user.html', {
            'form': form,
            'submited': submited,
            'contest': contest,
            'submits': submits,
        })
    else:
        return render(request, 'olymp/user.html', {
            'form': None,
            'submited': submited,
            'contest': contest,
            'submits': submits,
        })

def myresults(request, contest_id):
    return render_to_response('olymp/myresults.html', {
        'submits': submits,
        },
                              context_instance=RequestContext(request)
                              )


def is_jury(user):
    return Group.objects.get(name='Jury') in user.groups.all()


@user_passes_test(is_jury)
def jury_list(request):
    jury = User.objects.filter(groups__name__contains='Jury')
    return render_to_response('olymp/jury_list.html',
                              {'jury': jury,
                               },
                              context_instance=RequestContext(request)
                              )

def submit_statistics(contest_id):
    total = Submit.objects.filter(problem__contest__id=contest_id).count()
    zero = Submit.objects.filter(problem__contest__id=contest_id, first_mark=-2).count() 
    first = Submit.objects.filter(problem__contest__id=contest_id, first_mark__gt=-1, second_mark=-2).count() 
    second = Submit.objects.filter(problem__contest__id=contest_id, second_mark__gt=-1).count() 
    final = Submit.objects.filter(problem__contest__id=contest_id, final_mark__gt=-1).count()
    for_third = Submit.objects.filter(problem__contest__id=contest_id, second_mark__gt=-1,final_mark=-2).count()
    return (total, zero, first, second, for_third, final)


@user_passes_test(is_jury)
def jury(request, contest_id):
    # TODO: contest_id
    #if Submit.objects.filter(first_mark=-1, first_judge=request.user).count() > 0:
    #    submit = Submit.objects.filter(first_mark=-1, first_judge=request.user)[0]
    #    return HttpResponseRedirect(settings.SITE + '/check/1st/' + str(submit.problem_id) + '/' + str(submit.id))
    #if Submit.objects.filter(second_mark=-1, second_judge=request.user).count() > 0:
    #    submit = Submit.objects.filter(second_mark=-1, second_judge=request.user)[0]
    #    return HttpResponseRedirect(settings.SITE + '/check/2nd/' + str(submit.problem_id) + '/' + str(submit.id))
    #if Submit.objects.filter(final_mark=-1, third_judge=request.user).count() > 0:
    #    submit = Submit.objects.filter(final_mark=-1, third_judge=request.user)[0]
    #    return HttpResponseRedirect(settings.SITE + '/check/3rd/' + str(submit.problem_id) + '/' + str(submit.id))

    submits_stat = submit_statistics(contest_id)
    problems = Problem.objects.filter(contest__id=contest_id).order_by('id')
    problems_number = [Submit.objects.filter(problem=problem).count() for problem in problems]
    problems_zero = [Submit.objects.filter(problem=problem, first_mark=-2).count() for problem in problems]
    problems_first = [Submit.objects.filter(problem=problem, first_mark__gt=-1).filter(second_mark=-2).count() for problem in problems]
    problems_for_third = [Submit.objects.filter(problem=problem, second_mark__gt=-1).filter(final_mark=-2).count() for problem in problems]
    problems_checking = [Submit.objects.filter(problem=problem, first_mark=-1).count() + Submit.objects.filter(problem=problem, second_mark=-1).count() + Submit.objects.filter(problem=problem, final_mark=-1).count() for problem in problems]
    problems_final = [Submit.objects.filter(problem=problem, final_mark__gt=-1).count() for problem in problems]
    problems_first_me = [Submit.objects.filter(problem=problem, first_mark__gt=-1, second_mark=-2).exclude(first_judge=request.user).count() for problem in problems]
    problems_second_me = [Submit.objects.filter(problem=problem, second_mark__gt=-1, final_mark=-2).exclude(first_judge=request.user).exclude(second_judge=request.user).count() for problem in problems]
    probs = list(zip(problems, problems_number, problems_zero, problems_first, problems_first_me, problems_final, problems_checking, problems_second_me, problems_for_third))
    return render_to_response('olymp/statistics.html', {
        'submits_count': submits_stat[0],
        'zero_count': submits_stat[1],
        'first_count': submits_stat[2],
        'second_count': submits_stat[3],
        'for_third_count': submits_stat[4],
        'final_count': submits_stat[5],
        'submits_zero_percent': 100 * submits_stat[1] // submits_stat[0] if submits_stat[0] else 100,
        'submits_first_percent': 100 * submits_stat[2] // submits_stat[0] if submits_stat[0] else 100,
        'submits_second_percent': 100 * submits_stat[3] // submits_stat[0] if submits_stat[0] else 100,
        'submits_for_third_percent': 100 * submits_stat[4] // submits_stat[0] if submits_stat[0] else 100,
        'final_percent': 100 * submits_stat[5] // submits_stat[0] if submits_stat[0] else 100,
        'probs': probs,
        'contest_id': contest_id,
        },
                              context_instance=RequestContext(request)
                              )


@user_passes_test(is_jury)
def check(request, contest_id, time, problem_id, submit_id=None):
    contest = Contest.objects.get(pk=contest_id)
    if submit_id is None:
        if time == '1':
            submit = Submit.objects.filter(problem__id=problem_id, first_mark=-2).order_by('?')[0] #latest('datetime')
            submit.first_mark=-1
            submit.first_judge=request.user
        elif time == '2':
            submit = Submit.objects.filter(problem__id=problem_id, first_mark__gt=-1, second_mark=-2).exclude(first_judge=request.user).order_by('?')[0] #latest('datetime')	
            submit.second_mark=-1
            submit.second_judge=request.user
        else:
            submit = Submit.objects.filter(problem__id=problem_id, second_mark__gt=-1, final_mark__lt=0).exclude(first_judge=request.user).exclude(second_judge=request.user).order_by('?')[0] #latest('datetime')	
            submit.final_mark=-1
            submit.third_judge=request.user
        submit.save()
        return HttpResponseRedirect('/check/' + str(contest_id) + '/' + time + ('st/' if time == '1' else 'nd/' if time == '2' else 'rd/') + str(problem_id) + '/' + str(submit.id))
    else:
        submit = Submit.objects.get(id=submit_id)
        picture_type, pictures = is_picture(str(submit.file))
        return render(request, 'olymp/check.html', {
            'is_picture': picture_type,
            'submit': submit,
            'author': submit.author,
            'first_mark': submit.first_mark,
            'second_mark': submit.second_mark,
            'time': time,
            'marks': list(zip(settings.marks,range(settings.max_mark + 1))),
            'pictures': pictures,
            'contest_id': contest_id,
            'solutions': contest.solutions_file.url if contest.solutions_file else "",
            'criteria': contest.criteria_file.url if contest.criteria_file else "",
        })


@user_passes_test(is_jury)
def rate(request, contest_id, submit_id, time):
    submit = Submit.objects.get(id=submit_id)
    if time == '1':
        if request.POST["subm"] != _('no mark'):
            submit.first_mark = int(request.POST["subm"])
        else: 
            submit.first_mark = -2
        submit.first_judge = request.user
        submit.first_comment = request.POST["comment"]
    elif time == '2':
        if request.POST["subm"] != _('no mark'):
            submit.second_mark = int(request.POST["subm"])
            if submit.first_mark == submit.second_mark:
                submit.final_mark = submit.second_mark
        else: 
            submit.second_mark = -2
        submit.second_judge = request.user
        submit.second_comment = request.POST["comment"]
    else:
        if request.POST["subm"] != _('no mark'):     
            submit.final_mark = int(request.POST["subm"])
        else:
            submit.final_mark = -2
        submit.third_judge = request.user
        submit.third_comment = request.POST["comment"]
    submit.save()
#    return HttpResponseRedirect(reverse('statistics', args=[submit]))
    return HttpResponseRedirect(reverse('jury', args=[contest_id]))

@user_passes_test(is_jury)
def clear_minus_one(request):
    for submit in Submit.objects.filter(first_mark=-1):
        submit.first_mark = -2
        submit.save()
    for submit in Submit.objects.filter(second_mark=-1):
        submit.second_mark = -2
        submit.save()
    return HttpResponseRedirect(reverse('contest_list'))

@user_passes_test(is_jury)
def solution_stat(request, contest_id):
    problems = Problem.objects.filter(contest__id=contest_id).order_by('id')
    problems_nums = list(range(len(problems)))
    marks = list(range(settings.max_mark + 1))
    stats = [[mark, [Submit.objects.filter(problem=problem, final_mark=mark).count() for problem in problems]] for mark in marks]
    return render_to_response('olymp/solution_stat.html', {
        'problems_nums': problems_nums,
        'problems': problems,
        'marks': settings.marks,
        'stats': stats,
        'contest_id' : contest_id,
        },
                              context_instance=RequestContext(request)
                              )

@user_passes_test(is_jury)
def results(request, contest_id):
    problems_response = Problem.objects.filter(contest__id=contest_id) 
    problems = dict(zip(map(lambda x: x.id, 
                            problems_response), range(1, len(problems_response) + 1)))
    results = dict()
    for user in User.objects.all():
        results[user.id] = [None, None]
        results[user.id][0] = [user.last_name + ' ' + user.first_name, user.userprofile.grade, 
                               user.userprofile.maxgrade, user.userprofile.school, user.userprofile.city, user.userprofile.country, ]
        results[user.id][1] = [-4] * (len(problems_response) + 1)

        submits = Submit.objects.filter(author=user, problem__contest__id=contest_id).order_by('problem')
        for submit in submits:
            if submit.final_mark >= 0:
                results[user.id][1][problems[submit.problem.id]] = {'mark': submit.final_mark, 'id':submit.id}
            elif submit.second_mark >= 0:
                results[user.id][1][problems[submit.problem.id]] = {'mark':-1, 'id':submit.id, 'judges': [submit.first_judge, submit.second_judge]}
            elif submit.first_mark >= 0:
                results[user.id][1][problems[submit.problem.id]] = {'mark':-2, 'id':submit.id, 'judges': [submit.first_judge]}
            else:
                results[user.id][1][problems[submit.problem.id]] = {'mark':-3, 'id':submit.id}

    res = results.values()
    results = sorted([r for r in res], key = lambda x: str.lower(x[0][0][0])) 
    print(results)

    notempty_results = []
    for i in range(len(results)):
        if results[i][1].count(-4) != (len(problems_response) + 1):
            notempty_results.append(results[i])

    return render_to_response('olymp/results.html', {
        'results' : notempty_results,
        'problems': problems_response,
        'contest_id': contest_id,
        },
                              context_instance=RequestContext(request)
                              )


@user_passes_test(is_jury)
def source(request, submit_id):
    submit = Submit.objects.get(pk=submit_id)

    author = User.objects.get(pk=submit.author.id)
    picture_type, pictures = is_picture(str(submit.file))
    return render_to_response('olymp/source.html', {
        'submit': submit,
        'author': author,
        'is_picture': picture_type,
        'pictures': pictures,
        },
                              context_instance=RequestContext(request)
                              )