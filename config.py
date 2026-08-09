import os

from dotenv import load_dotenv

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GOOGLE_CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    os.path.join(BASE_DIR, "google-credentials.json")
)
ADMIN_LINE_USER_ID = os.getenv("ADMIN_LINE_USER_ID", "")
