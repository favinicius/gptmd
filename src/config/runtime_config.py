import os
from dotenv import load_dotenv

# Load/Reload environment variables
load_dotenv(override=True)

# Configuration Variables
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    # Fallback legacy names just in case
    GENAI_API_KEY = os.getenv("GEMINI_PAID_KEY")

GEMINI_MODEL_PREFERENCIAL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
GEMINI_MODEL_SECUNDARIO = os.getenv("GEMINI_MODEL_LIGHT", "gemini-2.0-flash")

# Database Configuration
DB_URL = os.getenv("DB_URL", "sqlite:///gptmd.db")

# API Keys Configuration (Tiered)
GENAI_PAID_KEY = os.getenv("GEMINI_PAID_KEY")
if not GENAI_PAID_KEY:
    # Fallback to single primary key if tiered setup is missing
    GENAI_PAID_KEY = os.getenv("GENAI_API_KEY")

GENAI_FREE_KEYS = []
for key, value in os.environ.items():
    if key.startswith("GEMINI_FREE_") or key.startswith("GEMINI_API_KEY_FREE"):
        if value and value != GENAI_PAID_KEY:
             GENAI_FREE_KEYS.append(value)

# If no paid key defined but we have free keys, logic handles it. 
# If absolutely no keys, we might want to warn, but we let Agent handle validation.
