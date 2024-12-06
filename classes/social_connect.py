from dataclasses import dataclass
from datetime import datetime


@dataclass
class Post:
    text: str
    sender: str
    date: datetime

    def __repr__(self):
        return f"<b>{self.sender}</b> (<i>{self.date:%-m/%-d/%y - %-I:%M %p}</i>):<br>{self.text}<br>"

    __str__ = __repr__


class SocialConnect:
    def __init__(self, user_name):
        self.user_name = user_name
        self._posts = []

        self.add_post("my first post!", self.user_name)
        self.add_post("post_number two!", self.user_name, datetime.now())

    def __getitem__(self, item):
        return getattr(self, item, "")

    def add_post(self, text, sender, date=datetime.now()):
        self._posts.append(Post(text, sender, date))

    @property
    def posts(self):
        return sorted(self._posts, key=lambda x: x.date, reverse=False)

    @property
    def recent_posts(self):
        return self.posts[-5:]

    def __str__(self):
        return f"Social Connect: {self.user_name}"
