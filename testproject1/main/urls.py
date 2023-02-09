from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("student_home/", views.student_home, name='student_home'),
    path("tutor_home/", views.tutor_home, name='tutor_home'),
    path("schedule/", views.schedule, name='schedule'),
    path("other/", views.other, name='other'),
    path("account/", views.account, name='account'),
    path("<str:class_id>", views.classes, name='class'),
]