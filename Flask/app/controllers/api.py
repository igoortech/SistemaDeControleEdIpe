from flask import jsonify,request
from app import app,db
from app.models.tables import User,Prestador,ControleAcesso,Ponto # tabelas do sqlalchemy
from flask_login import login_required,current_user
from app.models.marshmallow import ContrAcessSchema,PrestadorSchema,UserSchema,PontoSchema  #schemas do marshmallow 
from app.models.uteis import fields_required,mallowList  #uteis
from datetime import datetime as dt,date
from sqlalchemy import Date, cast
import json 


@app.route("/api/controle_acesso/<saida>") #nossa página principal
@login_required
def api(saida):
    sc = ContrAcessSchema()

    if saida == "pendentes":
        lista = ControleAcesso.query.filter_by(h_saida=None).all()
    else:
        lista = ControleAcesso.query.order_by(ControleAcesso.id.desc()).all()

    formated = [json.loads(sc.dumps(x)) for x in lista] # tranforma o objeto banco de dados em uma lista de objetos
    
    return jsonify(formated)


@app.route("/api/add_registro",methods=["POST"]) #nossa página principal
@login_required
@fields_required(["Documento","Destino"])
def add_registro(fields):
    prest = Prestador.query.filter_by(doc = fields["Documento"]).first()
    if prest:
        id_prestador    = prest.id
        apt             = fields["Destino"]
        h_entrada       = dt.now()
        id_ponto_e      = current_user.id_ponto
        registro        = ControleAcesso(id_prestador = id_prestador,h_entrada=h_entrada,h_saida=None,id_ponto_e=id_ponto_e,id_ponto_s=None,apt=apt)
        db.session.add(registro)
        db.session.commit()
        return "Registro cadastrado com sucesso!"
    else:
        return "prestador nao encontrado",400



@app.route("/api/prestadores") #nossa página principal
def prestadores():

    lista = Prestador.query.all() # pega todos os dados do banco e joga na variavel
    
    formated = mallowList(PrestadorSchema,lista) # responsavel por transformar os objetos do banco em dicionarios

    return jsonify(formated)


@app.route("/api/alterar_prestador",methods=["POST"]) #nossa página principal
@fields_required(["doc","empresa","id","nome","tipo_servico"])  #campos obrigatórios
def alterar_prestador(fields):

    id              = fields["id"]
    empresa         = fields["empresa"]
    doc             = fields["doc"]
    nome            = fields["nome"]
    tipo_servico    = fields["tipo_servico"]

    prestador = Prestador.query.filter_by(id=id).first() # encontra o prestador com o id certo
    if prestador:
        prestador.id_ponto = current_user.id_ponto
        prestador.nome = nome
        prestador.doc = doc
        prestador.empresa = empresa
        prestador.tipo_servico = tipo_servico
        db.session.commit()
        return "Dados alterados com successo!"
    else:
        return "Prestador nao encontrado",400




@app.route("/api/usuarios" , methods=['POST', 'GET']) #nossa página principal
@fields_required(["id_ponto","nome","documento","data_admissao","func","entrada","saida","dia_folga","endereco","username","senha"],methods=["POST"])
def usuarios(fields):
    print(fields["admin"])
    if request.method == 'GET':
        lista = User.query.all() # pega todos os dados do banco e joga na variavel
        
        formated = mallowList(UserSchema,lista) # responsavel por transformar os objetos do banco em dicionarios

        return jsonify(formated)
    else:
        id_ponto       = fields["id_ponto"]     
        nome           = fields["nome"] 
        documento      = fields["documento"]      
        data_admissao  = dt.strptime(fields["data_admissao"],"%d/%M/%Y")          
        func           = fields["func"] 
        entrada        = dt.strptime(fields["entrada"],"%H:%M").time() 
        saida          = dt.strptime(fields["saida"],"%H:%M").time()   
        dia_folga      = fields["dia_folga"]      
        endereco       = fields["endereco"]     
        username       = fields["username"]     
        senha          = fields["senha"]  
        admin          = False

        user           = User(id_ponto,nome,documento,data_admissao,func,entrada,saida,dia_folga,endereco,username,senha,admin)
        valida         = user.is__valid()
        if not valida[0]: return valida[1],400
        
        db.session.add(user)
        db.session.commit()
        return "Usuario cadastrado com sucesso!"
    return "asdasd"
       

#dt.strptime(date,"%d/%M/%Y")



@app.route("/api/darsaida",methods=["POST"])
@login_required
@fields_required(["id_controle_acesso"])
def darSaida(fields):

    registro = ControleAcesso.query.filter_by(id=fields["id_controle_acesso"]).first()
    if registro:
        registro.h_saida = dt.now()
        registro.id_ponto_s = current_user.id_ponto
        db.session.commit()
        return "Saída realizada com sucesso!"
    else:
        return "Registro nao encontrado na base de dados!",400



@app.route("/api/ponto", methods=["GET" , "POST"])
@fields_required(["tipo"],methods=["POST"])
#@login_required
def ponto(fields):
    if request.method == "GET":
        registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).all()
        formated = mallowList(PontoSchema,registro_ponto)
        return jsonify(formated)
    else:

        if request.remote_addr != app.config['IP_PERMITIDO']: #tras o ip do roteador
        #if request.headers["X-Forwarded-For"] != app.config['IP_PERMITIDO']: #tras o ip do roteador do cliente que está acessando
            return "Rede local nao permitida para realizar esta operação!",400


        registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).filter(cast(Ponto.entrada,Date) == date.today()).first() #valida se a dar de hoje
        #for igual a hoje 

        if fields["tipo"] == "entrada":
            if registro_ponto: return "já existe uma entrada para o dia de hoje!",400
            pt = Ponto(current_user.id_ponto,dt.now(),None,None,None)
            db.session.add(pt)
            #return PontoSchema().dumps(registro_ponto[0])

        elif fields["tipo"] == "saida_a":
            if registro_ponto and registro_ponto.saida_a != None : return "ponto já batido para este dia!",400
            if not registro_ponto: return "Primeiro bata o ponto de entrada",400  
            
            registro_ponto.saida_a = dt.now()

        elif fields["tipo"] == "volta_a":
            if registro_ponto and registro_ponto.volta_a != None : return "ponto já batido para este dia!",400
            if not registro_ponto: return "Primeiro bata o ponto de entrada",400  
            if registro_ponto.saida_a == None: return "Primeiro bata o ponto de saida para almoço!",400

            registro_ponto.volta_a = dt.now()

        elif fields["tipo"] == "saida":
            if registro_ponto and registro_ponto.saida != None : return "ponto já batido para este dia!",400
            if not registro_ponto: return "Primeiro bata o ponto de entrada",400
            
            registro_ponto.saida = dt.now()

        db.session.commit()
        return "Registro salvo com sucesso!"

       # registro_ponto = Ponto.query.filter_by(id_ponto=1).filter(cast(Ponto.entrada,Date) == date.today()).all()
        #if registro_ponto:
            #if fields["tipo"] == "entrada":
            #    return "já existe uma entrada para o dia de hoje!"
           # elif fields["tipo"] == "saida_a" and registro_ponto.saida_a 
        
   
@app.route("/ip")
def ip():
    return request.remote_addr


