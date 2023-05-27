from decouple import config
from fastapi_login import LoginManager

SECRET_KEY = config("SECRET_KEY", cast=str)

fake_db = {"admin@mail.com": {"password": "pass123"}}

manager = LoginManager(SECRET_KEY, token_url="/api/auth/token")


@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = fake_db.get(email)
    return user
