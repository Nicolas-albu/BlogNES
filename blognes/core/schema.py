from dataclasses import dataclass, field
from typing import List


@dataclass
class Comment:
    content: str
    author: str


@dataclass
class Post:
    title: str
    content: str
    comments: List[Comment] | None


@dataclass
class User:
    name: str
    cookie: str | None
    password: str = field(hash=True, compare=True)
    posts: List[Post] = field(default_factory=list)

    def __iter__(self):
        return iter(self.posts)


@dataclass
class Users:
    users: List[User] = field(default_factory=list)

    def __iter__(self):
        for user in self.users:
            yield iter(user.posts)
