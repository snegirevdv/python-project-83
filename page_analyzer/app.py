import os

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
from page_analyzer import utils

dotenv.load_dotenv(".env.development")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

utils.migrate()


@app.get("/")
def index():
    messages = get_flashed_messages(with_categories=True)
    url = request.args.get("url", "")
    return render_template("index.html", url=url, messages=messages)


@app.get("/urls/")
def url_list():
    url_list = utils.load_entries()
    return render_template("url_list.html", url_list=url_list)


@app.post("/urls/")
def url_post():
    url = request.form.to_dict()["url"]

    if not utils.validate_url(url):
        flash("Некорректный URL", "danger")
        return redirect(url_for("index", url=url))

    try:
        pure_url = utils.normalize_url(url)
        url_id = utils.find_entry_id(pure_url)

        if url_id:
            flash("Страница уже существует", "info")
        else:
            url_id = utils.create_entry(pure_url)
            flash("Страница успешно добавлена", "success")

        return redirect(f"/urls/{url_id}/")

    except Exception:
        flash("Ошибка базы данных", "danger")
        return redirect(url_for("index", url=url))


@app.get("/urls/<id>/")
def url_detail(id):
    try:
        messages = get_flashed_messages(with_categories=True)
        url_info = utils.get_url_info(id)
        return render_template(
            "url_detail.html",
            url_info=url_info,
            messages=messages,
        )

    except Exception:
        flash("Ошибка базы данных", "danger")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
