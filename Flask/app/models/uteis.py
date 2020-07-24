from flask import request
from functools import wraps
import json

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


def mallowList(schema,lista):
    sc = schema()
    return [json.loads(sc.dumps(x)) for x in lista if sc.dumps(x) != '{}']