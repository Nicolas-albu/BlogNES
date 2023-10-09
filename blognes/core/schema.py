from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List


@dataclass
class Comment:
    content: str
    author: str


@dataclass
class Post:
    title: str
    content: str
    comments: List[Comment] = field(default_factory=list)


@dataclass
class User:
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

    def add_post(self, post: Post) -> None:
        self.posts.append(post)

    def to_dict(self) -> Dict[str, str | date | List[Post]]:
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
