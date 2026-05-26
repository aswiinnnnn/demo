import json
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from .models import CartItem


class CartItemAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_create_url = reverse("cart-list-create")
        self.product = Product.objects.create(name="Mouse", price=15.00)

    def test_add_to_cart_success(self):
        payload = {
            "product_id": self.product.id,
            "quantity": 2
        }
        response = self.client.post(
            self.list_create_url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["product"]["name"], "Mouse")
        self.assertEqual(data["quantity"], 2)

    def test_add_to_cart_increments_quantity(self):
        # First add
        CartItem.objects.create(product=self.product, quantity=2)
        # Second add
        payload = {
            "product_id": self.product.id,
            "quantity": 3
        }
        response = self.client.post(
            self.list_create_url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        # Check database
        item = CartItem.objects.get(product=self.product)
        self.assertEqual(item.quantity, 5)

    def test_list_cart_items(self):
        CartItem.objects.create(product=self.product, quantity=1)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_delete_cart_item(self):
        item = CartItem.objects.create(product=self.product, quantity=1)
        detail_url = reverse("cart-detail", kwargs={"pk": item.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())
