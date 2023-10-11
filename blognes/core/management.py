from typing import Any, List, TypeVar, overload

from .config import __QUANTITY_POSTS_BY_PAGE__, __SESSION_ADMIN__
from .schema import Post, User

T = TypeVar("T")


class Management:
    """
    Classe para gerenciar usuários e postagens em um sistema.
    """

    __slots__ = ["__users", "__pages"]

    def __init__(self):
        """
        Inicializa uma instância de Management com usuários e páginas.
        Também adiciona um usuário administrador.
        """
        self.__users: list[User] = []
        self.__pages: List[List[Post]] = []

        self._initialization()

    def _initialization(self) -> None:
        """inicialização do sistema com um usuário administrador."""
        admin_user = User(**__SESSION_ADMIN__)
        self.add_user(admin_user)

    @property
    def users(self) -> list[User]:
        """
        Propriedade que retorna a lista de usuários registrados.

        Returns:
            list[User]: Lista de usuários registrados.
        """
        return self.__users

    @property
    def pages(self) -> List[List[Post]]:
        """
        Propriedade que retorna a lista de páginas de postagens.

        Returns:
            List[List[Post]]: Lista de páginas de postagens.
        """
        return self.__pages

    @staticmethod
    def __get_data(data: List[T], index: int) -> T | None:
        """
        Obtém um item de uma lista com base no índice, retornando None se
        o índice estiver fora dos limites.

        Args:
            data (List[T]): A lista de dados.
            index (int): O índice do item desejado.

        Returns:
            T | None: O item da lista ou None se o índice estiver fora dos
                limites.
        """
        try:
            return data[index]
        except IndexError:
            return None

    @overload
    def is_user(self, *, username: str, password: str) -> bool:
        """
        Verifica se um usuário com um nome de usuário e senha correspondentes
        existe.

        Args:
            username (str): Nome de usuário a ser verificado.
            password (str): Senha a ser verificada.

        Returns:
            bool: True se o usuário existir e as credenciais corresponderem,
                False caso contrário.
        """
        ...

    @overload
    def is_user(self, *, cookie: str) -> bool:
        """
        Verifica se um usuário com um cookie específico existe.

        Args:
            cookie (str): O cookie do usuário a ser verificado.

        Returns:
            bool: True se o usuário com o cookie existir, False caso contrário.
        """
        ...

    def is_user(self, **kwargs) -> bool:
        """
        Verifica se um usuário existe com base nas informações fornecidas.

        Args:
            **kwargs: Pode conter 'username' e 'password' ou 'cookie' para
                identificar o usuário.

        Returns:
            bool: True se o usuário existir, False caso contrário.
        """
        if "username" in kwargs and "password" in kwargs:
            username, password = kwargs["username"], kwargs["password"]

            for user in self.__users:
                if (user.name, user.password) == (username, password):
                    return True

        elif "cookie" in kwargs:
            for user in self.__users:
                if user.cookie == kwargs["cookie"]:
                    return True

        return False

    @overload
    def get_post(self, *, post_id: int) -> Post | None:
        """
        Obtém uma postagem com base no ID da postagem.

        Args:
            post_id (int): O ID da postagem a ser obtida.

        Returns:
            Post | None: A postagem correspondente ou None se não for
                encontrada.
        """
        ...

    @overload
    def get_post(self, *, search: str) -> List[Post] | None:
        """
        Procura postagens com base em um termo de pesquisa.

        Args:
            search (str): O termo de pesquisa.

        Returns:
            List[Post] | None: Uma lista de postagens correspondentes ou None
                se nenhuma for encontrada.
        """
        ...

    def get_post(self, **kwargs) -> List[Post] | Post | None:
        """
        Obtém postagens com base nos argumentos fornecidos.

        Args:
            **kwargs: Pode conter 'post_id' ou 'search' para identificar as
                postagens.

        Returns:
            List[Post] | Post | None: Uma lista de postagens ou uma postagem
                correspondente, ou None se não for encontrada nenhuma.
        """
        if post_id := kwargs.get("post_id"):
            for _user in self.__users:  # O(n^2)
                for post in _user.posts:
                    if post.id == post_id:
                        return post

        if search := kwargs.get("search"):
            posts = [
                post
                for _user in self.__users  # O(n^2)
                for post in _user.posts
                if search in post.title
            ]

            return posts

    def add_user(self, user: User, /) -> None:
        """
        Adiciona um usuário à lista de usuários registrados.

        Args:
            user (User): O usuário a ser adicionado.
        """
        self.__users.append(user)

    def get_user(self, *, cookie: str) -> User | None:
        """
        Obtém um usuário com base no cookie fornecido.

        Args:
            cookie (str): O cookie do usuário a ser usado para identificar o
                usuário.

        Returns:
            User | None: O usuário correspondente ou None se não for
                encontrado.
        """
        for user in self.__users:
            if user.cookie == cookie:
                return user

    def set_session(
        self, username: str, password: str, /, *, cookie: str
    ) -> None:
        """
        Define uma sessão para um usuário com base no nome de usuário e senha
        fornecidos.

        Args:
            username (str): Nome de usuário do usuário.
            password (str): Senha do usuário.
            cookie (str): O cookie a ser associado à sessão.
        """
        for user in self.__users:
            if (user.name, user.password) == (username, password):
                user.cookie = cookie
                break

    def update_user(self, data: dict[str, Any], /, *, cookie: str) -> None:
        """
        Atualiza as informações de um usuário com base no cookie fornecido.

        Args:
            data (dict[str, Any]): Dados a serem atualizados no usuário.
            cookie (str): O cookie do usuário para identificação.
        """
        for _user in self.__users:
            if _user.cookie == cookie:
                for key, value in data.items():
                    setattr(_user, key, value)
                break

    def add_post(self, new_post: Post, /) -> None:
        """
        Adiciona uma nova postagem à lista de postagens.

        Args:
            new_post (Post): A postagem a ser adicionada.
        """
        if (last_page := self.__get_data(self.__pages, -1)) is None:
            self.__pages.append([new_post])

        elif len(last_page) == __QUANTITY_POSTS_BY_PAGE__:
            self.__pages.append([new_post])

        else:
            self.__pages[-1].append(new_post)

    def get_page(self, *, number_page: int) -> List[Post] | None:
        """
        Obtém uma página específica de postagens com base no número da página.

        Args:
            number_page (int): O número da página a ser obtida.

        Returns:
            List[Post] | None: Uma lista de postagens correspondente à página
                ou None se a página não existir.
        """
        return self.__get_data(self.__pages, number_page)
