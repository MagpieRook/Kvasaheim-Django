from django.contrib import admin
from .models import Problem, ProblemInstance, Attempt, Comment, Category

#Attempt: readonly_fields(correct)
class AttemptAdmin(admin.ModelAdmin):
    fields = ('problem', 'user', 'answer', 'date', 'correct')
    readonly_fields = ('correct',)

admin.site.register(Problem)
admin.site.register(Category)
admin.site.register(ProblemInstance)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Comment)