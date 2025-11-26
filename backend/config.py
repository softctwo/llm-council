"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Council members - using free OpenRouter models and other services
COUNCIL_MODELS = [
    "openrouter:x-ai/grok-4.1-fast:free",  # Free OpenRouter model
    "deepseek:deepseek-chat",               # DeepSeek
    "moonshot:kimi-k2-thinking-turbo",      # Moonshot/KIMI Thinking Turbo
    "zhipu:glm-4.6",                        # Zhipu GLM-4.6
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "gemini:gemini-3-pro-preview"

# API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
MOONSHOT_API_URL = "https://api.moonshot.cn/v1/chat/completions"
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_pro"
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
