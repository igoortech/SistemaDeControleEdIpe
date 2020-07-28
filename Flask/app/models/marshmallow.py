from app import ma
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


class UserSchema(ModelSchema):
    id_ponto        = fields.Integer() 
    nome            = fields.String()
    documento       = fields.String()
    data_admissao	= fields.Date()
    func			= fields.String()
    entrada			= fields.Time()
    saida			= fields.Time()
    dia_folga		= fields.String()
    endereco		= fields.String()
    username		= fields.String()
    senha			= fields.String()
    admin			= fields.Boolean()


class PrestadorSchema(ma.ModelSchema):
    id		        = fields.Integer()
    nome	        = fields.String() 		
    doc	            = fields.String()			
    empresa	        = fields.String()		
    tipo_servico    = fields.String()
    id_ponto 		= fields.Integer()
    user            = fields.Nested(UserSchema)


class ContrAcessSchema(ma.ModelSchema):
    id              = fields.Integer() 
    id_prestador    = fields.Integer()     
    apt             = fields.Integer()
    h_entrada       = fields.DateTime(format='%d/%m %H:%M')
    h_saida         = fields.DateTime(format='%d/%m %H:%M')
    id_ponto_e      = fields.Integer()
    id_ponto_s      = fields.Integer()
    prestador       = fields.Nested(PrestadorSchema) 
    user_entrada    = fields.Nested(UserSchema) 
    user_saida      = fields.Nested(UserSchema)


class PontoSchema(ma.ModelSchema):
    id              = fields.Integer() 
    id_ponto        = fields.Integer()     
    entrada         = fields.DateTime(format='%d/%m-%H:%M')
    saida_a         = fields.DateTime(format='%d/%m-%H:%M')
    volta_a         = fields.DateTime(format='%d/%m-%H:%M')
    saida           = fields.DateTime(format='%d/%m-%H:%M')
    user            = fields.Nested(UserSchema) 


