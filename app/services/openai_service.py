# app/services/openai_service.py
import openai
from ..core.config import settings

# Configuración del cliente de OpenAI
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def get_chatbot_response(role: str, message: str) -> str:
    try:
        response = client.completions.create(
            model="gpt-4.1-nano-2025-04-14",  # Modelo de completions compatible
            prompt=f"Eres un asistente útil con el rol de {role}, deberás responder con lenguaje del rol. {message}. Respuesta:",
            max_tokens=128,
            temperature=0.7 # Creatividad 0-1
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error al obtener respuesta del API: {str(e)}"