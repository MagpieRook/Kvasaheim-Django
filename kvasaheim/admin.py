from django.contrib import admin
from .models import Category, Problem, TwoListProblem, CategoricalProblem, Path
from .models import ProblemInstance, TwoListInstance, CategoricalInstance
from .models import Attempt, Comment

class AttemptAdmin(admin.ModelAdmin):
    fields = ('problem', 'user', 'answer', 'date', 'correct')
    readonly_fields = ('correct',) # to prevent invalid correct answers

admin.site.register([Category, Path])
admin.site.register([Problem, TwoListProblem, CategoricalProblem])
admin.site.register([ProblemInstance, TwoListInstance, CategoricalInstance])
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Comment)