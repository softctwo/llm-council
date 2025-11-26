"""Multi-provider LLM API client for making requests to different services."""

import httpx
from typing import List, Dict, Any, Optional
from .config import (
    OPENROUTER_API_KEY, OPENROUTER_API_URL,
    DEEPSEEK_API_KEY, DEEPSEEK_API_URL,
    MOONSHOT_API_KEY, MOONSHOT_API_URL,
    MINIMAX_API_KEY, MINIMAX_API_URL,
    ZHIPU_API_KEY, ZHIPU_API_URL,
    GEMINI_API_KEY, GEMINI_API_URL
)


def parse_model_identifier(model: str) -> tuple[str, str]:
    """
    Parse model identifier to determine provider and actual model name.

    Args:
        model: Model identifier in format "provider:model_name" or just "model_name"

    Returns:
        Tuple of (provider, model_name)
    """
    if ":" in model:
        parts = model.split(":", 1)
        return parts[0], parts[1]
    return "openrouter", model


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via appropriate API provider.

    Args:
        model: Model identifier (e.g., "openrouter:x-ai/grok-4.1-fast:free", "deepseek:deepseek-chat")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    provider, model_name = parse_model_identifier(model)

    if provider == "openrouter":
        return await _query_openrouter(model_name, messages, timeout)
    elif provider == "deepseek":
        return await _query_deepseek(model_name, messages, timeout)
    elif provider == "moonshot":
        return await _query_moonshot(model_name, messages, timeout)
    elif provider == "minimax":
        return await _query_minimax(model_name, messages, timeout)
    elif provider == "zhipu":
        return await _query_zhipu(model_name, messages, timeout)
    elif provider == "gemini":
        return await _query_gemini(model_name, messages, timeout)
    else:
        print(f"Unknown provider: {provider}")
        return None


async def _query_openrouter(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float
) -> Optional[Dict[str, Any]]:
    """Query OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(OPENROUTER_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message = data['choices'][0]['message']
            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }
    except Exception as e:
        print(f"Error querying OpenRouter model {model}: {e}")
        return None


async def _query_deepseek(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float
) -> Optional[Dict[str, Any]]:
    """Query DeepSeek API."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message = data['choices'][0]['message']
            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }
    except Exception as e:
        print(f"Error querying DeepSeek model {model}: {e}")
        return None


async def _query_moonshot(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float
) -> Optional[Dict[str, Any]]:
    """Query Moonshot API."""
    headers = {
        "Authorization": f"Bearer {MOONSHOT_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(MOONSHOT_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message = data['choices'][0]['message']
            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }
    except Exception as e:
        print(f"Error querying Moonshot model {model}: {e}")
        return None


async def _query_minimax(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float
) -> Optional[Dict[str, Any]]:
    """Query MiniMax API."""
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(MINIMAX_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message = data['choices'][0]['message']
            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }
    except Exception as e:
        print(f"Error querying MiniMax model {model}: {e}")
        return None


async def _query_zhipu(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float
) -> Optional[Dict[str, Any]]:
    """Query Zhipu API."""
    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(ZHIPU_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message = data['choices'][0]['message']
            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }
    except Exception as e:
        print(f"Error querying Zhipu model {model}: {e}")
        return None


async def _query_gemini(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float
) -> Optional[Dict[str, Any]]:
    """Query Google Gemini API."""
    headers = {
        "Content-Type": "application/json",
    }

    # Convert messages format for Gemini
    contents = []
    for msg in messages:
        contents.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
        }
    }

    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if "candidates" in data and data["candidates"]:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    'content': content,
                    'reasoning_details': None
                }
            else:
                print(f"No valid response from Gemini: {data}")
                return None

    except Exception as e:
        print(f"Error querying Gemini model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of OpenRouter model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
