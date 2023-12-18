from app import app
from app import db
from models import agenda_model
from flask import render_template,redirect,request,flash,jsonify, url_for
from sqlalchemy.sql import and_

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
        busca1 = agenda_model.cadastrar.query.filter(and_(agenda_model.cadastrar.nome == nome), (agenda_model.cadastrar.cpf == cpf)).first()
        if not nome or not idade or not cpf or not endereco:
            flash("Preencha corretamente")
        elif busca1:
            flash("Cliente já cadastrado")
        else:
            flash("Salvo")
            salvar = agenda_model.cadastrar()
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
    cadastro = agenda_model.cadastrar.query.all()
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
    remcasd = agenda_model.cadastrar.query.filter_by(id=id).first()
    db.session.delete(remcasd)
    db.session.commit()
    flash(f"O usuario {remcasd.nome} foi deletado")
    return redirect(url_for("consulta"))

@app.route("/editar_cadastro/<int:id>", methods=["GET", "POST"])
def edita(id):
    editar = agenda_model.cadastrar.query.filter_by(id=id).first()
    if request.method == "POST":
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        endereco = request.form.get("endereco")
        cpf = request.form.get("cpf")
        
        salvar = agenda_model.cadastrar.query.filter_by(id=id).first()
        setattr(salvar, "nome", nome)
        setattr(salvar, "idade", idade)
        setattr(salvar, "endereco", endereco)
        setattr(salvar, "cpf", cpf)
        db.session.commit()
        flash(f"O usuario {salvar.nome} foi alterado com sucesso")
        return redirect(url_for("consulta"))
    return render_template("editar.html", editar=editar)