from parametros import parametros
from tools import UsaBD, json_para_dic

class Torra:
    def __init__(self, id=None, cafe=None, temp_inicial=None, temp_final=None, piso=None, temp_json=None,
                    fluxo_ar=None, velocidade_tambor=None, peso=None, data=None, observacoes=None):
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
                    observacoes = '{self.observacoes}' where id = {self.id};"""
            _SQL = _SQL.replace("''","NULL")
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

def apagar_torra(id):
    with UsaBD(parametros) as cursor:
        _SQL = f"""delete from torra where id = {id};"""
        cursor.execute(_SQL)

def json_torra(query):
    for item in query[0]:
        if 'bytes' in str(type(item)):
            dic = json_para_dic(item)
    return dic

def edit_gridform(id):

    tempgrid = json_torra(select_torra(id))

    input_grid = """
                    <section>
                        <div class='row justify-content-center' style='margin: 1em 0;'>
                        <div class='col-lg-3 col-md-5 col-sm-5 col-xs-5 bg-dark border-dark' style='border: 0 1em; margin: 0 auto; text-align: center;'>
                        <div id='inputFormRow'>
                        <div class='tempgrid mt-2'>
                            <h4 style='color:#fefefe'>grid</h4>
                        </div>
                  """
    cont = 0
    for a, b in tempgrid.items():
        input_grid = input_grid + f'''
                <input type="number" id="{a}" class='tempgrid' name="{a}" value="{b[0]}" autocomplete="off" style="width:4em;margin-right: 4em;">
            '''
        cont += 1
        x = str(cont)
    input_grid = input_grid + """
                        </div>
                        <div id='newRow'></div>
                            <button id='addRow' type='button' class='btn btn-outline-success btn-sm' style='width: 9em;'>
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
                        html += '<input type="number" name="tempgrid' + tempgrid + '" autocomplete="off" style="width:4em">';
                        html += '<button id="removeRow" type="button" class="btn btn-danger btn-sm" style="width:4em">X</button>';
                        html += '</div>';

                        $('#newRow').append(html);
                        $('html,body').animate({scrollTop: document.body.scrollHeight},"fast");
                    });
                    // remove row
                    $(document).on('click', '#removeRow', function () {
                        $(this).closest('#inputFormRow').remove();
                    });
                </script>
                    """ %(x)

    return input_grid