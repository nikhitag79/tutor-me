from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField

# Create your models here.
class User(AbstractUser):
    Tutor = 1
    Student = 2
    Administration = 3
    has_selected_role = models.BooleanField(default=False)
    available_classes = {(Tutor, 'Tutor'), (Student, 'Student'), (Administration, 'Administration')}
    user_type = models.PositiveIntegerField(choices=available_classes, default=2)
    tutor_rate = MoneyField(max_digits=2, decimal_places=2, default_currency='USD', default=0.00)


