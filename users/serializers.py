from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',]
        read_only_fields = ['id']

class UserCreateSerializer(UserSerializer):
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password1', 'password2']

    def validate(self, attrs):
        if attrs['password1']!=attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароль не совпадает'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class GetConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Не верные данные')
        attrs['user'] = user
        return attrs
    
class LoginSerializer(serializers.Serializer):
    auth_code = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6
        )
    email = serializers.EmailField(
        required=True
        )