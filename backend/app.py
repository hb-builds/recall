from flask import Flask, send_from_directory
from flask_cors import CORS 
from config import Config
from extensions import db, jwt, cache, celery, migrate, timestamp_limiter
import datetime, os

EXPORT_DIR = os.path.join(os.getcwd(), 'exports')
REPORTS_DIR = os.path.join(os.getcwd(), 'reports')


class ContextTask(celery.Task):

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    timestamp_limiter.init_app(app)
    celery.conf.update(app.config)
    celery.Task = ContextTask

    # Setting up CLI with the "seed" command
    import seeds
    app.cli.add_command(seeds.seed)

    # Initializing blueprints
    from api.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    from api.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    from api.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    from api.quiz import quiz_bp
    app.register_blueprint(quiz_bp, url_prefix='/api')
    from api.analytics import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api')

    # Setting up static serve of exports and reports
    app.add_url_rule(
        '/exports/<path:filename>', 'exports',
        lambda filename: send_from_directory(EXPORT_DIR, filename))
    app.add_url_rule(
        '/reports/<path:filename>', 'reports',
        lambda filename: send_from_directory(REPORTS_DIR, filename))
    return app


def isoformat(dt: datetime.datetime) -> str:
    return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

