from django.test import TestCase
from django.core import mail


class SubscribeValidPostTest(TestCase):
    def setUp(self):
        data = dict(
            name="Victor Vitória",
            cpf="12345678901",
            email="victor@mail.com",
            phone="86998059089",
        )
        self.client.post("/inscricao/", data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """ Email sended should contain a specific subject """
        expected = "Confirmação de inscrição"

        self.assertEqual(self.email.subject, expected)

    def test_subscription_email_from(self):
        """ Email should be to sent by a specific email """
        expected = "contato@eventex.com.br"

        self.assertEqual(self.email.from_email, expected)

    def test_subscription_email_to(self):
        """ Email should be able to sent for those above contacts """
        expected = ["contato@eventex.com.br", "victor@mail.com"]

        self.assertEqual(self.email.to, expected)

    def test_subscription_email_body(self):
        """ Email should contain the informations submited on form """
        contents = (
            "Victor Vitória",
            "12345678901",
            "victor@mail.com",
            "86998059089",
        )

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
