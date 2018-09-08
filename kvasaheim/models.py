import ast
from random import randint
import string

from django.utils import timezone
from django.db import models

import numpy

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Realm(models.Model):
    title     = models.CharField(max_length=200, unique=True)
    text      = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Category(models.Model):
    title       = models.CharField(max_length=200, unique=True)
    published   = models.BooleanField(default=False)
    realm       = models.ForeignKey(Realm, on_delete=models.CASCADE,
                    related_name='category', related_query_name='categories')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"

class Generator(models.Model):
    title          = models.CharField(max_length=200, blank=True)
    categorical    = models.BooleanField(default=False)
    random_low     = models.IntegerField(default=10)
    random_high    = models.IntegerField(default=100)
    num_rands_low  = models.PositiveIntegerField(default=5)
    num_rands_high = models.PositiveIntegerField(default=10)

    def __str__(self):
        if self.title:
            return self.title
        title = "Categorical Generator " if self.categorical else "Generator "
        title += str(self.pk)
        return title

class Problem(models.Model):
    title      = models.CharField(max_length=200, unique=True)
    text       = models.TextField()
    category   = models.ForeignKey(Category, on_delete=models.CASCADE,
                    related_name='problem', related_query_name='problems')
    published  = models.BooleanField(default=False)
    equation   = models.TextField(default="def solve(x):\n    return x")
    generators = models.ManyToManyField(Generator, symmetrical=False,
                    related_name='generator', related_query_name='generators')
    paths      = models.ManyToManyField('self', symmetrical=False,
                    related_name='path', related_query_name='path',
                    through='Path')
    formula    = models.TextField(default='<div style="margin:0 0 2em 2em;">')
    solution   = models.TextField()
    rcode      = models.TextField(default='<div class="r code">\n</div>')
    excel      = models.TextField(default='<div class="excel code">\n</div>')

    def __str__(self):
        return self.title

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

def generate_normal_list(num_rands_low, num_rands_high, random_low, random_high):
    num_rands = randint(num_rands_low, num_rands_high)
    loc = randint(random_low, random_high)
    scale = (loc - random_low) / 4
    numbers = list(numpy.random.normal(loc=loc,
        scale=scale, size=num_rands))
    return [int(n) for n in numbers]

class ProblemManager(models.Manager):
    def create_problem_instance(self, problem):
        numbers = None if len(problem.generators.all()) == 1 else '['
        count = 0
        categorical = False
        for generator in problem.generators.all():
            normal_list = generate_normal_list(generator.num_rands_low,
                            generator.num_rands_high, generator.random_low,
                            generator.random_high)
            if generator.categorical:
                categorical = True
                if numbers:
                    numbers += '['
                else:
                    numbers = '['
                for n in normal_list:
                    numbers += '"' + string.ascii_uppercase[n % 26] + '", '
                numbers = numbers[:-2]
                numbers += ']'
            else:
                if numbers:
                    numbers += str(normal_list)
                else:
                    numbers = str(normal_list)
            count += 1
            if count < len(problem.generators.all()):
                numbers += ', '
        if len(problem.generators.all()) > 1:
            numbers += ']'
        problem_instance = self.create(problem=problem, numbers=numbers,
                            lists=count, categorical=categorical,
                            answer_string=problem.equation)
        problem_instance.save()
        return problem_instance

class ProblemInstance(models.Model):
    problem       = models.ForeignKey(Problem, on_delete=models.CASCADE,
                    related_name='instances', related_query_name='instance')
    answer_string = models.TextField()
    numbers       = models.CharField(max_length=1000)
    lists         = models.PositiveIntegerField()
    categorical   = models.BooleanField()
    objects       = ProblemManager()

    @property
    def numbers_list(self):
        nlist = ast.literal_eval(self.numbers)
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
        if abs(self.problem.answer - float(self.answer)) < 0.001:
            return True
        return False

    def __str__(self):
        return "%s %s %s" % (self.user.username, self.problem,
            "Correct" if self.correct else "Incorrect")