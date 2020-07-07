from rest_framework import serializers
from .models import Bark
from django.conf import settings

MAX_BARK_LENGTH = settings.MAX_BARK_LENGTH

class BarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bark
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_BARK_LENGTH:
            raise serializers.ValidationError("This bark is too long. Please limit barks to 240 characters")
        return value