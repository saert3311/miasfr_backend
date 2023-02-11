from dotenv import load_dotenv, find_dotenv
import os
import requests

load_dotenv(find_dotenv())

class SMS:
    """
    Class to manage messages to transmit sms

    Attributes
    ----------
    message: str
        Message to be sent

    phone: str
        Phone number to send message

    Methods
    -------
    send():
        Send the message
    """
    SERVICE_ENDPOINT = 'https://api.transmitsms.com/'
    SEND_URL = 'send-sms.json'
    GET_NUMBERS = 'get-numbers.json'
    GET_BALANCE = 'get-balance.json'

    def __init__(self, message: str = '', phone: str = '') -> None:
        self.message = message
        self.phone = phone
        self.auth = (os.getenv('SMS_USER'), os.getenv('SMS_PWD'))

    @classmethod
    def get_balance(cls) -> str:
        """
        Static method to get the current balance of the service, mostly to check if we can send the message
        :return:
        An str of the balance
        """
        auth = (os.getenv('SMS_USER'), os.getenv('SMS_PWD'))
        url = cls.SERVICE_ENDPOINT+cls.GET_BALANCE
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            response_dict = response.json()
            return response_dict['balance']

    def get_numbers(self) -> list:
        """
        Method to get the active numbers
        :return:
        An array of the numbers
        """
        auth = (os.getenv('SMS_USER'), os.getenv('SMS_PWD'))
        url = SMS.SERVICE_ENDPOINT+SMS.GET_NUMBERS
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            response_dict = response.json()
            return response_dict['numbers']

    def send(self) -> dict:
        if len(self.message) > 160:
            raise ValueError('Message is longer than 160 characters')
        url = SMS.SERVICE_ENDPOINT+SMS.SEND_URL
        from_number = self.get_numbers()[0]['number']
        payload = {
            'message':self.message,
            'to':self.phone,
            'from':from_number
        }
        response = requests.post(url, auth=self.auth, data=payload)
        response.raise_for_status()
        response_dict = response.json()
        return response_dict