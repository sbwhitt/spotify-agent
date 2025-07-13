from strands import Agent
from strands.models.ollama import OllamaModel

def get_ollama_model() -> OllamaModel:
    return OllamaModel(
        host="http://localhost:11434",
        model_id="qwen3:1.7b"
    )
