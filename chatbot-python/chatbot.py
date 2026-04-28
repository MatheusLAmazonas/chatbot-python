from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "gemini-2.5-flash" 

chat = client.chats.create(model=MODEL_ID)

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

print(f"--- Chatbot Gemini Ativo ({MODEL_ID}) ---")

while True:
    texto = input("\nVocê: ")
    
    if texto.lower() == "sair":
        break
    
    try:
        prompt = f"""
{SYSTEM_PROMPT}

Base de conhecimento:
{FAQ}

Pergunta do usuário:
{texto}
"""

        resposta = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        print(f"Chatbot: {resposta.text}")
        
    except Exception as e:
        if "429" in str(e):
            print("\n[ERRO] Cota excedida. Aguarde alguns segundos...")
        else:
            print(f"\nErro inesperado: {e}")