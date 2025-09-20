import math
from datetime import datetime
from fastapi import APIRouter, Depends
from asteval import Interpreter

from app.schemas import ExpressionIn, ExpressionOut
from app.dependencies import expand_percent, get_history

router = APIRouter()

# Safe evaluator
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@router.post("/calculate")
def calculate(expr: ExpressionIn, history=Depends(get_history)):
    try:
        code = expand_percent(expr.expr)
        code = code.replace('÷', '/').replace('×', '*')
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        history.appendleft(ExpressionOut(
            timestamp=datetime.now().isoformat() + "Z",
            expr=expr.expr,
            result=result))
        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}
