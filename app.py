from flask import Flask, request, render_template, session, redirect
from tools import Login, logado, monta_temp_json, inverte_data_query, data_hoje
from werkzeug.datastructures import ImmutableMultiDict
from class_usuario import usuario_id
from class_torra import Torra, select_torras, select_torra, apagar_torra, edit_gridform, \
    json_torras, grafico_torras, js_torra, html_select_id
from class_cafe import Cafe, select_cafes, select_cafe, select_descricao_cafes, apagar_cafe, busca_descricao_cafe, busca_descricao_cafes
import json
import random
import logging

app = Flask(__name__)

app.secret_key = 'frase secretissima'

@app.route('/') # pagina inicial
def inicio():
    try:
        usuario = session['usuario']
        return render_template('inicio.html',
                               usuario = usuario)
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return redirect('/form_login',302)

@app.route('/form_login') # formulário de login
def form_login():
    return render_template('form_login.html')

@app.route('/logar', methods=['POST']) # autenticar usuario e setar sessão
def logar():
    usuario = request.form['usuario'].strip()
    senha = request.form['senha'].strip()
    if Login(usuario,senha).confere():
        session['usuario'] = usuario
        session['cafe_limite'] = 15
        session['torra_limite'] = 15
        return render_template('inicio.html')
    else:
        return form_login()
    
@app.route('/cafes', methods=['GET','POST']) # mostra a lista de cafés comprados
def cafes():
    try:
        if logado():
            ord = request.values.get('ord') or 'id'
            asc = request.values.get('asc_desc') or 'desc'
            usuario = usuario_id(session['usuario'])
            
            if request.values.get('mostra_cafes') == 'todos':
                session['cafe_limite'] = 1000000
            if request.values.get('mostra_cafes') == 'primeiros':
                session['cafe_limite'] = 15

            if request.values.get('asc_desc') == 'asc':
                asc_desc = 'desc'
            else:
                asc_desc = 'asc'

            return render_template(
                'cafes.html',
                cafes = select_cafes(ord, asc, usuario),
                asc_desc = asc_desc,
            )
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()
    
@app.route('/form_cafe') #formulario para fazer o cadastro dos cafés
def form_cafe():
    try:
        if logado():
            try:
                if request.values.get('id'):
                    id = int(request.values.get('id'))
                    cafe = select_cafe(id)
                    return render_template(
                        'form_cafe.html',
                        id = id,
                        cafe = cafe,
                    )
                else:
                    return render_template(
                        'form_cafe.html',
                        data_hoje = data_hoje(),
                    )
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return cafes()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/insere_cafe',methods=['GET','POST']) # action do formulario de cadastro de cafés
def insere_cafe():
    try:
        if logado():
            if request.form:
                try:
                    cafe = Cafe(
                        None,
                        request.form['descricao'],
                        request.form['quantidade'],
                        request.form['data_compra'],
                        request.form['origem'],
                        request.form['estoque'],
                        usuario_id(session['usuario'])
                    )
                    cafe.insere_banco()
                    return redirect('/cafes',302)
                except Exception:
                    logging.exception('ERRO APP CAFES E TORRRAS')
                    return form_cafe()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()
    
@app.route('/update_cafe',methods=['GET','POST']) # action do formulário de atualizacao de cafés
def update_cafe():
    try:
        if logado():
            try:
                if request.form:
                    cafe = Cafe(
                        request.form['id'],
                        request.form['descricao'],
                        request.form['quantidade'],
                        request.form['data_compra'],
                        request.form['origem'],
                        request.form['estoque'],
                        usuario_id(session['usuario'])
                    )
                    cafe.update_cafe()
                    return redirect('/cafes',302)
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return cafes()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/apaga_cafe', methods=['GET','POST']) # action para apagar um café do banco
def apaga_cafe():
    try:
        if logado():
            try:
                id = int(request.values.get('id'))
                apagar_cafe(id)
                return redirect('/cafes',302)
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return cafes()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/torras', methods=['GET','POST']) # tabela com torras já feitas
def torras():
    try:
        if logado():
            try:
                ord = request.values.get('ord') or 'id'
                asc = request.values.get('asc_desc') or 'desc'
                usuario = usuario_id(session['usuario'])
                select = html_select_id()
                
                if request.values.get('asc_desc') == 'asc':
                    asc_desc = 'desc'
                else:
                    asc_desc = 'asc'
                    
                if request.values.get('mostra_torras') == 'todas':
                    session['torra_limite'] = 1000000
                if request.values.get('mostra_torras') == 'primeiras':
                    session['torra_limite'] = 15
                    
                return render_template(
                    'torras.html',
                    torras = select_torras(ord,asc, usuario),
                    descricao_cafes = busca_descricao_cafes(),
                    ord = ord,
                    asc_desc = asc_desc,
                    select = select,
                )
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return inicio()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()
    
@app.route('/torra', methods=['GET','POST']) # tabela com os dados de uma torra específica
def torra():
    try:
        if logado():
            try:
                id = request.values.get('id')
                torra = select_torra(id)
                id_cafe = torra[0][1]
                descricao_cafe = busca_descricao_cafe(id_cafe) 
                grid_torra = json.loads(json_torras(id)[0][0])
                path_grafico = 'static/img/grafico.png'
                plot = grafico_torras(json_torras(id),path_grafico, 0)
                randomico = random.randrange(1,1000)
                return render_template(
                    'torra.html',
                    torra = torra,
                    grid_torra = grid_torra,
                    plot = plot,
                    id = id,
                    descricao_cafe = descricao_cafe[0][0],
                    randomico = randomico,
                )
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return torras()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()
    
@app.route('/form_torra', methods=['GET','POST']) # formulário para cadastrar uma torra
def form_torra():
    try:
        if logado():
            try:
                ids = request.form['torra_ids']
                print(len(ids))
                try:
                    torra = select_torra(ids)[0]
                except:
                    torra = []
                return render_template('form_torra.html',
                    select_cafes = select_descricao_cafes(0),
                    js = js_torra(ids), 
                    torra = torra,
                    data_hoje = data_hoje()                   
                )
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return torras()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/insere_torra', methods=['GET','POST']) # action do formulário de inserir nova torra
def insere_torra():
    try:
        if logado():
            try:
                if request.form:
                    torra = Torra(
                        None,
                        request.form['cafe'],
                        request.form['temp_inicial'],
                        request.form['temp_final'],
                        request.form['piso'],
                        monta_temp_json(request.form),
                        request.form['fluxo_ar'],
                        request.form['velocidade_tambor'],
                        request.form['peso'],
                        request.form['data'],
                        request.form['observacoes'],
                        usuario_id(session['usuario']))
                    torra.insere_banco()
                    return redirect('/torras',302)
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return torras()    
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/edita_torra') # formulário para editar uma torra já feita
def edita_torra():
    try:
        if logado():
            try:
                id = int(request.values.get('id'))
                torra = select_torra(id)
                id_cafe = torra[0][1]
                grid_torra = edit_gridform(id)
                select_cafes = select_descricao_cafes(id_cafe)
                return render_template('edita_torra.html',
                    torra = torra,  
                    grid_torra = grid_torra,  
                    select_cafes = select_cafes,
                    data =  inverte_data_query(torra),       
                )
            except:
                return torras()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()
    
@app.route('/update_torra', methods=['GET','POST']) # action para atualizar os dados de uma torra
def update_torra():
    try:
        if logado():
            try:
                if request.form:
                    torra = Torra(
                        request.form['id'],
                        request.form['cafe'],
                        request.form['temp_inicial'],
                        request.form['temp_final'],
                        request.form['piso'],
                        monta_temp_json(request.form),
                        request.form['fluxo_ar'],
                        request.form['velocidade_tambor'],
                        request.form['peso'],
                        request.form['data'],
                        request.form['observacoes'],
                        usuario_id(session['usuario'])
                    )
                    torra.update_torra()
                    url = '/torra?id=' + request.form['id']
                    return redirect(url, 302)
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return torras()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/compara_torras', methods=['GET','POST']) # compara grafico de torras
def compara_torras():
    try:
        if logado():
            try:
                if request.form:
                    form = request.form
                    ids = []
                    for i in form:
                        ids.append(int(i))
                    grid_torras = json_torras(ids)
                    print(grid_torras)
                    path_grafico = 'static/img/graficocomparativo.png'
                    grafico = grafico_torras(grid_torras, path_grafico, ids)
                    randomico = random.randrange(1,1000)  
                    return render_template('compara_torras.html',
                                    grafico = grafico,
                                    ids = ids,
                                    randomico = random.randrange(1,1000))
                else:
                    return redirect('/torras') 

                return render_template(
                       'compara_torras.html',
                       torras = select_torras(),
                )
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return torras()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()
    

@app.route('/apaga_torra', methods=['GET','POST']) # action para apagar uma torra
def apaga_torra():
    try:
        if logado():
            try:
                id = request.values.get('id')
                apagar_torra(id)
                return redirect('/torras',302)
            except Exception:
                logging.exception('ERRO APP CAFES E TORRRAS')
                return torras()
    except Exception:
        logging.exception('ERRO APP CAFES E TORRRAS')
        return form_login()

@app.route('/logoff') # sair do usuário logado
def logoff():
    session.pop('usuario', None)
    return redirect('/',302)

app.run(debug='True', host='0.0.0.0', port=5000)