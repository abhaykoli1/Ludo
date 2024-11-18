from mongoengine import Document, StringField, FloatField, BooleanField
from pydantic import BaseModel

class LoginTable(Document):
    identifyer = StringField(required=True)
    name = StringField(required=True)
    cre_date = StringField(required=True)

class LoginBody(BaseModel):
    identifyer : str
    name : str
    cre_date : str