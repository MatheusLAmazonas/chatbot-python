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

RACAS_DND = {
    'dragonborn': ['dragonborn', 'draconato'],
    'dwarf': ['anao', 'anão', 'dwarf'],
    'elf': ['elfo', 'elf'],
    'gnome': ['gnomo', 'gnome'],
    'half-elf': ['meio-elfo', 'half-elf', 'meio elfo', 'half elf'],
    'half-orc': ['meio-orc', 'half-orc', 'meio orc', 'half orc'],
    'halfling': ['halfling', 'hobbit'],
    'human': ['humano', 'human'],
    'tiefling': ['tiefling', 'tiefling'],
    'aarakocra': ['aarakocra', 'aracocra'],
    'aasimar': ['aasimar', 'assimar'],
    'firbolg': ['firbolg'],
    'goliath': ['goliath', 'golias'],
    'kenku': ['kenku'],
    'lizardfolk': ['lizardfolk', 'lagarto'],
    'tabaxi': ['tabaxi', 'gato'],
    'tortle': ['tortle', 'tartaruga'],
    'yuan-ti': ['yuan-ti', 'yuan ti']
}

DND_API_URL = "https://www.dnd5eapi.co/api"

def buscar_dnd_classe(pergunta):
    """Busca informações de classe do D&D"""
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

def buscar_dnd_raca(pergunta):
    nome_busca = None
    
    # Procura qual raça o usuário perguntou
    for raca, variacoes in RACAS_DND.items():
        for variacao in variacoes:
            if variacao in pergunta.lower():
                nome_busca = raca
                break
        if nome_busca:
            break
    
    if nome_busca:
        try:
            url = f"{DND_API_URL}/races/{nome_busca}"
            resposta = requests.get(url)
            dados = resposta.json()
            return dados
        except Exception as e:
            print(f"Erro na busca: {e}")
            return None
    return None

def buscar_dnd(pergunta):
    # Primeiro tenta buscar como classe
    dados = buscar_dnd_classe(pergunta)
    if dados:
        return dados
    
    # Se não for classe, tenta como raça
    dados = buscar_dnd_raca(pergunta)
    if dados:
        return dados
    
    return None