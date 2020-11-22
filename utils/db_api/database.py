from gino import Gino
from gino.schema import GinoSchemaVisitor
import logging
from data.config import POSTGRES_URI
from data.config import db_name

db = Gino()


async def create_db():
    await db.set_bind(POSTGRES_URI)
    logging.info(f"Connected to database: {db_name}")
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()
