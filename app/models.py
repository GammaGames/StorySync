from datetime import datetime
from pony.converting import str2datetime
from pony.orm import Database, PrimaryKey, Required, Optional, db_session

db = Database(provider="sqlite", filename="./db.sqlite", create_db=True)


async def get_model(Model, id=None, **kwargs):
    with db_session():
        return Model[id] if Model.exists(id=id) else Model(id=id, **kwargs)


class Story(db.Entity):
    id = Required(int)
    type = Required(str)
    title = Optional(str)
    subreddit = Required(str)
    source_permalink = Required(str)
    target_permalink = Optional(str)
    body = Required(str)

    PrimaryKey(id, type)


db.generate_mapping(create_tables=True)
