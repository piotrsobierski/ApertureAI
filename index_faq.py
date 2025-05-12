import json
import os
import time
import numpy as np
import faiss
from dotenv import load_dotenv
# Removed OpenSearch import
from openai_service import get_openai_embedding # Keep OpenAI embedding service

# Load environment variables from .env file (for OpenAI key)
load_dotenv()

# Configuration from Environment Variables (with defaults)
FAQ_SOURCE_FILE_REL_PATH = os.getenv("FAQ_SOURCE_JSON_FILE", "data/dummy_faq.json")
FAISS_DIR_NAME = os.getenv("FAISS_OUTPUT_DIR_NAME", "faiss_index")
FAISS_BASE_NAME = os.getenv("FAISS_INDEX_BASE_NAME", "faq-index")
VECTOR_DIMENSION = int(os.getenv("OPENAI_EMBEDDING_MODEL_DIMENSION", "1536"))

# Construct full paths based on the script's location
SCRIPT_DIR = os.path.dirname(__file__)
FAQ_FILE_PATH = os.path.join(SCRIPT_DIR, FAQ_SOURCE_FILE_REL_PATH)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, FAISS_DIR_NAME)
FAISS_INDEX_PATH = os.path.join(OUTPUT_DIR, f'{FAISS_BASE_NAME}.faiss')
FAQ_DATA_PATH = os.path.join(OUTPUT_DIR, f'{FAISS_BASE_NAME}_data.json')

def main():
    """
    Main function to load FAQs, generate embeddings, build a FAISS index,
    and save the index and corresponding text data.
    """
    print(f"Starting FAISS FAQ indexing process from file: {FAQ_FILE_PATH}")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Using output directory: {OUTPUT_DIR}")

    # --- 1. Load FAQ Data ---
    try:
        with open(FAQ_FILE_PATH, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
        print(f"Loaded {len(faqs)} FAQ entries from JSON file.")
    except FileNotFoundError:
        print(f"Error: FAQ file not found at {FAQ_FILE_PATH}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {FAQ_FILE_PATH}: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while loading the FAQ file: {e}")
        return

    if not faqs:
        print("No FAQs loaded, exiting.")
        return

    # --- 2. Generate Embeddings and Prepare Data ---
    print("\nStarting embedding generation...")
    embeddings_list = []
    faq_data_for_lookup = [] # Store corresponding text data
    failed_count = 0
    
    for i, faq in enumerate(faqs):
        question = faq.get('question')
        answer = faq.get('answer')

        if not question or not answer:
            print(f"Skipping FAQ entry {i+1} due to missing question or answer.")
            failed_count += 1
            continue

        print(f"Processing FAQ {i+1}/{len(faqs)}: '{question[:50]}...'")

        # Get embedding for the question
        embedding = get_openai_embedding(question)

        if embedding is None:
            print(f"  Failed to generate embedding for FAQ {i+1}. Skipping.")
            failed_count += 1
            time.sleep(1) # Small delay after a failure
            continue
            
        # Check dimension
        if len(embedding) != VECTOR_DIMENSION:
            print(f"  Error: Embedding dimension mismatch for FAQ {i+1}. Expected {VECTOR_DIMENSION}, got {len(embedding)}. Skipping.")
            failed_count += 1
            continue

        embeddings_list.append(embedding)
        # Store the original data with an ID corresponding to its position
        faq_data_for_lookup.append({
            'id': len(faq_data_for_lookup), # Simple sequential ID
            'question': question,
            'answer': answer
        })
        
        # Optional: Rate limiting for OpenAI API
        # time.sleep(0.1)

    print(f"\nSuccessfully generated embeddings for {len(embeddings_list)} FAQs.")
    if failed_count > 0:
        print(f"Failed to generate embeddings for {failed_count} FAQs.")

    if not embeddings_list:
        print("No embeddings were generated. Cannot build FAISS index.")
        return

    # --- 3. Build FAISS Index ---
    print("\nBuilding FAISS index...")
    try:
        embeddings_np = np.array(embeddings_list).astype('float32')
        
        # Normalize vectors (important for cosine similarity / IndexFlatIP)
        # OpenAI embeddings are typically pre-normalized, but good practice to ensure
        faiss.normalize_L2(embeddings_np)
        
        # Use IndexFlatIP for cosine similarity (Inner Product on normalized vectors)
        index = faiss.IndexFlatIP(VECTOR_DIMENSION)
        
        # Add vectors to the index
        index.add(embeddings_np)
        
        print(f"FAISS index built successfully. Index contains {index.ntotal} vectors.")
    except Exception as e:
        print(f"Error building FAISS index: {e}")
        return

    # --- 4. Save Index and Data ---
    try:
        print(f"Saving FAISS index to: {FAISS_INDEX_PATH}")
        faiss.write_index(index, FAISS_INDEX_PATH)
        print("FAISS index saved successfully.")
    except Exception as e:
        print(f"Error saving FAISS index: {e}")
        # Continue to try saving text data even if index saving fails

    try:
        print(f"Saving FAQ text data to: {FAQ_DATA_PATH}")
        with open(FAQ_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(faq_data_for_lookup, f, ensure_ascii=False, indent=2)
        print("FAQ text data saved successfully.")
    except Exception as e:
        print(f"Error saving FAQ text data: {e}")

    print("\nFAQ indexing process finished.")

if __name__ == "__main__":
    main() 