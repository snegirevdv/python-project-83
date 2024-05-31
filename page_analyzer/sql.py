URLS = """
SELECT
    id,
    name,
    created_at
FROM
    urls
"""

DETAIL = """
SELECT
    id,
    name,
    created_at
FROM
    urls
WHERE
    id = %s
"""

FIND_ID = """
SELECT
    id,
    name
FROM
    urls
WHERE
    name = %s
"""

CREATE_ENTRY = """
INSERT INTO
    urls (name, created_at)
VALUES
    (%s, %s)
RETURNING
    id
"""
