import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import router
from app.config import get_settings

settings = get_settings()
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="GrantBridge Europe API", version="0.1.0")
app.include_router(router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled API error", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

