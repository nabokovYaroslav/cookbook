from rest_framework import serializers
from users.models import User
from recipes.fields import TumbnailImageField


class RegisterUserSerializer(serializers.ModelSerializer):
  def create(self, data):
    email = data['email']
    user_name = data['user_name']
    password = data['password']
    user = self.Meta.model.objects.create_user(email, user_name, password)
    return user
  
  class Meta:
    model = User
    fields = ('email', 'user_name', 'password')
    extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
  image = TumbnailImageField(required=False)
  user = serializers.IntegerField(read_only=True, source='id')
  class Meta:
    model = User
    fields = ('user', 'email', 'user_name', 'image')
    lookup_field = "user_name"

class UserBasicSerializer(serializers.ModelSerializer):
  image = TumbnailImageField(required=False)
  user = serializers.IntegerField(read_only=True, source='id')
  class Meta:
    model = User
    fields = ('user', 'user_name', 'image')
    lookup_field = "user_name"