import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Import constants from config.py
import config

load_dotenv()

# Use constants from config.py, allowing .env to override if needed
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL_NAME", config.OPENAI_EMBEDDING_MODEL)
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL_NAME", config.OPENAI_CHAT_MODEL)
OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL_NAME", config.OPENAI_VISION_MODEL)

try:
    openai_client = OpenAI()
    print("OpenAI client initialized.")
except Exception as e:
    print(f"Fatal Error: Failed to initialize OpenAI client. Check OPENAI_API_KEY. Error: {e}")
    openai_client = None

def get_openai_embedding(text: str, model=OPENAI_EMBEDDING_MODEL) -> list[float] | None:
    if not openai_client:
        print("OpenAI client not available for embedding.")
        return None
    if not text or not isinstance(text, str):
        print("Embedding Error: Input text must be a non-empty string.")
        return None
    try:
        text = text.replace("\n", " ")
        response = openai_client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error calling OpenAI embedding API (model: {model}): {e}")
        return None

def get_openai_chat_completion(
    prompt: str,
    system_prompt: str = config.DEFAULT_SYSTEM_PROMPT,
    model=OPENAI_CHAT_MODEL
) -> str | None:
    if not openai_client:
        print("OpenAI client not available for chat completion.")
        return None
    if not prompt or not isinstance(prompt, str):
        print("Chat Completion Error: Input prompt must be a non-empty string.")
        return None
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=config.DEFAULT_CHAT_TEMPERATURE,
            max_tokens=config.DEFAULT_CHAT_MAX_TOKENS
        )
        content = response.choices[0].message.content
        return content.strip() if content else None
    except Exception as e:
        print(f"Error calling OpenAI chat completion API (model: {model}): {e}")
        return None

def get_openai_vision_description(
    image_bytes: bytes,
    prompt: str = config.DEFAULT_VISION_PROMPT,
    detail: str = config.DEFAULT_VISION_DETAIL,
    max_tokens: int = config.DEFAULT_VISION_MAX_TOKENS,
    model: str = OPENAI_VISION_MODEL
) -> str | None:
    if not openai_client:
        print("OpenAI client not available for vision description.")
        return None
    if not image_bytes:
        print("Vision Description Error: Image bytes are required.")
        return None
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{base64_image}"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url, "detail": detail}}
                ]
            }
        ]
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        content = response.choices[0].message.content
        return content.strip() if content else None
    except Exception as e:
        print(f"Error calling OpenAI vision API (model: {model}): {e}")
        return None