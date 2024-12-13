from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
import os

load_dotenv()

def init_db(app):
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    db_url = f"postgres://{db_user}:{db_password}@{db_host}/{db_name}"

    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
