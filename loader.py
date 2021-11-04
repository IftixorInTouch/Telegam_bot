import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PROVIDER_TOKEN = str(os.getenv("PROVIDER_TOKEN"))
