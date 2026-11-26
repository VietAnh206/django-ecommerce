from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from products.models import Category, Product

User = get_user_model()


class EcommerceFlowTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "pass12345")
        self.user = User.objects.create_user("bob", "b@b.com", "pass12345")
        cat = Category.objects.create(name="Veg", slug="veg")
        self.product = Product.objects.create(
            name="Carrot", unit="kg", price=100, discount=10, amount=50, category_id=cat
        )

    def test_public_can_read_products(self):
        r = self.client.get("/api/v1/product/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data["data"]), 1)

    def test_anonymous_cannot_create_product(self):
        r = self.client.post("/api/v1/product/", {}, format="json")
        self.assertIn(r.status_code, (401, 403))

    def test_order_total_is_auto_updated(self):
        self.client.force_authenticate(self.user)
        r = self.client.post("/api/v1/orders/", {
            "receiver_name": "Bob", "receiver_phone": "0123", "receiver_address": "Da Nang",
        }, format="json")
        self.assertEqual(r.status_code, 201)
        oid = r.data["data"]["id"]
        r = self.client.post(f"/api/v1/orders/{oid}/detail/", {
            "product_id": self.product.id, "amount": 2,
        }, format="json")
        self.assertEqual(r.status_code, 201)
        r = self.client.get(f"/api/v1/orders/{oid}/")
        self.assertEqual(r.data["data"]["total"], 180.0)  

    def test_user_cannot_see_other_orders(self):
        self.client.force_authenticate(self.user)
        self.client.post("/api/v1/orders/", {
            "receiver_name": "Bob", "receiver_phone": "0123", "receiver_address": "X",
        }, format="json")
        other = User.objects.create_user("eve", "e@e.com", "pass12345")
        self.client.force_authenticate(other)
        self.assertEqual(len(self.client.get("/api/v1/orders/").data["data"]), 0)
