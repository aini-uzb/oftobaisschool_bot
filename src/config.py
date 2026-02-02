import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ID like -100... or username @channel
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME") # To show in link
# Support multiple admins (comma separated in env)
raw_admins = os.getenv("ADMIN_ID", "0")
ADMIN_IDS = []
for x in raw_admins.split(","):
    if x.strip():
        try:
            ADMIN_IDS.append(int(x.strip()))
        except ValueError:
            print(f"⚠️ Error parsing ADMIN_ID: '{x}' is not an integer")

# Ensure the new admin is always added if not in env
if 8308877174 not in ADMIN_IDS:
    ADMIN_IDS.append(8308877174)

print(f"✅ Loaded ADMIN_IDS: {ADMIN_IDS}")

LEADS_GROUP_ID = os.getenv("LEADS_GROUP_ID") 
if not LEADS_GROUP_ID:
    LEADS_GROUP_ID = "-1003862593886" # User provided ID with - prefix assumption
    # If -100 is not needed, user can correct it. But for channels/groups usually needed.
    # The user gave 1003862593886. 
    # Let's try to be smart. If failure, we can adjust.
    # But usually 100... is the ID without -
    # But for bot API send_message it needs -100 for supergroups.
    # The user provided 1003862593886. 
    # Let's try adding - sign.
    LEADS_GROUP_ID = "-1003862593886"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Use SQLite locally
    DATABASE_URL = "sqlite+aiosqlite:///database.db" # Changed from bot.db to force reset Info

# Payment Info
# Payment Info
CARD_NUMBER = "9860 1001 2680 1388"
CARD_HOLDER = "Bakhrom Khakimov"

# Webinar Info
WEBINAR_DATE = "12 феврал"
WEBINAR_TIME = "18:00"
WEBINAR_ZOOM_LINK = "https://zoom.us/j/xxxxxxxxx"

# Links
COURSE_PLATFORM_LINK = "https://..."
CHAT_LINK = "https://t.me/+xxxxxx"
SEMINAR_GROUP_LINK = os.getenv("SEMINAR_GROUP_LINK", "https://t.me/+Y6rm-pxhSGtmNzg6")  # Private group for seminar participants

# Prices
PRICES = {
    "LITE": {"full": 3000000, "half": 1500000, "original": 5000000},
    "PRO": {"full": 6000000, "half": 3000000, "original": 10000000},
    "VIP": {"full": 25000000, "half": 12500000, "original": 40000000}
}

DISCOUNT_END_DATE = "2026-03-18"
