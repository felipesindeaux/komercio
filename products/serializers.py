from rest_framework import serializers
from users.serializers import DetailUserSerializer

from products.models import Product


class ListProductSerializer(serializers.ModelSerializer):

    class Meta():
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller_id"]

class CreateProductSerializer(serializers.ModelSerializer):

    seller = DetailUserSerializer(read_only=True)

    class Meta():
        model = Product
        fields = ['id', 'description', 'price', 'quantity', 'is_active', 'seller']
        extra_kwargs = {"quantity": {"min_value": 0}}

