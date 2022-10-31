from app.main.common.pydantic import EntityBaseModel


class Gemeente(EntityBaseModel):
    postcode: str
    naam: str