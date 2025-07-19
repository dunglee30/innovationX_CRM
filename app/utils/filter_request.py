from typing import Optional, Dict
from pydantic import BaseModel

class FilterQueryRequest(BaseModel):
    class Filter(BaseModel):
        field: str
        value: str
    filter: list[Filter]
    limit: int = 10
    exclusive_start_key: Optional[Dict] = None