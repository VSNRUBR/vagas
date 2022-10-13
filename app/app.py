from crypt import methods
import os

from flask import Flask, url_for, render_template, request, session, redirect
from models import db, Vaga
from dotenv import load_dotenv
from datetime import date, datetime


app = Flask(import_name='app')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite3'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    vagas = Vaga.query.order_by(Vaga.empresa).all()

    return render_template('index.html', vagas=vagas, user=user)

@app.route('/nova_vaga', methods=['GET', 'POST'])
def nova_vaga():
    if request.method == 'POST':
        empresa = request.form['empresa']
        vaga = request.form['vaga']
        data = date.today()
        print(data)
        link = request.form['link']
        new_v = Vaga(empresa=empresa, vaga=vaga, data=data,link=link)
        print(new_v.empresa)

        try:
            db.session.add(new_v)
            db.session.commit()
            return redirect('/')

        except:
            return 'Erro ao adicionar vaga'

    else:
        return render_template('nova_vaga.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' or 'user' in session:
        user = request.form['usuario']
        session['user'] = user
        return redirect(url_for('index'))

    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
