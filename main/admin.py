from django.contrib import admin
from .models import ClassList, Item\
    #, UserProfile

# Register your models here.
admin.site.register(ClassList)
admin.site.register(Item)
#admin.site.register(UserProfile)