from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Product, Review
from .serializers import ProductSerializer, AllProductSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from django.db.models import Avg


@api_view(['GET'])
def all_products(request):
  product = Product.objects.all().order_by('id')
  serializer = AllProductSerializer(product, many=True)
  return Response({
    'products':serializer.data
  }, status.HTTP_200_OK)


@api_view(['GET'])
def get_product(request, pk):
  product = get_object_or_404(Product, id=pk)
  serializer = AllProductSerializer(product, many=False)
  return Response({
    'product':serializer.data
  }, status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=ProductSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
  data = request.data
  serializer = ProductSerializer(data=data)
  if serializer.is_valid():
    product = Product.objects.create(**data, user = request.user)
    res = ProductSerializer(product, many=False)
    return Response({
      'details':res.data
    }, status.HTTP_201_CREATED)
  return Response({
    'error':serializer.errors
  }, status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='PUT', request_body=ProductSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
  data = request.data
  product = get_object_or_404(Product, id=pk)

  if product.user != request.user:
    return Response({
      'error':'You cannot update this product.'
    }, status.HTTP_401_UNAUTHORIZED)
  
  updatable_fields = ['name', 'description', 'price', 'brand', 'category', 'rating', 'stock']

  if not any(data.get(field) is not None for field in updatable_fields):
    return Response({'error': 'No valid fields provided for update.'}, status.HTTP_400_BAD_REQUEST)

  for field in updatable_fields:
    if field in data:
      setattr(product, field, data[field])

  product.save()
  serializer = ProductSerializer(product, many=False)
  return Response({
    'details':serializer.data
  }, status.HTTP_202_ACCEPTED)


@api_view(['DELETE'])
def delete_product(request, pk):
  product = get_object_or_404(Product, id=pk)
  if product.user != request.user:
    return Response({
      'error':'You are not authorised to delete this product.'
    }, status.HTTP_401_UNAUTHORIZED)
  product.delete()
  return Response({
    'details':'Product deleted sucessfully.'
  }, status.HTTP_202_ACCEPTED)



@swagger_auto_schema(method='POST', request_body=ProductSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):           # pk is the id of product.
  user = request.user
  data = request.data
  product = get_object_or_404(Product, id=pk)

  review = product.reviews.filter(user = user)

  required_fields = ['rating', 'comment']
  for field in required_fields:
    if field not in data:
      return Response({
        'error':f'Missing field {field}'
      }, status.HTTP_400_BAD_REQUEST)

  if data['rating'] < 0 or data['rating'] > 5:
    return Response({
      'error':'Please enter rating between 1-5'
    }, status.HTTP_400_BAD_REQUEST)
  if review.exists():
    new_review = {
      'rating':data['rating'],
      'comment':data['comment']
    }
    review.update(**new_review)
    rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
    product.ratings = rating['avg_ratings']
    product.save()
    return Response({
      'details':'Product updated sucessfully.'
    }, status.HTTP_202_ACCEPTED)
  else:
    Review.objects.create(
      user = user,
      product = product,
      rating = data['rating'],
      comment = data['comment']
    )
    rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
    product.ratings = rating['avg_ratings']
    product.save()
    return Response({
      'details':'Review posted'
    }, status.HTTP_201_CREATED)


  
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
  user = request.user
  product = get_object_or_404(Product, id=pk)

  review = product.reviews.filter(user=user)
  if review.exists():
    review.delete()

    # finding average rating
    rating = product.reviews.aggregate(avg_ratings = Avg('rating'))

    # if avg rating is none assign 0
    if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0

    product.ratings = rating['avg_ratings']     # save avg rating in the product
    product.save()
    return Response({
      'details':'Review deleted sucessfully.'
    }, status.HTTP_202_ACCEPTED)
  else:
    return Response({
      'error':'Review not found.'
    }, status.HTTP_404_NOT_FOUND)


