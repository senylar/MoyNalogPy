import functools
import json
import os
import string
from datetime import timezone, timedelta, datetime
from http.client import HTTPResponse, HTTPException
from random import random

import requests
from models.schemas import Service, Client, ProfileStorage
from CustomRequests import refresh_token


def token_refresh_decorator(func):
    @functools.wraps(func)
    def wrapper(self, **kwargs):
        print(f"{func.__name__.upper()} request to with data: {kwargs}")

        response = func(self, **kwargs)
        print(response)

        try:
            if response.get('code') == 'authentication.failed.expired.token':
                print("Token expired. Refreshing...")
                refresh_token()

                # Обновляем Authorization в заголовках, если он там есть
                if 'headers' in kwargs and 'Authorization' in kwargs['headers']:
                    profile = ProfileStorage.get()
                    kwargs['headers']['Authorization'] = f"Bearer {profile.token}"

                # Повторяем запрос с обновленным токеном
                response = func(self, **kwargs)
        except (ValueError, KeyError):
            pass  # Если ответ не в формате JSON или нет нужного ключа

        return response

    return wrapper

#TODO временные пояса
class MyTax:

    def __init__(self, timezone_shift = None):

        self.timezone_shift = timezone_shift if timezone_shift else 3
        self.profile = ProfileStorage.get()
        self.auth = {"Authorization" : "Bearer " + self.profile.token}


    def __get_curtime(self):
        tz = timezone(timedelta(hours=self.timezone_shift))
        current_time = datetime.now(tz)
        formatted_time_1 = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        return formatted_time_1



    @token_refresh_decorator
    def create_invoice(self, operationTime,
                       svs : list[Service] | Service,
                       client : Client = Client,
                       paymentType : str = "CASH",
                       ignoreMaxTotalIncomeRestriction : bool = False):

        url = "https://lknpd.nalog.ru/api/v1/income"

        services = [el.model_dump() for el in svs] if len(svs) > 1 else svs.model_dump()
        totalamount = sum([el.amount * el.quantity for el in svs]) if len(svs) > 1 else svs.amount * svs.quantity

        body = {
            "operationTime": operationTime,
            "requestTime": self.__get_curtime(),
            "services": services,
            "totalAmount": totalamount,
            "client": client.model_dump(),
            "paymentType": paymentType,
            "ignoreMaxTotalIncomeRestriction": ignoreMaxTotalIncomeRestriction
        }

        try:
            response = requests.post(url, headers=self.auth, json=body)
            return response.json()

        except HTTPException as e:
            print(f"HTTP error: {e}")
            return None

    @token_refresh_decorator
    def get_profile(self):

        url = "https://lknpd.nalog.ru/api/v1/user"

        response = requests.get(url, headers=self.auth)

        return response.json()

# print(check_auth())
# authenticate("79258678007")

api = MyTax()
api.get_profile()