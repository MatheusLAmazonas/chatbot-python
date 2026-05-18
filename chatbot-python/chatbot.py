from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import server
import dndhelper
import os
from config import IAMode, PromptType
from security import security_checker
from dual_ai import second_ai
from prompt_manager import prompt_manager

# Carrega variáveis do .env
load_dotenv()

# Configura o modelo principal (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Configura o modelo secundário (se disponível)
try:
    from langchain_openai import ChatOpenAI
    llm_secondary = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )
    has_secondary = True
except:
    has_secondary = False
    print("Segunda IA não configurada (OpenAI)")

def criar_prompt_dnd(dados, pergunta, tipo_prompt=None, modo=None):
    """Cria prompt para perguntas de D&D com engenharia de prompts"""
    
    if tipo_prompt:
        prompt_manager.set_prompt_type(tipo_prompt)
    if modo:
        prompt_manager.set_mode(modo)
    
    prompt_text, temperature = prompt_manager.create_prompt(pergunta, dados)
    
    return ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", pergunta)
    ]), temperature

def criar_prompt_dice(pergunta, tipo_prompt=None, modo=None):
    """Cria prompt para perguntas do Dice Tales com engenharia de prompts"""
    
    if tipo_prompt:
        prompt_manager.set_prompt_type(tipo_prompt)
    if modo:
        prompt_manager.set_mode(modo)
    
    dados_contexto = {"system": server.SYSTEM_PROMPT, "faq": server.FAQ}
    prompt_text, temperature = prompt_manager.create_prompt(pergunta, dados_contexto)
    
    return ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", pergunta)
    ]), temperature

def processar_com_dual_ai(pergunta, resposta_principal):
    """Processa com segunda IA para comparação"""
    # Determina especialização baseado na pergunta
    if any(word in pergunta.lower() for word in ["história", "lore", "origem"]):
        specialization = "historia"
    elif any(word in pergunta.lower() for word in ["regra", "mecânica", "dado"]):
        specialization = "mecanicas"
    else:
        specialization = "geral"
    
    # Consulta segunda IA
    resposta_secundaria = second_ai.query(pergunta, specialization)
    
    if resposta_secundaria["success"]:
        comparacao = second_ai.compare_responses(
            resposta_principal, 
            resposta_secundaria["response"]
        )
        return comparacao
    
    return None

def mostrar_menu():
    """Mostra menu de opções"""
    print("\n" + "="*50)
    print("COMANDOS DISPONÍVEIS:")
    print("  /modo <tecnico|resumido|professor|detalhado|suporte> - Muda o modo da IA")
    print("  /tipo <simples|estruturado|especializado> - Muda o tipo de prompt")
    print("  /dual - Ativa/desativa comparação com segunda IA")
    print("  /modos - Lista modos disponíveis")
    print("  /tipos - Lista tipos de prompt disponíveis")
    print("  /sair - Sai do programa")
    print("="*50)
    print(f"Modo atual: {prompt_manager.current_mode.value}")
    print(f"Tipo de prompt atual: {prompt_manager.current_prompt_type.value}")
    print("="*50)

# Configurações
usar_dual_ai = False

print(f"--- Chatbot Gemini Ativo (LangChain) ---")
print("Pergunte sobre: Dice Tales ou D&D")
mostrar_menu()

while True:
    texto = input("\nVocê: ")
    
    if texto.lower() == "sair":
        break
    
    # Comandos especiais
    if texto.startswith("/"):
        if texto.startswith("/modo "):
            modo_texto = texto.split(" ")[1]
            try:
                modo = IAMode(modo_texto)
                msg = prompt_manager.set_mode(modo)
                print(f"{msg}")
                continue
            except:
                print(f"Modo inválido. Use: {[m.value for m in IAMode]}")
                continue
        
        elif texto.startswith("/tipo "):
            tipo_texto = texto.split(" ")[1]
            try:
                tipo = PromptType(tipo_texto)
                msg = prompt_manager.set_prompt_type(tipo)
                print(f"{msg}")
                continue
            except:
                print(f"Tipo inválido. Use: {[t.value for t in PromptType]}")
                continue
        
        elif texto == "/dual":
            usar_dual_ai = not usar_dual_ai
            print(f"🔄 Comparação com segunda IA: {'ATIVADA' if usar_dual_ai else 'DESATIVADA'}")
            continue
        
        elif texto == "/modos":
            print(f"Modos disponíveis: {prompt_manager.get_available_modes()}")
            continue
        
        elif texto == "/tipos":
            print(f"Tipos de prompt: {prompt_manager.get_available_prompt_types()}")
            continue
        
        elif texto == "/help":
            mostrar_menu()
            continue
    
    # VERIFICAÇÃO DE SEGURANÇA
    allowed, message, risk = security_checker.check_all(texto)
    if not allowed:
        print(f"{message}")
        continue
    
    # Sanitiza entrada
    texto = security_checker.sanitize_input(texto)
    
    # Busca dados do D&D
    dados_dnd = dndhelper.buscar_dnd(texto)
    
    try:
        if dados_dnd:
            # Cria prompt com engenharia
            prompt, temperature = criar_prompt_dnd(dados_dnd, texto)
            # Aplica temperatura do modo
            llm.temperature = temperature
            resposta = prompt | llm
            result = resposta.invoke({})
            resposta_texto = result.content
        else:
            # Cria prompt com engenharia
            prompt, temperature = criar_prompt_dice(texto)
            llm.temperature = temperature
            resposta = prompt | llm
            result = resposta.invoke({})
            resposta_texto = result.content
        
        # Exibe resposta principal
        print(f"IA Principal: {resposta_texto}")
        
        # Se dual AI estiver ativado, consulta segunda IA
        if usar_dual_ai:
            print("\n🔄 Consultando segunda IA para comparação...")
            comparacao = processar_com_dual_ai(texto, resposta_texto)
            if comparacao:
                print(f"Segunda IA: {comparacao['secondary']}")
                print(f"Similaridade: {comparacao['similarity']:.2%}")
                print(f"Melhor resposta: {comparacao['best']}")
        
    except Exception as e:
        print(f"Erro: {e}")