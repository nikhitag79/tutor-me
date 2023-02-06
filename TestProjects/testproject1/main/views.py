from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ClassList, Item, ClassSelect


# Create your views here.

def account_creation(response):
    return render(response, "")


def home(response):
    return render(response, "main/home.html", {'name': 'Home'})


def student_home(response):
    selection = ClassSelect()
    if response.method == "POST":
        return redirect('/CS3240')
    return render(response, "main/student_home.html", {'name': 'Student', 'selection': selection})


def tutor_home(response):
    return render(response, "main/home.html", {'name': 'Tutor'})


def schedule(response):
    return render(response, "main/home.html", {'name': 'Schedule'})


def account(response):
    return render(response, "main/home.html", {'name': 'Account'})


def classes(response, class_id):
    ls = ClassList.objects.get(class_id=class_id)
    return render(response, "main/roster.html", {"ls": ls})


def other(response):
    return render(response, "main/home.html", {'name': 'Other'})
