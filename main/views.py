from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ClassList, Item, ClassSelect, UserProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


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
    if response.method == "POST":
        logout(response)
        return redirect("/")
    return render(response, "main/account.html", {'name': 'Account'})

def classes(response, class_id):
    ls = ClassList.objects.get(class_id=class_id)
    return render(response, "main/roster.html", {"ls": ls})


def other(response):
    return render(response, "main/home.html", {'name': 'Other'})


@login_required
def select_user(response):
    if response.method == "POST":
        print("hello", response.POST.get('user_type'))
        user_type = response.POST.get('user_type')
        response.user.user_type = user_type
        response.user.has_selected_type = True
        response.user.save()

        if user_type == "tutor":
            return redirect('/home/')
        elif user_type =="student":
            return redirect('/student_home/')
    else:
        return render(response, 'main/select_user.html')
