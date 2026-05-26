from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source="product"
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "created_at", "updated_at"]

    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data.get("quantity", 1)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item
