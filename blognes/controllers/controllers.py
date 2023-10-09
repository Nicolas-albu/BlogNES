from typing import Any, Dict

from flask import flash, make_response, redirect, render_template, url_for

from ..core import Authenticator, User, generate_token
from ..core.config import __COOKIE_NAME__

auth = Authenticator()


def get_posts_all_users():
    posts = []

    for user in auth.users:
        posts += user.posts

    return {"posts": posts}


def post_register(form: Dict[str, Any], /):
    global auth

    cookie = generate_token(form["password"])
    user = User(**form, cookie=cookie)

    auth.add_user(user)

    response = make_response(redirect(url_for("index")))
    response.set_cookie(__COOKIE_NAME__, cookie)

    return response


def get_login(*, cookies: Dict[str, str]):
    if __COOKIE_NAME__ in cookies:
        return redirect(url_for("index"))

    return render_template("login.html")


def post_login(*, username: str, password: str):
    global auth

    if auth.is_user(username, password):
        cookie = generate_token(password)
        auth.set_session(username, password, cookie=cookie)

        response = make_response(redirect(url_for("index")))
        response.set_cookie(__COOKIE_NAME__, cookie)
        return response

    flash("Nome de usuário e/ou senha incorreto", "error")
    return redirect(url_for("login"))


def get_profile(*, cookies: Dict[str, str]):
    if __COOKIE_NAME__ not in cookies:
        return redirect(url_for("login"))

    cookie = cookies[__COOKIE_NAME__]

    if _user := auth.get_user(cookie=cookie):
        return render_template("profile.html", user=_user.to_dict())

    return redirect(url_for("login"))


def update_user(form: Dict[str, Any], /, *, cookies: Dict[str, str]):
    if _cookie := cookies.get(__COOKIE_NAME__):
        auth.update_user(form, cookie=_cookie)
        return redirect(url_for("profile"))

    return redirect(url_for("login"))
