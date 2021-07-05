from tools import UsaBD
from parametros import parametros

class Cafe:
    def __init__(self, id=None, descricao=None, 
                 quantidade_comprada=None, data_compra=None, origem=None, estoque=None):
        self.id = id
        self.descricao = descricao
        self.quantidade_comprada = quantidade_comprada
        self.data_compra = data_compra
        self.origem = origem
        self.estoque = estoque
        
    def __str__(self):
        dic = {
            'descrição': self.descricao,
            'quantidade comprada': self.quantidade_comprada,
            'data da compra': self.data_compra,
            'origem': self.origem,
            'estoque': self.estoque
        }
        return str(dic)
    
    def insere_banco(self):
        with UsaBD(parametros) as cursor:
            _SQL = f"""insert into cafe(
                descricao,
                quantidade_comprada,
                data_compra,
                origem,
                estoque
                ) values (
                    '{self.descricao}',
                    '{self.quantidade_comprada}',
                    '{self.data_compra}',
                    '{self.origem}',
                    {self.estoque}
                );"""
            _SQL = _SQL.replace("''","NULL")
            cursor.execute(_SQL)
            
    def update_cafe(self):
        with UsaBD(parametros) as cursor:
            _SQL = f"""update cafe set
                descricao = '{self.descricao}',
                quantidade_comprada = '{self.quantidade_comprada}',
                data_compra = '{self.data_compra}',
                origem = '{self.origem}',
                estoque = {self.estoque}
                where id = {self.id};"""
            _SQL = _SQL.replace("''","NULL")
            cursor.execute(_SQL)
        
def apagar_cafe(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""delete from cafe where id={id};"""
        cursor.execute(_SQL)

def select_cafes():
    with UsaBD(parametros) as cursor:
        _SQL = """select * from cafe order by data_compra desc, id desc;"""
        cursor.execute(_SQL)
        cafes = cursor.fetchall()
    return cafes

def select_cafe(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select * from cafe where id = {id};"""
        cursor.execute(_SQL)
        cafe = cursor.fetchall()
    return cafe

def busca_descricao_cafe(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select descricao from cafe where id = {id};"""
        cursor.execute(_SQL)
        descricao = cursor.fetchall()
    return descricao[0][0]

def select_descricao_cafes(id_cafe):
    with UsaBD(parametros) as cursor:
        _SQL= f"""select id, substring(descricao, 1, 50) from cafe where id <> {id_cafe} and estoque = 1 order by data_compra desc;"""
        cursor.execute(_SQL)
        descricao_cafes = cursor.fetchall()
        if int(id_cafe) > 0:
            _SQL = f"""select id, substring(descricao, 1, 50) from cafe where id={int(id_cafe)}"""
            cursor.execute(_SQL)
            descricao_cafe_selecionado = cursor.fetchall()
            descricao = tuple(descricao_cafe_selecionado + descricao_cafes)
            select = """<select class="form-control" name="cafe" id="cafe">"""
        else:
            descricao = tuple(descricao_cafes)
            select = """<select class="form-control" name="cafe" id="cafe"><option>selecione um café</option>"""
        
        input = ''
        for cafe in descricao:
            input = input + f"""<option value={cafe[0]}>{cafe[1]}</option>"""
        
        select = select + input + "</select>"
        return select
