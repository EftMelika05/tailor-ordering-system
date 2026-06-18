from rest_framework import serializers

from products.models import (
    CustomTshirt,
    CustomHoodie,
    CustomPants
)

from .fabric_serializer import FabricSerializer
from .sticker_serializer import StickerSerializer
from .color_serializer import CustomProductColorSerializer

class CustomTshirtSerializer(serializers.ModelSerializer):

    fabrics = FabricSerializer(
        many=True,
        read_only=True
    )

    stickers = StickerSerializer(
        many=True,
        read_only=True
    )

    custom_colors = serializers.SerializerMethodField()

    class Meta:
        model = CustomTshirt

        fields = "__all__"

    def get_custom_colors(self, obj):

        colors = obj.product.custom_colors.all()

        return CustomProductColorSerializer(
            colors,
            many=True
        ).data

class CustomHoodieSerializer(serializers.ModelSerializer):

    fabrics = FabricSerializer(
        many=True,
        read_only=True
    )

    stickers = StickerSerializer(
        many=True,
        read_only=True
    )

    custom_colors = serializers.SerializerMethodField()

    class Meta:
        model = CustomHoodie

        fields = "__all__"

    def get_custom_colors(self, obj):

        colors = obj.product.custom_colors.all()

        return CustomProductColorSerializer(
            colors,
            many=True
        ).data

class CustomPantsSerializer(serializers.ModelSerializer):

    fabrics = FabricSerializer(
        many=True,
        read_only=True
    )

    stickers = StickerSerializer(
        many=True,
        read_only=True
    )

    custom_colors = serializers.SerializerMethodField()

    class Meta:
        model = CustomPants

        fields = "__all__"

    def get_custom_colors(self, obj):

        colors = obj.product.custom_colors.all()

        return CustomProductColorSerializer(
            colors,
            many=True
        ).data