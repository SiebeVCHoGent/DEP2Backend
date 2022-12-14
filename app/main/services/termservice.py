import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from googletrans import Translator
translator = Translator()

from app.main.persistance import termdao, scoredao


def add_searchterm(term: str, parent_id: str = None):
    return termdao.add_searchterm(term, parent_id)


def delete_searchterm(id: str):
    return termdao.delete_searchterm(id)


def get_all_terms():
    def get_children(id, terms):
        children = []
        for term in terms:
            if term.parent == id:
                dic = vars(term)
                dic["children"] = get_children(dic["id"], terms)
                children.append(dic)
        return children

    terms = termdao.get_all_terms()
    a = []
    for t in terms:
        if t.parent is None:
            dic = vars(t)
            dic["children"] = get_children(t.id, terms)
            a.append(dic)

    return a


def get_words_for_term(term_id: str):
    return termdao.get_words_for_term(term_id)


def add_word(term_id: str, word: str):
    #word generate translation
    trans = translator.translate(word, src='nl', dest='en')
    if trans.extra_data.get('confidence') is not None and trans.extra_data.get('confidence', 0) > 0.75:
        if trans.text != word:
            termdao.add_word(term_id, trans.text)

    return termdao.add_word(term_id, word)


def delete_word(id: str):
    return termdao.delete_word(id)


def get_scores_for_kmo(ondernemingsnummer: str):
    scoresdb = scoredao.get_scores_for_kmo(ondernemingsnummer)
    # make sum of scores
    scores=[]

    c = 0
    ws = 0
    jvs = 0
    for obj in scoresdb:
        ws += obj.Score.website_score
        jvs += obj.Score.jaarverslag_score

        scores.append({
            "verslag_id": obj.Verslag.id,
            "jaar": obj.Verslag.jaar,
            "term": obj.Searchterm.term,
            "website_score": obj.Score.website_score,
            "jaarverslag_score": obj.Score.jaarverslag_score,
        })
        c += 1
    if c == 0:
        return scores
    scores.insert(0, {"term": "Gemiddelde Score", "website_score": ws/c, "jaarverslag_score": jvs/c})
    return scores


def get_score_ranking_all(jaar: int, limit=100):
    return scoredao.get_score_ranking_all(jaar, limit)


def recalculate_scores(jaar):
    def format_woorden(woorden):
        # replace spaces with <-> operator
        return [woord.woord.strip().replace(' ', '<->') for woord in woorden]

    def score_verslag(woorden):
        scores = scoredao.calculate_score(woorden, jaar)
        # scores to dataframe
        df = pd.DataFrame(scores, columns=['verslag_id', 'jaarverslag_score', 'website_score'])

        # set null to 0
        df = df.fillna(0)
        if len(df) > 0:
            df['jaarverslag_score'] = MinMaxScaler().fit_transform(df['jaarverslag_score'].values.reshape(-1, 1))
            df['website_score'] = MinMaxScaler().fit_transform(df['website_score'].values.reshape(-1, 1))

        return df

    # remove all calculated scores for this year
    scoredao.delete_scores_for_year(jaar)

    zoektermen = termdao.get_all_terms()

    for term in zoektermen:
        woorden = format_woorden(termdao.get_words_for_term(term.id))
        if len(woorden):
            scoredao.scores_to_db(term.id, score_verslag(woorden))

    return get_score_ranking_all(jaar)


def get_score_ranking_sector(jaar, limit):
    return scoredao.get_score_ranking_sector(jaar, limit)


def get_score_ranking_hoofdsector(jaar, limit):
    return scoredao.get_score_ranking_hoofdsector(jaar, limit)


def get_score_ranking_sector_kmo(sector, jaar, limit):
    return scoredao.get_score_ranking_sector_kmo(sector, jaar, limit)


def get_score_ranking_hoofdsector_kmo(hoofdsector, jaar, limit):
    return scoredao.get_score_ranking_hoofdsector_kmo(hoofdsector, jaar, limit)