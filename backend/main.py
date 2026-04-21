from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse, SourceChunk, UploadResponse
from services.pdf_service import extract_text_from_pdf, chunk_text
from services.embedding_service import embedding_service
from services.llm_service import generate_answer

app = FastAPI(title="Local RAG API", version="1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        # Read file
        contents = await file.read()
        
        # Extract text
        text = extract_text_from_pdf(contents)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
            
        # Chunk text
        chunks = chunk_text(text)
        
        # Embed and store
        embedding_service.add_chunks(chunks, file.filename)
        
        return UploadResponse(
            message="Document processed successfully",
            filename=file.filename,
            chunks_processed=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        # 1. Search for relevant chunks
        results = embedding_service.search(request.query, request.top_k)
        
        # 2. Generate answer
        answer = generate_answer(request.query, results)
        
        # 3. Format response
        sources = [
            SourceChunk(
                text=res["chunk"],
                metadata=res["metadata"],
                score=res["score"]
            ) for res in results
        ]
        
        return QueryResponse(
            answer=answer,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
