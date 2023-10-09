from datetime import date as _date
from pathlib import Path
from typing import Any, Dict

import toml
from flask import Flask, render_template, request

from .controllers import (
    create_post,
    get_login,
    get_page_post,
    get_post,
    get_posts_all_users,
    get_profile,
    post_login,
    post_register,
    update_user,
)
from .core import hashed_password

app = Flask(__name__)

with open(Path.cwd() / ".secrets.toml", "r", encoding="utf-8") as file:
    app.secret_key = toml.load(file).get("FLASK_SECRET_KEY")


@app.route("/posts/all")
def get_all_posts():
    return get_posts_all_users()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/auth/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    form: Dict[str, Any] = request.form.to_dict()
    form["password"] = hashed_password(form["password"])

    record_user_date = map(int, form["date_of_birth"].split("-"))
    form["date_of_birth"] = _date(*record_user_date)

    return post_register(form)


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return get_login(cookies=request.cookies)

    return post_login(
        username=request.form["username"],
        password=hashed_password(request.form["password"]),
    )


@app.route("/profile", methods=["GET", "PUT"])
def profile():
    if request.method == "GET":
        return get_profile(cookies=request.cookies)

    form: Dict[str, Any] = request.form.to_dict()
    update_user_date = map(int, form["date_of_birth"].split("-"))

    form["date_of_birth"] = _date(*update_user_date)

    return update_user(form, cookies=request.cookies)


@app.route("/createPost", methods=["GET", "POST"])
def create_publication():
    if request.method == "GET":
        return get_page_post(cookies=request.cookies)

    return create_post(
        request.form.to_dict(),
        cookies=request.cookies,
    )


@app.route("/post/<int:post_id>")
def post(post_id: int):
    return get_post(post_id)
