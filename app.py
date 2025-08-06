from flask import Flask, render_template, request, jsonify
import json
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para usar matplotlib sem GUI
import io
import base64

app = Flask(__name__)

# Arquivo para armazenar os dados
DATA_FILE = 'atividades_data.json'

def carregar_dados():
    """Carrega os dados do arquivo JSON ou retorna dicionário vazio"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    """Salva os dados no arquivo JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

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
    
    salvar_dados(atividades)
    
    return jsonify({
        'sucesso': True,
        'atividades': atividades,
        'mensagem': f'Adicionado {tempo_horas:.2f}h à atividade "{atividade}"'
    })

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
    salvar_dados(atividades)
    
    return jsonify({
        'sucesso': True,
        'atividades': atividades,
        'mensagem': f'Atividade "{nome}" criada com sucesso'
    })

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
    salvar_dados(atividades)
    
    return jsonify({
        'sucesso': True,
        'atividades': atividades,
        'mensagem': f'Atividade "{nome}" removida com sucesso'
    })

@app.route('/api/grafico')
def get_grafico():
    """API para obter o gráfico atualizado"""
    atividades = carregar_dados()
    grafico = gerar_grafico(atividades)
    return jsonify({'grafico': grafico})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
