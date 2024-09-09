from django.db import models
from accounts.models import CustomUser

class Category(models.TextChoices):
  ELECTRONICS = 'Electronics'
  LAPTOPS = 'Laptops'
  ARTS = 'Arts'
  FOOD = 'Food'
  HOME = 'Home'
  KITCHEN = 'Kitchen'

class Product(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=150, blank=False, default="")
  description = models.CharField(max_length=250, blank=False, default="")
  price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
  brand = models.CharField(max_length=150, blank=False, default="")
  category = models.CharField(max_length=150, choices=Category.choices, blank=True)
  ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0)
  stock = models.IntegerField(default=0)
  user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

class Review(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
  user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
  rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
  comment = models.CharField(max_length=250, blank=False, default="")
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return (self.comment)
  

