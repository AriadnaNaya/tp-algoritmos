from flask_login import LoginManager, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, abort, Blueprint
from ..db import db
from ..db.models.User import User
from ..db.models.Gasto import Gasto
from sqlalchemy import func

profile = Blueprint('profile', __name__,
                   template_folder='templates')

#Gonza
@profile.route('/', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def get_profile():
    gastos = Gasto.query.filter_by(user=current_user).all()

    gastos_agrupados = db.session.query(
        Gasto.tipo,
        func.sum(Gasto.monto).label('total')
    ).filter(Gasto.user_id==current_user.id).group_by(Gasto.tipo).all()

    return render_template('profile.html', user=current_user,  agrupados=gastos_agrupados)

@profile.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def eliminar_profile(user_id):
    pass

@profile.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_profile(user_id):

    user = User.query.filter_by(id=user_id).first()

    if user_id != current_user.id:
        abort(403)  # Forbidden

    if request.method == 'POST':
        user.email = request.form['email']
        user.name = request.form['name']
        user.tel = request.form['tel']
        user.budget = request.form['budget']
        db.session.commit()
        return redirect(url_for('profile.get_profile'))

    return render_template('editar_profile.html', user=user)