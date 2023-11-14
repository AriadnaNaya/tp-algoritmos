from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db_path = 'gastos.db'

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            tipo TEXT NOT NULL,
            monto REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/view_gastos', methods=['GET', 'POST'])
def gastos():
    create_table()
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        monto = request.form['monto']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO gastos (descripcion, tipo, monto) VALUES (?, ?, ?)', (descripcion, tipo, monto))
        conn.commit()
        conn.close()

        return redirect(url_for('gastos'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gastos')
    gastos = cursor.fetchall()
    conn.close()

    return render_template('gastos.html', gastos=gastos)

if __name__ == '__main__':
    app.run(debug=True)
