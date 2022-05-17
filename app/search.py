from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    try:
        current_app.elasticsearch.index(index=index, id=model.id, body=payload)
    except:
        return

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    try:
        current_app.elasticsearch.delete(index=index, id=model.id)
    except:
        return

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    try:
        search = current_app.elasticsearch.search(
                index=index,
                body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
                      'from': (page - 1) * per_page, 'size': per_page})
    except:
        return [], 0
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
