from fastapi import FastAPI,HTTPException,Request,Response
from fastapi.responses import JSONResponse
from app.router.dna_routes import dna_router
app=FastAPI()


@app.exception_handler(HTTPException)
def handler(exception:HTTPException,req:Request):
    return JSONResponse(status_code=exception.status_code,
                        content=
                            {"error":
                                 {"status_code":exception.status_code,
                                  "message":exception.detail,"path":req.url.path
                                 }
                            }
                        )

app.include_router(dna_router)