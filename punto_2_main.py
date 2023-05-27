from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from decouple import config

from app.api import router as api
from app.auth import router as auth
from app.database.utils import load_initial_data

app = FastAPI()
app.include_router(api.router)
app.include_router(auth.router)

# * Initialize Tortoise ORM
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.database.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup_event():
    # * Load initial data to database if not exists
    await load_initial_data()
