"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
from sqlalchemy import event
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery
from flask_babel import Babel
from marshmallow import validate

from notifier.commons.apispec import APISpecExt


db = FlaskSQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
babel = Babel()
ma_validate = validate
db_event = event
