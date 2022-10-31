import typing as t

from app.main.model.gemeente import Gemeente
from app.main.model.sector import Sector
from app.main.model.verslag import Verslag
from app.main.common.pydantic import EntityBaseModel


class Kmo(EntityBaseModel):
    ondernemingsnummer: str
    naam: str
    email: t.Optional[str]
    telefoonnummer: t.Optional[str]
    adres: t.Optional[str]
    beursgenoteerd: bool
    isB2B: bool
    gemeente: t.Optional[Gemeente]
    sector: t.Optional[Sector]
    verslagen: t.Optional[t.List[Verslag]]
