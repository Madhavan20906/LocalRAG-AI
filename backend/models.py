from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class SourceChunk(BaseModel):
    text: str
    metadata: dict
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_processed: int
