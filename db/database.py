from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DBConnectionError
from tortoise import Tortoise

DATABASE_URL = 'postgres://postgres:2024@localhost:5432/vertx'

TORTOISE_ORM = {
      "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "app.vertx.models",
            ],
            "default_connection": "default",
        }
    },
}

async def init_db(app):
    try:
        register_tortoise(
            app,
            config=TORTOISE_ORM,
            generate_schemas=True,
            add_exception_handlers=True,
        )
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.get_connection("default").execute_query("SELECT 1")
        return True
    except DBConnectionError as e:
        print(f"❌ Database connection error: {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Unexpected database error: {str(e)}")
        raise
    finally:
        if Tortoise._inited:
            await Tortoise.close_connections()