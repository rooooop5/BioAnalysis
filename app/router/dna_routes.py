from typing import TYPE_CHECKING

from fastapi import APIRouter, Query

from app.schemas.dna_schemas import DNAAnalysisOptions, DNAAnalysisResponse, DNASequence

if TYPE_CHECKING:

    def analyze_dna(dna: DNASequence, options: DNAAnalysisOptions):
        pass

    def dna_validity(dna: DNASequence):
        pass


dna_router = APIRouter(prefix="/dna", tags=["DNA"])


@dna_router.post(
    "/check-validity",
    response_model=DNAAnalysisResponse,
    response_model_include={"validity"},
    summary="DNA Sequence Validity Check",
)
def check_validity(dna: DNASequence):
    return dna_validity(dna)


@dna_router.post("/analyze", response_model=DNAAnalysisResponse, summary="DNA Sequence Analysis")
def analysis(dna: DNASequence, options: DNAAnalysisOptions = Query()):
    return analyze_dna(dna, options)
