from django.db import models
from django.forms import widgets
from oauth_app.models import User
from django.contrib.auth.models import Group
import requests
import json
from oauth_app.models import User

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
    class_id = models.CharField(max_length=10, default = 'cl id')
    class_name = models.CharField(max_length=100, default='cl name')
    # professors = models.CharField(max_length=100, default = 'cl pr')
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




class ClassDatabase(models.Model):
    class_id = models.CharField(max_length=10, default = 'no class id')
    class_mnen = models.CharField(max_length=100, default = 'no class mnemonic')
    class_name = models.CharField(max_length=100, default='no class name')
    professors = models.CharField(max_length=100, default = 'no professor')
    available_tutors = models.BooleanField(default=False)
    tutors = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.class_id + ' ' + self.class_name + ' ' +  self.professors


