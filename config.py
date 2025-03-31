import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

SECRET_KEY = os.getenv("EDDIE_CORE_SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("EDDIE_CORE_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("EDDIE_CORE_ACCESS_TOKEN_EXPIRE_MINUTES", 60))
