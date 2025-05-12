OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
OPENAI_CHAT_MODEL = "gpt-3.5-turbo"
OPENAI_VISION_MODEL = "gpt-4o"

# OpenAI API Prompts

# Default system prompt for general chat completions
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."

# Default prompt for image description using the vision model
DEFAULT_VISION_PROMPT = "Describe this image concisely in one sentence."

# Prompt for the OpenAI Vision API in app.py
APP_VISION_PROMPT = "Provide a concise, one-sentence description of this image."

# System prompt for the query classification task in app.py
APP_CLASSIFY_SYSTEM_PROMPT = "You are a classification assistant."

# User prompt template for the query classification task in app.py
# Use .format(query=user_query)
APP_CLASSIFY_USER_PROMPT_TEMPLATE = """Classify the following user query based on whether it relates to an online retail store (e.g., questions about products, orders, shipping, returns, accounts, payments). Respond ONLY with 'RETAIL_RELATED' or 'NOT_RETAIL_RELATED'.

User Query: "{query}"
"""

# System prompt for the RAG task in app.py
APP_RAG_SYSTEM_PROMPT = "You are an AI assistant. Answer the user's question based ONLY on the provided FAQ context. If the context doesn't directly answer the question, say that you cannot answer based on the provided information. Do not mention the FAQ context in your response."

# User prompt template for the RAG task in app.py
# Use .format(context_question=context_question, context_answer=context_answer, query=user_query)
APP_RAG_USER_PROMPT_TEMPLATE = """Based on the following information from the FAQ:

Question: {context_question}
Answer: {context_answer}

Please answer the user's question: "{query}" """

 
DEFAULT_VISION_DETAIL = "low"
DEFAULT_VISION_MAX_TOKENS = 100
DEFAULT_CHAT_TEMPERATURE = 0.7
DEFAULT_CHAT_MAX_TOKENS = 150
 
FAQ_SOURCE_JSON_FILE="data/dummy_faq.json"
FAISS_OUTPUT_DIR_NAME="faiss_index"

AWS_DEFAULT_REGION = "eu-central-1" 
# Rekognition settings
REKOGNITION_MAX_LABELS = 20
REKOGNITION_MIN_CONFIDENCE = 75.0 