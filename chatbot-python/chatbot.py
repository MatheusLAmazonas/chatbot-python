from google import genai
from dotenv import load_dotenv
import server
import dndhelper
import os

DND_API_URL = "https://www.dnd5eapi.co/api?lang=pt"

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "gemini-2.5-flash" 

chat = client.chats.create(model=MODEL_ID)

print(f"--- Chatbot Gemini Ativo ({MODEL_ID}) ---")
print("Pergunte sobre: Dice Tales ou D&D (bárbaro, guerreiro, mago, ladino, clérigo, druida, etc)")

while True:
    texto = input("\nVocê: ")
    
    if texto.lower() == "sair":
        break
    
    # Busca dados do D&D usando a função do dndhelper
    dados_dnd = dndhelper.buscar_dnd(texto)
    
    try:
        if dados_dnd:
            
            prompt = f"""
            Você explica para um jogador novato de forma simples e direta e sucinta.
            
            Dados oficiais da classe {dados_dnd.get('name')} do D&D 5e:
            - Dado de Vida: d{dados_dnd.get('hit_die')}
            - Proficiências: {[p.get('name') for p in dados_dnd.get('proficiencies', [])]}
            - Salvaguardas: {[s.get('name') for s in dados_dnd.get('saving_throws', [])]}
            
            Pergunta do usuário: "{texto}"
            
            Sua missão:
            1. Analise estes dados oficiais
            2. Responda de forma SIMPLES, ANIMADA e ÚTIL
            3. Explique como essa classe funciona na prática
            4. De ideias de criação de
            5. Use exemplos do dia a dia para explicar as mecânicas
            
            IMPORTANTE: Baseie-se APENAS nos dados fornecidos. Não invente informações!
            """
        else:
            prompt = f"""
            {server.SYSTEM_PROMPT}

            Base de conhecimento (FAQ):
            {server.FAQ}

            Pergunta do usuário:
            {texto}

            Responda APENAS com base no FAQ do Dice Tales.
            Se a pergunta não for sobre o Dice Tales, diga: "Desculpe, só posso ajudar com dúvidas sobre o Dice Tales ou sobre classes do D&D (bárbaro, guerreiro, mago, ladino, clérigo, druida, bardo, monge, paladino, ranger)."
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