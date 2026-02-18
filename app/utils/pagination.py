from sqlalchemy.orm import Query


def apply_pagination(query: Query, page: int, limit: int):
    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit)
