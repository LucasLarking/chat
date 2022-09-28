from django.contrib import admin

# Register your models here.


# Add rooms to admin panel
from .models import Room, Topic, Message, TopicColor
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(TopicColor)