from pathlib import Path

import psycopg

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_db_config() -> dict:
    env_path = PROJECT_ROOT / ".env"

    if not env_path.is_file():
        raise FileNotFoundError("Local .env file not found")

    values = {}

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")

        if separator:
            values[key.strip()] = value.strip()

    return {
        "host": "127.0.0.1",
        "port": int(values["POSTGRES_PORT"]),
        "dbname": values["POSTGRES_DB"],
        "user": values["POSTGRES_USER"],
        "password": values["POSTGRES_PASSWORD"],
    }


def connect():
    return psycopg.connect(**load_db_config())
