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
        if session_id not in sessions:
            print(f"[DEBUG] Criando novo chat para sessão {session_id}")
            chat = cl.chats.create(model="gemini-2.5-flash")
            sessions[session_id] = chat
        else:
            print(f"[DEBUG] Usando chat existente para sessão {session_id}")
            chat = sessions[session_id]

        print(f"[DEBUG] Enviando mensagem para Gemini...")
        response = chat.send_message(message)
        response_text = response.text  # Assumindo que a resposta tem atributo .text como no SDK original
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
