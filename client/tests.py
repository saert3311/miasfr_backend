from django.test import TestCase
from .sms import SMS

class SmsSendTestCase(TestCase):
    def setUp(self) -> None:
        self.my_sms = SMS('Hello World', '+16692574658')

    def testCreation(self) -> None:
        self.assertTrue(isinstance(self.my_sms, SMS))

    def testSending(self) -> None:
        result = self.my_sms.send()
        self.assertEqual(result['error']['code'], 'SUCCESS')
