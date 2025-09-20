import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class BaseExpression(BaseModel):
    """Base class for expression models."""
    expr: str


class ExpressionIn(BaseExpression):
    """Input expression model."""
    pass


class ExpressionOut(BaseExpression):
    """Output expression model with result and timestamp."""
    result: Any
    timestamp: str = datetime.now().isoformat() + "Z"


# For backward compatibility
Expression = ExpressionIn
CalculatorLog = ExpressionOut
