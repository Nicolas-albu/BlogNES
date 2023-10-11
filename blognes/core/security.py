from pathlib import Path

import bcrypt
import toml


def generate_token(data: str, /):
    """
    Gera um token seguro com base nos dados fornecidos.

    Args:
        data (str): Os dados a serem usados para gerar o token.

    Returns:
        str: O token gerado como uma string.
    """
    return bcrypt.hashpw(data.encode("utf-8"), bcrypt.gensalt()).decode()


def hashed_password(passwd: str, /):
    """
    Gera uma senha segura com base na senha fornecida e na chave secreta
    armazenada no arquivo .secrets.toml.

    Args:
        passwd (str): A senha a ser usada como base para gerar a senha segura.

    Returns:
        str: A senha segura gerada como uma string.
    """
    with open(Path.cwd() / ".secrets.toml", "r", encoding="utf-8") as file:
        _pass = toml.load(file).get("SECRET_KEY", "").encode("utf-8")

    return bcrypt.hashpw(passwd.encode("utf-8"), _pass).decode("utf-8")
