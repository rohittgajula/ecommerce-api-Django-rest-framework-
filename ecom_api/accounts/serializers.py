from rest_framework import serializers
from .models import CustomUser


class SignUpSerializers(serializers.ModelSerializer):
  
  class Meta:
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'password', 'username']

    # def create(self, validated_data):
    #   user = CustomUser.objects.create(
    #     first_name = validated_data['first_name'],
    #     last_name = validated_data['last_name'],
    #     email = validated_data['email'],
    #     username = validated_data['username']
    #   )
    #   user.set_password(validated_data['password'])
    #   user.save()
    #   return user
    
class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_staff', 'is_superuser', 'is_active']

class UpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'password', 'username']

    extra_kwargs = {
      'first_name':{'required':False},
      'last_name':{'required':False},
      'email':{'required':False},
      'username':{'required':False},
      'password':{'required':False, 'write_only':True}
    }

    # i want the password to be stored in hashed formet   ***************************
    def update(self, instance, validated_data):
      for attr, value in validated_data.items():
          if value in [None, '']:  # Check for empty values (None or empty string)
              continue  # Skip updating this attribute if the value is empty
          
          if attr == 'password':
              instance.set_password(value)
          else:
              setattr(instance, attr, value)
      
      instance.save()
      return instance
    
