import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]



db_pass = str(os.getenv("DB_PASS"))
db_name = str(os.getenv("DB_NAME"))
host = str(os.getenv("ip"))
db_user= str(os.getenv("DB_USER"))


POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"