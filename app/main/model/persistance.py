import typing as t
from abc import ABC, abstractmethod

from app.main.model.gemeente import Gemeente
from app.main.model.kmo import Kmo
from app.main.model.sector import Sector
from app.main.model.verslag import Verslag
from app.main.common.pydantic import EntityBaseModel


class IsPersistance(ABC):
    @abstractmethod
    def to_object(self, *args, **kwargs) -> t.Any:
        pass

class KmoPersistance(EntityBaseModel, IsPersistance):
    ondernemingsnummer: str
    naam: str
    email: t.Optional[str]
    telefoonnummer: t.Optional[str]
    adres: t.Optional[str]
    beursgenoteerd: bool
    isB2B: bool

    def to_object(self, sector: Sector = None, gemeente: Gemeente = None, verslagen: t.List[Verslag] = None) -> Kmo:
        return Kmo(**vars(self), sector=sector, gemeente=gemeente, verslagen=verslagen)


class SectorPersistance(EntityBaseModel, IsPersistance):
    naam: str

    def to_object(self, hoofdsector: str) -> Sector:
        return Sector(**vars(self), hoofdsector=hoofdsector)



class HoofdsectorPersistance(EntityBaseModel, IsPersistance):
    naam: str

    def to_object(self) -> str:
        return self.naam


class GemeentePersistance(EntityBaseModel, IsPersistance):
    postcode: str
    naam: str

    def to_object(self) -> Gemeente:
        return Gemeente(**vars(self))


class VerslagPersistance(EntityBaseModel, IsPersistance):
    jaar: int
    omzet: float
    balanstotaal: float
    aantalwerknemers: float

    def to_object(self) -> Verslag:
        return Verslag(**vars(self))
