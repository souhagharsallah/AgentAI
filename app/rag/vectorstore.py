import json
from pathlib import Path
from typing import List, Dict, Any

import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.texts: List[str] = []
        self.metadata: List[Dict[str, Any]] = []

    def add_embeddings(self, embeddings: np.ndarray, chunks: List[Dict[str, Any]]) -> None:
        if len(embeddings) != len(chunks):
            raise ValueError("Le nombre d'embeddings doit être égal au nombre de chunks.")

        embeddings = embeddings.astype("float32")
        self.index.add(embeddings)

        for chunk in chunks:
            self.texts.append(chunk["text"])
            self.metadata.append(chunk["metadata"])

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "text": self.texts[idx],
                    "metadata": self.metadata[idx],
                }
            )

        return results

    def save(self, index_path: str, metadata_path: str) -> None:
        index_path = Path(index_path)
        metadata_path = Path(metadata_path)

        index_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(index_path))

        payload = {
            "texts": self.texts,
            "metadata": self.metadata,
            "dimension": self.dimension,
        }

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, index_path: str, metadata_path: str) -> "FAISSVectorStore":
        index_path = Path(index_path)
        metadata_path = Path(metadata_path)

        if not index_path.exists():
            raise FileNotFoundError(f"Index introuvable : {index_path}")

        if not metadata_path.exists():
            raise FileNotFoundError(f"Métadonnées introuvables : {metadata_path}")

        with open(metadata_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        dimension = payload["dimension"]
        store = cls(dimension=dimension)
        store.index = faiss.read_index(str(index_path))
        store.texts = payload["texts"]
        store.metadata = payload["metadata"]

        return store