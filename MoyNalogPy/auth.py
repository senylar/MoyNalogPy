import random
import string
import requests
from requests.exceptions import RequestException

from MoyNalogPy.schemas import ProfileStorage

class Authentication:

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.device_id = self.generate_device_id()
        self.challenge_token = None


    def generate_device_id(self, length=16):
        """
        Генерирует случайный идентификатор устройства заданной длины

        Args:
            length: Длина идентификатора (по умолчанию 16 символов)

        Returns:
            Случайная строка из букв и цифр
        """
        # Создаем набор символов: буквы (a-z, A-Z) и цифры (0-9)
        characters = string.ascii_letters + string.digits

        # Генерируем случайную строку
        random_string = ''.join(random.choice(characters) for _ in range(length))

        return random_string

    def init_auth(self):
        """
        Инициализирует процесс аутентификации, отправляя запрос на получение кода подтверждения.
        """
        req = {
            "phone": self.phone_number,
            "requireTpToBeActive": True
        }
        try:
            data_start = requests.post('https://lknpd.nalog.ru/api/v2/auth/challenge/sms/start', json=req)
        except RequestException as e:
            raise Exception(f"Network error during authentication initiation: {e}")

        if data_start.status_code == 200:
            challenge_token = data_start.json()['challengeToken']
            self.challenge_token = challenge_token
        else:
            raise Exception(f"Failed to start authentication process. Status: {data_start.status_code}, Response: {data_start.text}")

    def authenticate(self, code):
        """
        Выполняет аутентификацию, отправляя код подтверждения и получая токены.

        Args:
            code: Код подтверждения, полученный по SMS.
        """
        req = {
            "phone": self.phone_number,
            "code": code,
            "challengeToken": self.challenge_token,
            "deviceInfo": {
                "sourceDeviceId": self.device_id,
                "sourceType": "WEB",
                "appVersion": "1.0.0",
                "metaDetails": {
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15"
                }
            }
        }

        data = requests.post('https://lknpd.nalog.ru/api/v1/auth/challenge/sms/verify', json=req)

        if data.status_code == 200:
            data = data.json()
            data.update({"sourceDeviceId": self.device_id})
            profile_storage = ProfileStorage(**data)
            return profile_storage
        else:
            raise Exception(f"Authentication failed. Status: {data.status_code}, Response: {data.text}")
