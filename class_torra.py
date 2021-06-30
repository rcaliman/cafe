from parametros import parametros
from tools import UsaBD

class Torra:
    def __init__(self, cafe, temp_inicial, temp_final, piso, temp_json, fluxo_ar, velocidade_tambor, peso, data):
        self.cafe = cafe
        self.temp_inicial = temp_inicial
        self.temp_final = temp_final
        self.piso = piso
        self.temp_json = temp_json
        self.fluxo_ar = fluxo_ar
        self.velocidade_tambor = velocidade_tambor
        self.peso = peso
        self.data = data
        
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
            'data': self.data}
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
                data_torra
                )values(
                    '{self.cafe}',
                    '{self.temp_inicial}',
                    '{self.temp_final}',
                    '{self.piso}',
                    '{self.temp_json}',
                    '{self.fluxo_ar}',
                    '{self.velocidade_tambor}',
                    '{self.peso}',
                    '{self.data}'
                )"""
            cursor.execute(_SQL)
            
def select_torras():
    with UsaBD(parametros) as cursor:
        _SQL = """select * from torra;"""
        cursor.execute(_SQL)
        torras = cursor.fetchall()
    return torras