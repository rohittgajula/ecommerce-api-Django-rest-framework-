from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password

from .models import CustomUser
from .serializers import SignUpSerializers, UserSerializer, UpdateSerializer

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='POST', request_body=SignUpSerializers)
@api_view(['POST'])
def register(request):
  data = request.data
  serializer = SignUpSerializers(data=data)
  if serializer.is_valid():
    if not CustomUser.objects.filter(email=data['email']).exists():
      user = CustomUser.objects.create(
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        username = data['username'],
        password = make_password(data['password'])
      )
      return Response({
        'details':"User registered sucessfully."
      }, status.HTTP_201_CREATED)
    return Response({
      'error':"Email already exists."
    }, status.HTTP_400_BAD_REQUEST)
  return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_users(request):
  users = CustomUser.objects.all().order_by('id')
  serializer = UserSerializer(instance=users, many=True)
  return Response({
    'all users':serializer.data
  }, status.HTTP_200_OK)
  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
  user = request.user
  serializer = UserSerializer(instance=user)
  return Response({
    'current user':serializer.data
  }, status.HTTP_200_OK)

@swagger_auto_schema(method='PUT', request_body=UpdateSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
  user = request.user
  data = request.data

  serializer = UpdateSerializer(user, data=data, partial=True)
  if serializer.is_valid():
    if not serializer.validated_data:
      return Response({
        'error':'No fields provided for update.'
      }, status.HTTP_400_BAD_REQUEST)
    # handle password saperately
    password = data['password']
    if password is not None:
      user.set_password(password)
    # update other fields
    for attr, value in serializer.validated_data.items():
      setattr(user, attr, value)
    user.save()
    return Response({
      'details':'User updated sucessfully!'
    }, status.HTTP_202_ACCEPTED)
  return Response({
    'error':serializer.errors
  }, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
  user = request.user
  user.delete()
  return Response({
    'details':'User removed sucessfully!'
  }, status.HTTP_200_OK)


# add mamiltrap configurations and use it for reseting & updating password.