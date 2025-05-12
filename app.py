import streamlit as st
from PIL import Image
import io
from dotenv import load_dotenv

# Service Imports
from rekognition_service import get_image_labels # For Rekognition tags
from faiss_service import FAISSVectorStore     # For FAQ search
from openai_service import get_openai_vision_description, get_openai_chat_completion # For AI image description and chat completion

# Import constants from config.py
import config

# --- Initial Setup --- 
load_dotenv()
st.set_page_config(page_title="Simple AI Assistant", layout="wide")

# --- Helper Functions --- 

@st.cache_resource
def load_vector_store():
    """Loads the FAISS index and data, cached for efficiency."""
    print("Attempting to load FAISS index and FAQ data...")
    store = FAISSVectorStore()
    if not store.is_ready():
        # Log error to console, UI warning will be shown later if needed
        print("ERROR: FAQ Search Initialization Failed: Could not load FAISS index or data.") 
        return None
    print("FAISS index and FAQ data loaded successfully.")
    return store

def get_ai_vision_analysis(image_bytes):
    """Gets image description from OpenAI Vision."""
    try:
        # Use prompt from config
        description = get_openai_vision_description(image_bytes, prompt=config.APP_VISION_PROMPT, detail=config.DEFAULT_VISION_DETAIL)
        return description if description else "OpenAI Vision could not generate a description."
    except Exception as e:
        print(f"OpenAI Vision Error: {e}") 
        return f"Vision analysis failed: {e}"

def get_rekognition_analysis(image_bytes):
    """Gets image tags from AWS Rekognition."""
    try:
        rekognition_response = get_image_labels(image_bytes)
        if rekognition_response and 'Labels' in rekognition_response and rekognition_response['Labels']:
            tags = [label['Name'] for label in rekognition_response['Labels']]
            return ", ".join(tags)
        else:
            return "No tags detected by Rekognition."
    except Exception as e:
        print(f"Rekognition Error: {e}")
        return f"Rekognition analysis failed: {e}"

def get_faq_answer(vector_store_instance, query):
    """Classifies query topic, then searches FAISS & uses RAG for retail-related questions."""
    # 1. Classify Query Topic
    try:
        # Use prompt templates and system prompt from config
        classification_prompt = config.APP_CLASSIFY_USER_PROMPT_TEMPLATE.format(query=query)
        system_prompt_classify = config.APP_CLASSIFY_SYSTEM_PROMPT
        topic_classification = get_openai_chat_completion(prompt=classification_prompt, system_prompt=system_prompt_classify, model=config.OPENAI_CHAT_MODEL)

        print(f"Query Classification: {topic_classification}")

        if topic_classification != "RETAIL_RELATED":
            return "I specialize in questions about online retail stores. Please ask a question related to products, orders, shipping, returns, or your account."

    except Exception as e:
        print(f"Query Classification Error: {e}")
        # If classification fails, proceed cautiously.

    # 2. Proceed with RAG if Retail-Related
    if not vector_store_instance or not vector_store_instance.is_ready():
        return "FAQ search is not available (index not loaded)."

    try:
        search_results = vector_store_instance.search_faq_by_text(query, k=1)

        if not search_results:
            print("No relevant context found in FAISS for the query.")
            return "Sorry, I could not find any relevant information in the knowledge base to answer your question."

        top_result = search_results[0]
        context_question = top_result['question']
        context_answer = top_result['answer']

        # Use prompt template and system prompt from config
        rag_prompt = config.APP_RAG_USER_PROMPT_TEMPLATE.format(context_question=context_question, context_answer=context_answer, query=query)
        system_prompt_rag = config.APP_RAG_SYSTEM_PROMPT

        generated_answer = get_openai_chat_completion(prompt=rag_prompt, system_prompt=system_prompt_rag)

        if generated_answer:
            return generated_answer
        else:
            print("OpenAI generation failed after retrieving context. Returning raw answer.")
            return context_answer

    except Exception as e:
        print(f"FAQ RAG Error: {e}")
        return f"An error occurred during the FAQ process: {e}"

# --- Load Resources --- 
vector_store = load_vector_store()

# --- Streamlit App UI --- 
st.title("🤖 Simple AI Assistant")
st.caption("Describe photos and answer FAQ questions")

# --- Image Analysis Section ---
st.header("🖼️ Image Analysis")
st.write("Upload an image and click the button to get an AI-generated description and tags from AWS Rekognition.")

uploaded_file = st.file_uploader("1. Upload an image:", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded image", width=200)

    if st.button("Analyze Image"):
        # Process Image Analysis
        try:
            image_bytes = uploaded_file.getvalue()
            
            # Use columns to display results side-by-side
            col1, col2 = st.columns(2)
            
            with col1:
                with st.spinner("Getting AI Vision description... 👁️"):
                    ai_description = get_ai_vision_analysis(image_bytes)
                st.subheader("👁️ AI Vision Description:")
                st.markdown(ai_description)
                
            with col2:
                with st.spinner("Getting Rekognition tags... 🧠"):
                    rek_tags = get_rekognition_analysis(image_bytes)
                st.subheader("🧠 Rekognition Tags:")
                st.markdown(f"`{rek_tags}`")
                
        except Exception as e:
            st.error(f"Failed to process image: {e}")
    else:
        st.info("Click 'Analyze Image' to run analysis.")
else:
    st.info("Upload an image file (JPG, PNG) to enable analysis.")

st.divider()

# --- FAQ Section --- 
st.header("❓ Ask the Assistant (FAQ)")

if vector_store:
    user_question_faq = st.text_input("2. Enter your FAQ question:", label_visibility="collapsed")
    if user_question_faq:
        if st.button("Ask FAQ"):
            with st.spinner("Thinking... 🤔"): 
                answer = get_faq_answer(vector_store, user_question_faq) 
                st.subheader("💬 Assistant's Response:")
                st.markdown(answer) 
    else:
         st.info("Enter a question above and click 'Ask FAQ'.")
else:
    st.warning("FAQ search is unavailable. Failed to load the local index. Please check console logs and ensure `index_faq.py` was run successfully.")
