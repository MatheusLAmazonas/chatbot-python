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
Tutoriais:
- O sistema é baseado em RPGs de mesa presenciais, utilizando a vida real como base para criar um site com melhor experiência de jogo.
- Para criar conta: clique em "Criar uma Nova Conta" e preencha com username, e-mail válido e senha.
- Para fazer login: clique em "Login" e preencha com e-mail e senha (deve existir conta).
- Para resetar senha: clique em "Esqueceu sua Senha?" na página de login, então será redirecionado para
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
>> Mapa
    - Funciona por websocket (pode explicar de forma simples quando precisar).
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