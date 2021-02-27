from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        subscription = Subscription.objects.create(
            name="Victor Vitória",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86998059089",
        )
        self.response = self.client.get(f"/inscricao/{subscription.pk}/")

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, "subscriptions/subscription_detail.html"
        )
    
    def test_context(self):
        subscription = self.response.context["subscription"]
        self.assertIsInstance(subscription, Subscription)
    
    def test_html(self):
        contents = (
            "Victor Vitória",
            "12345678901",
            "victor@mail.com",
            "86998059089",
        )

        with self.subTest():
            for expected in contents:
                self.assertContains(self.response, expected)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        response = self.client.get(f"/inscricao/99/")
        self.assertEqual(404, response.status_code)
