from datetime import date, datetime
from typing import TypedDict
from page_analyzer.database import Database


Entry = TypedDict('Entry', {'id': int, 'name': str, 'created_at': date})


def migrate() -> None:
    with Database() as db:
        db.execute_file("database.sql")


def get_entry_from_row(row: tuple[int, str, datetime]) -> Entry:
    print(row)
    try:
        return {
            'id': row[0],
            'name': row[1],
            'created_at': row[2].date()
        }
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке данных из БД: {e}")


def load_entries() -> list[Entry]:
    with Database() as db:
        db.execute_query("SELECT * FROM urls")
        rows = db.fetch_all()

    return [get_entry_from_row(row) for row in rows]


def create_entry(url: str) -> int:
    with Database() as db:
        query_text = (
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id"
        )
        db.execute_query(query_text, url, datetime.now())

        if fetched_data := db.fetch_one():
            return fetched_data[0]

    raise Exception("Ошибка при создании записи в БД")


def get_entry_id(target_url: str) -> int:
    entries = load_entries()

    for entry in entries:
        if entry['name'] == target_url:
            return entry["id"]

    return create_entry(target_url)


def validate_url(url: str) -> list[Entry]:
    return []


def normalize_url(url: str) -> str:
    return url


def get_url_info(id: int) -> Entry:
    with Database() as db:
        db.execute_query("SELECT * FROM urls WHERE id = %s", id)
        row = db.fetch_one()

    if row:
        return get_entry_from_row(row)

    raise Exception
