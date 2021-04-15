from django.test import TestCase
from django.core.exceptions import ValidationError

from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name="Victor",
            slug="victor",
            photo="http://hbn.link/turing-pic",
        )

    def test_email(self):
        Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value="victor@mail.com",
        )

        self.assertTrue(Contact.objects.exists())
    
    def test_phone(self):
        Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.PHONE,
            value="00-00000000",
        )

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind="A",
            value="B",
        )

        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value="victor@mail.com",
        )

        self.assertEqual("victor@mail.com", str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name="Victor",
            slug="victor",
            photo="http://hbn.link/turing-pic",
        )
        s.contact_set.create(kind=Contact.EMAIL, value="victor@mail.com")
        s.contact_set.create(kind=Contact.PHONE, value="00-00000000")
    
    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ["victor@mail.com"]

        self.assertQuerysetEqual(qs, expected, lambda c: c.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ["00-00000000"]

        self.assertQuerysetEqual(qs, expected, lambda c: c.value)