from typing import TypedDict

class SearchResult(TypedDict):
    doc_id: int
    url: str
    snippet: str
    score: float
