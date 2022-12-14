from app.main.persistance import kmodao, scoredao


def get_kmo(ondernemingnummer: str):
    kmo = kmodao.get_full_kmo(ondernemingnummer)
    kmo["scores"] = scoredao.get_scores_for_kmo(ondernemingnummer)
    return kmo


def search_kmos(search: str):
    ondernemingsnummers = [kmo.ondernemingsnummer for kmo in kmodao.search_kmos(search)]
    return [get_kmo(ondernemingsnummer) for ondernemingsnummer in ondernemingsnummers]
