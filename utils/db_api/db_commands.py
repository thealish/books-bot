from utils.db_api.models import Item, User, Purchase
from typing import List
from sqlalchemy import and_
from utils.db_api.database import db
from utils.db_api.models import Item


async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem

async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino_all()

async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino_all()


async def count_items(category_code, subcategory_code = None):
    conditions = [Item.category_code == category_code]

    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)

    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total

async def get_items(category_code, subcategory_cdoe) -> List[Item]:
    items = await Item.query.where(
        and_(Item.category_code == category_code,
            Item.subcategory_code == subcategory_cdoe)
    ).gino_all()
    return items


async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item

