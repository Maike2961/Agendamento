from app import db

class cadastrar(db.Model):
    __tablename__ = "Cadastro"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    endereco = db.Column(db.String(100))
    cpf = db.Column(db.String(12))