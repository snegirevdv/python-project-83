import os
import dotenv
from flask import Flask, render_template

app = Flask(__name__)

dotenv.load_dotenv('.env.development')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/urls/', methods=['GET', 'POST'])
def urls():
    return "Hello World"
