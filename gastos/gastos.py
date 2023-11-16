from flask_login import LoginManager, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, abort, Blueprint
from backend.db import db
from backend.db.models.Gasto import Gasto

gastos = Blueprint('gastos', __name__,
                        template_folder='templates')


@gastos.route('/', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def create_gastos():
    return render_template('agregar_gasto.html')

@gastos.route('/list', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def listar_gastos():
    gastos = Gasto.query.filter_by(user=current_user).all()
    return render_template('gastos.html', gastos=gastos)


@gastos.route('/', methods=['POST'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def create_gastos_post():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        monto = request.form['monto']

        nuevo_gasto = Gasto(descripcion=descripcion, tipo=tipo, monto=monto, user=current_user)
        db.session.add(nuevo_gasto)
        db.session.commit()

    gastos = Gasto.query.filter_by(user=current_user).all()
    return render_template('gastos.html', gastos=gastos)

@gastos.route('/delete/<int:gasto_id>', methods=['POST'])
@login_required
def eliminar_gasto(gasto_id):
    gasto = Gasto.query.get_or_404(gasto_id)

    # Asegúrate de que el usuario actual sea el propietario del gasto
    if gasto.user != current_user:
        abort(403)  # Forbidden

    db.session.delete(gasto)
    db.session.commit()

    return redirect(url_for('gastos'))

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
        return redirect(url_for('gastos'))

    return render_template('editar_gasto.html', gasto=gasto)