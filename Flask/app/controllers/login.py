from app import app,lm

from flask_login import login_user,login_required,current_user,logout_user
from flask import render_template,redirect,url_for,jsonify,flash
from app.models.tables import User
from app.models.form import LoginForm



@app.route("/login",methods=["GET","POST"])
def login():
    form =  LoginForm() #estância do formulário da página de login
    #flash("Usuario invalido")
    if form.validate_on_submit(): #Entra quando for POST
        user = form.username.data #pega o usuario digitado na pagina
        senha = form.password.data #pega a senha digitada na pagina

        user_banco = User.query.filter_by(username=user).first()
        if user_banco:
            if user_banco.senha == senha:
                login_user(user_banco)  # autentica o usuario na sessao do sistema e coloca ele dentro do current_user
                return redirect(url_for("index"))#redireciona para a rota
            else:
                flash("Senha incorreta!")
        else:
            flash("Usuario inexistente!")

    return render_template('login.html', form = form)


@lm.user_loader
def load_user(id):  #função necessaria para o flask-login utilizar a parte de login, selecionando o usuario à utilizar a sessao
    return User.query.filter_by(id_ponto=id).first()


@app.route('/logout')
@login_required # rota necessita de estar logada
def logout():
    logout_user()
    return redirect(url_for("login"))

@lm.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))