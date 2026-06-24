"""Conversation memory: ChromaDB local store for retrieval."""

import os

import chromadb
from chromadb.config import Settings

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "vectorstore")


def get_collection(session_id: str = "default"):
    import chromadb

    client = chromadb.PersistentClient(path=os.path.abspath(DB_DIR))
    return client.get_or_create_collection(name=session_id)


def add_memory(session_id: str, text: str, metadata: dict | None = None):
    col = get_collection(session_id)
    import uuid

    col.add(documents=[text], metadatas=[metadata or {}], ids=[str(uuid.uuid4())])


def search_memory(session_id: str, query: str, n: int = 5) -> list[str]:
    col = get_collection(session_id)
    results = col.query(query_texts=[query], n_results=n)
    return results["documents"][0] if results["documents"] else []
