from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from rest_framework import serializers

from apps.user.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            "last_name",
            'password'
        )
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'first_name': {'required': True}
        }

    @staticmethod
    def validate_email(email):
        if User.objects.filter(**{'{}__iexact'.format(User.USERNAME_FIELD): email}).exists():
            raise ValidationError('User with this {} already exists'.format(User.USERNAME_FIELD))
        return email

    @staticmethod
    def validate_password(password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password


    def create(self, validated_data):
        return User.objects.create_user(
                    validated_data.pop('email'),
                    validated_data.pop('password'),
                    **validated_data
                )