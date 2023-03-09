from django.db import models
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User #Going to be used to attach users to Classes
import requests
import json


class View(models.Model):
    def get_json_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        else:
            print('Error:', response.status_code)




# Create your models here.

# I have used a quick database set up for this. We can edit later, it just helps to show
class ClassList(models.Model):
    class_id = models.CharField(max_length=10)
    class_name = models.CharField(max_length=100, default='Some Class')
    available_tutors = models.BooleanField(default=False)

    def __str__(self):
        return self.class_id

# The items are the tutors
class Item(models.Model):
    classlist = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    tutor_first_name = models.CharField(max_length=30, default='first')
    tutor_last_name = models.CharField(max_length=30, default='last')

    def __str__(self):
        return self.tutor_first_name + ' ' + self.tutor_last_name


# Should technically make a forms.py for this, but it behaves like a model, and I thought
# for testing purposes it was fine.
class ClassSelect(forms.Form):
    # available_classes = (('CS3240', 'CS3240'), ('ECE2660', 'ECE2660'))
    # url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
    # response = View.get_json_data(url)
    #
    # context = {'data': response}
    context = ClassList
    print(context.objects.all())
    list = []
    subjects = context.objects.all()
    for i in subjects:
        tuple = (str(i),str(i))
        list.append(tuple)
        print(type(i))
        print(i)

    class_select = forms.ChoiceField(choices=list, widget=forms.widgets.SelectMultiple(attrs={'size': 100}))



