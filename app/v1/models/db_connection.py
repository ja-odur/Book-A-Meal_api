from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm.exc import UnmappedInstanceError

from run_setup import app

DB = SQLAlchemy(app)