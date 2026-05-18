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
    'dragonborn': ['dragonborn', 'draconato', 'dragon born'],
    'dwarf': ['anao', 'anão', 'dwarf'],
    'elf': ['elfo', 'elf'],
    'gnome': ['gnomo', 'gnome'],
    'half-elf': ['meio-elfo', 'half-elf', 'half elf'],
    'half-orc': ['meio-orc', 'half-orc', 'half orc'],
    'halfling': ['halfling', 'hobbit', 'pequenino'],
    'human': ['humano', 'human'],
    'tiefling': ['tiefling'],
    'aarakocra': ['aarakocra', 'pássaro', 'ave'],
    'genasi': ['genasi', 'genasio'],
    'goliath': ['goliath', 'golias'],
    'tabaxi': ['tabaxi', 'gato', 'felino'],
    'tortle': ['tortle', 'tartaruga'],
    'kenku': ['kenku', 'corvo'],
    'firbolg': ['firbolg'],
    'aasimar': ['aasimar', 'anjo'],
    'warforged': ['warforged', 'constructo'],
    'shifter': ['shifter', 'mudador'],
    'changeling': ['changeling', 'metamorfo'],
    'centaur': ['centauro', 'centaur'],
    'minotaur': ['minotauro', 'minotaur'],
    'satyr': ['sátiro', 'satyr', 'satiro'],
    'leonin': ['leonin', 'leão'],
    'loxodon': ['loxodon', 'elefante']
}

DND_API_URL = "https://www.dnd5eapi.co/api"

def buscar_dnd(pergunta):
    """Busca informações de classes ou raças do D&D baseado na pergunta"""
    nome_busca = None
    tipo_busca = None  # 'class' ou 'race'
    
    # Primeiro procura por classe
    for classe, variacoes in CLASSES_DND.items():
        for variacao in variacoes:
            if variacao in pergunta.lower():
                nome_busca = classe
                tipo_busca = 'class'
                break
        if nome_busca:
            break
    
    # Se não achou classe, procura por raça
    if not nome_busca:
        for raca, variacoes in RACAS_DND.items():
            for variacao in variacoes:
                if variacao in pergunta.lower():
                    nome_busca = raca
                    tipo_busca = 'race'
                    break
            if nome_busca:
                break
    
    # Busca na API
    if nome_busca:
        try:
            if tipo_busca == 'class':
                url = f"{DND_API_URL}/classes/{nome_busca}"
            else:
                url = f"{DND_API_URL}/races/{nome_busca}"
            
            resposta = requests.get(url)
            dados = resposta.json()
            
            # Adiciona o tipo ao retorno para identificar depois
            dados['tipo_busca'] = tipo_busca
            
            return dados
        except Exception as e:
            print(f"Erro na busca: {e}")
            return None
    
    return None