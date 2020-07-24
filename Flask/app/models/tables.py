from app import db
from datetime import datetime as dt,time

class User(db.Model):
    __tablename__ = "users" #titutlo da tabela

    #id              = db.Column(db.Integer,autoincrement=True)
    id_ponto        = db.Column(db.Integer, primary_key=True,autoincrement=False)
    nome            = db.Column(db.String(255),nullable=False)
    documento       = db.Column(db.String(255),nullable=False)
    data_admissao	= db.Column(db.Date(),nullable=False)
    func			= db.Column(db.String(255),nullable=False)
    entrada			= db.Column(db.Time(),nullable=False)
    saida			= db.Column(db.Time(),nullable=False)
    dia_folga		= db.Column(db.String(255),nullable=False)
    endereco		= db.Column(db.String(255),nullable=False)
    username		= db.Column(db.String(255),nullable=False,unique=True)
    senha			= db.Column(db.String(255),nullable=False)
    admin			= db.Column(db.Boolean(),nullable=False)

    def __init__(self,id_ponto,nome,documento,data_admissao,func,entrada,saida,dia_folga,endereco,username,senha,admin): #passar o que vamos receber para o construtor
        self.id_ponto      = id_ponto     
        self.nome          = nome 
        self.documento     = documento      
        self.data_admissao = data_admissao          
        self.func          = func 
        self.entrada       = entrada    
        self.saida         = saida  
        self.dia_folga     = dia_folga      
        self.endereco      = endereco     
        self.username      = username     
        self.senha         = senha  
        self.admin         = admin

    def is__valid(self):
        valida_tipos = ("id_ponto",int),("nome",str,255),("documento",str,255),("data_admissao",dt),("func",str,255),("entrada",time),("saida",time),("dia_folga",str,255),("endereco",str,255),("username",str,255),("senha",str,255),("admin",bool)

        for x in valida_tipos:
            if not isinstance(getattr(self,x[0]),x[1]):
                return False,f"campo {x[0]} com tipo invalido!"
            if x[1] is str and len(getattr(self,x[0])) > x[2]:
                return False,f"o campo '{x[0]}' exede o máximo permitido ({x[2]})"
            if len(x) == 4 and not getattr(self,x[0]) in x[3]:
                return False,f"o campo '{x[0]}' não esta entre os valores permitidos ({'-'.join(x[3])})"
        
        #valida id_ponto
        v1 = self.query.filter_by(id_ponto = self.id_ponto).first()
        if v1: return False,f"id_ponto '{self.id_ponto}' ja esta cadastrado no sistema!"

        v2 = self.query.filter_by(documento = self.documento).first()
        if v2: return False,f"documento '{self.documento}' ja esta cadastrado no sistema!"

        v3 = self.query.filter_by(username = self.username).first()
        if v3: return False,f"username '{self.username}' ja esta cadastrado no sistema!"

        return True,"OK"



    def __repr__(self):#uma forma bonitinha de exibir os registros
        return "<User %r>" % self.username
    

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id_ponto)






class Prestador(db.Model):
    __tablename__ = "prestador" #titutlo da tabela

    id		        = db.Column(db.Integer,primary_key = True)
    nome	        = db.Column(db.String(255),nullable=False)  		
    doc	            = db.Column(db.String(255),nullable=False)			
    empresa	        = db.Column(db.String(255),nullable=False)		
    tipo_servico    = db.Column(db.String(255),nullable=False)
    id_ponto 		= db.Column(db.Integer,db.ForeignKey('users.id_ponto'))
    user            = db.relationship("User",foreign_keys=id_ponto) #relaciona uma foregin key com a classe existente


    def __init__(self,nome,doc,empresa,tipo_servico,id_ponto): #passar o que vamos receber para o construtor
        self.nome          = nome 
        self.doc           = doc
        self.empresa       = empresa    
        self.tipo_servico  = tipo_servico         
        self.id_ponto      = id_ponto     

    def __repr__(self):#uma forma bonitinha de exibir os registros
        return "<Prestador %r>" % self.nome

class ControleAcesso(db.Model):
    __tablename__ = "controle_acesso" #titutlo da tabela

    id		        = db.Column(db.Integer,primary_key = True)
    id_prestador    = db.Column(db.Integer,db.ForeignKey('prestador.id'))
    apt             = db.Column(db.Integer,nullable = False)			
    h_entrada	    = db.Column(db.DateTime(),nullable=False )	
    h_saida 	    = db.Column(db.DateTime())	
    id_ponto_e 	    = db.Column(db.Integer,db.ForeignKey('users.id_ponto'))
    id_ponto_s 	    = db.Column(db.Integer,db.ForeignKey('users.id_ponto'))	

    prestador       = db.relationship("Prestador",foreign_keys=id_prestador)
    user_entrada    = db.relationship("User",foreign_keys=id_ponto_e)
    user_saida      = db.relationship("User",foreign_keys=id_ponto_s)


    def __init__(self,id_prestador,apt,h_entrada,h_saida,id_ponto_e,id_ponto_s): #passar o que vamos receber para o construtor
        self.id_prestador   =  id_prestador         
        self.apt            =  apt
        self.h_entrada      =  h_entrada      
        self.h_saida        =  h_saida    
        self.id_ponto_e     =  id_ponto_e       
        self.id_ponto_s     =  id_ponto_s         

    def __repr__(self):#uma forma bonitinha de exibir os registros
        return "<Controle %r>" % self.prestador.nome


    	