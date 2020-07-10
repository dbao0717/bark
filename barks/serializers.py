from rest_framework import serializers
from .models import Bark
from django.conf import settings

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
    likes = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Bark
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_BARK_LENGTH:
            raise serializers.ValidationError("This bark is too long. Please limit barks to 240 characters")
        return value

class BarkSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    parent = BarkCreateSerializer(read_only = True)
    class Meta:
        model = Bark
        fields = ['id', 'content', 'likes', 'is_rebark', 'parent']

    def get_likes(self, obj):
        return obj.likes.count()