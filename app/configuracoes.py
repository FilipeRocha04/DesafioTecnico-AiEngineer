import os
from dotenv import load_dotenv


load_dotenv()

class Configuracoes:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", 0.2))

    if not OPENAI_API_KEY:
        raise RuntimeError("❌ OPENAI_API_KEY não foi encontrada no .env")


configuracoes = Configuracoes()
