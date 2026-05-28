from contextlib import contextmanager
import pyodbc
from config import DatabaseConfig


@contextmanager
def get_connection():
    conn = pyodbc.connect(DatabaseConfig.connection_string())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_one(table: str, data: dict) -> int:
    columns = ", ".join(data.keys())
    placeholders = ", ".join("?" for _ in data)
    values = list(data.values())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        cursor.close()
        return cursor.rowcount


def insert_many(table: str, columns: list[str], rows: list[tuple]) -> int:
    col_str = ", ".join(columns)
    placeholders = ", ".join("?" for _ in columns)
    sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(sql, rows)
        cursor.close()
        return cursor.rowcount


def execute_query(sql: str, params: list | None = None) -> list[pyodbc.Row]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        results = cursor.fetchall()
        cursor.close()
        return results
