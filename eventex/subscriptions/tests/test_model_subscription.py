from datetime import datetime

from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name="Victor Fontenele",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86-99999999",
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual("Victor Fontenele", str(self.obj))

    def test_paid_default_to_false(self):
        """ By default paid must be False """
        self.assertEqual(False, self.obj.paid)
