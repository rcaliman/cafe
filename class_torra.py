from parametros import parametros
from tools import UsaBD, json_para_dic

class Torra:
    def __init__(self, cafe, temp_inicial, temp_final, piso, temp_json, fluxo_ar, velocidade_tambor, peso, data, observacoes):
        self.cafe = cafe
        self.temp_inicial = temp_inicial
        self.temp_final = temp_final
        self.piso = piso
        self.temp_json = temp_json
        self.fluxo_ar = fluxo_ar
        self.velocidade_tambor = velocidade_tambor
        self.peso = peso
        self.data = data
        self.observacoes = observacoes
        
    def __str__(self):
        dic = {
            'cafe': self.cafe,
            'temperatura inicial': self.temp_inicial,
            'temperatura final': self.temp_final,
            'piso': self.piso,
            'grid de temperatura': self.temp_json,
            'fluxo de ar': self.fluxo_ar,
            'velocidade do tambor': self.velocidade_tambor,
            'peso': self.peso,
            'data': self.data,
            'observacoes': self.observacoes}
        return str(dic)
    
    def insere_banco(self):
        with UsaBD(parametros) as cursor:
            _SQL = f"""insert into torra(
                id_cafe,
                temp_inicial,
                temp_final,
                temp_piso,
                temp_minutos,
                fluxo_ar,
                velocidade_tambor,
                peso,
                data_torra,
                observacoes
                )values(
                    '{self.cafe}',
                    '{self.temp_inicial}',
                    '{self.temp_final}',
                    '{self.piso}',
                    '{self.temp_json}',
                    '{self.fluxo_ar}',
                    '{self.velocidade_tambor}',
                    '{self.peso}',
                    '{self.data}',
                    '{self.observacoes}'
                );"""
            cursor.execute(_SQL)
            
def select_torras():
    with UsaBD(parametros) as cursor:
        _SQL = """select * from torra order by data_torra desc, id desc;"""
        cursor.execute(_SQL)
        torras = cursor.fetchall()
    return torras

def select_torra(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select * from torra where id = {id};"""
        cursor.execute(_SQL)
        torra = cursor.fetchall()
    return torra


def json_torra(query):
    for item in query[0]:
        if 'bytes' in str(type(item)):
            dic = json_para_dic(item)
    return dic