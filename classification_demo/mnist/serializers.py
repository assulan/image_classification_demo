from rest_framework import serializers
from mnist.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image