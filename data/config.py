import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]
admin_id = [
    885582686,
    386134461
]

db_pass = str(os.getenv("DB_PASS"))
db_name = str(os.getenv("DB_NAME"))
host = str(os.getenv("IP"))
db_user = str(os.getenv("DB_USER"))

POSTGRES_URI = f"postgresql://{db_user}:{db_pass}@{host}/{db_name}"

I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
