import os
import logging
from logging.handlers import RotatingFileHandler

# Logging
LOG_FILE_NAME = "bot.log"
PORT = 5010

OWNER_ID = int(os.getenv("OWNER_ID", "8771195193"))
MSG_EFFECT =  5046509860389126442

# Shortener
SHORT_URL = os.getenv("SHORT_URL", "")
SHORT_API = os.getenv("SHORT_API", "")
SHORT_TUT = os.getenv("SHORT_TUT", "")

# Telegram
SESSION = os.getenv("SESSION", "Kaya")
TOKEN = os.getenv("TOKEN", "")
API_ID = int(os.getenv("API_ID", "29245477"))
API_HASH = os.getenv("API_HASH", "0abc83883262245c90ca337b7a0375c4")
WORKERS = int(os.getenv("WORKERS", "5"))

# MongoDB
DB_URI = os.getenv("DB_URI", "")
DB_NAME = os.getenv("DB_NAME", "cluster0")

# Channels
DB_CHANNEL =  -1002497924209
# Force Subscribe
FSUB_CHANNEL = int(os.getenv("FSUB_CHANNEL", "0"))
FSUB_REQUEST = os.getenv("FSUB_REQUEST", "True").lower() == "true"
FSUB_TIMER = int(os.getenv("FSUB_TIMER", "10"))
FSUBS = [[FSUB_CHANNEL, FSUB_REQUEST, FSUB_TIMER]]

# Auto Delete
AUTO_DEL = int(os.getenv("AUTO_DEL", "300"))

# Admins
ADMINS = [
    int(x)
    for x in os.getenv("ADMINS", "").split(",")
    if x.strip()
]

# Bot Settings
DISABLE_BTN = os.getenv("DISABLE_BTN", "True").lower() == "true"
PROTECT = os.getenv("PROTECT", "False").lower() == "true"

# Messages
MESSAGES = {
    "START": os.getenv("START_MESSAGE", ""),
    "FSUB": os.getenv("FSUB_MESSAGE", ""),
    "ABOUT": os.getenv("ABOUT_MESSAGE", ""),
    "REPLY": os.getenv("REPLY_MESSAGE", "Wrong Command"),
    "SHORT_MSG": os.getenv("SHORT_MESSAGE", ""),
    "START_PHOTO": os.getenv("START_PHOTO", ""),
    "FSUB_PHOTO": os.getenv("FSUB_PHOTO", ""),
    "SHORT_PIC": os.getenv("SHORT_PIC", ""),
    "SHORT": os.getenv("SHORT", ""),
}


def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE_NAME,
        maxBytes=50_000_000,
        backupCount=10,
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
