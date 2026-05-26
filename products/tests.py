import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_create_url = reverse("product-list-create")

    def test_create_product_success(self):
        payload = {
            "name": "Wireless Mouse",
            "desc": "A quiet click 2.4G wireless mouse.",
            "price": 19.99
        }
        response = self.client.post(
            self.list_create_url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], "Wireless Mouse")
        self.assertEqual(data["desc"], "A quiet click 2.4G wireless mouse.")
        self.assertEqual(data["price"], "19.99")
        self.assertTrue(Product.objects.filter(id=data["id"]).exists())

    def test_create_product_invalid_price(self):
        payload = {
            "name": "Invalid Mouse",
            "price": "not-a-number"
        }
        response = self.client.post(
            self.list_create_url,
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_list_products(self):
        Product.objects.create(name="P1", price=10.00)
        Product.objects.create(name="P2", price=20.00)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
