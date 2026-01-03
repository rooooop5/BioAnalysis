from fastapi import APIRouter,Query
from app.schemas.dna_schemas import DNASequence,DNAAnalysisOptions,DNAAnalysisResponse

dna_router=APIRouter(prefix="/dna",tags=["DNA"])

@dna_router.post("/analyze",response_model=DNAAnalysisResponse,summary="DNA Sequence Analysis and Validity Check")
def analysis(req:DNASequence,options:DNAAnalysisOptions=Query()):
    return {"msg":"ok"}