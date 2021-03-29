from django.test import TestCase
from django.shortcuts import resolve_url as r


class HomeTest(TestCase):
    fixtures = ["keynotes.json"]

    def setUp(self):
        self.response = self.client.get(r("home"))

    def test_get(self):
        """ GET / must return status code 200 """
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """ GET / must use index.html """
        self.assertTemplateUsed(self.response, "core/index.html")

    def test_subscription_link(self):
        expected = 'href="{}"'.format(r("subscriptions:new"))

        self.assertContains(self.response, expected)

    def test_speakers(self):
        contents = [
            f'href="{r("speaker_detail", slug="alan-turing")}"',
            "Alan Turing",
            "http://hbn.link/turing-pic",
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)
    
    def test_speakers_link(self):
        expected = f'href="{r("home")}#speakers'

        self.assertContains(self.response, expected)
