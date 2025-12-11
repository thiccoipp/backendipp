import os
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS

# -----------------------------------------------------------
# CONFIGURAÇÃO DO FLASK
# -----------------------------------------------------------
app = Flask(__name__)

# Habilita CORS para permitir que seu HTML (mesmo que em outro domínio/porta) 
# acesse este servidor.
CORS(app)

# -----------------------------------------------------------
# CONFIGURAÇÃO DE ARQUIVOS
# -----------------------------------------------------------

# Pasta onde o Excel ficará salvo. O Render cria esta pasta.
UPLOAD_FOLDER = 'dados'

# Nome padrão esperado pelo seu Dashboard.
FILE_NAME = 'base_hub_github.xlsx'

# Caminho completo para salvar o arquivo: (pasta 'dados'/nome-do-arquivo.xlsx)
FILE_PATH = os.path.join(UPLOAD_FOLDER, FILE_NAME)

# Cria a pasta 'dados' se ela não existir (útil para rodar localmente e no Render).
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# -----------------------------------------------------------
# ROTAS (Endpoints da API)
# -----------------------------------------------------------

# Rota de Status (para verificar se o servidor está ativo)
@app.route('/')
def home():
    """Retorna uma mensagem de status."""
    return f"Backend do Dashboard Ativo! Servidor rodando na porta {os.environ.get('PORT', 5000)}."

# Rota 1: Servir o Arquivo Excel para o Dashboard
@app.route('/api/data', methods=['GET'])
def get_data():
    """Entrega o arquivo Excel 'base_hub_github.xlsx'."""
    if os.path.exists(FILE_PATH):
        # send_file é usado para enviar o arquivo diretamente
        # as_attachment=False indica que é para servir como um arquivo de dados, não para download
        return send_file(FILE_PATH, as_attachment=False)
    else:
        # Se o arquivo não existir (porque ninguém fez upload ainda)
        return jsonify({
            "error": "Nenhum arquivo de dados encontrado. Faça upload primeiro na rota /api/upload."
        }), 404

# Rota 2: Receber o Upload do Novo Arquivo Excel
@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Recebe um arquivo via POST e salva como 'base_hub_github.xlsx'."""
    # 1. Verifica se a chave 'file' existe nos arquivos enviados
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum campo 'file' encontrado no formulário."}), 400
    
    file = request.files['file']
    
    # 2. Verifica se o nome do arquivo está vazio
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio."}), 400

    # 3. Salva o arquivo sobrescrevendo o antigo
    if file:
        file.save(FILE_PATH)
        return jsonify({
            "message": "Base de dados atualizada com sucesso!",
            "file_saved_as": FILE_NAME
        }), 200

# -----------------------------------------------------------
# EXECUÇÃO DO SERVIDOR
# -----------------------------------------------------------
if __name__ == '__main__':
    # Obtém a porta do ambiente (necessário para Render/Deploy) ou usa 5000 se rodando localmente
    # Esta linha é CRÍTICA para o deploy no Render
    port = int(os.environ.get('PORT', 5000))
    
    # Inicia o servidor Flask
    app.run(debug=False, host='0.0.0.0', port=port)