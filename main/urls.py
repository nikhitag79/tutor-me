from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name='home'),
    #path("class_finder/", views.student_home, name='class_finder'),
    path("tutor_home/", views.mnemonic, name='tutor_home'),
    path("tutor_home/searchbar/", views.searchbar_tutor, name='searchbar'),
    path("schedule/", views.schedule, name='schedule'),
    path("other/", views.other, name='other'),
    path("account/", views.account, name='account'),
    path("select_user/", views.select_user, name='select_user'),
    path("student_home/",views.mnemonic,name='student_home'),
    path("student_home/searchbar/",views.searchbar_tutee,name='searchbar'),
    path("<str:class_id>/", views.classes, name='class'),

]