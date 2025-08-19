import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: str):
    try:
        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        # TODO: Add history
        # Record into history (most recent first)
        history.appendleft({
            "expr": expr,
            "result": result,
            "time": datetime.utcnow().isoformat() + "Z",
        })
        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}

# TODO GET /hisory

@app.get("/history")
def get_history(limit: int = Query(50, ge=1, le=HISTORY_MAX)):
    # Return most recent first
    return list(history)[:limit]


# TODO DELETE /history
@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True}