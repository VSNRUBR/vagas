import os

from flask import Flask, url_for, render_template
from models import db, Vaga
from dotenv import load_dotenv
from datetime import date


app = Flask(import_name='app')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.sqlite3'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
