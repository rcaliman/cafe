from parametros import parametros
from tools import UsaBD, json_para_dic
import matplotlib.pyplot as plt
import json

class Torra:
    def __init__(self, id=None, cafe=None, temp_inicial=0, temp_final=0, piso=0, temp_json=None,
                    fluxo_ar=0, velocidade_tambor=0, peso=0, data='1900-01-01', observacoes=None, usuario=None):
        self.id = id
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
        self.usuario = usuario
        
    def __str__(self):
        dic = {
            'id': self.id,
            'cafe': self.cafe,
            'temperatura inicial': self.temp_inicial,
            'temperatura final': self.temp_final,
            'piso': self.piso,
            'grid de temperatura': self.temp_json,
            'fluxo de ar': self.fluxo_ar,
            'velocidade do tambor': self.velocidade_tambor,
            'peso': self.peso,
            'data': self.data,
            'observacoes': self.observacoes,
            'usuario': self.usuario,
            }
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
                observacoes,
                usuario
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
                    '{self.observacoes}',
                    {self.usuario}
                );"""
            _SQL = _SQL.replace("''","NULL")
            cursor.execute(_SQL)
            
    def update_torra(self):
        with UsaBD(parametros) as cursor:
            _SQL = f"""update torra set
                    id_cafe = '{self.cafe}',
                    temp_inicial = '{self.temp_inicial}',
                    temp_final = '{self.temp_final}',
                    temp_piso = '{self.piso}',
                    temp_minutos =  '{self.temp_json}',
                    fluxo_ar = '{self.fluxo_ar}',
                    velocidade_tambor = '{self.velocidade_tambor}',
                    peso = '{self.peso}',
                    data_torra = '{self.data}',
                    observacoes = '{self.observacoes}',
                    usuario = {self.usuario} 
                where id = {self.id};"""
            _SQL = _SQL.replace("''","NULL")
            cursor.execute(_SQL)
            
def select_torras(ord, asc, usuario):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select id,
                id_cafe,
                temp_inicial,
                temp_final,
                temp_piso,
                temp_minutos,
                fluxo_ar,
                velocidade_tambor,
                peso,
                DATE_FORMAT(data_torra,'%d-%m-%Y'),
                observacoes 
            from torra where usuario = {usuario} order by {ord} {asc};"""
        cursor.execute(_SQL)
        torras = cursor.fetchall()
    return torras

def select_torra(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select id,
                id_cafe,
                temp_inicial,
                temp_final,
                temp_piso,
                temp_minutos,
                fluxo_ar,
                velocidade_tambor,
                peso,
                DATE_FORMAT(data_torra,'%d-%m-%Y'),
                observacoes
            from torra where id = {id};"""
        cursor.execute(_SQL)
        torra = cursor.fetchall()
    return torra

def apagar_torra(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""delete from torra where id = {id};"""
        cursor.execute(_SQL)

def temperatura_inicial(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""select temp_inicial from torra where id = {id};"""
        cursor.execute(_SQL)
        temp_inicial = cursor.fetchall()
    return temp_inicial[0][0]

def json_torras(ids):
    ids = str(ids).replace('[','')
    ids = ids.replace(']','')
    with UsaBD(parametros) as cursor:
        _SQL = f"""select temp_minutos from torra where id in ({ids}) order by id;"""
        cursor.execute(_SQL)
        json_torras = cursor.fetchall()
    return json_torras

def js_torra(ids):
    array = []
    try:
        for i in json.loads(json_torras(ids)[0][0]).values():
            array.append(int(i[0]))
        js = f"""var temperaturas = {array};"""
    except:
        js = """var temperaturas = []"""      
    return js
   

def html_select_id():
    with UsaBD(parametros) as cursor:
        _SQL = 'select id from torra order by id desc'
        cursor.execute(_SQL)
        torra_ids = cursor.fetchall()
        select = """<select title='se quiser, selecione a torra que servirá de referencia' 
                        class='form-select-lg' name='torra_ids' id='torras_ids'><option>base</option>"""    
        for i in torra_ids:
            select = select + f"""<option value='{i[0]}'>torra {i[0]}</option>"""
        select = select + """</select>"""
        return select

def grafico_torras(json_torras, path_grafico, ids):
    try:
        plt.rcParams['figure.figsize'] = (13,6.5)
        axes = plt.gca()
        if ids != 0: # quando envio o zero digo que o gráfico só terá uma linha e não precisa de legenda
            ids = sorted(list(ids))
        axes.yaxis.grid(b=True, color='black', alpha=0.3, linestyle='-.', linewidth=1)
        tempomaximo = 0
        for json_torra in json_torras:
            for json_temperaturas in json_torra:
                dict_temperaturas = json.loads(json_temperaturas).values()
                lista_temperaturas = []
                for i in dict_temperaturas:
                    if len(dict_temperaturas) > tempomaximo:
                        tempomaximo = len(dict_temperaturas) # achar a torra mais longa para definir o tamanho do grafico
                    i[0]= float(i[0])
                    lista_temperaturas.append(i[0])
                sticks = list(range(0,tempomaximo))
                plt.xticks(sticks)
                plt.style.use('seaborn-darkgrid')
                plt.xticks(sticks)
                plt.xlabel('minutos')
                plt.ylabel('temperatura')
                try:
                    plt.plot(lista_temperaturas, linewidth=2, label=ids.pop(0))
                except:
                    plt.plot(lista_temperaturas, linewidth=2)
                plt.legend()
                plt.savefig(path_grafico,transparent=True)
        plt.close()
    except:
        plt.figure()
        plt.savefig(path_grafico,transparent=True)
        plt.close()
 
        

def edit_gridform(id):
    tempgrid = json.loads(json_torras(id)[0][0])
    input_grid = """
                    <section>
                        <div class='row justify-content-center' style='margin: 1em 0;'>
                        <div class='inputGrid' style='margin: 0 auto; text-align: center;'>                        
                        <div id='inputFormRow'>
                        <div class='tempgrid mt-2'>
                            <h5 style='color: #e6e6fa'>GRID</h5>
                        </div>
                  """
    cont = 0
    for a, b in tempgrid.items():
        input_grid = input_grid + f'''
                <input type="number" step='0.01' id="{a}" class='inputGrid' name="{a}" value="{b[0]}" autocomplete="off" style="width:4em;margin-right: 5px;">
                <div class="btn btn-danger btn-md" style="width:5em;cursor:default;opacity:60%">{cont}</div><br>
            '''
        cont += 1
        x = str(cont)
    input_grid = input_grid + """
                        </div>
                        <div id='newRow'></div>
                            <button id='addRow' type='button' class='btn btn-lg btn-outline-light btn-lg' style='width: 9em;'>
                              ✚
                            </button>
                        </div>
                    </div>
                </section>
                <script type="text/javascript">
                    // add row
                    var tempgrid = %s;
                    $("#addRow").click(function () {
                        var html = '';
                        tempgrid += 1
                        html += '<div id="inputFormRow">';
                        html += '<input type="number" step="0.01" class="inputGrid" name="tempgrid' + tempgrid + '" autocomplete="off" style="width:4em">';
                        html += '<button id="removeRow" type="button" title="apaga o campo ' + tempgrid +'" class="btn btn-danger btn-md" style="width:5em">' + tempgrid + '</button>';
                        html += '</div>';

                        $('#newRow').append(html);
                        $('html,body').animate({scrollTop: document.body.scrollHeight},"fast");
                        $("form").find("input:last").focus()
                    });
                    // remove row
                    $(document).on('click', '#removeRow', function () {
                        $(this).closest('#inputFormRow').remove();
                    });
                    document.querySelector('#form-torra').addEventListener('keypress', function (e) {
                        if (e.key === 'Enter') {
                            $('#addRow').click();
                            event.preventDefault();
                        }
                    });
                </script>
                    """ %(x)

    return input_grid