import requests

CLASSES_DND = {
    'barbarian': ['barbaro', 'bárbaro', 'barbarian'],
    'druid': ['druida', 'druid'],
    'wizard': ['mago', 'wizard'],
    'fighter': ['guerreiro', 'fighter'],
    'paladin': ['paladino', 'paladin'],
    'sorcerer': ['feiticeiro', 'sorcerer', 'feitiçeiro'],
    'cleric': ['clerigo', 'clérigo', 'cleric'],
    'rogue': ['ladino', 'rogue'],
    'bard': ['bardo', 'bard'],
    'monk': ['monge', 'monk'],
    'ranger': ['patrulheiro', 'ranger']
}

DND_API_URL = "https://www.dnd5eapi.co/api"

def buscar_dnd(pergunta):
    nome_busca = None
    
    # Procura qual classe o usuário perguntou
    for classe, variacoes in CLASSES_DND.items():
        for variacao in variacoes:
            if variacao in pergunta.lower():
                nome_busca = classe
                break
        if nome_busca:
            break
    
    if nome_busca:
        try:
            url = f"{DND_API_URL}/classes/{nome_busca}"
            resposta = requests.get(url)
            dados = resposta.json()
            return dados
        except Exception as e:
            print(f"Erro na busca: {e}")
            return None
    return None