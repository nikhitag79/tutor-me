from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name='home'),
    path("student_home/", views.student_home, name='student_home'),
    path("my_view/", views.my_view, name="my_view"),
    path("tutor_home/", views.tutor_home, name='tutor_home'),
    path("schedule/", views.schedule, name='schedule'),
    path("other/", views.other, name='other'),
    path("account/", views.account, name='account'),
    path("select_user/", views.select_user, name='select_user'),
    path("test/",views.a,name='a'),
    path("test/searchbar/",views.searchbar,name='searchbar'),
    path("<str:class_id>", views.classes, name='class'),
]