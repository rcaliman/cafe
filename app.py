from flask import Flask, request, render_template, session, redirect
from tools import Login, logado, monta_temp_json, grafico
from werkzeug.datastructures import ImmutableMultiDict
from class_torra import Torra, select_torras, select_torra, apagar_torra, edit_gridform, json_torras, grafico_torras
from class_cafe import Cafe, select_cafes, select_cafe, select_descricao_cafes, apagar_cafe, busca_descricao_cafe
import json
import random

app = Flask(__name__)

app.secret_key = 'frase secretissima'

@app.route('/') # pagina inicial
def inicio():
    try:
        usuario = session['usuario']
        return render_template('inicio.html',
                               usuario = usuario)
    except:
        return redirect('/form_login',302)

@app.route('/form_login') # formulário de login
def form_login():
    return render_template('form_login.html')

@app.route('/logar', methods=['POST']) # autenticar usuario e setar sessão
def logar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if Login(usuario,senha).confere():
        session['usuario'] = usuario
        return render_template('inicio.html')
    else:
        return form_login()
    
@app.route('/cafes', methods=['GET','POST']) # mostra a lista de cafés comprados
def cafes():
    try:
        if logado():
            return render_template(
                'cafes.html',
                cafes = select_cafes(),
            )
    except:
        return form_login()
    
@app.route('/form_cafe') #formulario para fazer o cadastro dos cafés
def form_cafe():
    try:
        if logado():
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
                )
    except:
        return form_login()

@app.route('/insere_cafe',methods=['GET','POST']) # action do formulario de cadastro de cafés
def insere_cafe():
    try:
        if logado():
            if request.form:
                cafe = Cafe(
                    None,
                    request.form['descricao'],
                    request.form['quantidade'],
                    request.form['data_compra'],
                    request.form['origem'],
                    request.form['estoque']
                )
                cafe.insere_banco()
        return redirect('/cafes',302)
    except:
        return form_login()
    
@app.route('/update_cafe',methods=['GET','POST']) # action do formulário de atualizacao de cafés
def update_cafe():
    try:
        if logado():
            if request.form:
                cafe = Cafe(
                    request.form['id'],
                    request.form['descricao'],
                    request.form['quantidade'],
                    request.form['data_compra'],
                    request.form['origem'],
                    request.form['estoque']
                )
                cafe.update_cafe()
        return redirect('/cafes',302)
    except:
        return form_login()

@app.route('/apaga_cafe', methods=['GET','POST']) # action para apagar um café do banco
def apaga_cafe():
    try:
        if logado():
            id = int(request.values.get('id'))
            apagar_cafe(id)
        return redirect('/cafes',302)
    except:
        return form_login()

@app.route('/torras', methods=['GET','POST']) # tabela com torras já feitas
def torras():
    try:
        if logado():
            return render_template(
                'torras.html',
                torras = select_torras(),
            )
    except:
        return form_login()
    
@app.route('/torra', methods=['GET','POST']) # tabela com os dados de uma torra específica
def torra():
    try:
        if logado():
            id = request.values.get('id')
            torra = select_torra(id)
            id_cafe = torra[0][1]
            descricao_cafe = busca_descricao_cafe(id_cafe) 
            grid_torra = json.loads(json_torras(id)[0][0])
            path_grafico = 'static/img/grafico.png'
            plot = grafico_torras(json_torras(id),path_grafico, id)
            randomico = random.randrange(1,1000)
            return render_template(
                'torra.html',
                torra = torra,
                grid_torra = grid_torra,
                plot = plot,
                id = id,
                descricao_cafe = descricao_cafe,
                randomico = randomico,
        )
    except:
        return form_login()
    
@app.route('/form_torra') # formulário para cadastrar uma torra
def form_torra():
    try:
        if logado():
            return render_template('form_torra.html',
                select_cafes = select_descricao_cafes(0),                       
            )
    except:
        return form_login()

@app.route('/insere_torra', methods=['GET','POST']) # action do formulário de inserir nova torra
def insere_torra():
    try:
        if logado():
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
                    request.form['observacoes'])
                torra.insere_banco()
                
        return redirect('/torras',302)
    except:
            return form_login()

@app.route('/edita_torra') # formulário para editar uma torra já feita
def edita_torra():
    try:
        if logado():
            id = int(request.values.get('id'))
            torra = select_torra(id)
            id_cafe = torra[0][1]
            grid_torra = edit_gridform(id)
            select_cafes = select_descricao_cafes(id_cafe)
            return render_template('edita_torra.html',
                torra = torra,  
                grid_torra = grid_torra,  
                select_cafes = select_cafes,        
            )
    except:
        return form_login()
    
@app.route('/update_torra', methods=['GET','POST']) # action para atualizar os dados de uma torra
def update_torra():
    try:
        if logado():
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
                    request.form['observacoes'])
                torra.update_torra()
                url = '/torra?id=' + request.form['id']
        return redirect(url, 302)
    except:
            return form_login()

@app.route('/compara_torras', methods=['GET','POST']) # compara grafico de torras
def compara_torras():
    try:
        if logado():
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
            return render_template(
                   'compara_torras.html',
                   torras = select_torras(),
            )
    except:
        return form_login()
    

@app.route('/apaga_torra', methods=['GET','POST']) # action para apagar uma torra
def apaga_torra():
    try:
        if logado():
            id = request.values.get('id')
            apagar_torra(id)
            return redirect('/torras',302)
    except:
        return form_login()

@app.route('/logoff') # sair do usuário logado
def logoff():
    session.pop('usuario', None)
    return redirect('/',302)

app.run(debug='True')
