from django.test import TestCase
from django.core import mail

from .forms import SubscriptionForm


class SubscribeTest(TestCase):
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
        self.assertContains(self.response, "<form")
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """ HTML must contain csrf """
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ Context must have subscription form """
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = self.response.context["form"]
        self.assertSequenceEqual(
            ["name", "cpf", "email", "phone"], list(form.fields)
        )


class SubscribePostTest(TestCase):
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

    def test_subscription_email_subject(self):
        """ Email sended should contain a specific subject """
        expected = "Confirmação de incrição"

        self.assertEqual(expected, self.email.subject)

    def test_subscription_email_from(self):
        """ Email should be to sent by a specific email """
        expected = "victor@mail.com"

        self.assertEqual(expected, self.email.from_email)

    def test_subscription_email_to(self):
        """ Email should be able to sent for those above contacts """
        expected = ["victor@mail.com", "fulano@mail.com"]

        self.assertEqual(expected, self.email.to)

    def test_subscription_email_body(self):
        """ Email should contain the informations submited on form """
        self.assertIn("Victor Vitória", self.email.body)
        self.assertIn("12345678901", self.email.body)
        self.assertIn("victor@mail.com", self.email.body)
        self.assertIn("86998059089", self.email.body)


class SubscribeInvalidPost(TestCase):
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


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(
            name="Victor Vitória",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86998059089",
        )
        response = self.client.post("/inscricao/", data, follow=True)

        self.assertContains(response, "Inscrição realizada com sucesso!")