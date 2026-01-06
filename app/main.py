from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.router.dna_routes import dna_router
desc="""
# Bioanalysis allows you to do awesome stuff🚀
"""
app = FastAPI(description=desc)


@app.exception_handler(HTTPException)
def handler(req: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"error": {"status_code": exception.status_code, "message": exception.detail, "path": req.url.path}},
    )


app.include_router(dna_router)
