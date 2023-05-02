# Nikhita Guntu gjs2xs
import django_filters
from django import forms
from .models import ClassDatabase, Professors, ClassDescription, ClassName
class FilterCourses(django_filters.FilterSet):
    class_id = django_filters.ModelChoiceFilter(
        queryset=ClassDatabase.objects.none(),
        widget=forms.Select,
        label="Class ID"
    )
    class_name = django_filters.ModelChoiceFilter(
        queryset=ClassDatabase.objects.none(),
        widget=forms.Select,
        label="Class Name"
    )
    professors = django_filters.ModelChoiceFilter(
        queryset=ClassDatabase.objects.none(),
        widget=forms.Select,
        label="Professor"
    )

    def __init__(self, *args, **kwargs):
        filter_value = kwargs.pop('filter_value', None)
        super().__init__(*args, **kwargs)

        # Filter queryset based on user input value
        if filter_value:
            self.filters['class_id'].queryset = ClassDescription.objects.filter(class_mnen=filter_value)
            self.filters['class_name'].queryset = ClassName.objects.filter(class_mnen=filter_value)
            self.filters['professors'].queryset = Professors.objects.filter(class_mnen=filter_value)
        print(self.filters['class_id'].queryset)
    class Meta:
        model =ClassDatabase
        fields = ["class_id", "class_name", "professors",]

        def __str__(self):
            return self.class_id + ' ' + self.class_name + ' ' + self.professors + ' ' + self.available_tutors