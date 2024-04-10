import unittest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from..views import *
from..models import *


class HacerSuperusuarioViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_hacer_superusuario_view(self):
        request = self.factory.get('/')
        request.user = self.user  # Simulate an authenticated user

        response = hacer_superusuario(request, self.user.id)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_superuser)


