import requests

from models.schemas import ProfileStorage


def refresh_token():
    url = "https://lknpd.nalog.ru/api/v1/auth/token"

    data = ProfileStorage.get()

    if data.refreshToken:
        req = {
            "refreshToken": data.refreshToken,
            "deviceInfo": {
                "sourceDeviceId": data.sourceDeviceId,
                "sourceType": "WEB",
                "appVersion": "1.0.0",
                "metaDetails": {
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15"
                }
            }
        }

        response = requests.post(url, json=req)
        print(response)
        if response.status_code == 200:
            response = response.json()
            data.refreshToken = response['refreshToken']
            data.token = response['token']
            data.save()
            print("Token refreshed successfully.")
        else:
            raise Exception("Что то пошло не так.\nДля устранения проблемы попробуйте удалить файл profile.json и заново пройти аутентификацию.\nДля этого запустите команду 'python auth.py'")


class CustomRequests:

    def chek(self, response):
        if response.json().get('code') == 'authentication.failed.expired.token':
            print("Token expired. Refreshing...")
            refresh_token()
            return False
        return True

    def post(self, url, **kwargs):
        print(f"POST request to {url} with data: {kwargs}")

        response = requests.post(url, **kwargs)

        if not self.chek(response):
            # Если токен истек, повторяем запрос
            response = requests.post(url, **kwargs)

        return response

    def get(self, url, **kwargs):
        print(f"GET request to {url} with data: {kwargs}")

        response = requests.get(url, **kwargs)

        if not self.chek(response):
            # Если токен истек, повторяем запрос
            response = requests.get(url, **kwargs)

        return response