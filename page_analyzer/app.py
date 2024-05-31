from datetime import datetime
import os
from urllib.parse import urlparse, urlunparse

import dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer import consts, sql
from page_analyzer.database import Database
from validators.url import url as validate_url

dotenv.load_dotenv(".env.development")

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

with Database() as db:
    db.execute_file(consts.MIGRATION)


@app.get("/")
def index() -> str:
    messages: list = get_flashed_messages(with_categories=True)
    url: str = request.args.get("url", "")

    return render_template(
        consts.INDEX_TEMPLATE,
        url=url,
        messages=messages
    )


@app.get("/urls/")
def urls() -> str:
    with Database() as db:
        db.execute_query(sql.URLS)
        entries = db.fetch_all()

    return render_template(
        consts.URLS_TEMPLATE,
        entries=entries
    )


@app.get("/urls/<id>/")
def detail(id: int):
    messages: list = get_flashed_messages(with_categories=True)

    with Database() as db:
        db.execute_query(sql.DETAIL, id)
        entry = db.fetch_one()

    if entry:
        return render_template(
            consts.DETAIL_TEMPLATE,
            entry=entry,
            messages=messages
        )

    flash(consts.DOESNT_EXIST, consts.DANGER)
    return redirect(url_for('index'))


@app.post("/urls/")
def urls_post():
    url = request.form.to_dict()["url"]

    if validate_url(url) is not True:
        flash(consts.INVALID_URL, consts.DANGER)
        return redirect(url_for("index", url=url))

    parsed_url = urlparse(url)

    pure_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, '', '', '', '')
    )

    with Database() as db:
        db.execute_query(sql.FIND_ID, pure_url)
        search_result = db.fetch_one()

    if search_result:
        url_id = search_result["id"]
        flash(consts.ALREADY_EXISTS, consts.INFO)
        return redirect(url_for('detail', id=url_id))

    with Database() as db:
        db.execute_query(sql.CREATE_ENTRY, url, datetime.now())
        created_entry = db.fetch_one()

    if created_entry:
        url_id = created_entry["id"]
        flash(consts.ADD_SUCCESS, consts.SUCCESS)
        return redirect(url_for('detail', id=url_id))

    flash(consts.ADD_FAILURE, consts.DANGER)
    return redirect(url_for('index', url=url))


if __name__ == "__main__":
    app.run(debug=True)
