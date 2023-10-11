from typing import Any, List, TypeVar, overload

from .config import __QUANTITY_POSTS_BY_PAGE__, __SESSION_ADMIN__
from .schema import Post, User

T = TypeVar("T")


class Management:
    __slots__ = ["__users", "__pages"]

    def __init__(self):
        self.__users: list[User] = []
        self.__pages: List[List[Post]] = []

        self._initialization()

    def _initialization(self) -> None:
        admin_user = User(**__SESSION_ADMIN__)
        self.add_user(admin_user)

    @property
    def users(self) -> list[User]:
        return self.__users

    @property
    def pages(self) -> List[List[Post]]:
        return self.__pages

    @staticmethod
    def __get_data(data: List[T], index: int) -> T | None:
        try:
            return data[index]
        except IndexError:
            return None

    @overload
    def is_user(self, *, username: str, password: str) -> bool:
        ...

    @overload
    def is_user(self, *, cookie: str) -> bool:
        ...

    def is_user(self, **kwargs) -> bool:
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
        ...

    @overload
    def get_post(self, *, search: str) -> List[Post] | None:
        ...

    def get_post(self, **kwargs) -> List[Post] | Post | None:
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
        self.__users.append(user)

    def get_user(self, *, cookie: str) -> User | None:
        for user in self.__users:
            if user.cookie == cookie:
                return user

    def set_session(
        self, username: str, password: str, /, *, cookie: str
    ) -> None:
        for user in self.__users:
            if (user.name, user.password) == (username, password):
                user.cookie = cookie
                break

    def update_user(self, data: dict[str, Any], /, *, cookie: str) -> None:
        for _user in self.__users:
            if _user.cookie == cookie:
                for key, value in data.items():
                    setattr(_user, key, value)
                break

    def add_post(self, new_post: Post, /) -> None:
        if (last_page := self.__get_data(self.__pages, -1)) is None:
            self.__pages.append([new_post])

        elif len(last_page) == __QUANTITY_POSTS_BY_PAGE__:
            self.__pages.append([new_post])

        else:
            self.__pages[-1].append(new_post)

    def get_page(self, *, number_page: int) -> List[Post] | None:
        return self.__get_data(self.__pages, number_page)
