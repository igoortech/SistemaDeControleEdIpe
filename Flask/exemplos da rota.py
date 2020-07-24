from app import app #do módulo app(pasta), import a variável #app

@app.route("/index")
@app.route("/") #rota
def index():
    return "<h1>MEu amor foi buscar minha janta, teste! <h1>"


@app.route("/teste")
def teste():
    return "<h2> O segundo teste do meu amor</h2>"

@app.route("/cadastrar")
@app.route("/cadastrar/<name>") #variavel que recebe o que é digitado
def cadastrar(name=None):#variavel sendo passada como parametro #paradrão se não for digitado nada, é none
    if name:
        return "<h2>Olá , %r!</h2>" % name
    else:
        return "<h2>Olá usuário!</h2>"  

@app.route("/rodadeinteiro")
@app.route("/rodadeinteiro/<int:id>")
def inteiros(id=None):
    if id:
        return "Este número é, %s "  %id
    else:
        return "Nenhum inteiro foi digitado!"

@app.route("/test/", methods=['GET']) #limitar os metodos que podem acontecer na pagina.
def test():
    return "teste metodos"

