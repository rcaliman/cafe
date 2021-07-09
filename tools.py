import mysql.connector
import json
from parametros import parametros
from flask import session
from werkzeug.datastructures import ImmutableMultiDict
import pandas as pd
import matplotlib.pyplot as plt

class UsaBD:
    def __init__(self, config):
        self.config = config
    
    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    


class Login:
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha
        
    def confere(self):
        with UsaBD(parametros) as cursor:
            SQL = f"""select usuario, senha from usuarios where
                usuario='{self.usuario}' and senha='{self.senha}';"""
            cursor.execute(SQL)
            return cursor.fetchall()
        
        
def logado():
    logado = True if session['usuario'] else False
    return logado 

def monta_temp_json(request_form):
    dict = request_form.to_dict(flat=False)
    tempgrid0 = dict['temp_inicial']
    tempgrid = {'tempgrid0':tempgrid0}
    for a, b in dict.items():
        if 'tempgrid' in a:
            tempgrid[a] = b
    return json.dumps(tempgrid)

def json_para_dic(js):
    return json.loads(js)

