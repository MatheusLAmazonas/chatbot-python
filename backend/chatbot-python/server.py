import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app, origins="http://localhost:8000")
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

# Configuração do Modelo e Prompt LangChain
# Aqui definimos o 'cérebro' (LLM) com temperatura 0 para respostas mais precisas (menos criativas)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# O ChatPromptTemplate organiza a estrutura da conversa para o modelo
prompt = ChatPromptTemplate.from_messages([
    ("system", f"{SYSTEM_PROMPT}\n\nBase de conhecimento:\n{FAQ}"),
    MessagesPlaceholder(variable_name="history"), # Espaço reservado para as mensagens anteriores
    ("human", "{input}"),
])

# Criamos a 'corrente' (chain): o prompt alimenta o modelo
chain = prompt | llm 

# Função que o LangChain usa para buscar o histórico de uma sessão específica
def get_session_history(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = ChatMessageHistory()
    return sessions[session_id]

# Envolvemos a nossa chain com um gerenciador de histórico automático
chain_with_history = RunnableWithMessageHistory( 
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado JSON fornecido"}), 400
    
    message = data.get('message')
    session_id = data.get('session_id') or str(uuid.uuid4())
    
    if not message:
        return jsonify({"error": "Campo 'message' obrigatório"}), 400

    # O session_id agora é a chave para manter o contexto da conversa
    print(f"\n[DEBUG] Sessão: {session_id}")
    print(f"[DEBUG] Pergunta do usuário: {message}")

    try:
        # O .invoke substitui o antigo generate_content()
        response = chain_with_history.invoke(
            {"input": message}, # LangChain injeta o histórico aqui automaticamente
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"[DEBUG] Resposta da IA: {response.content[:50]}...")

        return jsonify({
            "response": response.content,
            "session_id": session_id
        })

    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'quota' in error_msg.lower() or 'too many requests' in error_msg.lower():
            return jsonify({"error": "Cota excedida (429). Aguarde alguns minutos e tente novamente."}), 429
        else:
            return jsonify({"error": f"Erro interno do servidor: {error_msg}"}), 500

if __name__ == "__main__":
    print("[DEBUG] Servidor Flask iniciando em http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
