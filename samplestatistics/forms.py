from django import forms

class AnswerForm(forms.Form):
    answer = forms.DecimalField(label='Answer', decimal_places=4)
    problem_instance = forms.IntegerField(label='Problem Instance')

class CommentForm(forms.Form):
    text = forms.CharField(label='Comment', max_length=255, widget=forms.Textarea)
    answer = forms.IntegerField(label='Answer')