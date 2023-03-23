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

# Create your views here.
search_mnemonic = ""

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
        logout(response)
        return redirect("/")
    return render(response, "main/account.html", {'name': 'Account'})


def classes(response, class_id, first_professors, last_professors):
    print("here",class_id)
    print("type", type(class_id))
    professors = first_professors + " "+ last_professors
    my_instance = ClassDatabase.objects.filter(class_id= class_id, professors = professors)
    print("my instance", len(my_instance))
    header = class_id + " " + professors
    if response.method == "GET":
        user = response.user
        print("inside get")
        print(class_id)
        print(first_professors)
        print(last_professors)
        group = Group.objects.get(name=class_id + professors)
        group.user_set.add(user)
        group.save()
        is_member = group.user_set.filter(username=user).exists()
        print("here" , is_member)


    return render(response, "main/roster.html", {'header': header})


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
    

def searchbar_tutee(response):
    if response.method == 'GET':
        search = response.GET.get('mnemonic')
        if not search is None:
            search_mnemonic = str(search).upper()
            print("here")
            existing_list = []
            existing_classes = ClassDatabase.objects.all()
            for i in existing_classes:
                existing_list.append(str(i))
            pages = 100
            for page_number in range(1, pages):
                print("pages numbers", page_number)
                url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=" + search_mnemonic + "&page=" + str(page_number)
                # To remove the other classes that we did not search just perform a if search in database is not 'a' we remove it.
                url_data = View.get_json_data(url)
                context = {'data': url_data}
                if (context["data"] == []):
                    print("breaking")
                    break;
                for j in range(len(context["data"])):
                    class_info = context['data'][j]['catalog_nbr']
                    instructor = context['data'][j]["instructors"][0]["name"]
                    name = context['data'][j]['descr']
                    all = search_mnemonic + class_info + " " + name + " " + instructor
                    if not all in existing_list:
                        existing_list.append(all)
                        class_instance = ClassDatabase.objects.create(class_id=search_mnemonic + class_info,
                                                                      class_name=name,
                                                                      professors=instructor, class_mnen=str(search))

            selection = ClassDatabase.objects.filter(class_mnen= search_mnemonic)
            if not selection:
                messages.error(response,"Not an exisiting mnemonic")
                return redirect('/student_home/',{'name':'Home'})
                #return render(response, "main/mnemonic_page.html", {"error_message": "Not an exisiting mnemonic"})
            filters = FilterCourses(response.GET,queryset= selection)
            context = {"filters": filters,'name':search_mnemonic}
        else:
            print("else")
            selection = ClassDatabase.objects.all()
            filters = FilterCourses(response.GET, queryset=selection)
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


    return render(response, "main/class_finder.html", context)


def searchbar_tutor(response):
    if response.method == 'GET':
        search = response.GET.get('mnemonic')
        user = response.user
        print("user", user)
        if not search is None:
            search_mnemonic = str(search).upper()
            print("here")
            existing_list = []
            existing_classes = ClassDatabase.objects.all()
            for i in existing_classes:
                existing_list.append(str(i))
            pages = 100
            for page_number in range(1, pages):
                print("pages numbers", page_number)
                url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=" + search_mnemonic + "&page=" + str(page_number)
                # To remove the other classes that we did not search just perform a if search in database is not 'a' we remove it.
                url_data = View.get_json_data(url)
                context = {'data': url_data}
                if (context["data"] == []):
                    print("breaking")
                    break;
                for j in range(len(context["data"])):
                    class_info = context['data'][j]['catalog_nbr']
                    instructor = context['data'][j]["instructors"][0]["name"]
                    name = context['data'][j]['descr']
                    all = search_mnemonic + class_info + " " + name + " " + instructor
                    if not all in existing_list:
                        existing_list.append(all)
                        group = Group.objects.create(name=search_mnemonic + class_info + instructor)
                        group.save()
                        class_instance = ClassDatabase.objects.create(class_id=search_mnemonic + class_info,
                                                                      class_name=name,
                                                                      professors=instructor, class_mnen=search_mnemonic, tutors=group)

            selection = ClassDatabase.objects.filter(class_mnen=search_mnemonic)
            if not selection:
                messages.error(response, "Not an exisiting mnemonic")
                return redirect('/student_home/', {'name': 'Home'})
                # return render(response, "main/mnemonic_page.html", {"error_message": "Not an exisiting mnemonic"})
            filters = FilterCourses(response.GET, queryset=selection)
            context = {"filters": filters, 'name': search_mnemonic, 'user': user}
        else:
            print("else")
            selection = ClassDatabase.objects.all()
            filters = FilterCourses(response.GET, queryset=selection)
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

            context = {"filters": filters, 'name': class_name}

    return render(response, "main/searchbar_tutor.html", context)