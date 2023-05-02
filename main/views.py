from django.shortcuts import render, redirect

from .models import View, ClassDatabase, Event, Request, TextMessages, ClassDescription, Professors, ClassName
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filters import FilterCourses
from django.contrib.auth.models import Group
from oauth_app.models import User
import json
from json import dumps
import datetime
import sys
import re


# Create your views here.

def home(response):
    if response.POST.get('logout'):
        logout(response)
        return redirect("/")
    return render(response, "main/home.html", {'name': 'Home'})


def student_home(response):
    if response.method == "POST":
        if response.POST.get('logout'):
            logout(response)
            return redirect("/")
        return redirect('/CS3240')
    return render(response, "main/student_home.html")


def tutor_home(response):
    if response.POST.get('logout'):
        logout(response)
        return redirect("/")
    requests = Request.objects.filter(tutor = response.user)
    return render(response, "main/tutor_home.html", {'name': 'Home', 'requests': requests})


def schedule(response):
    if response.POST.get('logout'):
        logout(response)
        return redirect("/")
    user = response.user
    if user.user_type == 1:
        all_events = Event.objects.filter(tutor=response.user)
        all_groups = Group.objects.filter(user=response.user)
        context = {
            "events": all_events, "name": 'Schedule', "user": response.user, "groups": all_groups
        }
    elif user.user_type == 2:
        all_events = Event.objects.filter(student=response.user)
        context = {
            "events": all_events, "name": 'Schedule', "user": response.user
        }
    return render(response, "main/schedule.html", context)


def add_event(request):
    group = Group.objects.get(name=request.GET.get("title"))
    print(group.name)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    print(end)
    title = request.GET.get("title", None)
    data = {"group": group.name}
    format = "%Y-%m-%d %H:%M:%S"
    slot_time = 30
    time = datetime.datetime.strptime(start, format)
    end = datetime.datetime.strptime(end, format)
    while time < end:
        print('event start', time)
        print('event end', time + datetime.timedelta(minutes=slot_time))
        if Event.objects.filter(name=str(title), start=time, end=time+datetime.timedelta(minutes=slot_time), tutor=request.user).exists():
            return JsonResponse(data)
        event = Event(name=str(title), start=time, end=time + datetime.timedelta(minutes=slot_time), tutor=request.user,
                      month=time.strftime("%B"), weekday=time.strftime("%A"), day=time.strftime("%d"),
                      start_hour=time.strftime("%H:%M"),
                      end_hour=(time + datetime.timedelta(minutes=slot_time)).strftime("%H:%M"))
        event.save()
        time += datetime.timedelta(minutes=slot_time)
    return JsonResponse(data)


def all_events(request, class_id="", first_professors="", middle="", last_professors=""):
    user = request.user
    if user.user_type == 1:
        all_events = Event.objects.filter(tutor=user)
    elif user.user_type == 2:
        all_events = Event.objects.filter(student=user)
    out = []
    now = datetime.datetime.now()
    for event in all_events:
        event_end = event.end
        if now.timestamp() > event_end.timestamp():
            if event.student:
                TextMessages.objects.create(subject="Appointment Deleted",
                                        content="The appointment with " + event.student.username + " on " + event.weekday + ", " + event.month + ", " + event.day + " has passed and has been deleted",
                                        time_stamp=datetime.datetime.now(),
                                        viewed=False,
                                        receiver=event.tutor,
                                        )
                TextMessages.objects.create(subject="Appointment Deleted",
                                            content="The appointment with " + event.tutor.username + " on " + event.weekday + ", " + event.month + ", " + event.day + " has passed and has been deleted",
                                            time_stamp=datetime.datetime.now(),
                                            viewed=False,
                                            receiver=event.tutor,
                                            )
            else:
                TextMessages.objects.create(subject="Appointment Deleted",
                                            content="The appointment with on " + str(event.weekday) + ", " + str(event.month) + ", " + str(event.day) + " was not accepted, has passed, and has been deleted",
                                            time_stamp=datetime.datetime.now(),
                                            viewed=False,
                                            receiver=event.tutor,
                                            )
            event.delete()
        else:
            out.append({
                'title': event.name,
                'id': event.id,
                'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
                'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            })
    return JsonResponse(out, safe=False)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


 
def remove(request):
    user = request.user
    id = request.GET.get("id", None)
    event = Event.objects.get(id=id)
    data = {}
    if user.user_type == 1:
        if event.student:
            TextMessages.objects.create(subject="Appointment Deleted",
                                        content=request.user.username + " canceled their appointment on " + event.weekday + ", " + event.month + ", " + event.day + ".\nPlease make sure to schedule another tutoring session if it is still required.!",
                                        time_stamp=datetime.datetime.now(),
                                        viewed=False,
                                        receiver=event.student,
                                        )
        event.delete()
    if user.user_type == 2:
        event.student = None
        event.isAval = True
        event.save()
        TextMessages.objects.create(subject="Appointment Deleted",
                                    content=str(user.username) + " canceled their appointment on " + str(event.weekday) + ", " + str(event.month) + ", " + str(event.day) + ".\nThe appointment is once again open!",
                                    time_stamp=datetime.datetime.now(),
                                    viewed=False,
                                    receiver=event.tutor,
                                    )
    return JsonResponse(data)


def account(response):
    # user_id = response.GET.get("username")
    # print(user_id)
    if response.method == "POST":
        if response.POST.get('logout'):
            logout(response)
            return redirect("/")
        elif response.POST.get('set_username'):
            new_username = response.POST.get('username')
            if response.user.username == new_username or new_username == '':
                return render(response, "main/account.html",
                              {'name': 'Account', 'error': 'That is already your username!'})
            elif User.objects.filter(username=new_username).exists():
                return render(response, "main/account.html",
                              {'name': 'Account', 'error': 'That user name is already taken. Try again'})
            elif len(new_username) >= 20:
                return render(response, "main/account.html",
                              {'name': 'Account', 'error': 'The user name could not be changed, The username must be shorter than 30 characters!'})
            else:
                response.user.username = new_username
                response.user.save()
        elif response.POST.get('set_hourly'):
            hourly_rate = response.POST.get('hourly_rate')
            response.user.tutor_rate = hourly_rate
            response.user.save()
    return render(response, "main/account.html", {'name': 'Account'})


def classes(response, class_id, first_professors, middle="", last_professors=""):
    user = response.user
    print(user.user_type)
    if (middle == ""):
        print("single")
        professors = first_professors + " " + last_professors
    else:
        print("double")
        professors = first_professors + " " + middle + " " + last_professors
    print("professors", professors)
    my_instance = ClassDatabase.objects.filter(class_id=class_id, professors=professors)
    header = class_id + " " + professors
    dict = {}
    group_name = Group.objects.get(name=header)
    now = datetime.datetime.now()
    event_name = Event.objects.all()
    for event in event_name:
        event_end = event.end
        if now.timestamp() > event_end.timestamp():
            if event.student:
                TextMessages.objects.create(subject="Appointment Deleted",
                                        content="The appointment with " + event.student.username + " on " + event.weekday + ", " + event.month + ", " + event.day + " has passed and has been deleted",
                                        time_stamp=datetime.datetime.now(),
                                        viewed=False,
                                        receiver=event.tutor,
                                        )
                TextMessages.objects.create(subject="Appointment Deleted",
                                            content="The appointment with " + event.tutor.username + " on " + event.weekday + ", " + event.month + ", " + event.day + " has passed and has been deleted",
                                            time_stamp=datetime.datetime.now(),
                                            viewed=False,
                                            receiver=event.student,
                                            )
            else:
                TextMessages.objects.create(subject="Appointment Deleted",
                                            content="The appointment on " + event.weekday + ", " + event.month + ", " + event.day + " was not accepted, has passed, and has been deleted",
                                            time_stamp=datetime.datetime.now(),
                                            viewed=False,
                                            receiver=event.tutor,
                                            )
            event.delete()
    event_name = Event.objects.all()
    print('event_name', event_name)
    # This is what we will use, using a different one for testing
    # event_name = Event.objects.get(name= header)
    users = group_name.user_set.all()
    print("users", type(users), users)
    letters_only = ''.join(filter(str.isalpha, class_id))


    if response.method == "POST":
        if response.POST.get('logout'):
            logout(response)
            return redirect("/")
        user = response.user
        group = Group.objects.get(name=class_id + " " + professors)
        if user.user_type == 1:
            if not group.user_set.filter(username=user).exists():
                group.user_set.add(user)
                group.save()
                my_instance = ClassDatabase.objects.filter(class_id=class_id, professors=professors).first()
                my_instance.available_tutors = True
                my_instance.save()
                context = {
                    "events": event_name, "name": 'Schedule', "user": response.user
                }
                return redirect("/" + class_id + ' ' + professors, context)
            else:
                if response.POST.get('remove'):
                    group.user_set.remove(user)
                    if group.user_set.all().count() == 0:
                        cleaned_events = Event.objects.filter(tutor=user, name = header)
                        for event in cleaned_events:
                            TextMessages.objects.create(subject="Appointment Deleted",
                                                        content="The appointment on " + event.weekday + ", " + event.month + ", " +  event.day + " has been deleted.",
                                                        time_stamp=datetime.datetime.now(),
                                                        viewed=False,
                                                        receiver=event.student,
                                                        )
                            event.delete()
                        my_instance = ClassDatabase.objects.filter(class_id=class_id, professors=professors).first()
                        my_instance.available_tutors = False
                        my_instance.save()
                return redirect("/tutor_home/searchbar/?mnemonic=" + letters_only)
        elif user.user_type == 2:
            event_query = Event.objects.filter(id=response.POST.get('event_name'))
            actual_event = []
            for event in event_query:
                actual_event.append(event)
            this_event = actual_event[0]
            if not Request.objects.filter(event_id=response.POST.get('event_name'), student=user).exists():
                request = Request.objects.create(event_id=response.POST.get('event_name'), event_start=this_event.start,
                                                 event_stop=this_event.end, tutor=this_event.tutor, student=user,
                                                 actual_event=this_event, event_month=this_event.month,
                                                 event_weekday=this_event.weekday, event_day=this_event.day,
                                                 event_start_hour=this_event.start_hour,
                                                 event_end_hour=this_event.end_hour)
                request.save()
                TextMessages.objects.create(subject="Requested Appointment",
                                            content="Sent a request to " + request.tutor.username + " for " + request.event_weekday + ", " + request.event_month + ", " + request.event_day + "\nYou will be notified if they are able attend.",
                                            time_stamp=datetime.datetime.now(),
                                            viewed=False,
                                            receiver=response.user,
                                            )
                return redirect("/student_home/searchbar/?mnemonic=" + letters_only)

            TextMessages.objects.create(subject="Requested Appointment",
                                        content="You already requested this appointment so the request was not made! " + this_event.tutor.username + " will get in touch with you regarding your previous event when they can.",
                                        time_stamp=datetime.datetime.now(),
                                        viewed=False,
                                        receiver=response.user,
                                        )
            return redirect("/student_home/searchbar/?mnemonic=" + letters_only)

    user_in_group = 0
    if user.groups.filter(name=header).exists():
        user_in_group = 1
    data_dict = {'group': header}
    data_json = dumps(data_dict)
    return render(response, "main/roster.html",
                  {'header': header, 'user': user, 'group': group_name, 'event': event_name,
                   'user_in_group': user_in_group, 'events': event_name, 'data_json': data_json})


def mnemonic(response):
    
    user = response.user
    requests = ''
    if user.id is not None:
        requests = Request.objects.filter(tutor=user)
        if requests:
            messages.info(response, "You have unseen requests")
    if response.method == "POST":
        if response.POST.get('logout'):
            logout(response)
            return redirect("/")
    return render(response, "main/mnemonic_page.html", {'name': 'Home', 'user': user,})



def messages_and_requests(response):
    user = response.user
    unplanned_events=[]
    if user.user_type == 1:
        unplanned_events = Event.objects.filter(tutor = user, isAval = True)
        booked_events = Event.objects.filter(tutor = user, isAval = False)
    if user.user_type == 2:
        booked_events = Event.objects.filter(student=user)
    if user.id is not None:
        requests = Request.objects.filter(tutor = response.user)
        cal = {}
        sorted_cal = {}
        month = {'January': 1, "February": 2, " March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                 " September": 9, "October": 10, "November": 11, "December": 12}
        for request in requests:
            if request.event_month not in cal:
                cal[month[request.event_month]] = request.event_month
        scal = sorted(cal)
        for m in scal:
            sorted_cal[cal[m]] = cal[m]
        page = ''
        unread_received_texts = TextMessages.objects.filter(receiver = response.user, viewed = False)
        read_texts = TextMessages.objects.filter(receiver = response.user, viewed = True)
        sent_texts = TextMessages.objects.filter(sender = response.user)
    if response.GET.get:
        if response.GET:
            page = response.GET['message_option']
    if response.POST.get('logout'):
        logout(response)
        return redirect("/")
    if response.POST.get("Accept"):
        request = Request.objects.get(id=response.POST.get("Accept"))
        adjusted_event = Event.objects.get(id=request.event_id)
        adjusted_event.student = request.student
        adjusted_event.isAval = False
        adjusted_event.save()
        request.delete()
        new_text = TextMessages.objects.create(subject="Appointment Accepted",
                                               content=request.tutor.username + " has accepted an appointment with you on " + request.event_weekday + ", " + request.event_month + ", " + request.event_day + "\nSee you there, and message me if you need too!",
                                               time_stamp=datetime.datetime.now(),
                                               viewed=False,
                                               receiver=request.student,
                                               sender=request.tutor,
                                               )
        requests = Request.objects.filter(tutor=response.user)
    elif response.POST.get("Reject"):
        request = Request.objects.get(id=response.POST.get("Reject"))
        new_text = TextMessages.objects.create(subject="Appointment Rejection",
                                           content = "Unfortunately, " + request.tutor.username + " was unable to meet with you on " + request.event_weekday + ", " + request.event_month + ", " + request.event_day + "\nPlease try finding another time or available tutor!",
                                           time_stamp = datetime.datetime.now(),
                                           viewed = False,
                                           receiver = request.student
                                           )                                                        ,
        request.delete()
        requests = Request.objects.filter(tutor=response.user)
    elif response.POST.get("Mark as Read"):
        message = TextMessages.objects.get(id=response.POST.get("Mark as Read"))
        message.viewed = True
        message.save()
        unread_received_texts = TextMessages.objects.filter(receiver=response.user, viewed=False)
    elif response.POST.get("Delete"):
        message = TextMessages.objects.get(id=response.POST.get("Delete"))
        if message.receiver == user:
            if message.sender:
                message.receiver = None
                message.save()
            else:
                message.delete()
        else:
            if message.receiver:
                message.sender = None
                message.save()
            else:
                message.delete()
        read_texts = TextMessages.objects.filter(receiver=response.user, viewed=True)
    elif response.POST.get("Delete_Event"):
        modified_event = Event.objects.get(id=response.POST.get("Delete_Event"))
        if user.user_type == 1:
            modified_event.delete()
            unplanned_events = Event.objects.filter(tutor=user, isAval=True)
            booked_events = Event.objects.filter(tutor=user, isAval=False)
        if user.user_type == 2:
            modified_event.student = None
            modified_event.isAval = True
            modified_event.save()
            booked_events = Event.objects.filter(student=user)
    elif response.POST.get("Reply"):
        message = TextMessages.objects.get(id=response.POST.get("Reply"))
        message.viewed = True
        message.save()
        new_message = TextMessages.objects.create(content=response.POST.get('reply_message'),
                                                  subject="Reply from " + user.username,
                                                  time_stamp=datetime.datetime.now(),
                                                  viewed=False,
                                                  receiver=message.sender,
                                                  sender=user
                                                  )
        page = "Sent"

    return render(response, "main/message_request.html", {'name': 'Messages and Requests', 'user': user, 'requests': requests, 'sorted_calendar': sorted_cal, 'unread_received_texts': unread_received_texts, 'read_texts': read_texts, 'sent_texts': sent_texts, 'unbooked': unplanned_events, 'booked': booked_events, 'page': page})


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
            return redirect('/tutor_home/')
        elif user_type == "Student":
            return redirect('/student_home/')

    else:
        return render(response, 'main/select_user.html')
    

def searchbar_tutee(request):
    if request.POST.get('logout'):
        logout(request)
        return redirect("/")
    sys.path.append('../')
    if request.method == 'GET':
        search = request.GET.get('mnemonic')
        if not search is None:
            search_mnemonic = str(search).upper()
            print("search mnemon", search_mnemonic)
            existing_list = []
            existing_classes = ClassDatabase.objects.filter(class_mnen=search_mnemonic).order_by('class_id')
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
                                if not ClassDescription.objects.filter(class_id=search_mnemonic + class_info).exists():
                                    ClassDescription.objects.create(class_id=search_mnemonic + class_info,
                                                                    class_name=name, class_mnen=search_mnemonic)
                                if not Professors.objects.filter(professors=instructor,
                                                                 class_mnen=search_mnemonic).exists():
                                    Professors.objects.create(professors=instructor, class_mnen=search_mnemonic)
                                if not ClassName.objects.filter(class_name=name).exists():
                                    ClassName.objects.create(class_name=name, class_mnen=search_mnemonic)
                    else:
                        messages.error(request, "Not an existing mnemonic")
                        return redirect('/student_home/', {'name': 'Home'})
            filters = FilterCourses(request.GET,queryset= existing_classes, filter_value=search_mnemonic)
            context = {"filters": filters,'name':search_mnemonic}
        else:
            print(request.GET)
            if request.GET['class_id']:
                full_class_id = request.GET['class_id']
                selected_description = ClassDescription.objects.get(id=full_class_id)
                selected_mnem = selected_description.class_mnen
                selection = ClassDatabase.objects.filter(class_mnen=selected_mnem)
                filters = FilterCourses(request.GET, queryset=selection, filter_value=selected_mnem)
            elif request.GET['class_name']:
                full_class_name = request.GET['class_name']
                selected_description = ClassName.objects.get(id=full_class_name)
                selected_mnem = selected_description.class_mnen
                selection = ClassDatabase.objects.filter(class_mnen=selected_mnem)
                filters = FilterCourses(request.GET, queryset=selection, filter_value=selected_mnem)
            elif request.GET['professors']:
                full_class_name = request.GET['professors']
                selected_description = Professors.objects.get(id=full_class_name)
                selected_mnem = selected_description.class_mnen
                selection = ClassDatabase.objects.filter(class_mnen=selected_mnem)
                filters = FilterCourses(request.GET, queryset=selection, filter_value=selected_mnem)
            else:
                messages.error(request, "You must choose a valid parameter before searching!")
                if request.user.user_type == 1:
                    return redirect('/tutor_home/')
                elif request.user.user_type == 2:
                    return redirect('/student_home/')
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
    if request.POST.get('logout'):
        logout(request)
        return redirect("/")
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
                                if not ClassDescription.objects.filter(class_id=search_mnemonic + class_info).exists():
                                    ClassDescription.objects.create(class_id=search_mnemonic + class_info,
                                                                    class_name=name, class_mnen=search_mnemonic)
                                if not Professors.objects.filter(professors=instructor,
                                                                 class_mnen=search_mnemonic).exists():
                                    Professors.objects.create(professors=instructor, class_mnen=search_mnemonic)
                                if not ClassName.objects.filter(class_name=name).exists():
                                    ClassName.objects.create(class_name=name, class_mnen=search_mnemonic)
                    else:
                        messages.error(request, "Not an existing mnemonic")
                        return redirect('/tutor_home/', {'name': 'Home', "results": tutor_group})
            filters = FilterCourses(request.GET, queryset=existing_classes, filter_value=search_mnemonic)

            context = {"filters": filters, 'name': search_mnemonic, 'user': user, 'results': tutor_group}
        else:
            print(request.GET)
            if request.GET['class_id']:
                full_class_id = request.GET['class_id']
                selected_description = ClassDescription.objects.get(id=full_class_id)
                selected_mnem = selected_description.class_mnen
                selection = ClassDatabase.objects.filter(class_mnen=selected_mnem)
                filters = FilterCourses(request.GET, queryset=selection, filter_value=selected_mnem)
            elif request.GET['class_name']:
                full_class_name = request.GET['class_name']
                selected_description = ClassName.objects.get(id=full_class_name)
                selected_mnem = selected_description.class_mnen
                selection = ClassDatabase.objects.filter(class_mnen=selected_mnem)
                filters = FilterCourses(request.GET, queryset=selection, filter_value=selected_mnem)
            elif request.GET['professors']:
                full_class_name = request.GET['professors']
                selected_description = Professors.objects.get(id=full_class_name)
                selected_mnem = selected_description.class_mnen
                selection = ClassDatabase.objects.filter(class_mnen=selected_mnem)
                filters = FilterCourses(request.GET, queryset=selection, filter_value=selected_mnem)
            else:
                print('user', request.user.user_type)
                messages.error(request, "You must choose a valid parameter before searching!")
                if request.user.user_type == 1:
                    return redirect('/tutor_home/')
                elif request.user.user_type == 2:
                    return redirect('/student_home/')
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
            major_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232"
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
                    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=" + search_mnemonic_json + "&page=" + str(
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
                            if not ClassDescription.objects.filter(class_id=acronym + class_info).exists():
                                ClassDescription.objects.create(class_id=acronym + class_info,
                                                                          class_name=name,class_mnen=acronym)
                            if not Professors.objects.filter(professors=instructor, class_mnen=acronym).exists():
                                Professors.objects.create(professors=instructor, class_mnen=acronym)
    return render(request, "main/database.html", {'name': 'Database Setup', 'user': user})
