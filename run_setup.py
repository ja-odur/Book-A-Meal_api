from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:13811923@localhost:5432/test_db'
app.config['SWAGGER'] = {
    'title': 'BOOK-A-MEAL API',
    'version': 1,
}
