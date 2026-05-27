import os
import traceback
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import uuid
import dndhelper

load_dotenv()

# Verificação rápida da API Key
if not os.getenv("GOOGLE_API_KEY"):
    print("\n[AVISO] Variável GOOGLE_API_KEY não encontrada! Verifique seu arquivo .env")

app = Flask(__name__)
CORS(app)  # Permite todas as origens

# ============ CONFIGURAÇÃO DA IA ============

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# ============ FAQ DO DICE TALES ============

FAQ = """
Tutoriais:
- Para criar conta: clique em "Criar uma Nova Conta" e preencha com username, e-mail existente e senha com mínimo de 8 caracteres.
- Para fazer login: clique em "Login" e preencha com e-mail e senha.
- Para resetar senha: Acesse a página de login, clique em "Esqueci minha senha", insira seu e-mail e siga as instruções.
- Para criar um jogo: faça login, clique em 'Criar Jogo' e preencha com o nome do Jogo e sistema de RPG.

Explicações:
- Página Principal: Header com Home, Fichas, Jogos e Comunidade. Sessões de Jogos e Fichas.
- Página de Jogo: Fichas de Personagem (CRUD) e Mapas ou Cenas (CRUD).
- Mapas: Atualização em tempo real, hierarquia de camadas para tokens, assets e imagens.

Regras:
- Só responda perguntas sobre o Dice Tales.
- Se não souber, diga que não sabe.
- Seja claro, educado e amigável.
"""

# ============ PROMPTS ============

PROMPT_DICE_TALES = f"""
Você é um assistente de suporte amigável do Dice Tales, um site de RPG de mesa online.

REGRAS:
- Responda apenas dúvidas relacionadas ao Dice Tales
- Baseie suas respostas no FAQ abaixo
- Seja simpático, claro e direto
- Use uma linguagem casual e amigável

FAQ:
{FAQ}

Pergunta do usuário: {{pergunta}}

Resposta (seja natural e amigável):
"""

PROMPT_DND = """
Você é um mestre de RPG especialista em D&D 5ª Edição, muito amigável e didático.

Informações adicionais da API (use como complemento, não como única fonte):
{dados_api}

REGRAS:
- Use SEU CONHECIMENTO de D&D para responder naturalmente
- As informações da API são apenas um complemento
- Seja didático, explique como se estivesse ensinando um amigo
- Use exemplos práticos
- Seja entusiasmado e amigável
- Responda em português do Brasil

Pergunta do usuário: {pergunta}

Resposta (como um mestre explicando para um jogador):
"""

# ============ FUNÇÕES ============

def is_dnd_query(message):
    """Detecta se a pergunta é sobre D&D"""
    dnd_keywords = [
        "d&d", "dnd", "dd", "dungeons", "dragons", "classe", "raça", "magia", 
        "feitiço", "monstro", "personagem", "barbaro", "mago", "guerreiro", 
        "ladino", "clérigo", "feiticeiro", "druida", "paladino", "monge",
        "bardo", "bruxo", "ranger", "anão", "elfo", "halfling", "humano",
        "tiefling", "gnomo", "meio-elfo", "meio-orc", "dragao", "dragão",
        "bola de fogo", "fireball", "magia", "nível", "dano"
    ]
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in dnd_keywords)

def responder_dnd(pergunta):
    """Responde perguntas sobre D&D usando conhecimento da IA + API"""
    
    # Tenta buscar dados complementares na API
    dados_api = dndhelper.buscar_dnd(pergunta)
    dados_formatados = dndhelper.formatar_dados_dnd(dados_api) if dados_api else "Nenhum dado específico encontrado na API."
    
    # Cria o prompt
    prompt_text = PROMPT_DND.format(
        dados_api=dados_formatados,
        pergunta=pergunta
    )
    
    # Se não achou nada na API, adiciona um aviso amigável
    if not dados_api:
        prompt_text += "\n\nOBS: Não encontrei dados específicos na API, mas vou usar meu conhecimento de D&D para responder!"
    
    response = llm.invoke(prompt_text)
    return response.content

def responder_dice_tales(pergunta):
    """Responde perguntas sobre Dice Tales"""
    prompt_text = PROMPT_DICE_TALES.format(pergunta=pergunta)
    response = llm.invoke(prompt_text)
    return response.content

# ============ ENDPOINTS ============

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado JSON fornecido"}), 400
    
    message = data.get('message')
    session_id = data.get('session_id') or str(uuid.uuid4())
    
    if not message:
        return jsonify({"error": "Campo 'message' obrigatório"}), 400
    
    if len(message) > 500:
        return jsonify({"error": "Mensagem muito longa"}), 400
    
    print(f"\n[DEBUG] Sessão: {session_id}")
    print(f"[DEBUG] Mensagem: {message}")
    
    try:
        # Verifica se é pergunta sobre D&D
        if is_dnd_query(message):
            print("[DEBUG] 🎲 Pergunta sobre D&D detectada")
            response_text = responder_dnd(message)
            return jsonify({
                "response": response_text,
                "session_id": session_id,
                "type": "dnd"
            })
        else:
            print("[DEBUG] 🎲 Pergunta sobre Dice Tales")
            response_text = responder_dice_tales(message)
            return jsonify({
                "response": response_text,
                "session_id": session_id,
                "type": "dicetales"
            })
    
    except Exception as e:
        print(f"[ERRO] {e}")
        traceback.print_exc()
        error_msg = str(e)
        if '429' in error_msg or 'quota' in error_msg.lower():
            return jsonify({"error": "Cota excedida. Aguarde alguns minutos."}), 429
        return jsonify({"error": f"Erro interno: {error_msg}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "model": "gemini-2.5-flash",
        "features": ["dicetales", "dnd-5e"]
    })

if __name__ == "__main__":
    print("="*50)
    print("🎲 SERVIDOR DICE TALES + D&D 5e")
    print("="*50)
    print("[DEBUG] Servidor rodando em http://0.0.0.0:5000")
    print("[DEBUG] CORS: Habilitado para todas as origens")
    print("[DEBUG] D&D API: Integrada (como complemento)")
    print("[DEBUG] A IA usa seu conhecimento de D&D + API")
    print("="*50)
    app.run(host='0.0.0.0', port=5000, debug=True)