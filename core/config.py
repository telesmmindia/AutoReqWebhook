import os
from dotenv import load_dotenv

load_dotenv()

WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", 3002))
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL", "https://reqbot.telesmm.in")
OTHER_BOTS_PATH = os.getenv("OTHER_BOTS_PATH", f"/webhook/{{bot_token}}")


active_bots = {}
