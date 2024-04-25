from django.shortcuts import render
from .models import Order,Category,Product,User
from rest_framework import generics
from .serializers import ProductSerializer,OrderSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def categories_products(request, pk):
    try:
        products = Product.objects.all().filter(category_id = pk)
    except Product.DoesNotExist as e:
        return Response({'message': str(e)}, status=400)
    if request.method == 'GET':
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def categories_product_details(request, pk, product_id):
    try:
        products = Product.objects.all().filter(category_id = pk)
        products = products.all().filter(id = product_id)

    except Product.DoesNotExist as e:
        return Response({'message': str(e)}, status=400)

    if request.method == 'GET':
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)

@api_view(['GET'])
def products_top_ten(request):

    top_ten_products = Product.objects.all().order_by('-rate')[:10]

    # Serialize the products data
    serializer = ProductSerializer(top_ten_products, many=True)

    # Return the serialized data in the response
    return Response(serializer.data)
