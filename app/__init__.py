# app/__init__.py
from flask import Flask, g, session
from flask_sqlalchemy import SQLAlchemy
from app.config import load_config
from datetime import datetime
import secrets

db=SQLAlchemy()
from .models import User
def create_app():
    app = Flask(__name__)

    # Load configuration
    config=load_config()
    app.config.update(config)
    app.secret_key=secrets.token_hex(32)
    
    db.init_app(app)
    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    @app.before_request
    def before_request():
        g.site_name=app.config['SITE_NAME']
        g.current_year=datetime.now().year
        user_id=session.get('user_id')
        if user_id:
            g.user=User.query.filter_by(uid=user_id).first()
        else:
            g.user=User()
                
    return app
