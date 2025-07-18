from typing import Optional, Dict
from pydantic import BaseModel

class FilterQueryRequest(BaseModel):
    filter: list[Dict[str, str]]
    limit: int = 10
    exclusive_start_key: Optional[Dict] = None