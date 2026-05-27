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
    'tiefling': ['tiefling']
}

DND_API_URL = "https://www.dnd5eapi.co/api"

def buscar_dnd(pergunta):
    """Busca informações de classes ou raças do D&D baseado na pergunta"""
    nome_busca = None
    tipo_busca = None
    
    # Procura por classe
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
            dados['tipo_busca'] = tipo_busca
            return dados
        except Exception as e:
            print(f"Erro na busca: {e}")
            return None
    
    return None

def formatar_dados_dnd(dados):
    """Formata os dados da API de forma amigável"""
    if not dados:
        return None
    
    tipo = dados.get('tipo_busca', 'unknown')
    
    if tipo == 'class':
        nome = dados.get('name', 'Classe desconhecida')
        hit_die = dados.get('hit_die', 'N/A')
        
        # Pega algumas proficiências principais
        proficiencias = dados.get('proficiencies', [])
        prof_names = [p['name'] for p in proficiencias[:5]]  # Limita a 5
        
        texto = f"""
Classe: {nome}
Dado de Vida: d{hit_die}
Proficiências: {', '.join(prof_names) if prof_names else 'Variadas'}
"""
        return texto
    
    elif tipo == 'race':
        nome = dados.get('name', 'Raça desconhecida')
        speed = dados.get('speed', 'N/A')
        
        # Pega alguns traços raciais
        traits = dados.get('traits', [])
        trait_names = [t['name'] for t in traits[:3]]
        
        texto = f"""
Raça: {nome}
Deslocamento: {speed} pés
Traços Raciais: {', '.join(trait_names) if trait_names else 'Variados'}
"""
        return texto
    
    return None