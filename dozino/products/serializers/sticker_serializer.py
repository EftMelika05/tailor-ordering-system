from rest_framework import serializers

from products.models import Sticker


class StickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sticker

        fields = "__all__"