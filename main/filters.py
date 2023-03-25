# Nikhita Guntu gjs2xs
import django_filters
from .models import ClassDatabase
class FilterCourses(django_filters.FilterSet):
    class Meta:
        model =ClassDatabase
        fields = ["class_id", "class_name", "professors", "available_tutors"]

        def __str__(self):
            return self.class_id + ' ' + self.class_name + ' ' + self.professors + ' ' + available_tutors