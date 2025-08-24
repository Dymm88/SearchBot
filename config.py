from decouple import config

DATABASE_URL = config('DATABASE_URL')
BOT_TOKEN = config('BOT_TOKEN')
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
REDIRECT_URI = config('REDIRECT_URI')
EMAIL = config('EMAIL')
APPLICATION = config('APPLICATION')
ADMINS = config('ADMINS').split(',')
