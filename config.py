import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SERVICE_AUTH_KEY = os.getenv("SERVICE_AUTH_KEY")
SERVICE_AUTH_ALGORITHM = os.getenv("SERVICE_AUTH_ALGORITHM")

USER_AUTH_KEY = os.getenv("USER_AUTH_KEY", "supersecretley")
USER_AUTH_ALGORITHM = os.getenv("USER_AUTH_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

SYSTEM_API_KEY = os.getenv("SYSTEM_API_KEY", "supersecretapikey")
SYSTEM_USER_PASSWORD = os.getenv("SYSTEM_USER_PASSWORD", "supersecretpassword")