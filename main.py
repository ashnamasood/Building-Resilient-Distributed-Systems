from fastapi import FastAPI, Request, HTTPException, status
import time
import asyncio
import math
from typing import Optional

app = FastAPI()



@app.middleware("http")
async def add_student_id_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = "bscs23058"
    return response



class CircuitBreaker:
    def __init__(self, failure_threshold: int = 2, reset_timeout: int = 10):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.open_until = 0.0

    def allow(self) -> bool:
        return time.time() >= self.open_until

    def on_success(self) -> None:
        self.failure_count = 0

    def on_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.open_until = time.time() + self.reset_timeout


breaker = CircuitBreaker(failure_threshold=2, reset_timeout=10)


# =========================
# Simulated LLM work (slow)
# =========================
async def simulated_llm_work(delay: int = 10):
    # Simulates a long-running external LLM call
    await asyncio.sleep(delay)
    return {"response": "LLM result after delay"}



@app.get("/broken")
async def broken_endpoint():
    # BAD: blocking the event loop with time.sleep
    time.sleep(10)
    return {"status": "completed (blocked)", "note": "This blocked the event loop"}


@app.get("/fixed")
async def fixed_endpoint(timeout: Optional[int] = 3):
    # If circuit breaker is open, return fast fallback
    if not breaker.allow():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="LLM temporarily unavailable (circuit open)")

    try:
        # enforce a short timeout so a slow LLM doesn't hang the server
        result = await asyncio.wait_for(simulated_llm_work(delay=10), timeout=timeout)
        breaker.on_success()
        return {"status": "ok", "result": result}

    except (asyncio.TimeoutError, Exception):
        breaker.on_failure()
        # Fast fallback response
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail="LLM timeout or error — returned fallback")


@app.get("/breaker-status")
async def breaker_status():
    return {"allow": breaker.allow(), "failure_count": breaker.failure_count,
            "open_until": breaker.open_until}