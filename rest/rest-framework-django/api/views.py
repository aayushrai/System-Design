from django.shortcuts import render,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Song,Audiobook,Podcast,SongSerializer,PodcastSerializer,AudiobookSerializer
# Create your views here.

@api_view(['GET'])
def index(request,fileType):
    if request.method == "GET":
        if fileType == "song":
            songs = Song.objects.all()
            serilizeSong = SongSerializer(songs,many=True)
            return Response(serilizeSong.data,status=status.HTTP_200_OK)
        
        elif fileType == "podcast":
            podcasts = Podcast.objects.all()
            serilizePodcast = PodcastSerializer(podcasts,many=True)
            return Response(serilizePodcast.data,status=status.HTTP_200_OK)
        
        elif fileType == "audiobook":
            audiobooks = Audiobook.objects.all()
            serilizeAudiobook = AudiobookSerializer(audiobooks,many=True)
            return Response(serilizeAudiobook.data,status=status.HTTP_200_OK)
        
        else:
            return Response(data={"Error":"Invalid file type in URL"},status=status.HTTP_400_BAD_REQUEST)
        
    return Response(data={"Error":"Something went"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def create(request):
    data = request.data
    audioFileType = data["audioFileType"]
    audioFileMetadata = data["audioFileMetadata"]
    
    if audioFileType.lower() == "song":
        print(audioFileType)
        try:
            Name = audioFileMetadata["Name"]
            Duration = audioFileMetadata["Duration"]
            obj = Song(Name=Name,Duration=Duration)
            obj.save()
            return Response(data={"id":obj.id},status=status.HTTP_200_OK)
        except:
            return Response(data={"Error":"Invalid audioFileMetadata"},status=status.HTTP_400_BAD_REQUEST)
        
    elif audioFileType.lower() == "podcast":
        try:
            Name = audioFileMetadata["Name"]
            Duration = audioFileMetadata["Duration"]
            Host = audioFileMetadata["Host"]
            Participants = audioFileMetadata["Participants"]
            
            if len(Participants) > 10:
                print("[Error] More than 10 participants")
                return Response(data={"Error":"More than 10 Participants"},status=status.HTTP_400_BAD_REQUEST)
            obj = Podcast(Name=Name,Duration=Duration,Host=Host,Participants=Participants)
            
            obj.save()
            return Response(data={"id":obj.id},status=status.HTTP_200_OK)
        
        except:
            return Response(data={"Error":"Invalid audioFileMetadata"},status=status.HTTP_400_BAD_REQUEST)
        
    elif audioFileType.lower() == "audiobook":
        try:
            Title = audioFileMetadata["Title"]
            Duration = audioFileMetadata["Duration"]
            Author = audioFileMetadata["Author"]
            Narrator =  audioFileMetadata["Narrator"]
            obj = Audiobook(Title=Title,Duration=Duration,Author=Author,Narrator=Narrator)
            obj.save()
            return Response(data={"id":obj.id},status=status.HTTP_200_OK)
        except:
            return Response(data={"Error":"Invalid audioFileMetadata"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={"Error":"Invalid audioFileType"},status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data={"Error":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT","GET","DELETE"])
def index2(request,fileType,sid):
    
    if request.method == "GET":
        if fileType == "song":
            songs = Song.objects.get(id=sid)
            serilizeSong = SongSerializer(songs)
            return Response(serilizeSong.data,status=status.HTTP_200_OK)
            
        elif fileType == "podcast":
            podcasts = Podcast.objects.get(id=sid)
            serilizePodcast = PodcastSerializer(podcasts)
            return Response(serilizePodcast.data,status=status.HTTP_200_OK)
        
        elif fileType == "audiobook":
            audiobooks = Audiobook.objects.get(id=sid)
            serilizeAudiobook = AudiobookSerializer(audiobooks)
            return Response(serilizeAudiobook.data,status=status.HTTP_200_OK)

        else:
            return Response(data={"Error":"Invalid file type in URL"},status=status.HTTP_400_BAD_REQUEST)
        
    
    if request.method == "DELETE":
        if fileType == "song":
            song = Song.objects.get(id=sid)
            song.delete()
            return Response({"status":"successfully deleted"},status=status.HTTP_200_OK)
        elif fileType == "podcast":
            podcast = Podcast.objects.get(id=sid)
            podcast.delete()
            return Response({"status":"successfully deleted"},status=status.HTTP_200_OK)
        elif fileType == "audiobook":
            audiobook = Audiobook.objects.get(id=sid)
            audiobook.delete()
            return Response({"status":"successfully deleted"},status=status.HTTP_200_OK)
        else:
            return Response(data={"Error":"Invalid file type in URL"},status=status.HTTP_400_BAD_REQUEST)
        
        
    
    if request.method == "PUT":
        audioFileMetadata = request.data["audioFileMetadata"]
        
        if fileType == "song":
            try:
                song = Song.objects.get(id=sid)
                song.Name = audioFileMetadata["Name"]
                song.Duration = audioFileMetadata["Duration"]
                song.save()
            except:
                return Response(data={"Error":"Invalid audioFileMetadata"},status=status.HTTP_400_BAD_REQUEST)
            
            serilizeSong = SongSerializer(song)
            return Response(serilizeSong.data,status=status.HTTP_200_OK)
        
        elif fileType == "podcast":
            
            try:
                podcast = Podcast.objects.get(id=sid)
                podcast.Name = audioFileMetadata["Name"]
                podcast.Duration = audioFileMetadata["Duration"]
                podcast.Host = audioFileMetadata["Host"]
                Participants = audioFileMetadata["Participants"]
                if len(Participants) > 10:
                    print("[Error] More than 10 participants")
                    return Response(data={"Error":"More than 10 Participants"},status=status.HTTP_400_BAD_REQUEST)
                podcast.Participants = audioFileMetadata["Participants"]
                podcast.save()
            except:
                return Response(data={"Error":"Invalid audioFileMetadata"},status=status.HTTP_400_BAD_REQUEST)
            
            serilizePodcast = PodcastSerializer(podcast)
            return Response(serilizePodcast.data,status=status.HTTP_200_OK)
        
        elif fileType == "audiobook":
            
            try:
                audiobook = Audiobook.objects.get(id=sid)
                audiobook.Title = audioFileMetadata["Title"]
                audiobook.Duration = audioFileMetadata["Duration"]
                audiobook.Author = audioFileMetadata["Author"]
                audiobook.Narrator =  audioFileMetadata["Narrator"]
                audiobook.save()
            except:
                return Response(data={"Error":"Invalid audioFileMetadata"},status=status.HTTP_400_BAD_REQUEST)
            
            serilizeAudiobook = AudiobookSerializer(audiobook)
            return Response(serilizeAudiobook.data,status=status.HTTP_200_OK)
        else:
            return Response(data={"Error":"Invalid file type in URL"},status=status.HTTP_400_BAD_REQUEST)
        
    return Response(data={"Error":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



