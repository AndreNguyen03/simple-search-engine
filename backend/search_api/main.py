from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from search_api import search

app = FastAPI()

class SearchRequest(BaseModel):
    q: str
    page: Optional[int] = 1
    limit: Optional[int] = 20

@app.post("/search")
def search_api(req: SearchRequest):
    results = search.search(req.q, top_k=req.limit, page=req.page)
    return {"query": req.q, "results": results, "page": req.page, "limit": req.limit}
