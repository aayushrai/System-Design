from rest_framework import viewsets,status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import Product, User
from .serializers import ProductSerializer
import random

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):  #/api/products  (GET Request)
        products = Product.objects.all()
        serializeProducts = ProductSerializer(products, many=True)
        return Response(serializeProducts.data)

    def create(self,reqeust): #/api/products (POST Request)
        serializeProduct = ProductSerializer(data=reqeust.data)
        serializeProduct.is_valid(raise_exception=True)
        serializeProduct.save()
        return Response(serializeProduct.data, status=status.HTTP_201_CREATED)

    def retrieve(self,request, pk=None): #/api/products/<str:id>  (GET Request)
        product = Product.objects.get(id=pk)
        serializeProduct = ProductSerializer(product)
        return Response(serializeProduct.data)

    def update(self,request, pk=None): #/api/products/<str:id>    (PUT Request)
        product = Product.objects.get(id=pk)
        serializeProduct = ProductSerializer(instance=product,data=request.data)
        serializeProduct.is_valid(raise_exception=True)
        serializeProduct.save()
        return Response(serializeProduct.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self,request, pk=None): #/api/products/<str:id>    (DELETE Request)
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserApiView(APIView):
    def get(self,request):
        users = User.objects.all()
        user = random.choice(users)

        return Response({
            'id': user.id
        })


    