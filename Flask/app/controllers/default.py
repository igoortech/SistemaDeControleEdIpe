from flask import render_template, jsonify , redirect,url_for, request,flash
from app import app,db #do módulo app(pasta), import a variável #app
from app.models.tables import User,Prestador,Ponto
from datetime import datetime as dt,date
from flask_login import login_required,current_user, login_manager
from app.models.uteis import ponto_required
from sqlalchemy import Date, cast
import traceback

@app.route("/admin")
@login_required
def admin():
   return render_template("admin.html" ,user=current_user)

@app.route("/addfun")
@login_required
def addfun():

   return render_template("cadastrafun.html" ,user=current_user)


@app.route("/func")
@login_required
def func():

   return render_template("func.html", user=current_user)


@app.route("/relogio")
@login_required
def relogio():
   
   return render_template("relogio.html",user= current_user)

 

@app.route("/relatorio")
@login_required
def relatorio():

   return render_template("relatorio.html")


###################################################ROTAS DA PRINCIPAL ABAIXO. ROTAS DE LOGIN ACIMA.




@app.route("/") #nossa página principal
@login_required
@ponto_required()
def index():
  # if current_user.admin:
   #   return render_template('admin.html',user=current_user)
   #else:
      #return render_template('index.html',user=current_user)
    
   return render_template('index.html',user=current_user)

@app.route("/relogiofun")
@login_required
@ponto_required()
def relogiofun():
   return render_template('pontofun.html', user = current_user)


@app.route("/registro")
@login_required
@ponto_required()
def registro():
   return render_template('registro.html' ,user = current_user)

@app.route("/cadastrar")
@login_required
@ponto_required()
def cadastrar():
   return render_template("cadastrar.html", user=current_user)
   
@app.route("/prestador")
@login_required
@ponto_required()
def prestador():
   return render_template('prestador.html', user= current_user)


@app.route("/insert", methods = ['POST'])
def insert():
     if request.method == 'POST':
         nome = request.form['nome']
         documento = request.form['Documento']
         empresa = request.form['empresa']
         tipo = request.form['tipo']
         user = current_user.id_ponto

         if "" in [documento.strip(),empresa.strip(),tipo.strip(),nome.strip(),nome.strip()]:
            flash("todos os campos devem estar preenchidos!")
            return redirect(url_for('cadastrar'))

         validaNome = [x for x in "1234567890" if x in nome]
         if validaNome:
            flash("Nome contem números por favor insira apenas letras!")
            return redirect(url_for('cadastrar'))
         
         validaDoc = [x for x in documento if not x in "1234567890"]
         if validaDoc:
            flash("documento deve conter apenas numeros!")
            return redirect(url_for('cadastrar'))

         item = Prestador.query.filter_by(doc = documento).all()
         if item:
            flash("Documento ja cadastrado!")
            return redirect(url_for('cadastrar'))
         

         dados =  Prestador(nome,documento ,empresa,tipo,user)

         db.session.add(dados)
         db.session.commit()

         flash("usuario cadastrado com sucesso!")
         return redirect(url_for('index'))

         

@app.route("/atualizar")
def atualizar():
   return render_template('a')

@app.route("/baterPonto")
@login_required
def baterPonto():

   registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).filter(cast(Ponto.entrada,Date) == date.today()).first() #valida se a dar de hoje
   #for igual a hoje

   if registro_ponto: 
      flash("já existe uma entrada para o dia de hoje!")
      return render_template('baterPonto.html',user=current_user)

   pt = Ponto(current_user.id_ponto,dt.now(),None,None,None)
   db.session.add(pt)
   db.session.commit()
   return redirect(url_for('index'))
      #return PontoSchema().dumps(registro_ponto[0])


@app.route("/teste") #nossa página principal
def teste():
   try:
      
      return render_template('teste.html',user = User.query.first())
   except:
      return traceback.format_exc()