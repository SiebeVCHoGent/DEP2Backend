from app.main.persistance import termdao


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