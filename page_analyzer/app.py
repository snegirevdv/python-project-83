import os
import dotenv
from flask import Flask

app = Flask(__name__)

dotenv.load_dotenv('.env.development')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return '<img src="https://media1.giphy.com/media/w4g8JSKEkCmpwfMiRU/giphy.gif">'
