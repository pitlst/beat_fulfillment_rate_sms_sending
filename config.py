import os
from dotenv import load_dotenv

load_dotenv()


class ApiConfig:
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:12382")
    BATCH_QUERY_PATH = "/api/batch-query"

    @classmethod
    def batch_query_url(cls) -> str:
        return f"{cls.BASE_URL.rstrip('/')}{cls.BATCH_QUERY_PATH}"


class DatabaseConfig:
    DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
    SERVER = os.getenv("DB_SERVER", "localhost")
    PORT = os.getenv("DB_PORT", "1433")
    DATABASE = os.getenv("DB_DATABASE", "")
    USERNAME = os.getenv("DB_USERNAME", "")
    PASSWORD = os.getenv("DB_PASSWORD", "")

    @classmethod
    def connection_string(cls) -> str:
        return (
            f"DRIVER={cls.DRIVER};"
            f"SERVER={cls.SERVER},{cls.PORT};"
            f"DATABASE={cls.DATABASE};"
            f"UID={cls.USERNAME};"
            f"PWD={cls.PASSWORD}"
        )

    @classmethod
    def validate(cls) -> bool:
        missing = []
        if not cls.DATABASE:
            missing.append("DB_DATABASE")
        if not cls.USERNAME:
            missing.append("DB_USERNAME")
        if not cls.PASSWORD:
            missing.append("DB_PASSWORD")
        if missing:
            raise ValueError(f"缺少必要的数据库配置: {', '.join(missing)}")
        return True


PROJECTS = [
    {"board": "assembly", "project_no": "B2434B01", "train_no": "B2434B010005"},
    {"board": "delivery", "project_no": "B2433B01", "train_no": "B2433B010003"},
]
