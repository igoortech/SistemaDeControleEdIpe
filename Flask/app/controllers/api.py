from flask import jsonify,request
from app import app,db
from app.models.tables import User,Prestador,ControleAcesso,Ponto,Mural # tabelas do sqlalchemy
from flask_login import login_required,current_user
from app.models.marshmallow import ContrAcessSchema,PrestadorSchema,UserSchema,PontoSchema,MuralSchema  #schemas do marshmallow 
from app.models.uteis import fields_required,mallowList,validate,admin_required  #uteis
from datetime import datetime as dt,date
from sqlalchemy import or_   #condição ou sqlalachmey
from sqlalchemy import Date, cast #cast converte uma string para formatdo valido de data
import json 


@app.route("/api/controle_acesso/<saida>") #nossa página principal
@login_required
def api(saida):

    if saida == "pendentes":
        lista = ControleAcesso.query.filter_by(h_saida=None).all()
    else:
        lista = ControleAcesso.query.order_by(ControleAcesso.id.desc()).all()

    formated = mallowList(ContrAcessSchema,lista) # tranforma o objeto banco de dados em uma lista de objetos
    
    return jsonify(formated)


@app.route("/api/controle_acesso",methods=["PUT","DELETE"]) #nossa página principal
@login_required
@fields_required(["id","id_prestador","apt","id_ponto_e","id_ponto_s","h_entradaf","h_saidaf"],methods=["PUT"])
@fields_required(["id_reg"],methods=["DELETE"],out="fields2")
def editControleAcesso(fields,fields2):

    if request.method == "PUT":
        if not validate(fields["h_entradaf"],"%d/%m/%Y %H:%M"): 
            return "Campo hora_entradaf no formato invalido, o formato permitido é 01/01/2020 00:00",400
        if not validate(fields["h_saidaf"],"%d/%m/%Y %H:%M"): 
            return "Campo hora_entradaf no formato invalido, o formato permitido é 01/01/2020 00:00",400

        registro = ControleAcesso.query.filter_by(id=fields["id"]).first()
        if registro:
            prestador = Prestador.query.filter_by(id=fields["id_prestador"]).first()
            if prestador:
                func_entrada = User.query.filter_by(id_ponto = fields["id_ponto_e"]).first()
                if func_entrada:
                    func_saida = User.query.filter_by(id_ponto = fields["id_ponto_s"]).first()
                    if func_saida:
                        registro.id_prestador = prestador.id
                        registro.apt = fields["apt"]
                        registro.id_ponto_e = func_entrada.id_ponto
                        registro.id_ponto_s = func_saida.id_ponto
                        registro.h_entrada = dt.strptime(fields["h_entradaf"],"%d/%m/%Y %H:%M")
                        registro.h_saida = dt.strptime(fields["h_saidaf"],"%d/%m/%Y %H:%M")
                        db.session.commit()
                        return "Registro alterado com sucesso!"
                    else:
                        return "Funcionario de saida não encontrado!",400
                else:
                    return "Funcionario de entrada não encontrado!",400
            else:
                return "Prestador não encontrado!",400
        else:
            return "Registro não encontrado!",400
    else:
        registro = ControleAcesso.query.filter_by(id=fields2["id_reg"]).first()
        if registro:
            db.session.delete(registro)
            db.session.commit()
            return "registro deletado com sucesso!"
        else:
            return "Registro não encontrado!",400



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
@login_required
def prestadores():

    lista = Prestador.query.all() # pega todos os dados do banco e joga na variavel
    
    formated = mallowList(PrestadorSchema,lista) # responsavel por transformar os objetos do banco em dicionarios

    return jsonify(formated)



@app.route("/api/user_atividades/<id_ponto>", methods=['GET']) #Atividades funcionários
@login_required
def atividades(id_ponto):

    lista = ControleAcesso.query.filter(or_(ControleAcesso.id_ponto_e == id_ponto, ControleAcesso.id_ponto_s == id_ponto)).all() # %% # pega todos os dados do banco e joga na variavel
    
    if lista:
        formated = mallowList(ContrAcessSchema,lista) # responsavel por transformar os objetos do banco em dicionarios

        return jsonify(formated)

    else:
        return "Atividades nao encontradas"


@app.route("/api/alterar_prestador",methods=["POST"]) #nossa página principal
@login_required
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




@app.route("/api/usuarios" , methods=['POST', 'GET','PUT']) #nossa página principal
@login_required
@admin_required(methods=['POST','PUT','GET'])
@fields_required(["id_ponto","nome","documento","data_admissao","func","entrada","saida","dia_folga","endereco","username","senha"],methods=["POST","PUT"])
def usuarios(fields):

    if request.method == 'GET':
        lista = User.query.all() # pega todos os dados do banco e joga na variavel
        
        formated = mallowList(UserSchema,lista) # responsavel por transformar os objetos do banco em dicionarios

        return jsonify(formated)

    else:
        if not validate(fields["data_admissao"],"%d/%M/%Y"): return "Campo data_admissao no formato invalido, o formato permitido é 01/01/2020",400
        if not validate(fields["entrada"],"%H:%M"): return "Campo entrada no formato invalido, o formato permitido é 00:00",400
        if not validate(fields["saida"],"%H:%M"): return "Campo saida no formato invalido, o formato permitido é 00:00",400

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
        status         = True

        if request.method == "POST":
            user           = User(id_ponto,nome,documento,data_admissao,func,entrada,saida,dia_folga,endereco,username,senha,admin,status)
            valida         = user.is__valid()
            if not valida[0]: return valida[1],400
            
            db.session.add(user)
        else:
            user = User.query.filter_by(id_ponto = fields["id_ponto"]).first()
            user.nome = nome
            user.documento = documento
            user.data_admissao = data_admissao
            user.func = func
            user.entrada = entrada
            user.saida = saida
            user.dia_folga = dia_folga
            user.username = username
            user.senha = senha
            admin = admin


        db.session.commit()
        return "Usuario cadastrado com sucesso!"
       

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
@login_required
@fields_required(["tipo"],methods=["POST"])
#@login_required
def ponto(fields):
    if request.method == "GET":
        if current_user.admin:
            registro_ponto = Ponto.query.all()
        else:
            registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).all()
        formated = mallowList(PontoSchema,registro_ponto)
        return jsonify(formated)
    else:

        #if request.remote_addr != app.config['IP_PERMITIDO']: #tras o ip do roteador
        if request.headers["X-Forwarded-For"] != app.config['IP_PERMITIDO']: #tras o ip do roteador do cliente que está acessando
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

   
@app.route("/ip")
def ip():
    return request.headers["X-Forwarded-For"]


@app.route("/api/mural", methods=['GET','POST','DELETE'])
@login_required
@admin_required(methods=["POST","DELETE"])
@fields_required(["titulo","mensagem","validade"], methods=['POST'])
@fields_required(["id"], methods=['DELETE'],out="fields2") #out renomeia fields para 2
def posta(fields,fields2):
    if request.method == 'POST':
        if not validate(fields["validade"],"%d/%m/%Y"): 
            return "Campo validade no formato invalido, o formato permitido é 01/01/2020",400

        validade = dt.strptime(fields["validade"],"%d/%m/%Y") #converte o campo string para o tipo data 

        registro = Mural(fields['titulo'],fields['mensagem'],validade)

        db.session.add(registro)
        db.session.commit()
        return "Mensagem postada com sucesso!"

    elif  request.method == 'DELETE':
        registro = Mural.query.get(fields2["id"])
        if registro:
            db.session.delete(registro)
            db.session.commit()
            return "Registtro deletado com sucesso!"
        else:
            return "Registro não encontrado!",400
    else:
#        registro = Mural.query.all()

        registro = Mural.query.filter(cast(Mural.validade,Date) >= date.today()).all() # cast significa converter

        formated = mallowList(MuralSchema,registro)
        return jsonify(formated)


@app.route("/api/status", methods=['POST'])
@login_required
@admin_required()
@fields_required(["id_ponto","status"], methods=['POST'])
def status(fields):
    func = User.query.filter_by(id_ponto = fields["id_ponto"]).first()
    if func:
        func.status = fields["status"]
        db.session.commit()
        return "status alterado com sucesso!"
    else:
        return "Funcionario nao encontrado!",400

