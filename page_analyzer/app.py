import os
import dotenv
from flask import Flask, redirect, render_template, request

from page_analyzer import utils

dotenv.load_dotenv(".env.development")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

utils.migrate()


@app.get("/")
def index():
    url = ""
    errors = {}
    return render_template("index.html", url=url, errors=errors)


@app.get("/urls/")
def url_list():
    url_list = utils.load_entries()
    return render_template("url_list.html", url_list=url_list)


@app.post("/urls/")
def url_post():
    url = request.form.to_dict()["url"]

    errors = utils.validate_url(url)
    if errors:
        return render_template("index.html", url=url, errors=errors), 422

    pure_url = utils.normalize_url(url)

    try:
        url_id = utils.get_entry_id(pure_url)
    except Exception as e:
        print(e)
        return render_template(
            "index.html", url=url, errors={"db": "Database error"}
        ), 500

    return redirect(f"/urls/{url_id}/", code=302)


@app.get("/urls/<id>/")
def url_detail(id):
    try:
        url_info = utils.get_url_info(id)
    except Exception:
        raise  # доделать

    return render_template("url_detail.html", url_info=url_info)


if __name__ == "__main__":
    app.run(debug=True)
