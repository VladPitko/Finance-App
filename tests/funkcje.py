
from unittest import TestCase

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


class FinanceViewsTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

