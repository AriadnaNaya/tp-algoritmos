from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from backend.main import main as main_blueprint
from backend.auth.auth import auth as auth_blueprint
from backend.gastos.gastos import gastos as gastos_blueprint
from backend.db import db
from backend.db.models.User import User
from backend.db.models.Gasto import Gasto

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gastos.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(gastos_blueprint, url_prefix='/gastos')
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
