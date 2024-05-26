import datetime
import os
import dotenv
from flask import Flask, redirect, render_template, request

from page_analyzer.database import Database

dotenv.load_dotenv(".env.development")

app = Flask(__name__)
db = Database(os.getenv("DATABASE_URL"))

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

try:
    db.migrate("database.sql")
except Exception as e:
    print(f"Migration error: {e}")


@app.get("/")
def index():
    print("Index route accessed")
    url = ""
    errors = {}
    return render_template("index.html", url=url, errors=errors)


@app.get("/urls/")
def url_list():
    print("URL list route accessed")
    try:
        url_list = get_url_list()
    except Exception as e:
        print(f"Error fetching URL list: {e}")
        url_list = []
    return render_template("url_list.html", url_list=url_list)


@app.post("/urls/")
def url_post():
    print("URL post route accessed")
    url = request.form.to_dict()["url"]
    errors = validate_url(url)
    if errors:
        return render_template("index.html", url=url, errors=errors), 422
    pure_url = sanitize_url(url)
    try:
        url_id = get_url_id(pure_url)
    except Exception as e:
        print(f"Error getting URL ID: {e}")
        return (
            render_template("index.html", url=url, errors={"db": "Database error"}),
            500,
        )
    return redirect(f"/urls/{url_id}/", code=302)


@app.get("/urls/<id>/")
def url_detail(id):
    print(f"URL detail route accessed with id: {id}")
    try:
        url_info = get_url_info(id)
    except Exception as e:
        print(f"Error fetching URL info: {e}")
        url_info = {"id": id, "name": "Error", "created_at": "Unknown"}
    return render_template("url_detail.html", url_info=url_info)


def validate_url(url):
    return {}


def sanitize_url(url):
    return url


def get_url_list():
    query_text = "SELECT id, name FROM urls"
    db.execute_query(query_text)
    description = db.fetch_description() or []
    columns = [desc[0] for desc in description]
    url_list = [dict(zip(columns, row)) for row in db.fetch_all()]
    return url_list


def get_url_info(id):
    query_text = "SELECT id, name, created_at FROM urls WHERE id = %s"
    db.execute_query_with_args(query_text, id)
    url_info = db.fetch_one()
    if not url_info:
        return {"id": id, "name": "Not found", "created_at": "Unknown"}
    columns = ["id", "name", "created_at"]
    return dict(zip(columns, url_info))


def get_url_id(target_url):
    select_query_text = "SELECT id, name FROM urls"
    db.execute_query(select_query_text)
    urls = db.fetch_all()
    for id, url in urls:
        if url == target_url:
            return id
    insert_query_text = (
        "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id"
    )
    db.execute_query_with_args(insert_query_text, target_url, datetime.datetime.now())
    data = db.fetch_one()
    if not data:
        raise ValueError("Insertion failed")
    db.commit()
    id = data[0]
    return id


if __name__ == "__main__":
    app.run(debug=True)
