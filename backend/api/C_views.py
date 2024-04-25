from telnetlib import STATUS
from xml.dom import NotFoundErr
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework import generics,permissions

from .models import Order,Category,Product,Comment
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer,CommentSerializer




class AllowAnyForGet(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
class GenericListCategories(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class GenericRetrieveCategory(generics.RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        # Retrieve the category instance by its ID
        category_id = self.kwargs.get('pk')
        return Category.objects.get(id=category_id)   
 
class GenericListCreateProducts(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
class GenericRetrieveProduct(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class = ProductSerializer

# @permission_classes[IsAuthenticated]
class GenericListCreateMyProducts(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user_id = request.user.id  # Get the user ID from the authenticated user
        products = Product.objects.filter(owner=user_id)

        if not products:
            raise NotFound("Products not found for this user")

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class GenericRetrieveUpdateDestroyMyProductDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        try:
            obj = queryset.get(pk=pk)
            if obj.owner != self.request.user:
                raise PermissionDenied("You do not have permission to perform this action.")
            return obj
        except Product.DoesNotExist:
            raise NotFound("Product not found")
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GenericListCreateComments(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAnyForGet]
    def get(self,pk):
        try:
            comments=Comment.objects.filter(product_id=pk)
        except Comment.DoesNotExist:
            raise NotFoundErr("Product not found")
        serializer=CommentSerializer(comments)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        permission_classes=[IsAuthenticated]
        product_id = kwargs.get('product_id')
        try:
    
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        # Add user_id and product_id to the comment data
        request.data['user_id'] = request.user.id
        request.data['product_id'] = product_id

        # Call the super method to perform the creation
        return super().create(request, *args, **kwargs)
    
class GenericListCreateMyOrders(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(client=user)
    
    def create(self, request, *args, **kwargs):
        request.data['client'] = request.user.id
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        return Response(serializer.data)