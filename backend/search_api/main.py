from fastapi import FastAPI
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

@app.post("/search")
def search_api(req: SearchRequest):
    results, total, elapsed = search.search(req.query, top_k=req.limit, page=req.page)
    return {"query": req.query, "results": results, "page": req.page, "limit": req.limit, "total": total, "time" : round(elapsed, 3)}
