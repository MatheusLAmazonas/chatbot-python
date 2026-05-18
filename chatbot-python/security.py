import re
from typing import Tuple, Optional
from enum import Enum

class RiskLevel(Enum):
    SAFE = "safe"
    SUSPECT = "suspect"
    BLOCKED = "blocked"

class SecurityChecker:
    """Sistema completo de proteção contra ameaças"""
    
    def __init__(self):
        # Padrões de Prompt Injection
        self.prompt_injection = [
            r"ignore previous instructions",
            r"ignore all previous commands",
            r"forget your previous instructions",
            r"disregard previous prompts",
            r"you are now a different AI",
            r"from now on, act as",
            r"pretend you are",
            r"override your system prompt",
            r"system prompt:",
            r"new role:",
            r"忽略之前的指令",
        ]
        
        # Comandos maliciosos
        self.malicious_commands = [
            r"rm -rf", r"del /f", r"format", r"drop table",
            r"delete from", r"shutdown", r"sudo", r"chmod 777",
            r"eval\(", r"exec\(", r"system\(", r"shell_exec",
            r"base64_decode", r"nmap", r"sqlmap",
        ]
        
        # Conteúdo inadequado
        self.inappropriate = [
            r"hack.*system", r"crack.*password", r"steal.*data",
            r"invadir", r"roubar.*senha", r"hackear",
            r"golpe", r"fraude", r"extorsão",
        ]
        
        # Quebra de regras
        self.rule_breaking = [
            r"bypass.*restriction", r"circumvent.*safety",
            r"remove.*limit", r"disable.*security",
            r"no restrictions", r"unrestricted mode", r"jailbreak",
            r"contornar.*regra", r"quebrar.*limite",
        ]
        
        # Palavras bloqueadas
        self.blocked_words = [
            "assassinar", "suicídio", "estupro", "pedofilia",
            "torturar", "sequestrar", "bombas", "fazer explosivos"
        ]
    
    def check_all(self, text: str) -> Tuple[bool, str, RiskLevel]:
        """Executa todas as verificações"""
        
        # Verifica tamanho
        if len(text) > 2000:
            return False, "Texto muito longo (máx 2000 caracteres)", RiskLevel.BLOCKED
        
        text_lower = text.lower()
        
        # Verifica prompt injection
        for pattern in self.prompt_injection:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, f"Prompt Injection detectado", RiskLevel.BLOCKED
        
        # Verifica comandos maliciosos
        for pattern in self.malicious_commands:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, f"Comando malicioso detectado", RiskLevel.BLOCKED
        
        # Verifica conteúdo inadequado
        for word in self.blocked_words:
            if word in text_lower:
                return False, f"Conteúdo inadequado bloqueado", RiskLevel.BLOCKED
        
        for pattern in self.inappropriate:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, f"Pedido inadequado detectado", RiskLevel.BLOCKED
        
        # Verifica quebra de regras
        for pattern in self.rule_breaking:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, f"Tentativa de quebrar regras", RiskLevel.BLOCKED
        
        return True, "Entrada segura", RiskLevel.SAFE
    
    def sanitize_input(self, text: str) -> str:
        """Sanitiza a entrada removendo caracteres perigosos"""
        # Remove caracteres de controle
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        # Remove múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        # Remove caracteres especiais perigosos
        dangerous = ['`', ';', '&&', '||', '|', '$', '%', '!']
        for char in dangerous:
            text = text.replace(char, '')
        return text.strip()

security_checker = SecurityChecker()