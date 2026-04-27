from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> np.ndarray:
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings

    def embed_chunks(self, chunks: List[dict]) -> np.ndarray:
        texts = [chunk["text"] for chunk in chunks]
        return self.embed_texts(texts)