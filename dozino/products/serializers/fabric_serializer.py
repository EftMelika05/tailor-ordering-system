from rest_framework import serializers

from products.models import Fabric


class FabricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fabric

        fields = "__all__"