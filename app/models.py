from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(50), nullable=False)
    vaga = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date)
    link = db.Column(db.String(128), nullable=False)

    def __init__(self, empresa, vaga, data, link):
        self.empresa = empresa
        self.vaga = vaga
        self.data = data
        self.link = link
