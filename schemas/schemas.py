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


from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Service(BaseModel):
    """Модель услуги в чеке"""
    name: str
    quantity: int
    serviceNumber: int
    amount: float


class CancellationInfo(BaseModel):
    """Информация об отмене чека"""
    operationTime: str
    registerTime: str
    taxPeriodId: int
    comment: str


class Receipt(BaseModel):
    """Модель чека от сервиса Мой налог"""
    approvedReceiptUuid: str
    name: str
    services: List[Service]
    operationTime: str
    requestTime: str
    registerTime: str
    taxPeriodId: int
    paymentType: str
    incomeType: str
    partnerCode: Optional[str] = None
    totalAmount: float
    cancellationInfo: Optional[CancellationInfo] = None
    sourceDeviceId: str | None
    clientInn: Optional[str] = None
    clientDisplayName: Optional[str] = None
    partnerDisplayName: Optional[str] = None
    partnerLogo: Optional[str] = None
    partnerInn: Optional[str] = None
    inn: str
    profession: str = ""
    description: List = Field(default_factory=list)
    invoiceId: Optional[str] = None

class Incomes(BaseModel):
    """Модель доходов"""
    content : List[Receipt]
    hasMore : bool
    currentOffset : int
    currentLimit : int

class UserProfile(BaseModel):
    lastName: Optional[str] = None
    id: int
    displayName: str
    middleName: Optional[str] = None
    email: Optional[str] = None
    phone: str
    inn: str
    snils: str
    avatarExists: bool
    initialRegistrationDate: datetime
    registrationDate: datetime
    firstReceiptRegisterTime: datetime
    firstReceiptCancelTime: datetime
    hideCancelledReceipt: bool
    registerAvailable: Optional[bool] = None
    status: str
    restrictedMode: bool
    pfrUrl: str
    login: str