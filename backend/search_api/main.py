from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*" # Cho phép tất cả các nguồn gốc (origins) truy cập vào API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cho phép frontend nào gọi được
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các method (GET, POST, OPTIONS,...)
    allow_headers=["*"],  # Cho phép tất cả headers
)

class SearchRequest(BaseModel):
    query: str
    page: Optional[int] = 1
    limit: Optional[int] = 20

@app.get("/")
async def root():
    return {"message": "Search API is running"}

@app.post("/search")
def search_api(req: SearchRequest):
    try:
        results, total, elapsed = search.search(req.query, top_k=req.limit, page=req.page)
        return {
            "query": req.query,
            "results": results,
            "total": total,
            "page": req.page,
            "limit": req.limit,
            "time": elapsed,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))