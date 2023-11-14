from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Gasto
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/gastos')
@login_required
def view_gastos():
    gastos = Gasto.query.filter_by(user=current_user).all()
    return render_template('gastos.html', gastos=gastos)
