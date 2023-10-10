from typing import Any, overload

from .config import __SESSION_ADMIN__
from .schema import Post, User


class Management:
    __slots__ = ["__users"]

    def __init__(self):
        self.__users: list[User] = []

        self._initialization()

    def _initialization(self) -> None:
        admin_user = User(**__SESSION_ADMIN__)
        self.add_user(admin_user)

    @property
    def users(self) -> list[User]:
        return self.__users

    def add_user(self, user: User, /) -> None:
        self.__users.append(user)

    @overload
    def is_user(self, username: str, password: str) -> bool:
        ...

    @overload
    def is_user(self, cookie: str) -> bool:
        ...

    def is_user(self, *args, **kwargs) -> bool:
        if "username" in kwargs and "password" in kwargs:
            username, password = kwargs["username"], kwargs["password"]

            for user in self.__users:
                if (user.name, user.password) == (username, password):
                    return True

        elif "cookie" in kwargs:
            for user in self.__users:
                if user.cookie == kwargs["cookie"]:
                    return True

        elif args:
            # Tratar como (username, password)
            if len(args) == 2:
                username, password = args[0], args[1]

                for user in self.__users:
                    if (user.name, user.password) == (username, password):
                        return True

        return False

    def get_user(self, *, cookie: str) -> User | None:
        for user in self.__users:
            if user.cookie == cookie:
                return user

    def set_session(
        self,
        username: str,
        password: str,
        /,
        *,
        cookie: str,
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

    def get_post(self, post_id: int, /) -> Post | None:
        for _user in self.__users:
            for post in _user.posts:
                if post.id == post_id:
                    return post
