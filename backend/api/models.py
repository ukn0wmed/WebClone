from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100)
    icon_image = models.ImageField(upload_to='category_icons')
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    owner= models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.DecimalField(max_digits=5, decimal_places=2,default=None)
    images = models.CharField(max_length=300 ,default='https://resources.cdn-kaspi.kz/img/m/p/h32/h70/84378448199710.jpg?format=preview-large')
    def __str__(self):
        return self.name



class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.client}"


class Comment(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    text=models.CharField(max_length=200)
    product_id =models.ForeignKey(Product,on_delete=models.CASCADE)