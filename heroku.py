from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from app.v1.views.orders import orders

from flasgger import Swagger
from run_setup import app, create_app


app= create_app(dev=False)

swagger = Swagger(app)

app.register_blueprint(users)

app.register_blueprint(meals)

app.register_blueprint(menu)

app.register_blueprint(orders)

