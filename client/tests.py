from django.test import TestCase
from client.models import Client
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ClientCreationTestCase(TestCase):
    def setUp(self):

        Client.objects.create(
            first_name='Juan',
            last_name='Prueba',
            email='prueba@prueba.com',
            alternative_email='prueba2@email.com',
            main_phone='+17866094429',
            alternative_phone='17866094430',
            user_id=1
        )

    def test_constraints(self):
        Client.objects.create(
            first_name='Juan2',
            last_name='Prueba2',
            email='prueba@prueba.com',
            main_phone='+17866094429',
            user_id=1
        )

