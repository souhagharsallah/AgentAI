from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.query_service import QueryService

app = FastAPI(title="Polytech RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

query_service = QueryService()


class QuestionRequest(BaseModel):
    question: str
    formation: str | None = None
    annee: str | None = None
    top_k: int = 2


@app.get("/")
def root():
    return {"message": "API RAG en marche"}


@app.post("/ask")
def ask_question(payload: QuestionRequest):
    response = query_service.ask(payload.question, payload.formation, payload.annee, top_k=payload.top_k)
    return response
