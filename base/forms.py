from django.forms import ModelForm
from .models import Room


# Create foorm users will use to create a room
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host'] # SÄTT HOST AUTOMATISKT
