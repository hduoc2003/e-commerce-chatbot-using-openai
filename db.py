import os
from mongoengine import Document, StringField, DictField, IntField, ListField, connect

connect(host=os.getenv('MONGO_CONNECTION_STRING'))

class Conversation(Document):
    user_id = StringField(required=True)
    msg = DictField(required=True, default={"user_msg": {"content": "", "time": ""}, "bot_reply": {"content": "", "time": ""}})
    meta: dict[str, str] = {
        "collection": "conversations"
    }

class Product(Document):
    name = StringField(required=True)
    condition = StringField(required=True)
    category = StringField(required=True)
    description = StringField(required=True)
    # details = ListField
    gender = StringField(required=True)
    price = IntField(required=True)
    countInStock = IntField(required=True)
    sizes = ListField(required=True)

    meta: dict[str, str] = {
        "collection": "products"
    }
