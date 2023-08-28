from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco.db"
app.config["SECRET_KEY"] = "dont tells please"
db = SQLAlchemy(app)

class cadastrar(db.Model):
    __tablename__ = "Cadastro"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    endereco = db.Column(db.String(100))
    cpf = db.Column(db.String(12))

#ROTA INICIA
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

#ROTA CADASTRO
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome1 = request.form["nome"]
        nome = nome1.upper()
        idade = request.form["idade"]
        cpf = request.form["cpf"]
        endereco = request.form["endereco"]
        busca1 = cadastrar.query.filter(and_(cadastrar.nome == nome), (cadastrar.cpf == cpf)).first()
        if not nome or not idade or not cpf or not endereco:
            flash("Preencha corretamente")
        elif busca1:
            flash("Cliente já cadastrado")
        else:
            flash("Salvo")
            salvar = cadastrar()
            salvar.nome = nome
            salvar.idade = idade
            salvar.endereco = endereco
            salvar.cpf = cpf
            db.session.add(salvar)
            db.session.commit()
            return redirect(url_for('cadastro'))
    return render_template("cadastro.html")

#ROTA CONSULTA
@app.route("/consulta", methods=["GET", "POST"])
def consulta():
    return render_template("consulta.html")

#JSON - CONSULTA
@app.route("/lista/rodajson")
def lista_cadastro():
    cadastro = cadastrar.query.all()
    cadastrolist = []
    for cadas in cadastro:
        cadastroObj = {}
        cadastroObj["id"] = cadas.id
        cadastroObj["nome"] = cadas.nome
        cadastroObj["idade"] = cadas.idade
        cadastroObj["endereco"] = cadas.endereco
        cadastroObj["cpf"] = cadas.cpf
        cadastrolist.append(cadastroObj)
    return jsonify({"cadastro" : cadastrolist})

@app.route("/remover_cadastro/<int:id>")
def remover(id):
    remcasd = cadastrar.query.filter_by(id=id).first()
    db.session.delete(remcasd)
    db.session.commit()
    flash(f"O usuario {remcasd.nome} foi deletado")
    return redirect(url_for("consulta"))

@app.route("/editar_cadastro/<int:id>", methods=["GET", "POST"])
def edita(id):
    editar = cadastrar.query.filter_by(id=id).first()
    if request.method == "POST":
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        endereco = request.form.get("endereco")
        cpf = request.form.get("cpf")
        
        salvar = cadastrar.query.filter_by(id=id).first()
        setattr(salvar, "nome", nome)
        setattr(salvar, "idade", idade)
        setattr(salvar, "endereco", endereco)
        setattr(salvar, "cpf", cpf)
        db.session.commit()
        flash(f"O usuario {salvar.nome} foi alterado com sucesso")
        return redirect(url_for("consulta"))
    return render_template("editar.html", editar=editar)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)