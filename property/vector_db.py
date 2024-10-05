# property/vector_db.py

import os
import logging
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma  # Updated import
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# Fetch API key, use fake key if not set
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or 'fake_openai_key'

# Embeddings setup
try:
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY, 
        model="text-embedding-3-small"
    )
except Exception as e:
    logger.error(f"Failed to initialize OpenAIEmbeddings: {e}")
    embeddings = None

# Chroma vector database setup
try:
    persist_directory = os.path.join(BASE_DIR := os.path.dirname(os.path.abspath(__file__)), "chroma")
    vector_db = Chroma(
        collection_name="airbnb",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    ) if embeddings else None
except Exception as e:
    logger.error(f"Failed to initialize Chroma vector_db: {e}")
    vector_db = None

def add_data(meta_data, id):
    if not vector_db:
        logger.warning("vector_db is not initialized. Skipping add_data.")
        return

    try:
        doc = Document(
            page_content=meta_data,
            metadata={"id": str(id)}  
        )
        vector_db.add_documents(documents=[doc])
    except Exception as e:
        logger.error(f"Error adding document to vector_db: {e}")
