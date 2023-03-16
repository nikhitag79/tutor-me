from django.shortcuts import render, redirect
from .models import ClassList, Item, View, ClassDatabase
from .forms import ClassSelect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .filters import FilterCourses

# Create your views here.

def my_view(request):
    subject = ClassSelect()

    return render(request, 'main/student_home.html', {'context': subject})

def account_creation(response):
    return render(response, "")


def home(response):
    return render(response, "main/home.html", {'name': 'Home'})


def student_home(response):
    #till 37 keep for testing
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
    url_data = View.get_json_data(url)

    context = {'data': url_data}
    subjects = context["data"]["subjects"]
    existing_list = []
    existing_classes = ClassDatabase.objects.all()
    for i in existing_classes:
        existing_list.append(str(i))
    # for i in subjects:
    #     if not i["subject"] in existing_list:
    #         class_instance = ClassDatabase.objects.create(class_id = i["subject"], class_name="")

    # for i in subjects:
        url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=" + "CS" +"&page=1"
        url_data = View.get_json_data(url)
        context = {'data': url_data}
        for j in range(len(context["data"])):
            class_info = context['data'][j]['catalog_nbr']
            instructor = context['data'][j]["instructors"][0]["name"]
            name = context['data'][j]['descr']
            all= "CS"+class_info +" " + name + " "+ instructor
            if not all in existing_list:
                existing_list.append(all)
                class_instance = ClassDatabase.objects.create(class_id="CS" + class_info, class_name=name, professors=instructor)

    # move later


    selection = ClassDatabase.objects.all()
    filters = FilterCourses(response.GET,queryset= selection)
    context = {"filters": filters}
    if response.method == "POST":
        return redirect('/CS3240')
    return render(response, "main/student_home.html", context)


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


def mnemonic(response):
    # url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
    # url_data = View.get_json_data(url)
    #
    # context = {'data': url_data}
    # subjects = context["data"]["subjects"]
    # existing_list = []
    # existing_classes = ClassDatabase.objects.all()
    # for i in existing_classes:
    #     existing_list.append(str(i))
    return render(response, "main/mnemonic_page.html")



def other(response):
    return render(response, "main/home.html", {'name': 'Other'})


@login_required
def select_user(response):
    # url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
    # url_data = View.get_json_data(url)
    #
    # context = {'data': url_data}
    # subjects = context["data"]["subjects"]
    # existing_classes = ClassList.objects.all()
    # for i in subjects:
    #     if not i["subject"] in existing_classes:
    #         print(i["subject"])
    #         # class_instance = ClassList.objects.create(class_id = i["subject"], class_name="")

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
    

def searchbar(response):
    if response.method == 'GET':
        search = response.GET.get('mnemonic')
        if not search is None:
            print("here")
            existing_list = []
            existing_classes = ClassDatabase.objects.all()
            for i in existing_classes:
                existing_list.append(str(i))
            pages = 100
            for page_number in range(1, pages):
                print("pages numbers", page_number)
                url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=" + str(
                    search) + "&page=" + str(page_number)
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
                    all = str(search) + class_info + " " + name + " " + instructor
                    if not all in existing_list:
                        existing_list.append(all)
                        class_instance = ClassDatabase.objects.create(class_id=str(search) + class_info,
                                                                      class_name=name,
                                                                      professors=instructor, class_mnen=str(search))

            selection = ClassDatabase.objects.filter(class_mnen= str(search))
            if not selection:
                return render(response, "main/mnemonic_page.html", {"error_message": "Not an exisiting mnemonic"})
            filters = FilterCourses(response.GET,queryset= selection)
            context = {"filters": filters}
        else:
            print("else")
            selection = ClassDatabase.objects.all()
            filters = FilterCourses(response.GET, queryset=selection)
            context = {"filters": filters}

    return render(response, "main/student_home.html", context)