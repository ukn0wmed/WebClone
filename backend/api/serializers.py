from rest_framework import serializers
from api.models import Category,Product,Comment,Order
from django.contrib.auth.models import User

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name=serializers.CharField()
    icon_image=serializers.ImageField()
    def create(self, validated_data):
        instance=Category.objects.create(
            name=validated_data.get("name"),
            icon_image=validated_data.get("icon_image"),
            
        )
        return instance
   
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','cost','owner','category_id','description','rate','images']

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=200)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def create(self, validated_data):
        """
        Create and return a new `Comment` instance, given the validated data.
        """
        return Comment.objects.create(**validated_data)
 

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','client','products','total_cost']