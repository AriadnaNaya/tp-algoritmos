from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user:
        return redirect(url_for('gastos.listar_gastos'))

    return render_template('login.html')
