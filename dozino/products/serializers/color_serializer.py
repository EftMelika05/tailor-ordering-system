from rest_framework import serializers

from products.models import Color
from products.models import CustomProductColor


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color

        fields = "__all__"


class CustomProductColorSerializer(serializers.ModelSerializer):

    color = ColorSerializer(read_only=True)

    class Meta:
        model = CustomProductColor

        fields = "__all__"