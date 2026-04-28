import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app, origins="http://localhost:8000")

client = None
sessions = {}

SYSTEM_PROMPT = """
Você é um assistente de suporte do Dice Tales, um site de RPG de mesa (Role-Playing-Game) online.

REGRAS OBRIGATÓRIAS:
- Nunca responda fora do contexto
- Nunca invente informações
- Baseie suas respostas principalmente no FAQ, sem inventar informações
- Seja claro, direto e educado
"""

FAQ = """
Tutoriais:
- O sistema é baseado em RPGs de mesa presenciais, utilizando a vida real como base para criar um site com melhor experiência de jogo.
- Para criar conta: clique em "Criar uma Nova Conta" e preencha com username, e-mail existente e senha com mínimo de 8 caracteres.
- Para fazer login: clique em "Login" e preencha com e-mail e senha (deve existir conta).
- Para resetar senha: 1. Acesse a página de login 2. Clique em "Esqueci minha senha" 3. Insira seu e-mail cadastrado 4. Siga as instruções enviadas para seu e-mail.'
- Para criar um 'jogo', 'campanha' ou 'sessão', faça login, e ao estar na página inicial, clique em 'Criar Jogo' e preencha com o nome do Jogo, sistema de RPG e imagem de capa (opcional).
- Para criar uma 'ficha avulsa/isolada': clique em 'fichas' na header para ser redirecionado para a página de Fichas e clique em 'Criar Ficha', ou, na Página Principal, clique em 'Criar Ficha' na sessão chamada 'Your Sheets' na direita.
- Para criar uma 'ficha relacionada ao jogo/que pertence ao jogo': entre na Página de Jogos, clique no menu superior direito, clique no ícone de folha, e clique em 'Criar Ficha'.

Explicações:
 >> Página Principal:
    - Tem a Header, com 'Home', 'Fichas', 'Jogos' e 'Comunidade'
    - Tem duas sessões principais:
        > Jogos (visualização, edição e exclusão)
        > Fichas (visualização, edição e exclusão)
    - Tem o Footer, com informações de contato e um espaço para mandar feedback.
    
 >> Página de Jogo:
    - Tem as funcionalidades de:
        > Fichas de Personagem (CRUD)
        > Mapas ou Cenas (CRUD)
        
 >> Mapas:
    - Funciona por websocket: explique de forma simples como "atualização em tempo real entre usuários".
    - Tem a funcionalidade de hierarquia entre camadas para tokens, assets, imagens e textos.
    - Pode ser acessado por várias pessoas ao mesmo tempo.
    - É composto por:
        > Tokens de Personagens
        > Assets
        > Imagens de Fundo (Mapas / Cenário)

Tipos de Perguntas:
- Se a pergunta NÃO tiver a ver com o sistema, responda com:
  "Desculpe, só posso ajudar com dúvidas sobre o Dice Tales."
- Se a pergunta for sobre:
    > Fichas de forma mais aprofundada
    > Novos Sistemas de RPG
    > Editor de Fichas Personalizadas
    > Assinaturas e Pagamentos,
responda que a funcionalidade ainda não foi implementada pois o sistema ainda está em desenvolvimento.
- Se a pergunta for sobre algo que não têm resposta no FAQ, diga "Desculpe, não tenho a resposta para essa pergunta."
"""


def get_client():
    global client
    if client is None:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        client = genai.Client(api_key=api_key)
    return client

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado JSON fornecido"}), 400

    message = data.get('message')
    if not message:
        return jsonify({"error": "Campo 'message' obrigatório"}), 400

    session_id = data.get('session_id')
    print(f"[DEBUG] Mensagem recebida: {message[:50]}...")
    print(f"[DEBUG] Session ID: {session_id}")

    if session_id is None:
        session_id = str(uuid.uuid4())
        print(f"[DEBUG] Nova sessão criada: {session_id}")

    try:
        cl = get_client()

        prompt = f"""
{SYSTEM_PROMPT}

Base de conhecimento:
{FAQ}

Pergunta do usuário:
{message}
"""

        response = cl.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print(f"[DEBUG] Enviando mensagem para Gemini...")

        response_text = response.text
        print(f"[DEBUG] Resposta recebida: {response_text[:50]}...")

        return jsonify({
            "response": response_text,
            "session_id": session_id
        })

    except Exception as e:
        error_msg = str(e)
        print(f"[DEBUG] Erro ocorrido: {error_msg}")
        if '429' in error_msg or 'quota' in error_msg.lower() or 'too many requests' in error_msg.lower():
            return jsonify({"error": "Cota excedida (429). Aguarde alguns minutos e tente novamente."}), 429
        else:
            return jsonify({"error": f"Erro interno do servidor: {error_msg}"}), 500

if __name__ == "__main__":
    print("[DEBUG] Servidor Flask iniciando em http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
