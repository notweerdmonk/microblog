from flask import current_app

def add_to_index(index, model):
    pass

def remove_from_index(index, model):
    pass

def query_index(index, query, page, per_page):
    try:
        query = query.split()
        expression = query[0]
        for exp in query[1:]:
            expression += ' & ' + exp
        search = index.query.filter(index.body_tsvector.match(expression,
            postgresql_regconfig='english'))
        total = search.count()
        results = search.paginate(page, per_page, False).items
    except:
        return [], 0
    ids = []
    for r in results:
        ids.append(r.id)
    return ids, total
