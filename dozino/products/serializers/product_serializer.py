from rest_framework import serializers

from products.models import Product
from products.models import ProductImage

from .category_serializer import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product

        fields = "__all__"