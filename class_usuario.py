from tools import UsaBD
from parametros import parametros

def usuario_id(usuario):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select id from usuarios where usuario = '{usuario}';"""
        cursor.execute(_SQL)
        usuario_id = cursor.fetchall()
    return int(usuario_id[0][0])
    
    