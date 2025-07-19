from typing import Optional, Dict
from pydantic import BaseModel

class FilterQueryRequest(BaseModel):
    class Filter(BaseModel):
        field: str
        value: str
    filter: list[Filter]
    limit: int = 10
    exclusive_start_key: Optional[Dict] = None
    sort_by: Optional[str] = None  # Field to sort by, e.g. 'first_name', 'email'
    sort_order: Optional[str] = "asc"  # 'asc' or 'desc' (default: ascending)