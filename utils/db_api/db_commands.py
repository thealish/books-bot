from typing import List

from sqlalchemy import and_

from utils.db_api.models import Item, User
from utils.db_api.database import db


# Функция для создания нового товара в базе данных. Принимает все возможные аргументы, прописанные в Item
async def add_new_item(**kwargs):
    new_item = await Item(**kwargs).create()
    return new_item


async def add_new_user(**kwargs):
    new_user = await User(**kwargs).create()
    return new_user


# Функция для вывода товаров с РАЗНЫМИ категориями
async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_name).gino.all()


# Функция для подсчета товаров с выбранными категориями и подкатегориями
async def count_items(category_code):
    # Прописываем условия для вывода (категория товара равняется выбранной категории)
    conditions = [Item.category_code == category_code]

    # Функция подсчета товаров с указанными условиями
    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


# Функция вывода всех товаров, которые есть в переданных категории и подкатегории
async def get_items(category_code) -> List[Item]:
    item = await Item.query.where(
        and_(Item.category_code == category_code)
    ).gino.all()
    return item


# Функция для получения объекта товара по его айди
async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


async def get_item_by_name(item_name) -> Item:
    item = await Item.query.where(Item.name == item_name).gino.first()
    return item


async def get_description(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


