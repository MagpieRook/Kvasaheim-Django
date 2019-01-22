import string

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .forms import AnswerForm
from .models import Realm, Category, Problem, ProblemInstance, Attempt

def home(request, title=None, cpk=None):
    if title:
        realms = Realm.objects.filter(title=title, published=True)
    else:
        realms = Realm.objects.filter(published=True)
    if cpk:
        categories = Category.objects.filter(pk=cpk, published=True)
    else:
        categories = Category.objects.filter(published=True)
    problems = Problem.objects.filter(published=True)
    return render(request, 'kvasaheim/home.html',
        {'realms': realms, 'title': title, 'categories': categories, 'cpk': cpk,
        'problems': problems})

def problem_detail(request, pk, ipk=None):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            nattempt = Attempt()
            nattempt.user = request.user
            nattempt.answer = form.cleaned_data['answer']
            nattempt.problem = get_object_or_404(ProblemInstance,
                pk=form.cleaned_data['problem_instance'])
            nattempt.save()
        return HttpResponseRedirect(reverse('kvasaheim:problem_answer',
         args=(pk, nattempt.id)))
    else:
        problem = get_object_or_404(Problem, pk=pk)
        form = AnswerForm()
        if ipk:
            instance = get_object_or_404(ProblemInstance, pk=ipk)
            if instance.problem != problem:
                raise Http404('No instance with that ID for this problem.')
        else:
            instance = ProblemInstance.objects.create_problem_instance(problem)
        list_sum = None
        if instance.lists > 1:
            for nlist in instance.numbers_list:
                if isinstance(nlist[0], int):
                    if list_sum:
                        list_sum = [list_sum] + sum(nlist)
                    else:
                        list_sum = sum(nlist)
        else:
            if isinstance(instance.numbers_list[0], int):
                list_sum = sum(instance.numbers_list)
        if problem.published:
            return render(request, 'kvasaheim/problem_detail.html',
                {'problem': problem, 'instance': instance,
                'form': form, 'list_sum': list_sum})
        else:
            raise PermissionDenied('Please log in.')

def problem_answer(request, pk, apk):
    if request.user.is_authenticated:
        problem = get_object_or_404(Problem, pk=pk)
        answer = get_object_or_404(Attempt, pk=apk)
        return render(request, 'kvasaheim/problem_answer.html',
            {'problem': problem, 'answer': answer,})
    else:
        raise PermissionDenied('Please log in.')

def user_profile(request, user):
    u = get_object_or_404(User, username=user)
    answers = Attempt.objects.filter(user=u).order_by('problem', 'date')
    categories = set()
    problems = set()
    for answer in answers:
        categories.add(Category.objects.get(problems=answer.problem.problem))
        problems.add(Problem.objects.get(instance=answer.problem))
    return render(request, 'kvasaheim/user_profile.html',
    {'u': u, 'categories': categories, 'problems': problems, 'answers': answers})