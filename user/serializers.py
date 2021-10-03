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

class ChronicDSerializer(serializers.Serializer):
    immunodeficiency_disorder = serializers.BooleanField(default=False)
    cardiovascular_disease = serializers.BooleanField(default=False)
    chronic_kidney_disease = serializers.BooleanField(default=False)
    COPD = serializers.BooleanField(default=False)
    asthma = serializers.BooleanField(default=False)
    cancer = serializers.BooleanField(default=False)
    hypertension = serializers.BooleanField(default=False)
    diabetes = serializers.BooleanField(default=False)

class SignupSerializer(serializers.ModelSerializer):
    chronic_diseases = ChronicDSerializer()
    email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', "country","phone_number","gender","age","chronic_diseases")
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id',)
        depth = 2

    def create(self, validated_data):
        password = validated_data.pop("password")
        chronic_diseases = validated_data.pop("chronic_diseases")
        user = User.objects.create_user(
            **validated_data
        )
        user.set_password(password)
        print(chronic_diseases)

        for k in chronic_diseases:
            print(chronic_diseases[k])
            if chronic_diseases[k]:
                chronic_disease = ChronicDisease.objects.filter(name = k).first()
                user.chronic_diseases.add(chronic_disease)
        user.save()
        return user

class UserinfoSerializer(serializers.ModelSerializer):
    
    #email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('id',"avater", 'username','email', "country","gender","age")

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