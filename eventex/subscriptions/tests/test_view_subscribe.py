from django.test import TestCase
from django.core import mail

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGetTest(TestCase):
    def setUp(self):
        self.response = self.client.get("/inscricao/")

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


class SubscribeValidPostTest(TestCase):
    def setUp(self):
        data = dict(
            name="Victor Vitória",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86998059089",
        )
        self.response = self.client.post("/inscricao/", data)
        self.email = mail.outbox[0]

    def test_post(self):
        """ Valid POST should redirect to /incricao/ """
        self.assertRedirects(self.response, "/inscricao/", 302)

    def test_send_subscribe_email(self):
        """ Valid POST shoul send an email """
        self.assertEqual(len(mail.outbox), 1)


class SubscribeInvalidPostTest(TestCase):
    def setUp(self):
        self.response = self.client.post("/inscricao/", {})

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


class SubscribeSuccessMessageTest(TestCase):
    def test_message(self):
        data = dict(
            name="Victor Vitória",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86998059089",
        )
        response = self.client.post("/inscricao/", data, follow=True)

        self.assertContains(response, "Inscrição realizada com sucesso!")