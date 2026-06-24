from rest_framework import serializers

from products.models import ReadyProduct
from products.models import ReadyProductVariant

from .color_serializer import ColorSerializer


class ReadyProductVariantSerializer(serializers.ModelSerializer):

    color = ColorSerializer(read_only=True)

    class Meta:
        model = ReadyProductVariant

        fields = "__all__"


class ReadyProductSerializer(serializers.ModelSerializer):

    variants = ReadyProductVariantSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ReadyProduct

        fields = "__all__"