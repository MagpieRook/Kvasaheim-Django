from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .forms import AnswerForm, CommentForm
from .models import Problem, ProblemInstance, Attempt, Comment

def home(request):
    problems = Problem.objects.filter(published=True)
    return render(request, 'samplestatistics/home.html', {'problems': problems})

def problem_detail(request, pk):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            nattempt = Attempt()
            nattempt.user = request.user
            nattempt.answer = form.cleaned_data['answer']
            print(form['problem_instance'].value()) # debug statement
            nattempt.problem = get_object_or_404(ProblemInstance, pk=form.cleaned_data['problem_instance'])
            nattempt.save()
        else: # debug statement
            print(form.errors)
        return HttpResponseRedirect(reverse('samplestatistics:problem_answer', args=(pk,)))
    else:
        problem = get_object_or_404(Problem, pk=pk)
        form = AnswerForm()
        probleminstance = ProblemInstance.objects.create_problem_instance(problem)
        if problem.published:
            return render(request, 'samplestatistics/problem_detail.html', {'problem': problem, 'probleminstance': probleminstance, 'form': form})
        else:
            raise PermissionDenied

def problem_answer(request, pk):
    answers = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            ncomment = Comment()
            ncomment.user = request.user
            ncomment.text = form.cleaned_data['text']
            ncomment.attempt = get_object_or_404(Attempt, pk=form.cleaned_data['answer'])
            ncomment.save()
        return HttpResponseRedirect(reverse('samplestatistics:problem_answer', args=(pk,)))
    else:
        if request.user.is_authenticated:
            form = CommentForm()
            answers = Attempt.objects.filter(user=request.user)
            problem = get_object_or_404(Problem, pk=pk)
            return render(request, 'samplestatistics/problem_answer.html', {'problem': problem, 'answers': answers, 'form': form})
        else:
            raise PermissionDenied