from flask import request,render_template
from functools import wraps
import json
from flask_login import current_user
from app.models.tables import Ponto,Mural
from datetime import datetime as dt,date
from sqlalchemy import Date, cast


def fields_required(lista,methods="*",out="fields"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            xstr = lambda s: s or ""
            contentJson = "json" in xstr(request.headers.get("Content-Type"))

            if methods == "*" or request.method in methods:
                if request.method == "GET":
                    fields = request.args.to_dict()
                elif request.method in ["POST","PUT","DELETE","DEL"]:
                    fields =  request.json if contentJson else request.form.to_dict()
                
                notfound = [x for x in lista if not x in fields]
                if notfound:
                    return "campos nao encontrados!:\n\t" + "\n\t".join(notfound),400

                kwargs[out] = fields
                result = function(*args, **kwargs)
                return result
            else:
                kwargs[out] = []
                return function(*args, **kwargs)

        return wrapper
    return decorator

def ponto_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not current_user.admin: #senão for admin...
                registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).filter(cast(Ponto.entrada,Date) == date.today()).first()
                if not registro_ponto:
                    registro = Mural.query.filter(cast(Mural.validade,Date) >= date.today()).all()
                    return render_template("baterPonto.html" ,user=current_user,mural=registro) #retorna a página de bater ponto se a entrada nao existir

            return function(*args, **kwargs) # vai pra proxima função

        return wrapper
    return decorator

def admin_required(methods="*"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not current_user.admin:
                if methods == "*":
                    return "Usuario nao permitido para fazer este tipo de requisição",400
                else:
                    if request.method in methods:
                        return "Usuario nao permitido para fazer este tipo de requisição",400

            return function(*args, **kwargs) # vai pra proxima função
        return wrapper
    return decorator



def mallowList(schema,lista):#coverte dados da api para formtado jdson
    sc = schema()
    return [json.loads(sc.dumps(x)) for x in lista if sc.dumps(x) != '{}']

def validate(date_text,formt): #valida formato de data
    try:
        dt.strptime(date_text, formt)
        return True
    except ValueError:
        return  False