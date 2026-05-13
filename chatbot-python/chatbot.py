from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import server
import dndhelper
import os

load_dotenv()

# Configura o modelo
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

print(f"--- Chatbot Gemini Ativo (LangChain) ---")
print("Pergunte sobre: Dice Tales ou D&D")

def criar_prompt_dnd(dados, pergunta):
    """Cria prompt para perguntas de D&D"""
    return ChatPromptTemplate.from_messages([
        ("system", f"""Você explica de forma breve mas fácil de entender

Dados da classe {dados.get('name')}:
- Dado de Vida: d{dados.get('hit_die')}
- Proficiências: {[p.get('name') for p in dados.get('proficiencies', [])]}

Responda de forma SIMPLES e DIRETA sobre esta classe do D&D."""),
        ("human", pergunta)
    ])

def criar_prompt_dice(pergunta):
    """Cria prompt para perguntas do Dice Tales"""
    return ChatPromptTemplate.from_messages([
        ("system", f"""{server.SYSTEM_PROMPT}

FAQ:
{server.FAQ}

Responda APENAS com base no FAQ."""),
        ("human", pergunta)
    ])

while True:
    texto = input("\nVocê: ")
    
    if texto.lower() == "sair":
        break
    
    dados_dnd = dndhelper.buscar_dnd(texto)
    
    try:
        if dados_dnd:
            prompt = criar_prompt_dnd(dados_dnd, texto)
            resposta = prompt | llm
            result = resposta.invoke({})
            print(f"Chatbot: {result.content}")
        else:
            prompt = criar_prompt_dice(texto)
            resposta = prompt | llm
            result = resposta.invoke({})
            print(f"Chatbot: {result.content}")
            
    except Exception as e:
        print(f"Erro: {e}")