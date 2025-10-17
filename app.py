from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para usar matplotlib sem GUI
import io
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cronometro_secret_key_change_in_production'  # Mude em produção

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar esta página.'

# Arquivo para armazenar usuários
USERS_FILE = 'users.json'

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

@login_manager.user_loader
def load_user(username):
    users = carregar_usuarios()
    if username in users:
        return User(username)
    return None

def carregar_usuarios():
    """Carrega os usuários do arquivo JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    """Salva os usuários no arquivo JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

def get_user_data_file(username):
    """Retorna o nome do arquivo de dados do usuário"""
    return f'atividades_data_{username}.json'

def carregar_dados():
    """Carrega os dados do cookie do navegador ou arquivo JSON do usuário logado"""
    if current_user.is_authenticated:
        # Se está logado, carrega do arquivo do usuário
        data_file = get_user_data_file(current_user.username)
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    else:
        # Se não está logado, carrega dos cookies
        dados_cookie = request.cookies.get('atividades_data')
        if dados_cookie:
            try:
                return json.loads(dados_cookie)
            except:
                return {}
        return {}

def salvar_dados(dados):
    """Salva os dados no arquivo JSON do usuário logado ou prepara para cookie"""
    if current_user.is_authenticated:
        # Se está logado, salva no arquivo do usuário
        data_file = get_user_data_file(current_user.username)
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    # Se não está logado, os dados serão salvos via cookie nas rotas de resposta

def gerar_grafico(atividades):
    """Gera o gráfico de pizza e retorna como base64"""
    plt.figure(figsize=(10, 10))
    
    if not atividades:
        # Se não há atividades, mostra uma mensagem
        plt.text(0.5, 0.5, 'Nenhuma atividade cadastrada\nCrie uma atividade para começar!', 
                ha='center', va='center', fontsize=16, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')
    else:
        labels = list(atividades.keys())
        valores = list(atividades.values())
        
        # Filtrar atividades com 0 horas
        dados_filtrados = [(label, valor) for label, valor in zip(labels, valores) if valor > 0]
        
        if dados_filtrados:
            labels_filtrados, valores_filtrados = zip(*dados_filtrados)
            plt.pie(valores_filtrados, labels=labels_filtrados, autopct='%1.1f%%', startangle=90)
            plt.title("Distribuição de Horas Semanalmente", fontsize=16)
        else:
            plt.text(0.5, 0.5, 'Todas as atividades têm 0 horas\nUse o cronômetro para adicionar tempo!', 
                    ha='center', va='center', fontsize=16,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.axis('off')
    
    plt.axis('equal')
    
    # Salvar em buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    
    # Converter para base64
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = carregar_usuarios()
        
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'error')
            return render_template('register.html')
        
        users = carregar_usuarios()
        
        if username in users:
            flash('Usuário já existe!', 'error')
            return render_template('register.html')
        
        # Criar novo usuário
        users[username] = {
            'password': generate_password_hash(password),
            'created_at': str(datetime.now())
        }
        
        salvar_usuarios(users)
        flash('Usuário criado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    """Página principal"""
    atividades = carregar_dados()
    grafico = gerar_grafico(atividades)
    return render_template('index.html', atividades=atividades, grafico=grafico)

@app.route('/api/atividades')
def get_atividades():
    """API para obter todas as atividades"""
    return jsonify(carregar_dados())

@app.route('/api/adicionar_tempo', methods=['POST'])
def adicionar_tempo():
    """API para adicionar tempo a uma atividade"""
    data = request.json
    atividade = data.get('atividade')
    tempo_horas = data.get('tempo_horas', 0)
    
    if not atividade:
        return jsonify({'erro': 'Atividade não especificada'}), 400
    
    atividades = carregar_dados()
    
    if atividade in atividades:
        atividades[atividade] += tempo_horas
    else:
        atividades[atividade] = tempo_horas
    
    # Se o usuário estiver logado, salva no arquivo
    if current_user.is_authenticated:
        salvar_dados(atividades)
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Adicionado {tempo_horas:.2f}h à atividade "{atividade}"'
        })
    else:
        # Se não estiver logado, salva nos cookies
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Adicionado {tempo_horas:.2f}h à atividade "{atividade}"'
        })
        response.set_cookie('atividades_data', json.dumps(atividades), max_age=30*24*60*60)  # 30 dias
    
    return response

@app.route('/api/nova_atividade', methods=['POST'])
def nova_atividade():
    """API para criar uma nova atividade"""
    data = request.json
    nome = data.get('nome')
    
    if not nome:
        return jsonify({'erro': 'Nome da atividade não especificado'}), 400
    
    atividades = carregar_dados()
    
    if nome in atividades:
        return jsonify({'erro': 'Atividade já existe'}), 400
    
    atividades[nome] = 0
    
    # Se o usuário estiver logado, salva no arquivo
    if current_user.is_authenticated:
        salvar_dados(atividades)
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Atividade "{nome}" criada com sucesso'
        })
    else:
        # Se não estiver logado, salva nos cookies
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Atividade "{nome}" criada com sucesso'
        })
        response.set_cookie('atividades_data', json.dumps(atividades), max_age=30*24*60*60)  # 30 dias
    
    return response

@app.route('/api/zerar-atividades', methods=['POST'])
def atualizar_atividade():
    atividades = carregar_dados()

    for atividade in atividades:
        atividades[atividade] = 0
    
    if current_user.is_authenticated:
        salvar_dados(atividades)
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': 'Tempos zerados com sucesso'
        })
    else:
        # Se não estiver logado, salva nos cookies
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': 'Tempos zerados com sucesso'
        })
        response.set_cookie('atividades_data', json.dumps(atividades), max_age=30*24*60*60)
    
    return response

@app.route('/api/zerar-tempo-atividade', methods=['POST'])
def zerarTempoAtividade():
    """API para zerar o tempo de uma atividade"""
    data = request.json
    atividade = data.get('atividade')
    
    if not atividade:
        return jsonify({'erro': 'Atividade não especificada'}), 400
    
    atividades = carregar_dados()
    
    if atividade in atividades:
        atividades[atividade] = 0
    
    if current_user.is_authenticated:
        salvar_dados(atividades)
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Tempo zerado com sucesso para a atividade "{atividade}"'
        })

    else:
        # Se não estiver logado, salva nos cookies
        response = jsonify({
            'sucesso': True,    
            'atividades': atividades,
            'mensagem': f'Tempo zerado com sucesso para a atividade "{atividade}"'
        })
        response.set_cookie('atividades_data', json.dumps(atividades), max_age=30*24*60*60)
    
    return response
@app.route('/api/remover_atividade', methods=['POST'])
def remover_atividade():
    """API para remover uma atividade"""
    data = request.json
    nome = data.get('nome')
    
    if not nome:
        return jsonify({'erro': 'Nome da atividade não especificado'}), 400
    
    atividades = carregar_dados()
    
    if nome not in atividades:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    
    del atividades[nome]
    
    # Se o usuário estiver logado, salva no arquivo
    if current_user.is_authenticated:
        salvar_dados(atividades)
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Atividade "{nome}" removida com sucesso'
        })
    else:
        # Se não estiver logado, salva nos cookies
        response = jsonify({
            'sucesso': True,
            'atividades': atividades,
            'mensagem': f'Atividade "{nome}" removida com sucesso'
        })
        response.set_cookie('atividades_data', json.dumps(atividades), max_age=30*24*60*60)  # 30 dias
    
    return response

@app.route('/api/grafico')
def get_grafico():
    """API para obter o gráfico atualizado"""
    atividades = carregar_dados()
    grafico = gerar_grafico(atividades)
    return jsonify({'grafico': grafico})

if __name__ == '__main__':
    import os
    # Configurações para desenvolvimento
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
