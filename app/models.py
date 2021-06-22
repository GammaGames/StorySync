from datetime import datetime
from pony.converting import str2datetime
from pony.orm import Database, PrimaryKey, Required, Optional, Set

db = Database(provider="sqlite", filename="/opt/db.sqlite", create_db=True)

class User(db.Entity):
    username = PrimaryKey(str)


class Subreddit(db.Entity):
    id = PrimaryKey(int)
    posts = Set(lambda: Post)


class Post(db.Entity):
    id = PrimaryKey(int)
    subreddit = Required(Subreddit)
    url = Required(str)
    title = Required(str)
    body = Required(str)
    author = Required(str)
    comments = Set(lambda: Comment)
    created = Required(datetime)
    updated = Required(datetime)


class Comment(db.Entity):
    id = PrimaryKey(int)
    url = Required(str)
    body = Required(str)
    created = Required(datetime)
    updated = Required(datetime)


db.generate_mapping(create_tables=True)
