from backend.db import db

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('gastos', lazy=True))

    def __repr__(self):
        return f"Gasto('{self.descripcion}', '{self.tipo}', '{self.monto}')"