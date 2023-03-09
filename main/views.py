from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ClassList, Item, ClassSelect, View
#   , UserProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# Create your views here.

def my_view(request):
    subject = ClassSelect()

    return render(request, 'main/student_home.html', {'context': subject})

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
    return render(response, "main/home.html", {'name': 'Home'})


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
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
    url_data = View.get_json_data(url)

    context = {'data': url_data}
    subjects = context["data"]["subjects"]
    for i in subjects:
        class_instance = ClassList.objects.create(class_id = i["subject"], class_name="")

    if response.method == "POST":
        user_type = response.POST.get('user_type')
        if (user_type == "Tutor"):
            response.user.user_type = 1
        if (user_type == "Student"):
            response.user.user_type = 2

        response.user.has_selected_role = True
        response.user.save()

        if user_type == "Tutor":
            return redirect('/home/')
        elif user_type == "Student":
            return redirect('/student_home/')

    else:
        return render(response, 'main/select_user.html')
