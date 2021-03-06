from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r("subscriptions:new"))

    def test_get(self):
        """ GET /inscricao/ must return status code 200 """
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """ GET /inscricao/ must use subscriptions/subscription_form.html """
        self.assertTemplateUsed(
            self.response, "subscriptions/subscription_form.html"
        )

    def test_html(self):
        """ HTML must contain input tags """
        tags = (
            ("<form", 1),
            ("<input", 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """ HTML must contain csrf """
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ Context must have subscription form """
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewValidPost(TestCase):
    def setUp(self):
        data = dict(
            name="Victor Vitória",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86998059089",
        )
        self.response = self.client.post(r("subscriptions:new"), data)
        self.email = mail.outbox[0]

    def test_post(self):
        """ Valid POST should redirect to /incricao/1/ """
        self.assertRedirects(self.response, r("subscriptions:detail", 1), 302)

    def test_send_subscribe_email(self):
        """ Valid POST shoul send an email """
        self.assertEqual(len(mail.outbox), 1)

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post(r("subscriptions:new"), {})

    def test_post(self):
        """ Invalid POST should not redirect """
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """
        Invalid POST /inscricao/ must use subscriptions/subscription_form.html 
        with form errors
        """
        self.assertTemplateUsed(
            self.response, "subscriptions/subscription_form.html"
        )

    def test_has_form(self):
        """ Invalid POST /inscricao/ must use SubscriptionForm """
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        """ Invalid POST /inscricao/ must use SubscriptionForm with errors """
        form = self.response.context["form"]
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
