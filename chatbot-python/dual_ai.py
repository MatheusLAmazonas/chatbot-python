import os
import requests
from typing import Dict, Any

class SecondAI:
    """Segunda API de IA para comparação e especialização"""
    
    def __init__(self):
        # Usando Hugging Face como segunda API gratuita
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
    
    def query(self, prompt: str, specialization: str = "geral") -> Dict[str, Any]:
        """Consulta a segunda IA"""
        try:
            # Prepara prompt especializado
            specialized_prompt = self._prepare_prompt(prompt, specialization)
            
            # Se não tem API key, usa simulação
            if not self.api_key:
                return self._simulate_response(prompt, specialization)
            
            response = requests.post(self.api_url, headers=self.headers, json={
                "inputs": specialized_prompt,
                "parameters": {"max_length": 200}
            })
            
            if response.status_code == 200:
                return {"success": True, "response": response.json()[0]['generated_text']}
            else:
                return self._simulate_response(prompt, specialization)
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _prepare_prompt(self, prompt: str, specialization: str) -> str:
        """Prepara prompt especializado"""
        if specialization == "historia":
            return f"Explain the lore and story background for: {prompt}"
        elif specialization == "mecanicas":
            return f"Explain the game mechanics and rules for: {prompt}"
        else:
            return f"Answer about RPG: {prompt}"
    
    def _simulate_response(self, prompt: str, specialization: str) -> Dict[str, Any]:
        """Resposta simulada para teste sem API key"""
        responses = {
            "historia": "Visão alternativa sobre a história e lore...",
            "mecanicas": "Perspectiva diferente sobre as mecânicas...",
            "geral": "Resposta complementar da segunda IA..."
        }
        return {
            "success": True,
            "response": responses.get(specialization, responses["geral"]),
            "simulated": True
        }
    
    def compare_responses(self, primary_response: str, secondary_response: str) -> Dict[str, Any]:
        """Compara as respostas das duas IAs"""
        return {
            "primary": primary_response,
            "secondary": secondary_response,
            "similarity": self._calculate_similarity(primary_response, secondary_response),
            "best": self._choose_best(primary_response, secondary_response)
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade básica entre textos"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0.0
    
    def _choose_best(self, text1: str, text2: str) -> str:
        """Escolhe a melhor resposta baseado em heurísticas simples"""
        # Prefere a resposta mais longa (mais detalhada)
        return "primary" if len(text1) > len(text2) else "secondary"

second_ai = SecondAI()