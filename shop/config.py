import os
import django
import sys

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')

BOT_TOKEN=os.getenv('BOT_TOKEN')
CHANEL_ID=os.getenv('CHANEL_ID')
GROUP_ID=os.getenv('GROUP_ID')
CHANEL_URL=os.getenv('CHANEL_URL')
GROUP_URL=os.getenv('GROUP_URL')
YOOKASSA_SECRET_KEY=os.getenv('YOOKASSA_SECRET_KEY')
YOOKASSA_SHOP_ID=os.getenv('YOOKASSA_SHOP_ID')
