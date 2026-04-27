from typing import List, Dict, Any


class TextChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_into_paragraphs(self, text: str) -> List[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        return paragraphs

    def build_chunks_from_paragraphs(self, paragraphs: List[str]) -> List[str]:
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if not current_chunk:
                current_chunk = para
                continue

            candidate = current_chunk + "\n\n" + para

            if len(candidate) <= self.chunk_size:
                current_chunk = candidate
            else:
                chunks.append(current_chunk)
                current_chunk = para

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def add_overlap(self, chunks: List[str]) -> List[str]:
        if not chunks:
            return []

        overlapped_chunks = []

        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped_chunks.append(chunk)
                continue

            prev = chunks[i - 1]
            prefix = prev[-self.overlap:] if len(prev) > self.overlap else prev
            overlapped_chunks.append(prefix + "\n\n" + chunk)

        return overlapped_chunks

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = document["text"]
        metadata = document["metadata"]

        paragraphs = self.split_into_paragraphs(text)
        raw_chunks = self.build_chunks_from_paragraphs(paragraphs)
        final_chunks = self.add_overlap(raw_chunks)

        chunked_documents = []

        for idx, chunk_text in enumerate(final_chunks):
            chunked_documents.append(
                {
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_id": idx,
                        "chunk_size": len(chunk_text),
                    },
                }
            )

        return chunked_documents

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_chunks = []

        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))

        return all_chunks