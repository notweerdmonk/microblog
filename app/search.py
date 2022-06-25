from flask import current_app
from sqlalchemy import text
from app import db

def add_to_index(index, model):
    pass

def remove_from_index(index, model):
    pass

def query_index(index, query, page, per_page):
    try:
        sql = text("SELECT post.id AS post_id FROM post WHERE to_tsvector('english', post.body) @@ websearch_to_tsquery('english', '{exp}')".format(exp=query))
        result = db.session.execute(sql)
        search = [r[0] for r in result]
        total = len(search)
        ids = search[(page - 1) * per_page:page * per_page]
    except:
        return [], 0
    return ids, total
