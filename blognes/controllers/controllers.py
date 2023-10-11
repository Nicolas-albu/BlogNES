from typing import Any, Dict

from flask import flash, make_response, redirect, render_template, url_for

from ..core import Comment, Management, Post, User, generate_id, generate_token
from ..core.config import __COOKIE_NAME__

management = Management()
generator = generate_id()


# API
def get_posts(*, page: str | None, search: str | None):
    """
    Obtém publicações de acordo com a página ou termo de pesquisa.

    Args:
        page (str | None): Número da página a ser recuperada.
        search (str | None): Termo de pesquisa para recuperar publicações.

    Returns:
        dict: Um dicionário contendo as publicações encontradas.
    """
    if page and page.isdigit():
        if posts := management.get_page(number_page=int(page)):
            return {"posts": posts}

    if search:
        if posts := management.get_post(search=search):
            return {"posts": posts}

    return {"posts": []}


# Caso de Uso: Registrar-se
def get_register(*, cookie: str | None):
    """
    Retorna a página de registro se o usuário não estiver logado.

    Args:
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma página de registro ou redirecionamento para a página
            inicial.
    """
    if cookie:
        return redirect(url_for("get_index"))

    return render_template("register.html")


def post_register(form: Dict[str, Any], /):
    """
    Processa o formulário de registro e cria um novo usuário.

    Args:
        form (Dict[str, Any]): Um dicionário contendo os dados do formulário
            de registro.

    Returns:
        response: Uma resposta Flask com redirecionamento para a página
            inicial.
    """
    global management

    cookie = generate_token(form["password"])
    user = User(**form, cookie=cookie)

    management.add_user(user)

    response = make_response(redirect(url_for("get_index")))
    response.set_cookie(__COOKIE_NAME__, cookie)

    return response


# Caso de Uso: Acessar o Sistema (Login)
def get_login(*, cookie: str | None):
    """
    Retorna a página de login se o usuário não estiver logado.

    Args:
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma página de login ou redirecionamento para a página
            inicial.
    """
    if cookie:
        return redirect(url_for("get_index"))

    return render_template("login.html")


def post_login(*, username: str, password: str):
    """
    Processa o formulário de login e autentica o usuário.

    Args:
        username (str): Nome de usuário fornecido.
        password (str): Senha fornecida.

    Returns:
        response: Uma resposta Flask com redirecionamento para a página
            inicial ou mensagem de erro.
    """
    global management

    if management.is_user(username=username, password=password):
        cookie = generate_token(password)
        management.set_session(username, password, cookie=cookie)

        response = make_response(redirect(url_for("get_index")))
        response.set_cookie(__COOKIE_NAME__, cookie)
        return response

    flash("Nome de usuário e/ou senha incorreto", "error")
    return redirect(url_for("get_post_login"))


# Caso de Uso: Visualizar Perfil
def get_profile(*, cookie: str | None):
    """
    Retorna a página de perfil do usuário logado.

    Args:
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma página de perfil ou redirecionamento para a página de
            login.
    """
    if cookie and (_user := management.get_user(cookie=cookie)):
        return render_template("profile.html", user=_user.to_dict())

    return redirect(url_for("get_post_login"))


# Caso de Uso: Atualizar Perfil
def update_profile(form: Dict[str, Any], /, *, cookie: str | None):
    """
    Atualiza o perfil do usuário logado.

    Args:
        form (Dict[str, Any]): Um dicionário contendo os dados do formulário
            de atualização.
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma resposta Flask com redirecionamento para a página de
            perfil ou login.
    """
    if cookie:
        management.update_user(form, cookie=cookie)
        return redirect(url_for("get_put_profile"))

    return redirect(url_for("get_post_login"))


# Caso de Uso: Criação de Publicação
def get_publication_creation(*, cookie: str | None):
    """
    Retorna a página de criação de publicação se o usuário estiver logado.

    Args:
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma página de criação de publicação ou redirecionamento para
            a página de login.
    """
    if cookie:
        return render_template("create_post.html")

    return redirect(url_for("get_post_login"))


def post_publication_creation(
    form: Dict[str, Any],
    /,
    *,
    cookie: str | None,
):
    """
    Processa o formulário de criação de publicação e cria uma nova publicação.

    Args:
        form (Dict[str, Any]): Um dicionário contendo os dados do formulário
            de criação.
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma resposta Flask com redirecionamento para a página
            inicial ou login.
    """
    global management

    if cookie and (_user := management.get_user(cookie=cookie)):
        post = Post(id=next(generator), **form, author=_user.name)
        _user.add_post(post)
        management.add_post(post)

        return redirect(url_for("get_index"))

    return redirect(url_for("get_post_login"))


# Caso de Uso: Visualizar Publicação
def get_publication(post_id: int, /, *, author: str | None):
    """
    Retorna a página de uma publicação específica.

    Args:
        post_id (int): O ID da publicação a ser visualizada.
        author (str | None): O autor da publicação, se fornecido.

    Returns:
        response: Uma página de publicação ou redirecionamento para a página
            inicial.
    """
    if author and (_post := management.get_post(post_id=post_id)):
        return render_template("post.html", post=_post, author=author)

    return redirect(url_for("get_index"))


# Caso de Uso: Adicionar Comentário
def post_comment(form: Dict[str, Any], /, *, cookie: str | None):
    """
    Processa o formulário de adição de comentário e adiciona um novo
    comentário à publicação.

    Args:
        form (Dict[str, Any]): Um dicionário contendo os dados do formulário
            de comentário.
        cookie (str | None): O cookie do usuário, se estiver logado.

    Returns:
        response: Uma resposta Flask com redirecionamento para a página da
            publicação ou login.
    """
    global auth
    post_id, comment = form.values()

    if cookie and (_user := management.get_user(cookie=cookie)):
        new_comment = Comment(comment, author=_user.name)

        if _post := management.get_post(post_id=int(post_id)):
            _post.add_comment(new_comment)

            return redirect(
                url_for(
                    "get_publication",
                    post_id=form["post_id"],
                    author=_user.name,
                ),
            )

    return redirect(url_for("get_post_login"))
