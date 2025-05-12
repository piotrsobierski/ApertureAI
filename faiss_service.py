import faiss
import json
import numpy as np
import os
from openai_service import get_openai_embedding
from dotenv import load_dotenv

load_dotenv()

FAISS_DIR_NAME = os.getenv("FAISS_OUTPUT_DIR_NAME", "faiss_index")
FAISS_BASE_NAME = os.getenv("FAISS_INDEX_BASE_NAME", "faq-index")

SCRIPT_DIR = os.path.dirname(__file__)
OUTPUT_DIR_FULL_PATH = os.path.join(SCRIPT_DIR, FAISS_DIR_NAME)
FAISS_INDEX_PATH_FULL = os.path.join(OUTPUT_DIR_FULL_PATH, f'{FAISS_BASE_NAME}.faiss')
FAQ_DATA_PATH_FULL = os.path.join(OUTPUT_DIR_FULL_PATH, f'{FAISS_BASE_NAME}_data.json')

class FAISSVectorStore:
    def __init__(self, index_path: str = FAISS_INDEX_PATH_FULL, data_path: str = FAQ_DATA_PATH_FULL):
        self.index_path = index_path
        self.data_path = data_path
        self.index = None
        self.faq_data = []
        self._load_resources()

    def _load_resources(self):
        try:
            if not os.path.exists(self.index_path):
                print(f"Error: FAISS index file not found at {self.index_path}. Run indexing script first.")
                return
            self.index = faiss.read_index(self.index_path)
            print(f"FAISS index loaded from {self.index_path} ({self.index.ntotal} vectors).")
        except Exception as e:
            print(f"Error loading FAISS index from {self.index_path}: {e}")
            self.index = None
            return

        try:
            if not os.path.exists(self.data_path):
                print(f"Error: FAQ metadata file not found at {self.data_path}. Index may be unusable.")
                return
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.faq_data = json.load(f)
            print(f"FAQ metadata loaded from {self.data_path} ({len(self.faq_data)} entries).")
        except Exception as e:
            print(f"Error loading FAQ metadata from {self.data_path}: {e}")
            self.faq_data = []
            self.index = None
            print("Index invalidated due to metadata loading failure.")

        if self.index is not None and len(self.faq_data) != self.index.ntotal:
            print(f"Warning: Mismatch between vector count ({self.index.ntotal}) and metadata entries ({len(self.faq_data)}). Results may be inconsistent.")

    def is_ready(self) -> bool:
        return self.index is not None and bool(self.faq_data)

    def search_faq_by_text(self, query_text: str, k: int = 3) -> list[dict]:
        if not self.is_ready():
            print("Error: FAISSVectorStore is not ready (index or data not loaded). Cannot search.")
            return []
        if not query_text:
            print("Error: Query text cannot be empty.")
            return []

        query_embedding = get_openai_embedding(query_text)
        if query_embedding is None:
            print("Error: Failed to generate embedding for the query text.")
            return []
        
        query_np = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(query_np)

        try:
            print(f"Searching FAISS index for {k} nearest neighbors...")
            distances, indices = self.index.search(query_np, k)
            
            results = []
            if indices.size > 0:
                for i in range(indices.shape[1]):
                    vector_index = indices[0, i]
                    if 0 <= vector_index < len(self.faq_data):
                        matched_metadata = self.faq_data[vector_index]
                        results.append({
                            'id': matched_metadata.get('id', vector_index),
                            'question': matched_metadata.get('question', 'N/A'),
                            'answer': matched_metadata.get('answer', 'N/A'),
                            'similarity_score': float(distances[0, i])
                        })
                    else:
                        print(f"Warning: Retrieved index {vector_index} is out of bounds for metadata (size {len(self.faq_data)}).")
            
            print(f"Found {len(results)} results from FAISS search.")
            return results
        except Exception as e:
            print(f"Error performing FAISS search: {e}")
            return []