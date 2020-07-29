from rest_framework import serializers
from django.conf import settings
from .models import Bark
from profiles.serializers import PublicProfileSerializer

MAX_BARK_LENGTH = settings.MAX_BARK_LENGTH
BARK_ACTION_OPTIONS = settings.BARK_ACTION_OPTIONS

class BarkActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank = True, required = False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in BARK_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for barks")
        return value

class BarkCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source = 'user.profile', read_only = True)
    likes = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Bark
        fields = ['user', 'id', 'content', 'likes', 'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_BARK_LENGTH:
            raise serializers.ValidationError("This bark is too long. Please limit barks to 240 characters")
        return value

class BarkSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source = 'user.profile', read_only = True)
    likes = serializers.SerializerMethodField(read_only = True)
    parent = BarkCreateSerializer(read_only = True)
    class Meta:
        model = Bark
        fields = ['user', 'id', 'content', 'likes', 'is_rebark', 'parent', 'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()