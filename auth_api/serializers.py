from rest_framework import serializers
from django.forms import ValidationError
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator, MaxLengthValidator

from api.utils.exceptions import BadRequestException
from apps.user.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "blank": "ایمیل الزامی است.",
            "required": "ایمیل الزامی است.",
            "invalid": "ایمیل وارد شده نادرست میباشد",
        },
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            "required": "گذرواژه الزامی است.",
            "blank": "گذرواژه الزامی است.",
        },
    )

    def validate(self, attrs):
        user = authenticate(username=attrs["email"], password=attrs["password"])

        if not user:
            raise BadRequestException(
                detail="ایمیل یا رمز عبور وارد شده اشتباه می‌باشد",
                code="authentication_failed",
            )

        if not user.is_active:
            raise BadRequestException(
                detail="حساب کاربری شما مسدود شده است",
                code="account_disabled",
            )

        return {"user": user}


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="حساب کاربری با این ایمیل از قبل وجود دارد",
            )
        ],
        error_messages={
            "required": "ایمیل الزامی است.",
            "blank": "ایمیل الزامی است.",
            "invalid": "ایمیل وارد شده نادرست میباشد",
        },
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "required": "گذرواژه الزامی است.",
            "blank": "گذرواژه الزامی است.",
        },
    )
    first_name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(2, "نام باید حداقل ۲ حرف باشد."),
            MaxLengthValidator(30, "نام نباید بیش از ۳۰ حرف باشد."),
        ],
        error_messages={
            "required": "نام الزامی است.",
            "blank": "نام الزامی است.",
        },
    )
    last_name = serializers.CharField(
        required=False,
        validators=[
            MinLengthValidator(2, "نام خانوادگی باید حداقل ۲ حرف باشد."),
            MaxLengthValidator(30, "نام خانوادگی نباید بیش از ۳۰ حرف باشد."),
        ],
        error_messages={
            "blank": "نام خانوادگی الزامی است.",
        },
    )

    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return list(obj.groups.values_list("name", flat=True))

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "roles")
        extra_kwargs = {
            "password": {"required": True, "write_only": True},
            "first_name": {"required": True},
            "id": {"read_only": True},
            "roles": {"read_only": True},
        }

    @staticmethod
    def validate_email(email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "حساب کاربری با این ایمیل از قبل وجود دارد"
            )
        return email

    @staticmethod
    def validate_password(password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(
                "رمز عبور شما باید حداقل ۸ حرف و شامل عدد باشد"
            )
        return password

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.pop("email"),
            validated_data.pop("password"),
            **validated_data
        )
