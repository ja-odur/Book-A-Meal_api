from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from app.v1.views.orders import orders
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
import os
DB = SQLAlchemy()

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgresql://postgres:13811923@localhost:5432/Book-A-Meal')

app.config['DEBUG'] = os.environ.get('DEBUG', False)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'title': 'BOOK-A-MEAL API',
    'version': 1,
}
DB.init_app(app)
CORS(app)

swagger = Swagger(app)

app.register_blueprint(users)

app.register_blueprint(meals)

app.register_blueprint(menu)

app.register_blueprint(orders)


if __name__ == '__main__':
    app.run(debug=True)

