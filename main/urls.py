from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name='home'),
    path("database/", views.database_setup, name='database_setup'),
    #path("class_finder/", views.student_home, name='class_finder'),
    path("tutor_home/", views.mnemonic, name='tutor_home'),
    path("tutor_home/searchbar/", views.searchbar_tutor, name='searchbar'),
    path("schedule/", views.schedule, name='schedule'),
    path('schedule/all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path("messages_and_requests/", views.messages_and_requests, name='messages_and_requests'),
    path("account/", views.account, name='account'),
    path("select_user/", views.select_user, name='select_user'),
    path("student_home/",views.mnemonic,name='student_home'),
    path("student_home/searchbar/",views.searchbar_tutee,name='searchbar'),
    path("<str:class_id> <str:first_professors> <str:middle> <str:last_professors>/all_events/", views.all_events,name='all_events'),
    path("<str:class_id> <str:first_professors> <str:last_professors>/all_events/", views.all_events, name='all_events'),
    path("<str:class_id> <str:first_professors> <str:middle> <str:last_professors>/", views.classes, name='class'),
    path("<str:class_id> <str:first_professors> <str:last_professors>/", views.classes, name='class'),

]