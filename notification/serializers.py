

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import action



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","username"]



        
class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, User):
            serializer = UserSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    recipient = UserSerializer(User, read_only=True)
    actor = GenericNotificationRelatedField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    action = GenericNotificationRelatedField(read_only=True)
    verb = serializers.CharField()
    level = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField(read_only=True)
    unread = serializers.BooleanField()
    public = serializers.BooleanField()
    deleted = serializers.BooleanField()
    emailed = serializers.BooleanField()
