from utils.db_api.database import db
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence, TIMESTAMP, BOOLEAN, JSON, ForeignKey)
from sqlalchemy import sql


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger, unique=True)
    full_name = Column(String(100))
    username = Column(String(50))
    query: sql.select


class Item(db.Model):
    __tablename__ = 'items'
    item_id = Column(Integer, Sequence("user_id_seq"), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    photo = Column(String(250))
    price = Column(Integer)
    description = Column(String(255))
    category_name = Column(String(55))
    category_code = Column(Integer)
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


