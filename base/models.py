from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

colorList = [
    '#FFF5E4',
    '#FFE3E1',
    '#FFD1D1',
    '#FF9494',
    '#B1B2FF',
    '#AAC4FF',
    '#D2DAFF',
    '#CDF0EA',
    '#ECC5FB',
    '#FAF4B7',
    '#ECC5FB',
    '#A7D2CB',
    '#F2D388',
    '#F675A8',
    '#FFCCB3',
    '#F29393',
    '#FFB3B3',
    '#FFE9AE',
    '#C1EFFF',
    '#B2C8DF',
    '#C4DFAA',  # ss
    '#F2D7D9',
    '#D3CEDF',
    '#CDF0EA',
    '#9ADCFF',
    '#B4CFB0',
    '#C3DBD9',
    '#FDCEB9',
    '#FFEFEF',
    '#EEC373',
    '#96C7C1',
    '#FFDEFA',
    '#C6D57E',
]


class TopicColor(models.Model):
    color = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.color


class Topic(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # order rooms with newset first
    class Meta:
        ordering = ['-updated', '-created']

    # create uuid field

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Visa nyaste meddelandena först
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]  # visa endast första 50 bokstäverna
