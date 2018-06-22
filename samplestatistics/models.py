from django.db import models
from django.utils import timezone
from random import randint

import types

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Problem(models.Model):
    title           = models.CharField(max_length=200, unique=True)
    text            = models.TextField()
    published       = models.BooleanField(default=False)
    equation        = models.TextField()
    random_low      = models.IntegerField()
    random_high     = models.IntegerField()
    num_rands_low   = models.IntegerField()
    num_rands_high  = models.IntegerField()

    # category, realm, etc.

    def __str__(self):
        return self.title

class ProblemManager(models.Manager):
    def create_problem_instance(self, problem):
        numbers = ""
        num_rands = randint(problem.num_rands_low, problem.num_rands_high)
        for i in range(num_rands):
            numbers += str(
                randint(problem.random_low, problem.random_high)
            ) + ", "
        numbers = numbers[0:len(numbers)-2]
        problem_instance = self.create(problem=problem,
            numbers=numbers, answer_string=problem.equation)
        problem_instance.save()
        return problem_instance

class ProblemInstance(models.Model):
    problem       = models.ForeignKey(Problem, related_name='instance', on_delete=models.CASCADE)
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
        helpme = "" + self.answer_string
        exec(helpme, globals())
        if (self.numbers != ''):
            return solve(self.numbers_list)
        else:
            return 0

    # def __str__(self):
    #     return str(self.problem) + " " + str(self.answer)

class Attempt(models.Model):
    problem = models.ForeignKey(ProblemInstance, related_name='attempts', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user', related_name='attempts', on_delete=models.SET(get_sentinel_user))
    answer = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

    @property
    def correct(self):
        if str(self.answer) == str(self.problem.answer):
            return True
        return False

    def __str__(self):
        return self.user.username + ' ' + str(self.problem) + ' ' + str(self.correct)

class Comment(models.Model):
    user = models.ForeignKey('auth.user', related_name='comments', on_delete=models.SET(get_sentinel_user))
    attempt = models.ForeignKey(Attempt, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.date) + " - " + str(self.user) + ": " + str(self.text)
