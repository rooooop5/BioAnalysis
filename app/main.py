from fastapi import FastAPI
from app.router.dna_routes import dna_router
app=FastAPI()
app.include_router(dna_router)

