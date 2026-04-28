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
- Use apenas o FAQ
- Seja claro e educado
"""

FAQ = """
- O sistema é baseado em RPGs de mesa presenciais, utilizando a vida real como base para criar um site com melhor experiência de jogo.
- Para criar conta: clique em "Criar uma Nova Conta" e preencha com username, e-mail e senha.
- Para fazer login: clique em "Login" e preencha com e-mail e senha.
- Para resetar senha: clique em "Esqueceu sua Senha?" na página de login.
- Para criar um 'jogo', 'campanha' ou 'sessão', faça login, e ao estar na página inicial, clique em 'Criar Jogo' e preencha as informações do modal.
- Depois de criar o jogo, o usuário será redirecionado para a Página de Jogo, que terá o Tabletop com websocket (explique de forma simples).
- Na página de jogo é onde estão as funcionalidades de:
    > Fichas (CRUD)
    > Tokens de Personagem (CRUD)
    > Mapa (CRUD)
- Na edição do mapa, o jogador pode utilizar as layers para ter hierarquia de elementos (tokens, assets)
- Se a pergunta NÃO tiver a ver com o sistema, responda com:
  "Desculpe, só posso ajudar com dúvidas sobre o Dice Tales."
- Se a pergunta for sobre:
    > Novos Sistemas de RPG além de D&D
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
        # if session_id not in sessions:
        #     print(f"[DEBUG] Criando novo chat para sessão {session_id}")
        #     chat = cl.chats.create(model="gemini-2.5-flash")
        #     sessions[session_id] = chat
        # else:
        #     print(f"[DEBUG] Usando chat existente para sessão {session_id}")
        #     chat = sessions[session_id]

        # print(f"[DEBUG] Enviando mensagem para Gemini...")
        # response = chat.send_message(message)
        # response_text = response.text  # Assumindo que a resposta tem atributo .text como no SDK original
        # print(f"[DEBUG] Resposta recebida: {response_text[:50]}...")

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
