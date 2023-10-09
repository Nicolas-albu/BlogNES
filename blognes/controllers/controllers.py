from typing import Any, Dict

from flask import flash, make_response, redirect, render_template, url_for

from ..core import (
    Authenticator,
    Comment,
    Post,
    User,
    generate_id,
    generate_token,
)
from ..core.config import __COOKIE_NAME__

auth = Authenticator()
generator = generate_id()


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


def get_page_post(*, cookies: Dict[str, str]):
    if __COOKIE_NAME__ not in cookies:
        return redirect(url_for("login"))

    return render_template("create_post.html")


def create_post(form: Dict[str, Any], /, *, cookies: Dict[str, str]):
    global auth

    _cookie = cookies[__COOKIE_NAME__]

    if _user := auth.get_user(cookie=_cookie):
        post = Post(id=next(generator), **form)
        _user.add_post(post)
        return redirect(url_for("index"))

    return redirect(url_for("login"))


def get_post(post_id: int):
    if _post := auth.get_post(post_id):
        return render_template("post.html", post=_post)

    return redirect(url_for("index"))


def post_comment(form: Dict[str, Any], /, *, cookies: Dict[str, str]):
    global auth

    _cookie = cookies[__COOKIE_NAME__]
    post_id, comment = form.values()

    if _user := auth.get_user(cookie=_cookie):
        new_comment = Comment(comment, author=_user.name)

        if _post := auth.get_post(int(post_id)):
            _post.add_comment(new_comment)
            return redirect(url_for("post", post_id=form["post_id"]))

    return redirect(url_for("login"))
