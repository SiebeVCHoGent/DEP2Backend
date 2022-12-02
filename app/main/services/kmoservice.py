from app.main.persistance import kmodao


def get_kmo(ondernemingnummer: str):
    return kmodao.get_full_kmo(ondernemingnummer)


def search_kmos(search: str):
    ondernemingsnummers = [kmo.ondernemingsnummer for kmo in kmodao.search_kmos(search)]
    return [get_kmo(ondernemingsnummer) for ondernemingsnummer in ondernemingsnummers]
