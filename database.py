from tortoise.contrib.fastapi import register_tortoise


def init_db(app):
    register_tortoise(
        app,
        db_url="postgres://samandar:1234@localhost/weather_db",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
