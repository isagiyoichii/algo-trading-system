import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("🔍 Verifying environment variables...\n")

credentials = {
    "API_KEY": os.getenv("API_KEY"),
    "API_SECRET": os.getenv("API_SECRET"),
    "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
    "KITE_USERNAME": os.getenv("KITE_USERNAME"),
    "KITE_PASSWORD": os.getenv("KITE_PASSWORD"),
    "REDIRECT_URI": os.getenv("REDIRECT_URI"),
    "DB_HOST": os.getenv("DB_HOST"),
    "DB_NAME": os.getenv("DB_NAME"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PORT": os.getenv("DB_PORT"),
}

for key, value in credentials.items():
    hidden = value if value and len(value) < 10 else value[:4] + "..." if value else "❌ NOT SET"
    print(f"{key:15}: {hidden}")
