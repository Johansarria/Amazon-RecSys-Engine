import requests
import json

class ReasoningAgent:
    """
    Agente de razonamiento basado en Ollama.
    Este servicio está preparado, pero permanece inactivo hasta la Fase 4.3.
    """
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llama3" # Modelo por defecto
        
    def generate_explanation(self, user_history, recommendations):
        """
        Genera una explicación de por qué se recomendaron ciertos items
        basado en el historial de lectura del usuario.
        """
        prompt = f"""
        Eres un experto bibliotecario y curador de contenido.
        Un usuario ha leído el siguiente historial de revistas:
        {user_history}
        
        Tu motor matemático le ha recomendado estas nuevas revistas:
        {recommendations}
        
        Por favor, escribe un párrafo breve y muy elegante (máximo 3 oraciones) 
        explicando por qué estas recomendaciones son perfectas para él, basándote
        en la conexión temática entre lo que leyó y lo que se le recomienda.
        Responde en español.
        """
        
        try:
            # Lógica comentada/inactiva para evitar fallos si Ollama no está corriendo
            """
            response = requests.post(f"{self.ollama_url}/api/generate", json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            if response.status_code == 200:
                return response.json().get("response", "")
            """
            return "El servicio del agente de razonamiento está actualmente inactivo."
            
        except Exception as e:
            return f"Error conectando con el Agente: {e}"

# Instancia singleton para ser importada en main.py cuando se active
agent = ReasoningAgent()
