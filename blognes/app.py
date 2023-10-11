import datetime
from pathlib import Path
from typing import Any, Dict

import toml
from flask import Flask, render_template, request

from . import controllers
from .core import hashed_password
from .core.config import __COOKIE_NAME__

app = Flask(__name__)

with open(Path.cwd() / ".secrets.toml", "r", encoding="utf-8") as file:
    app.secret_key = toml.load(file).get("FLASK_SECRET_KEY")


@app.route("/api/getPosts")
def get_posts():
    """
    Rota para obter publicações com base em parâmetros de página e pesquisa.

    Returns:
        dict: Um dicionário contendo as publicações encontradas.
    """
    return controllers.get_posts(
        page=request.args.get("page"),
        search=request.args.get("search"),
    )


@app.route("/")
def get_index():
    """
    Rota para a página inicial.

    Returns:
        str: A página inicial.
    """
    return render_template("index.html")


@app.route("/auth/register", methods=["GET", "POST"])
def get_post_register():
    """
    Rota para registro de usuário. Suporta solicitações GET e POST.

    Returns:
        response: A página de registro (GET) ou o registro de um
            novo usuário (POST).
    """
    if request.method == "GET":
        cookie = request.cookies.get(__COOKIE_NAME__)
        return controllers.get_register(cookie=cookie)

    form: Dict[str, Any] = request.form.to_dict()
    form["password"] = hashed_password(form["password"])

    record_user_date = map(int, form["date_of_birth"].split("-"))
    form["date_of_birth"] = datetime.date(*record_user_date)

    return controllers.post_register(form)


@app.route("/auth", methods=["GET", "POST"])
def get_post_login():
    """
    Rota para login de usuário. Suporta solicitações GET e POST.

    Returns:
        response: A página de login ou inicia uma sessão para este
            usuário (POST).
    """
    if request.method == "GET":
        cookie = request.cookies.get(__COOKIE_NAME__)
        return controllers.get_login(cookie=cookie)

    return controllers.post_login(
        username=request.form["username"],
        password=hashed_password(request.form["password"]),
    )


@app.route("/profile", methods=["GET", "PUT"])
def get_put_profile():
    """
    Rota para visualizar e atualizar o perfil do usuário. Suporta solicitações
    GET e PUT.

    Returns:
        response: A página de perfil (GET) ou atualização do perfil (PUT).
    """
    cookie = request.cookies.get(__COOKIE_NAME__)

    if request.method == "GET":
        return controllers.get_profile(cookie=cookie)

    form: Dict[str, Any] = request.form.to_dict()

    update_user_date = map(int, form["date_of_birth"].split("-"))
    form["date_of_birth"] = datetime.date(*update_user_date)

    return controllers.update_profile(form, cookie=cookie)


@app.route("/createPost", methods=["GET", "POST"])
def get_post_publication_creation():
    """
    Rota para criação de publicação. Suporta solicitações GET e POST.

    Returns:
        response: A página de criação de publicação (GET) ou criação de um
            novo Post (POST).
    """
    cookie = request.cookies.get(__COOKIE_NAME__)

    if request.method == "GET":
        return controllers.get_publication_creation(cookie=cookie)

    return controllers.post_publication_creation(
        request.form.to_dict(),
        cookie=cookie,
    )


@app.route("/post/<int:post_id>")
def get_publication(post_id: int):
    """
    Rota para visualizar uma postagem específica.

    Args:
        post_id (int): O ID da postagem a ser visualizada.

    Returns:
        response: A página da postagem ou redirecionamento para a página
            inicial.
    """
    author = request.args.get("author")

    return controllers.get_publication(post_id, author=author)


@app.route("/newComment", methods=["POST"])
def post_comment():
    """
    Rota para adicionar comentários a uma postagem. Suporta solicitações POST.

    Returns:
        response: Redirecionamento para a página da postagem ou página de
            login.
    """
    cookie = request.cookies.get(__COOKIE_NAME__)

    return controllers.post_comment(
        request.form.to_dict(),
        cookie=cookie,
    )
