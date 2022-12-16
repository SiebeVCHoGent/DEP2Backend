from app.main.persistance import kmodao, scoredao


def get_kmo(ondernemingnummer: str):
    kmo = kmodao.get_full_kmo(ondernemingnummer)

    if not kmo:
        return kmo

    kmo = dict(kmo)

    kmo_ret = {}

    for key, value in kmo.items():
        # Split the key on the dash character
        split_key = key.split('-')
        if len(split_key) == 1:
            kmo_ret[key] = value
        else:
            if split_key[0] not in kmo_ret:
                kmo_ret[split_key[0]] = {}
            kmo_ret[split_key[0]][split_key[1]] = value

    kmo_ret["scores"] = scoredao.get_scores_for_kmo(ondernemingnummer)
    return kmo_ret


def search_kmos(search: str):
    ondernemingsnummers = [kmo.ondernemingsnummer for kmo in kmodao.search_kmos(search)]
    return [get_kmo(ondernemingsnummer) for ondernemingsnummer in ondernemingsnummers]
