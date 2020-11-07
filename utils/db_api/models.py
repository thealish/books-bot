from utils.db_api.database import db
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence, TIMESTAMP, BOOLEAN, JSON)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    referral = Column(Integer)

    query: sql.select
class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    category_name = Column(db.String(20))
    category_code = Column(db.String(50))
    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)
     # Код подкатегории (для отображения в колбек дате)
    subcategory_code = Column(String(50))

    # Название подкатегории (для отображения в кнопке)
    subcategory_name = Column(String(20))

    def __repr__(self):
        return f"""
    Товар №{self.id} - {self.name}
    Цена: {self.price}
                """


class Purchase(db.Model):
    __tablename__ = 'purchases'
    query: sql.select
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    amount = Column(Integer)
    purchase_time = Column(TIMESTAMP)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    receiver = Column(String(100))
    successful = Column(BOOLEAN, default=False)
