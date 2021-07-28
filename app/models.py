from datetime import datetime
from pony.converting import str2datetime
from pony.orm import Database, PrimaryKey, Required, Optional, db_session

db = Database(provider="sqlite", filename="./db.sqlite", create_db=True)


class Story(db.Entity):
    id = Required(str)
    type = Required(str)
    title = Optional(str)
    subreddit = Optional(str)
    source_permalink = Optional(str)
    target_permalink = Optional(str, nullable=True)
    body = Optional(str, nullable=True)

    PrimaryKey(id, type)


db.generate_mapping(create_tables=True)
