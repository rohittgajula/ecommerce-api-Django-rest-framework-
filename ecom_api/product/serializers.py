from rest_framework import serializers
from .models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):

  class Meta:
    model = Review
    fields = ['comment', 'rating', 'user', 'created_at']

class AllProductSerializer(serializers.ModelSerializer):

  reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'brand', 'category', 'user', 'ratings', 'stock', 'created_at', 'reviews']

  def get_reviews(self, obj):
    reviews = obj.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return serializer.data


class ProductSerializer(serializers.ModelSerializer):

  class Meta:
    model = Product
    fields = ['id', 'name', 'description', 'price', 'brand', 'category', 'ratings', 'stock', 'created_at']

    extra_kwargs = {
      "name":{'required':True},
      "description":{'required':True},
      "brand": {"required":True},
      "category": {"required":True},
      "price":{"required":True},
      "stock":{"required":True}
    }
  
