from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    Tutor = 1
    Student = 2
    has_selected_role = models.BooleanField(default=False)
    available_classes = {(Tutor, 'Tutor'), (Student, 'Student')}
    user_type = models.PositiveIntegerField(choices=available_classes, default=2)