from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery import Celery
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
celery = Celery(__name__)
migrate = Migrate()
# Implementing a rate limiter, settig limit to 1000 requests per minute
timestamp_limiter = Limiter(key_func=get_remote_address,
                            default_limits=["1000 per minute"])
