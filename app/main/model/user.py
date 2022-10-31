import json
import typing as t

import ulid
from pydantic import Field

from app.main.common.pydantic import EntityBaseModel


class User(EntityBaseModel):
    id: str = Field(default_factory=ulid.ulid)
    password: str = ''
    email: str
    roles: t.List[str] = ["standaard"]

    def get_jwt_data(self):
        return {'id': self.id, 'email': self.email, 'roles': self.roles}

    def to_db(self):
        d = vars(self)
        d['roles'] = json.dumps(d['roles'])
        return d

    @classmethod
    def from_db(cls, db):
        d = vars(db)
        d['roles'] = json.loads(d['roles'])
        return cls(**d)