from django import forms
from .models import ClassList

# Should technically make a forms.py for this, but it behaves like a model, and I thought
# for testing purposes it was fine.
class ClassSelect(forms.Form):
    context = ClassList
    list = []
    subjects = context.objects.all()
    for i in subjects:
        tuple = (str(i),str(i))
        list.append(tuple)
    class_select = forms.ChoiceField(choices=list, widget=forms.widgets.SelectMultiple(attrs={'size': 100}))