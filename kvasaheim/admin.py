from django.contrib import admin
from .models import Realm, Category, Generator, Problem
from .models import Path, ProblemInstance, Attempt

# probleminstances are readonly to avoid accidental changes
class ProblemInstanceAdmin(admin.ModelAdmin):
    fields = ('problem', 'answer_string', 'numbers', 'lists', 'categorical')
    readonly_fields = ('problem', 'answer_string', 'numbers', 'lists',
                       'categorical')

# attempts are readonly to avoid accidental changes
class AttemptAdmin(admin.ModelAdmin):
    fields = ('problem', 'user', 'answer', 'date', 'correct')
    readonly_fields = ('problem', 'user', 'answer', 'date', 'correct')


admin.site.register([Realm, Category, Generator, Problem,Path])
admin.site.register(ProblemInstance, ProblemInstanceAdmin)
admin.site.register(Attempt, AttemptAdmin)
