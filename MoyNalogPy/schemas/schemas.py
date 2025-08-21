import json
import os

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
class Service(BaseModel):
    """
    Модель услуги.

    Атрибуты:
        name (str): Название услуги.
        amount (float): Сумма услуги.
        quantity (int): Количество услуг.
    """
    name : str
    amount : float
    quantity : int


class Client(BaseModel):
    """
    Модель клиента.

    Атрибуты:
        contactPhone (str, optional): Контактный телефон клиента.
        displayName (str, optional): Отображаемое имя клиента.
    """
    contactPhone : str = Field(default=None)
    displayName : str = Field(default=None)
    inn : str = Field(default=None)
    incomeType : str = Field(default="FROM_INDIVIDUAL")


class ProfileStorage(BaseModel):

    refreshToken : str = Field(required=True)
    token : str = Field(required=True)
    sourceDeviceId : str = Field(required=True)
    profile : dict



class CancellationInfo(BaseModel):
    """
    Информация об отмене чека.


    Атрибуты:
        operationTime (str): Время операции.
        registerTime (str): Время регистрации.
        taxPeriodId (int): Идентификатор налогового периода.
        comment (str): Комментарий.
    """
    operationTime: str
    registerTime: str
    taxPeriodId: int
    comment: str


class Receipt(BaseModel):
    """
    Модель чека от сервиса Мой налог.

    Атрибуты:
        approvedReceiptUuid (str): Уникальный идентификатор утвержденного чека.
        name (str): Название чека.
        services (List[Service]): Список услуг.
        operationTime (str): Время операции.
        requestTime (str): Время запроса.
        registerTime (str): Время регистрации.
        taxPeriodId (int): Идентификатор налогового периода.
        paymentType (str): Тип оплаты.
        incomeType (str): Тип дохода.
        partnerCode (Optional[str]): Код партнера.
        totalAmount (float): Общая сумма.
        cancellationInfo (Optional[CancellationInfo]): Информация об отмене.
        sourceDeviceId (Optional[str]): Идентификатор исходного устройства.
        clientInn (Optional[str]): ИНН клиента.
        clientDisplayName (Optional[str]): Отображаемое имя клиента.
        partnerDisplayName (Optional[str]): Отображаемое имя партнера.
        partnerLogo (Optional[str]): Логотип партнера.
        partnerInn (Optional[str]): ИНН партнера.
        inn (str): ИНН.
        profession (str): Профессия.
        description (List): Описание.
        invoiceId (Optional[str]): Идентификатор счета.
    """
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
    """
    Модель доходов.

    Атрибуты:
        content (List[Receipt]): Список чеков.
        hasMore (bool): Есть ли еще данные.
        currentOffset (int): Текущий сдвиг.
        currentLimit (int): Текущий лимит.
    """
    content : List[Receipt]
    hasMore : bool
    currentOffset : int
    currentLimit : int

class UserProfile(BaseModel):
    """
    Модель профиля пользователя.

    Атрибуты:
        lastName (Optional[str]): Фамилия.
        id (int): Идентификатор.
        displayName (str): Отображаемое имя.
        middleName (Optional[str]): Отчество.
        email (Optional[str]): Электронная почта.
        phone (str): Телефон.
        inn (str): ИНН.
        snils (str): СНИЛС.
        avatarExists (bool): Наличие аватара.
        initialRegistrationDate (datetime): Дата первоначальной регистрации.
        registrationDate (datetime): Дата регистрации.
        firstReceiptRegisterTime (datetime): Время регистрации первого чека.
        firstReceiptCancelTime (datetime): Время отмены первого чека.
        hideCancelledReceipt (bool): Скрывать отмененные чеки.
        registerAvailable (Optional[bool]): Доступна ли регистрация.
        status (str): Статус.
        restrictedMode (bool): Ограниченный режим.
        pfrUrl (str): URL ПФР.
        login (str): Логин.
    """
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