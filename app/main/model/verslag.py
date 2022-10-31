import typing as t

from app.main.common.pydantic import EntityBaseModel


class Verslag(EntityBaseModel):
    jaar: int
    omzet: t.Optional[float]
    balanstotaal: t.Optional[float]
    aantalwerknemers: t.Optional[float]

    codingtree: t.Optional[str]

    jaarverslag_id: t.Optional[str]
    jaarverslag_url: t.Optional[str]
    jaarverslag_tekst: t.Optional[str]


    website_url: t.Optional[str]
    website_tekst: t.Optional[str]