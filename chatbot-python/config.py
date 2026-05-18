from enum import Enum

class IAMode(Enum):
    TECNICO = "tecnico"
    RESUMIDO = "resumido"
    PROFESSOR = "professor"
    DETALHADO = "detalhado"
    SUPORTE_TECNICO = "suporte_tecnico"

class PromptType(Enum):
    SIMPLES = "simples"
    ESTRUTURADO = "estruturado"
    ESPECIALIZADO = "especializado"

# Configurações de cada modo
MODE_SETTINGS = {
    IAMode.TECNICO: {
        "temperature": 0.3,
        "system_prompt": "Você é um especialista técnico em RPG. Use terminologia precisa, explique mecânicas com detalhes exatos, cite regras específicas e seja objetivo. Evite analogias."
    },
    IAMode.RESUMIDO: {
        "temperature": 0.5,
        "system_prompt": "Você é um assistente conciso. Dê respostas curtas e diretas com máximo de 2-3 frases. Seja extremamente objetivo."
    },
    IAMode.PROFESSOR: {
        "temperature": 0.7,
        "system_prompt": "Você é um professor paciente e didático. Explique conceitos passo a passo, use analogias e verifique a compreensão."
    },
    IAMode.DETALHADO: {
        "temperature": 0.4,
        "system_prompt": "Você é um especialista que fornece respostas completas e aprofundadas. Inclua exemplos, casos especiais e explicações extensas."
    },
    IAMode.SUPORTE_TECNICO: {
        "temperature": 0.6,
        "system_prompt": "Você é um agente de suporte técnico. Seja empático, ofereça soluções práticas e guie o usuário passo a passo."
    }
}

# Templates para cada tipo de prompt
PROMPT_TEMPLATES = {
    PromptType.SIMPLES: """
{system_prompt}

Pergunta: {question}

Resposta:""",
    
    PromptType.ESTRUTURADO: """
{system_prompt}

PERGUNTA: {question}

Por favor, estruture sua resposta da seguinte forma:
1. Resumo da resposta
2. Explicação detalhada
3. Pontos importantes
4. Conclusão

RESPOSTA:""",
    
    PromptType.ESPECIALIZADO: """
{system_prompt}

CONTEXTO ESPECIALIZADO:
{dados_contexto}

PERGUNTA ESPECIALIZADA: {question}

Por favor, responda como um especialista, incluindo:
- Termos técnicos apropriados
- Referências específicas
- Melhores práticas
- Possíveis variações ou exceções

RESPOSTA ESPECIALIZADA:"""
}

# Assuntos para cada IA (segunda API)
IA_SPECIALIZATIONS = {
    "gemini": ["regras_gerais", "mecanicas", "classes", "racas"],
    "gpt": ["historia", "lore", "narrativa", "personagens"]
}