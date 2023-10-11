from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List


@dataclass
class Comment:
    """
    Classe para representar um comentário em uma postagem.

    Attributes:
        content (str): O conteúdo do comentário.
        author (str): O autor do comentário.
    """

    content: str
    author: str


@dataclass
class Post:
    """
    Classe para representar uma postagem em um sistema.

    Attributes:
        id (int): O ID único da postagem.
        title (str): O título da postagem.
        author (str): O autor da postagem.
        content (str): O conteúdo da postagem.
        comments (List[Comment]): Uma lista de comentários na postagem.

    Methods:
        add_comment(comment: Comment, /): Adiciona um comentário à postagem.
        to_dict() -> Dict[str, str | int | List[Comment]]: Converte a postagem
            em um dicionário.
    """

    id: int
    title: str
    author: str
    content: str
    comments: List[Comment] = field(default_factory=list)

    def add_comment(self, comment: Comment, /):
        """Adiciona um comentário à postagem.

        Args:
            comment (Comment): Comentário que será adicionado neste post.
        """
        self.comments.append(comment)

    def to_dict(self) -> Dict[str, str | int | List[Comment]]:
        """Converte a postagem em um dicionário.

        Returns:
            Dict[str, str | int | List[Comment]]: Dicionário com os atributos
                desse Post.
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "comments": self.comments,
        }


@dataclass
class User:
    """
    Classe para representar um usuário em um sistema.

    Attributes:
        cep (str): O CEP do usuário.
        name (str): O nome do usuário.
        city (str): A cidade do usuário.
        email (str): O endereço de e-mail do usuário.
        telephone (str): O número de telefone do usuário.
        home_address (str): O endereço residencial do usuário.
        cookie (str | None): O cookie de autenticação do usuário, se estiver
            logado.
        date_of_birth (date): A data de nascimento do usuário.
        password (str): A senha do usuário.
        posts (List[Post]): Uma lista de postagens do usuário.

    Methods:
        get_posts() -> List[Dict[str, str | int | List[Comment]]]: Obtém as
            postagens do usuário em forma de dicionários.
        add_post(post: Post) -> None: Adiciona uma postagem à lista de
            postagens do usuário.
        to_dict() -> Dict[str, str | date | List[Post]]: Converte o usuário em
            um dicionário.
    """

    cep: str
    name: str
    city: str
    email: str
    telephone: str
    home_address: str
    cookie: str | None
    date_of_birth: date
    password: str
    posts: List[Post] = field(default_factory=list)

    def get_posts(self) -> List[Dict[str, str | int | List[Comment]]]:
        """Obtém as postagens do usuário em forma de dicionários.

        Returns:
            List[Dict[str, str | int | List[Comment]]]: Lista de todas as
                postagens desse usuário.
        """
        return [_post.to_dict() for _post in self.posts]

    def add_post(self, post: Post) -> None:
        """Adiciona uma postagem à lista de postagens do usuário.

        Args:
            post (Post): Postagem que será adicionado neste usuário.
        """
        self.posts.append(post)

    def to_dict(self) -> Dict[str, str | date | List[Post]]:
        """Converte o usuário em um dicionário.

        Returns:
            Dict[str, str | date | List[Post]]: Dicionário com os atributos
                desse Usuário.
        """
        return {
            "cep": self.cep,
            "name": self.name,
            "city": self.city,
            "email": self.email,
            "telephone": self.telephone,
            "home_address": self.home_address,
            "date_of_birth": self.date_of_birth,
            "password": self.password,
            "posts": self.posts,
        }
