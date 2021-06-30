from tools import UsaBD
from parametros import parametros

class Cafe:
    def __init__(self, descricao, quantidade_comprada, data_compra, origem):
        self.descricao = descricao
        self.quantidade_comprada = quantidade_comprada
        self.data_compra = data_compra
        self.origem = origem
        
    def __str__(self):
        dic = {
            'descrição': self.descricao,
            'quantidade comprada': self.quantidade_comprada,
            'data da compra': self.data_compra,
            'origem': self.origem
        }
        return str(dic)
    
    def insere_banco(self):
        with UsaBD(parametros) as cursor:
            _SQL = f"""insert into cafe(
                descricao,
                quantidade_comprada,
                data_compra,
                origem
                ) values (
                    '{self.descricao}',
                    '{self.quantidade_comprada}',
                    '{self.data_compra}',
                    '{self.origem}'
                );"""
            cursor.execute(_SQL)
        


def select_cafes():
    with UsaBD(parametros) as cursor:
        _SQL = """select * from cafe;"""
        cursor.execute(_SQL)
        cafes = cursor.fetchall()
    return cafes

def select_descricao_cafes():
    with UsaBD(parametros) as cursor:
        _SQL= """select id, substring(descricao, 1, 50) from cafe;"""
        cursor.execute(_SQL)
        descricao_cafes = cursor.fetchall()
    return descricao_cafes
        