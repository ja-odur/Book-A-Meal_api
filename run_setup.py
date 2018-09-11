from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__, instance_relative_config=True)
CORS(app)


def create_app(dev=True):
    if dev:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                               'postgresql://postgres:13811923@localhost:5432/Book-A-Meal_test_db')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                               'postgresql://postgres:13811923@localhost:5432/Book-A-Meal')

    app.config['DEBUG'] = os.environ.get('DEBUG', False)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'BOOK-A-MEAL API',
        'version': 1,
    }
    return app


create_app(dev=False)


