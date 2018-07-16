from django.db import models
from django.utils import timezone
from random import randint

import numpy

import types

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Category(models.Model):
    title       = models.CharField(max_length=200, unique=True)
    published   = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"

class Problem(models.Model):
    title           = models.CharField(max_length=200, unique=True)
    text            = models.TextField()
    category        = models.ForeignKey(Category, on_delete=models.CASCADE,
                        related_name='problems', related_query_name='problem')
    published       = models.BooleanField(default=False)
    equation        = models.TextField(default="def solve(x):\n    return x")
    random_low      = models.IntegerField()
    random_high     = models.IntegerField()
    num_rands_low   = models.IntegerField()
    num_rands_high  = models.IntegerField()
    spread          = models.FloatField()
    paths           = models.ManyToManyField('self', symmetrical=False,
                        related_name='path', related_query_name='path',
                        through='Path')
    formula         = models.TextField()
    solution        = models.TextField()
    rcode           = models.TextField(default='<div class="r code">\n</div>')
    excel           = models.TextField(default='<div class="excel code">\n</div>')

    def __str__(self):
        return self.title

class TwoListProblem(Problem):
    second_random_low      = models.IntegerField()
    second_random_high     = models.IntegerField()
    second_num_rands_low   = models.IntegerField()
    second_num_rands_high  = models.IntegerField()
    second_spread          = models.IntegerField()

class CategoricalProblem(Problem):
    categorical_num_rands_low   = models.IntegerField()
    categorical_num_rands_high  = models.IntegerField()
    # TODO: way to determine categorical data source/randomness

PATH_DEPENDS = 1
PATH_RECOMMENDS = 2
PATH_CHOICES = (
    (PATH_DEPENDS, 'Depends'),
    (PATH_RECOMMENDS, 'Recommends'),
)

class Path(models.Model):
    from_problem    = models.ForeignKey(Problem, on_delete=models.CASCADE,
                        related_name='from_problems',
                        related_query_name='from_problem')
    to_problem      = models.ForeignKey(Problem, on_delete=models.CASCADE,
                        related_name='to_problems',
                        related_query_name='to_problem')
    direction       = models.IntegerField(choices=PATH_CHOICES)

class ProblemManager(models.Manager):
    def create_problem_instance(self, problem):
        numbers = ""
        num_rands = randint(problem.num_rands_low, problem.num_rands_high)
        loc = (problem.random_low + problem.random_high) / 2
        numbers = numpy.random.normal(loc=loc,
            scale=problem.spread, size=num_rands)
        problem_instance = self.create(problem=problem,
            numbers=numbers, answer_string=problem.equation)
        problem_instance.save()
        return problem_instance

    def create_two_list_instance(self, problem):
        numbers = []
        numbers.append('')
        num_rands = randint(problem.num_rands_low, problem.num_rands_high)
        loc = (problem.random_low + problem.random_high) / 2
        numbers[0] = numpy.random.normal(loc=loc,
            scale=problem.spread, size=num_rands)
        numbers.append('')
        num_rands = randint(problem.second_num_rands_low,
            problem.second_num_rands_high)
        loc = (problem.second_random_low + problem.seond_random_high) / 2
        numbers[1] = numpy.random.normal(loc=loc,
            scale=problem.second_spread, size=num_rands)
        problem_instance = self.create(problem=problem, numbers=numbers[0],
            answer_string=problem.equation, second_numbers=numbers[1])

    def create_categorical_instance(self, problem):
        numbers = ""
        num_rands = randint(problem.num_rands_low, problem.num_rands_high)
        loc = (problem.random_low + problem.random_high) / 2
        numbers = numpy.random.normal(loc=loc,
            scale=problem.spread, size=num_rands)
        categorical = '' # TODO: way to generate categorical data?
        categorical_instance = self.create(problem=problem, numbers=numbers,
            categorical_list=categorical, answer_string=problem.equation)

class ProblemInstance(models.Model):
    problem       = models.ForeignKey(Problem, on_delete=models.CASCADE,
                    related_name='instances', related_query_name='instance')
    answer_string = models.TextField()
    numbers       = models.CharField(max_length=200)
    objects       = ProblemManager()

    @property
    def numbers_list(self):
        nlist = self.numbers.strip().split(',')
        nlist = [int(n) for n in nlist]
        return nlist

    @property
    def answer(self):
        answer = "" + self.answer_string
        exec(answer, globals())
        if (self.numbers != ''):
            return solve(self.numbers_list)
        else:
            return 0

    def __str__(self):
        return str(self.problem) + " " + str(self.id)

class TwoListInstance(ProblemInstance):
    second_numbers  = models.CharField(max_length=200)
    
    @property
    def second_numbers_list(self):
        nlist = self.numbers.strip().split(',')
        nlist = [int(n) for n in nlist]
        return nlist

    @property
    def answer(self):
        answer = "" + self.answer_string
        exec(answer, globals())
        if (self.numbers != '' and self.second_numbers != ''):
            return solve(self.numbers_list + self.second_numbers_list)
        else:
            return 0

    def __str__(self):
        return str(self.problem) + " " + str(self.id)
    
class CategoricalInstance(ProblemInstance):
    categorical_list = models.TextField()

    @property
    def answer(self):
        answer = "" + self.answer_string
        exec(answer, globals())
        if (self.numbers_list != '' and self.categorical_list != ''):
            return solve(self.categorical_list + self.second_numbers_list)
        else:
            return 0

class Attempt(models.Model):
    problem = models.ForeignKey(ProblemInstance, on_delete=models.CASCADE,
                related_name='attempts', related_query_name='attempt')
    user    = models.ForeignKey('auth.user',
                related_name='attempts',  related_query_name='attempt',
                on_delete=models.SET(get_sentinel_user))
    answer  = models.CharField(max_length=200)
    date    = models.DateTimeField(default=timezone.now)

    @property
    def correct(self):
        if abs(self.problem.answer - self.answer) < 0.001:
            return True
        return False

    def __str__(self):
        return "%s %s %s" % (self.user.username, self.problem, self.correct)

class Comment(models.Model):
    user    = models.ForeignKey('auth.user',
                related_name='comments', related_query_name='comment',
                on_delete=models.SET(get_sentinel_user))
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE,
                related_name='comments', related_query_name='comment')
    text    = models.TextField()
    date    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s %s: %s" % (str(self.date), str(self.user), str(self.text))
