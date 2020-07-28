from flask import request,render_template
from functools import wraps
import json
from flask_login import current_user
from app.models.tables import Ponto
from datetime import datetime as dt,date
from sqlalchemy import Date, cast

def fields_required(lista,methods="*"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            xstr = lambda s: s or ""
            contentJson = "json" in xstr(request.headers.get("Content-Type"))

            if methods == "*" or request.method in methods:
                if request.method == "GET":
                    fields = request.args.to_dict()
                elif request.method == "POST":
                    fields =  request.json if contentJson else request.form.to_dict()
                
                notfound = [x for x in lista if not x in fields]
                if notfound:
                    return "campos nao encontrados!:\n\t" + "\n\t".join(notfound),400

                result = function(fields=fields,*args, **kwargs)
                return result
            else:
                return function(fields=None,*args, **kwargs)

        return wrapper
    return decorator

def ponto_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not current_user.admin:
                registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).filter(cast(Ponto.entrada,Date) == date.today()).first()
                if not registro_ponto:
                    return render_template("baterPonto.html" ,user=current_user) #retorna a página de bater ponto se a entrada nao existir

            return function(*args, **kwargs) # vai pra proxima função

        return wrapper
    return decorator


def mallowList(schema,lista):
    sc = schema()
    return [json.loads(sc.dumps(x)) for x in lista if sc.dumps(x) != '{}']