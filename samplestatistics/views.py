from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .forms import AnswerForm, CommentForm
from .models import Category, Problem, ProblemInstance, Attempt, Comment

def home(request, pk=None):
    if pk:
        categories = Category.objects.filter(pk=pk, published=True)
    else:
        categories = Category.objects.filter(published=True)
    problems = Problem.objects.filter(published=True)
    return render(request, 'samplestatistics/home.html',
        {'categories': categories, 'pk': pk, 'problems': problems})

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
        return HttpResponseRedirect(reverse('samplestatistics:problem_answer',
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
        list_sum = sum(instance.numbers_list)
        if problem.published:
            return render(request, 'samplestatistics/problem_detail.html',
                {'problem': problem, 'instance': instance,
                'form': form, 'list_sum': list_sum})
        else:
            raise PermissionDenied('Please log in.')

def problem_answer(request, pk, apk):
    if request.user.is_authenticated:
        problem = get_object_or_404(Problem, pk=pk)
        answer = get_object_or_404(Attempt, pk=apk)
        return render(request, 'samplestatistics/problem_answer.html',
            {'problem': problem, 'answer': answer,})
    else:
        raise PermissionDenied('Please log in.')

def user_profile(request, user):
    u = get_object_or_404(User, username=user)
    answers = Attempt.objects.filter(user=u).order_by('problem', 'date')
    categories = set()
    problems = set()
    for answer in answers:
        categories.add(Category.objects.get(problem=answer.problem.problem))
        problems.add(Problem.objects.get(instance=answer.problem))
    return render(request, 'samplestatistics/user_profile.html',
    {'u': u, 'categories': categories, 'problems': problems, 'answers': answers})