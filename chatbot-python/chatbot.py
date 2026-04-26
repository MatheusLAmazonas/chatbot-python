from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "gemini-2.5-flash" 

chat = client.chats.create(model=MODEL_ID)

print(f"--- Chatbot Gemini Ativo ({MODEL_ID}) ---")

while True:
    texto = input("\nVocê: ")
    
    if texto.lower() == "sair":
        break
    
    try:
        resposta = chat.send_message(texto)
        print(f"Chatbot: {resposta.text}")
        
    except Exception as e:
        if "429" in str(e):
            print("\n[ERRO] Cota excedida. Aguarde alguns segundos...")
        else:
            print(f"\nErro inesperado: {e}")