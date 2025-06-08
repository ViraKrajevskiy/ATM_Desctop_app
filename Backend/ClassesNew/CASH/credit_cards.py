from peewee import *
import datetime

from Backend.data_base.core import BaseModel


class PhoneNumber(BaseModel):
    id = AutoField()
    balance = IntegerField()
    phone_number = CharField(max_length=12)

class CreditCards(BaseModel):
    card_id = AutoField()

    card_number = IntegerField()
    balance = IntegerField()
    security_code = IntegerField()
    special_identificator = CharField()

    bank_name = CharField()
    card_type = CharField(max_length=50)

    card_give_date = DateField(default=datetime.datetime.now)
    card_end_date = DateField()
    phone_field = ManyToManyField(PhoneNumber, backref='phones')

CreditCardsPhoneThrough = CreditCards.phone_field.get_through_model()
