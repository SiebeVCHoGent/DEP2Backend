import typing as t

from app.main.common.pydantic import EntityBaseModel


class Sector(EntityBaseModel):
    naam: str
    hoofdsector: t.Optional[str]