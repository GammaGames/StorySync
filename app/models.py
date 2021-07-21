from datetime import datetime
from pony.converting import str2datetime
from pony.orm import Database, PrimaryKey, Required, Optional, Set

db = Database(provider="sqlite", filename="/opt/db.sqlite", create_db=True)


class Story(db.Entity):
    id = Required(int)
    type = Required(str)
    title = Optional(str)
    url = Required(str)
    body = Required(str)

    PrimaryKey(id, type)


db.generate_mapping(create_tables=True)
