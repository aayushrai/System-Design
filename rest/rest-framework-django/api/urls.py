from django.urls import path
from .views import index,create,index2

urlpatterns = [
    path('<str:fileType>',index,name="index"),
    path('',create,name="create"),
    path('<str:fileType>/<int:sid>',index2,name="index2"),

]