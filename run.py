from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from app.v1.views.orders import orders

from flasgger import Swagger
from manage import manager
from run_setup import app

swagger = Swagger(app)

app.register_blueprint(users)

app.register_blueprint(meals)

app.register_blueprint(menu)

app.register_blueprint(orders)


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()
