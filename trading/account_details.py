import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class AccountDetails(Enum):
    API_KEY: str = os.getenv("API_KEY")
    API_SECRET: str = os.getenv("API_SECRET")
    BASE_URL: str = os.getenv("BASE_URL")
