from django.db import models
import uuid
from rest_framework import serializers
# Create your models here.

class Song(models.Model):
    Name = models.CharField(max_length=100)
    Duration = models.IntegerField()
    Uploaded_time = models.DateTimeField(auto_now_add=True)

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"

class Podcast(models.Model):
    Name = models.CharField(max_length=100)
    Duration = models.IntegerField()
    Uploaded_time = models.DateTimeField(auto_now_add=True)
    Host = models.CharField(max_length=100)
    Participants = models.JSONField()
   
class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"
         
class Audiobook(models.Model):
    Title = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    Narrator = models.CharField(max_length=100)
    Duration = models.IntegerField()
    Uploaded_time = models.DateTimeField(auto_now_add=True)

class AudiobookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audiobook
        fields = "__all__"
