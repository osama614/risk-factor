from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.utils import timezone
from .models import ChronicDisease
from django.utils.text import gettext_lazy as _

User = get_user_model()

class ChronicDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicDisease
        fields = "__all__"
        read_only_fields = ('id',)

class SignupSerializer(serializers.ModelSerializer):
    chronic_disease = ChronicDSerializer()
    email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', "country","phone_number","gender","age","chronic_disease")
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id',)
        depth = 2

    def create(self, validated_data):
        password = validated_data.pop("password")
        chronic_disease = validated_data.pop("chronic_disease")
        user = User.objects.create_user(
            **validated_data
        )
        user.set_password(password)
        P = ChronicDisease.objects.create(owner=user, **chronic_disease)
        user.save()
        return user


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')