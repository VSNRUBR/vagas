import os

from flask import Flask, url_for, render_template, request, redirect, flash
from models import db, Vaga, User, LoginForm, RegisterForm
from datetime import date
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.sqlite3'}
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    vagas = Vaga.query.order_by(Vaga.empresa).all()
    user = current_user.username

    return render_template('index.html', vagas=vagas, user=user)


@app.route('/nova_vaga', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('index'))

        except:
            return 'Erro ao adicionar vaga'

    else:
        return render_template('nova_vaga.html')


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    row_to_delete = Vaga.query.get(id)

    try:
        db.session.delete(row_to_delete)
        db.session.commit()

        return redirect(url_for('index'))

    except:
        return 'Erro ao deletar vaga.'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hash_pw)
        check_user = User.query.filter_by(username=new_user.username).first()
        if check_user:
            flash('Usuario ja resgistrado.')

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Usuario errado ou nao registrado.')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=False)
