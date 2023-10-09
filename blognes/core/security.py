from pathlib import Path

import bcrypt
import toml


def generate_token(data: str, /):
    return bcrypt.hashpw(data.encode("utf-8"), bcrypt.gensalt()).decode()


def hashed_password(passwd: str, /):
    with open(Path.cwd() / ".secrets.toml", "r", encoding="utf-8") as file:
        _pass = toml.load(file).get("SECRET_KEY", "").encode("utf-8")

    return bcrypt.hashpw(passwd.encode("utf-8"), _pass).decode("utf-8")
