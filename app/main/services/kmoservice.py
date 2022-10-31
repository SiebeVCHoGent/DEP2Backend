from app.main.persistance import kmodao


def get_kmo(ondernemingnummer: str):
    return kmodao.get_full_kmo(ondernemingnummer)


def search_kmos(search: str):
    return kmodao.search_kmos(search)