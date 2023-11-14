from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gastos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Gasto  # Importa el modelo Gasto

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    @app.route('/gastos', methods=['GET', 'POST'])
    @login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
    def gastos():
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            tipo = request.form['tipo']
            monto = request.form['monto']

            nuevo_gasto = Gasto(descripcion=descripcion, tipo=tipo, monto=monto, user=current_user)
            db.session.add(nuevo_gasto)
            db.session.commit()

        gastos = Gasto.query.filter_by(user=current_user).all()
        return render_template('gastos.html', gastos=gastos)

    @app.route('/eliminar_gasto/<int:gasto_id>', methods=['POST'])
    @login_required
    def eliminar_gasto(gasto_id):
        gasto = Gasto.query.get_or_404(gasto_id)

        # Asegúrate de que el usuario actual sea el propietario del gasto
        if gasto.user != current_user:
            abort(403)  # Forbidden

        db.session.delete(gasto)
        db.session.commit()

        return redirect(url_for('gastos'))

    @app.route('/editar_gasto/<int:gasto_id>', methods=['GET', 'POST'])
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

    return app
