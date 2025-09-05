from pydantic import BaseModel
from typing import List
from calculator import expand_percent


class Expression(BaseModel):
    """Request Body of the `/calculate` API."""
    expr: str
    
    def expand_percent(self) -> str:
        """Return the expression after expanding the % symbols."""
        return expand_percent(self.expr)


class CalculatorLog(BaseModel):
    """Response Body of the `/history` API."""
    timestamp: str
    expr: str
    result: float
