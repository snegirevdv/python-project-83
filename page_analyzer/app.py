import os
import dotenv
from flask import Flask

app = Flask(__name__)

dotenv.load_dotenv('.env.development')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return 'Good Soup'
