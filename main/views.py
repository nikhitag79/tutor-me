from django.shortcuts import render, redirect
from .models import ClassList, Item, View, ClassDatabase
# from .forms import ClassSelect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .filters import FilterCourses
from oauth_app.models import User
from django.contrib.auth.models import Group
import json
import sys


# Create your views here.

def home(response):
    return render(response, "main/home.html", {'name': 'Home'})


def student_home(response):
    if response.method == "POST":
        return redirect('/CS3240')
    return render(response, "main/student_home.html")


def tutor_home(response):
    return render(response, "main/home.html", {'name': 'Home'})


def schedule(response):
    return render(response, "main/home.html", {'name': 'Schedule'})


def account(response):
    # user_id = response.GET.get("username")
    # print(user_id)
    if response.method == "POST":
        if response.POST.get('logout'):
            logout(response)
            return redirect("/")
        elif response.POST.get('set_hourly'):
            hourly_rate = response.POST.get('hourly_rate')
            response.user.tutor_rate = hourly_rate
            response.user.save()
    return render(response, "main/account.html", {'name': 'Account'})


def classes(response, class_id, first_professors, middle ="", last_professors=""):
    user = response.user
    print(user.user_type)
    if (middle == ""):
        print("single")
        professors = first_professors + " " + last_professors
    else:
        print("double")
        professors = first_professors + " " + middle + " " + last_professors
    print("profesors", professors)
    my_instance = ClassDatabase.objects.filter(class_id= class_id, professors = professors)
    header = class_id + " " + professors
    dict = {}
    group_name = Group.objects.get(name= header)
    users = group_name.user_set.all()
    print("users", type(users), users)


    if response.method == "POST":
        user = response.user
        group = Group.objects.get(name=class_id +" "+ professors)
        if not group.user_set.filter(username=user).exists():
            group.user_set.add(user)
            group.save()
            my_instance = ClassDatabase.objects.filter(class_id=class_id, professors=professors).first()
            my_instance.available_tutors = True
            my_instance.save()
            letters_only = ''.join(filter(str.isalpha, class_id))
            return redirect("/tutor_home/searchbar/?mnemonic=" + letters_only)
        else:
            if response.POST.get('remove'):
                group.user_set.remove(user)
            letters_only = ''.join(filter(str.isalpha, class_id))
            return redirect("/tutor_home/searchbar/?mnemonic=" + letters_only)

    return render(response, "main/roster.html", {'header': header, 'user': user, 'group': group_name})


def mnemonic(response):
    return render(response, "main/mnemonic_page.html",{'name':'Home'})



def other(response):
    return render(response, "main/home.html", {'name': 'Other'})


@login_required
def select_user(response):
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
    

def searchbar_tutee(request):
    sys.path.append('../')
    if request.method == 'GET':
        search = request.GET.get('mnemonic')
        if not search is None:
            search_mnemonic = str(search).upper()
            print("search mnemon", search_mnemonic)
            existing_list = []
            existing_classes = ClassDatabase.objects.filter(class_mnen=search_mnemonic)
            for i in existing_classes:
                existing_list.append(str(i))
            if not existing_list:
                with open("class_database.json") as database_json:
                    database_file = json.load(database_json)
                    if search_mnemonic in database_file:
                        for item in database_file[search_mnemonic]:
                            class_info = item[0]['class_info']
                            instructor = item[1]['instructors'][0]['name']
                            name = item[2]['descr']
                            database_object = search_mnemonic + class_info + " " + name + " " + instructor
                            if not database_object in existing_list:
                                existing_list.append(database_object)
                                group = Group.objects.create(name=search_mnemonic + class_info + " " + instructor)
                                group.save()
                                class_instance = ClassDatabase.objects.create(class_id=search_mnemonic + class_info,
                                                                              class_name=name,
                                                                              professors=instructor,
                                                                              class_mnen=search_mnemonic, tutors=group)
                    else:
                        messages.error(request, "Not an exisiting mnemonic")
                        return redirect('/student_home/', {'name': 'Home'})
            filters = FilterCourses(request.GET,queryset= existing_classes)
            context = {"filters": filters,'name':search_mnemonic}
        else:
            selection = ClassDatabase.objects.all()
            filters = FilterCourses(request.GET, queryset=selection)
            class_name = ""
            for index, item in enumerate(filters.qs):
                if index == 0 and len(filters.qs) == 1:
                    class_name = item.class_name + " with " + item.professors
                elif index == 0:
                    class_name = item.class_name
                elif class_name == item.class_name:
                    continue
                else:
                    class_name = item.professors
                    break

            context = {"filters": filters,'name': class_name}


    return render(request, "main/class_finder.html", context)


def searchbar_tutor(request):
    sys.path.append('../')
    user = request.user
    results = Group.objects.filter(user=user)
    tutor_group={}
    for each in results:
        tutor_group[str(each)]= str(each)
    context = {"results": tutor_group}

    if request.method == 'GET':
        search = request.GET.get('mnemonic')
        if not search is None:
            search_mnemonic = str(search).upper()
            existing_list = []
            existing_classes = ClassDatabase.objects.filter(class_mnen=search_mnemonic)
            for i in existing_classes:
                existing_list.append(str(i))
            if not existing_list:
                with open("class_database.json") as database_json:
                    database_file = json.load(database_json)
                    if search_mnemonic in database_file:
                        for item in database_file[search_mnemonic]:
                            class_info = item[0]['class_info']
                            instructor = item[1]['instructors'][0]['name']
                            name = item[2]['descr']
                            database_object = search_mnemonic + class_info + " " + name + " " + instructor
                            if not database_object in existing_list:
                                existing_list.append(database_object)
                                group = Group.objects.create(name=search_mnemonic + class_info + " " + instructor)
                                group.save()
                                class_instance = ClassDatabase.objects.create(class_id=search_mnemonic + class_info,
                                                                              class_name=name,
                                                                              professors=instructor,
                                                                              class_mnen=search_mnemonic, tutors=group)
                    else:
                        messages.error(request, "Not an exisiting mnemonic")
                        return redirect('/tutor_home/', {'name': 'Home', "results": tutor_group})
            filters = FilterCourses(request.GET, queryset=existing_classes)

            context = {"filters": filters, 'name': search_mnemonic, 'user': user, 'results': tutor_group}
        else:
            selection = ClassDatabase.objects.all()
            filters = FilterCourses(request.GET, queryset=selection)
            class_name = ""
            for index, item in enumerate(filters.qs):
                if index == 0 and len(filters.qs) == 1:
                    class_name = item.class_name + " with " + item.professors
                elif index == 0:
                    class_name = item.class_name
                elif class_name == item.class_name:
                    continue
                else:
                    class_name = item.professors
                    break
            context = {"filters": filters, 'name': class_name, "results": tutor_group}
    return render(request, "main/searchbar_tutor.html", context)

def database_setup(request):
    sys.path.append('../')
    user = request.user
    if request.method == "GET":
        if request.GET.get("create_database_json"):
            major_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
            major_url_data = View.get_json_data(major_url)
            major_data = {'data': major_url_data}
            json_dict = {}
            for j in range(len(major_data["data"]['subjects'])):
                print('major_data', major_data['data']['subjects'][j]['subject'])
                search_mnemonic_json = major_data['data']['subjects'][j]['subject']
                class_list = []
                pages = 100
                for page_number in range(1, pages):
                    print("pages numbers", page_number)
                    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=" + search_mnemonic_json + "&page=" + str(
                        page_number)
                    url_data = View.get_json_data(url)
                    data = {'data': url_data}
                    if (data["data"] == []):
                        print("breaking")
                        break
                    for j in range(len(data["data"])):
                        class_info = data['data'][j]['catalog_nbr']
                        class_info_dict = {'class_info': class_info}
                        instructor = data['data'][j]["instructors"][0]["name"]
                        instructor_dict = {'instructors': [{'name': instructor}]}
                        name = data['data'][j]['descr']
                        name_dict = {'descr': name}
                        class_list.append([class_info_dict, instructor_dict, name_dict])
                json_dict[search_mnemonic_json] = class_list
            json_object = json.dumps(json_dict, indent=4)
            with open('class_database.json', 'w') as file:
                file.write(json_object)
            return redirect("/database/" , {'name': 'Database Setup', 'user': user})
        if request.GET.get("create_database"):
            with open("class_database.json") as database_json:
                database_file = json.load(database_json)
                existing_list = []
                existing_classes = ClassDatabase.objects.all()
                for i in existing_classes:
                    existing_list.append(str(i))
                for acronym in database_file:
                    print('acronym', acronym)
                    for item in database_file[acronym]:
                        class_info = item[0]['class_info']
                        instructor = item[1]['instructors'][0]['name']
                        name = item[2]['descr']
                        database_object = acronym + class_info + " " + name + " " + instructor
                        print('database object', database_object)
                        if not database_object in existing_list:
                            existing_list.append(database_object)
                            group = Group.objects.create(name= acronym + class_info + " " + instructor)
                            group.save()
                            class_instance = ClassDatabase.objects.create(class_id=acronym + class_info,
                                                                          class_name=name,
                                                                          professors=instructor,
                                                                          class_mnen=acronym, tutors=group)
                            class_instance.save()
    return render(request, "main/database.html", {'name': 'Database Setup', 'user': user})
