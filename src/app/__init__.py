import logging
import calendar
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from .celery_config import celery_init_app
from logging.handlers import RotatingFileHandler



db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'  

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SECRET_KEY'] = 'SADSA@#@#!@#!@%$@%#'
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    CSRFProtect(app)

    login_manager.init_app(app)
    
    @app.template_filter('month_name')
    def month_name(month_number):
        try:
            return calendar.month_name[month_number]
        except IndexError:
            return 'Invalid Month'

    if not app.debug:
        file_handler = RotatingFileHandler('app.log')
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    from .app_modules import blue_prints

    for bp in blue_prints:
        app.register_blueprint(bp)
    
    with app.app_context():
        from .command import register_commands
        register_commands(app)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app_modules.users.models import User
    return User.query.get(int(user_id))


#user vishal@yopmail.com/test@123