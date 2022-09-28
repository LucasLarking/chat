from django.forms import ModelForm
from .models import Room, Topic, TopicColor


# Create foorm users will use to create a room
class RoomForm(ModelForm):
    class Meta:
        model = Room

        exclude = ['host']  # SÄTT HOST AUTOMATISKT
        required = False

        labels = {
            'topic': 'Trådens Ämne',
            'name': 'Trådens Namn',
            'description': 'Trådens Beskrivning',
        }

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs\
            .update({
                'placeholder': 'T.ex "Vilken är den bästa fotbollspelaren?"',
                'class': 'inputName',

                'blank': 'True',

            })
        self.fields['name'].required = False
        self.fields['description'].widget.attrs\
            .update({
                'placeholder': 'T.ex "Här diskuteras vilken den bästa fotbollsspelaren i klubbfotboll är idag!"',
                'class': 'inputDescription',

                'blank': 'True',

            })
        self.fields['description'].required = False

#  fields = '__all__'


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        exclude = ['color']
