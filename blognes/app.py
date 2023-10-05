from flask import Flask

from .core import __USERS__

app = Flask(__name__)


@app.route("/post/all")
def get_all_post():
    # Captura o cookie da sessão atual e verifica o acesso

    posts = []

    for user in __USERS__:
        ...
    ...


@app.route("/")
def index():
    ...
