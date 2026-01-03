from typing import TYPE_CHECKING
from fastapi import APIRouter,Query
from app.schemas.dna_schemas import DNASequence,DNAAnalysisOptions,DNAAnalysisResponse

if TYPE_CHECKING:
    def analyze_dna(dna:DNASequence):
        pass
    def dna_validity(dna:DNASequence):
        pass

dna_router=APIRouter(prefix="/dna",tags=["DNA"])

@dna_router.post("/analyze",response_model=DNAAnalysisResponse,summary="DNA Sequence Analysis and Validity Check")
def analysis(dna:DNASequence,options:DNAAnalysisOptions=Query()):
    return analyze_dna(dna)

@dna_router.post("/check-validity",response_model=DNAAnalysisResponse,response_model_include={"validity"})
def check_validity(dna:DNASequence):
    return dna_validity(dna)