from django.contrib import admin
from .models import ClassList, Item, ClassDatabase,Event
    #, UserProfile

# Register your models here.
admin.site.register(ClassList)
admin.site.register(Item)
admin.site.register(ClassDatabase)
admin.site.register(Event)
#admin.site.register(UserProfile)