from config import IAMode, PromptType, MODE_SETTINGS, PROMPT_TEMPLATES
from typing import Dict, Any

class PromptManager:
    """Gerencia a engenharia de prompts"""
    
    def __init__(self):
        self.current_mode = IAMode.PROFESSOR
        self.current_prompt_type = PromptType.ESTRUTURADO
    
    def set_mode(self, mode: IAMode):
        """Define o modo da IA"""
        self.current_mode = mode
        return f"Modo alterado para: {mode.value}"
    
    def set_prompt_type(self, prompt_type: PromptType):
        """Define o tipo de prompt"""
        self.current_prompt_type = prompt_type
        return f"Tipo de prompt alterado para: {prompt_type.value}"
    
    def create_prompt(self, question: str, dados_contexto: Dict = None) -> tuple:
        """Cria o prompt baseado no modo e tipo atual"""
        
        # Pega as configurações do modo atual
        mode_config = MODE_SETTINGS[self.current_mode]
        system_prompt = mode_config["system_prompt"]
        temperature = mode_config["temperature"]
        
        # Escolhe o template baseado no tipo de prompt
        template = PROMPT_TEMPLATES[self.current_prompt_type]
        
        # Prepara o prompt
        if self.current_prompt_type == PromptType.ESPECIALIZADO and dados_contexto:
            prompt = template.format(
                system_prompt=system_prompt,
                dados_contexto=str(dados_contexto),
                question=question
            )
        else:
            prompt = template.format(
                system_prompt=system_prompt,
                question=question
            )
        
        return prompt, temperature
    
    def get_available_modes(self) -> list:
        """Retorna lista de modos disponíveis"""
        return [mode.value for mode in IAMode]
    
    def get_available_prompt_types(self) -> list:
        """Retorna lista de tipos de prompt disponíveis"""
        return [pt.value for pt in PromptType]

prompt_manager = PromptManager()