import json
import os

from pydantic import BaseModel, Field


class Service(BaseModel):
    name : str
    amount : float
    quantity : int


class Client(BaseModel):
    contactPhone : str = Field(default=None)
    displayName : str = Field(default=None)
    inn : str = Field(default=None)
    incomeType : str = Field(default="FROM_INDIVIDUAL")


class ProfileStorage(BaseModel):

    refreshToken : str = Field(required=True)
    token : str = Field(required=True)
    sourceDeviceId : str = Field(required=True)
    profile : dict

    @classmethod
    def get(cls):
        """
        Метод для получения экземпляра класса DataStorage из файла profile.json
        :return: экземпляр класса DataStorage
        """

        profile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profile.json')
        with open(profile_path, 'r') as f:
            data = json.loads(f.read())
            return cls.model_validate(data)

    def save(self):
        """
        Метод для сохранения экземпляра класса DataStorage в файл profile.json
        :return: None
        """
        profile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'profile.json')
        with open(profile_path, 'w') as f:
            try:
                # Пробуем использовать model_dump() (Pydantic v2)
                f.write(json.dumps(self.model_dump()))
            except AttributeError:
                # Запасной вариант для Pydantic v1
                f.write(json.dumps(self.dict()))


# d = ProfileStorage.get()
# d.profile['middleName'] = 'hui'
# print(d)
#
# d.save()


    