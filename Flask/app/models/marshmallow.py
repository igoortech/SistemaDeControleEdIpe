from app import ma
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class UserSchema(ModelSchema):
    id_ponto        = fields.Integer() 
    nome            = fields.String()
    documento       = fields.String()
    data_admissao	= fields.Date(format='%d/%m/%Y')
    func			= fields.String()
    entrada			= fields.Date(format='%H:%M')
    saida			= fields.Date(format='%H:%M')
    dia_folga		= fields.String()
    endereco		= fields.String()
    username		= fields.String()
    senha			= fields.String()
    admin			= fields.Boolean()
    status			= fields.Boolean()


class PrestadorSchema(ModelSchema):
    id		        = fields.Integer()
    nome	        = fields.String() 		
    doc	            = fields.String()			
    empresa	        = fields.String()		
    tipo_servico    = fields.String()
    id_ponto 		= fields.Integer()
    user            = fields.Nested(UserSchema)


def formata(value):
    if value.h_saida is None: return None
    return  value.h_saida.strftime("%d/%m/%Y %H:%M")

class ContrAcessSchema(ModelSchema):
    id              = fields.Integer() 
    id_prestador    = fields.Integer()     
    apt             = fields.Integer()
    h_entrada       = fields.DateTime(format='%d/%m %H:%M')
    h_saida         = fields.DateTime(format='%d/%m %H:%M')
    h_entradaf      = fields.Function(lambda obj: obj.h_entrada.strftime("%d/%m/%Y %H:%M"))
    h_saidaf        = fields.Function(formata)
    id_ponto_e      = fields.Integer()
    id_ponto_s      = fields.Integer()
    prestador       = fields.Nested(PrestadorSchema) 
    user_entrada    = fields.Nested(UserSchema) 
    user_saida      = fields.Nested(UserSchema)




class PontoSchema(ModelSchema):
    id              = fields.Integer() 
    id_ponto        = fields.Integer()     
    data_entrada    = fields.Function(lambda obj: obj.entrada.strftime("%d/%m/%Y"))
    entrada         = fields.DateTime(format='%d/%m-%H:%M')
    saida_a         = fields.DateTime(format='%d/%m-%H:%M')
    volta_a         = fields.DateTime(format='%d/%m-%H:%M')
    saida           = fields.DateTime(format='%d/%m-%H:%M')
    user            = fields.Nested(UserSchema)



class MuralSchema(ModelSchema):
    id		        = fields.Integer()
    titulo	        = fields.String() 		
    mensagem	    = fields.String()			
    validade        = fields.Date()		
  