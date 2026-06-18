# serializers.py

from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'images',
            'uploaded_images',
        ]

    
    
    def create(self, validated_data):

        uploaded_images = validated_data.pop('uploaded_images', [])

        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(
                product=product,
                image=image
            )

        return product
    
    
    
    # serializers.py

from rest_framework import serializers
from .models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'image',
        ]