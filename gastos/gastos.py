from flask_login import LoginManager, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, abort, Blueprint
from sqlalchemy import func

from ..db import db
from ..db.models.Gasto import Gasto


gastos = Blueprint('gastos', __name__,
                        template_folder='templates')


@gastos.route('/', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def create_gastos():
    return render_template('agregar_gasto.html')

@gastos.route('/list', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def listar_gastos():
    total = 0
    gastos = Gasto.query.filter_by(user=current_user).all()

    gastos_agrupados = db.session.query(
        Gasto.tipo,
        func.sum(Gasto.monto).label('total')
    ).filter(Gasto.user_id==current_user.id).group_by(Gasto.tipo).all()

    for gasto in gastos:
        total+= gasto.monto

    return render_template('gastos.html', gastos=gastos, total=total, agrupados=gastos_agrupados, user=current_user)


@gastos.route('/', methods=['POST'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def create_gastos_post():

    total = 0

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        monto = request.form['monto']

        nuevo_gasto = Gasto(descripcion=descripcion, tipo=tipo, monto=monto, user=current_user)
        db.session.add(nuevo_gasto)
        db.session.commit()

    gastos = Gasto.query.filter_by(user=current_user).all()
    gastos_agrupados = db.session.query(
        Gasto.tipo,
        func.sum(Gasto.monto).label('total')
    ).filter(Gasto.user_id==current_user.id).group_by(Gasto.tipo).all()

    for gasto in gastos:
        total+= gasto.monto

    return render_template('gastos.html', gastos=gastos, total=total, agrupados=gastos_agrupados, user=current_user)

@gastos.route('/delete/<int:gasto_id>', methods=['POST'])
@login_required
def eliminar_gasto(gasto_id):
    gasto = Gasto.query.get_or_404(gasto_id)

    # Asegúrate de que el usuario actual sea el propietario del gasto
    if gasto.user != current_user:
        abort(403)  # Forbidden

    db.session.delete(gasto)
    db.session.commit()

    return redirect(url_for('gastos.listar_gastos'))

@gastos.route('/edit/<int:gasto_id>', methods=['GET', 'POST'])
@login_required
def editar_gasto(gasto_id):
    gasto = Gasto.query.get_or_404(gasto_id)

    # Asegúrate de que el usuario actual sea el propietario del gasto
    if gasto.user != current_user:
        abort(403)  # Forbidden

    if request.method == 'POST':
        # Actualizar los campos del gasto con los nuevos valores
        gasto.descripcion = request.form['descripcion']
        gasto.tipo = request.form['tipo']
        gasto.monto = request.form['monto']

        db.session.commit()
        return redirect(url_for('gastos.listar_gastos'))

    return render_template('editar_gasto.html', gasto=gasto)