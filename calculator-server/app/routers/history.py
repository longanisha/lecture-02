from fastapi import APIRouter, Depends
from collections import deque

from app.schemas import ExpressionOut
from app.dependencies import get_history, HISTORY_MAX

router = APIRouter()


@router.get("/history")
def get_history_endpoint(limit: int = 50, history=Depends(get_history)) -> list[ExpressionOut]:
    return list(history)[: max(0, min(limit, HISTORY_MAX))]


@router.delete("/history")
def clear_history(history=Depends(get_history)):
    history.clear()
    return {"ok": True, "cleared": True}
