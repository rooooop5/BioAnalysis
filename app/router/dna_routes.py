from typing import TYPE_CHECKING

from fastapi import APIRouter, Query, Depends
from app.bio.dna_services import analyze_dna,dna_validity
from app.schemas.dna_schemas import DNAAnalysisOptions, DNAAnalysisResponse, DNASequence,DNAValidityResponse



dna_router = APIRouter(prefix="/dna", tags=["DNA"])


@dna_router.post(
    "/check-validity",
    response_model=DNAValidityResponse,
    summary="DNA Sequence Validity Check",
)
def check_validity(dna: DNASequence):
    reasons_dict=dna_validity(dna)
    invalidity_reasons=DNAValidityResponse.model_validate(reasons_dict)
    return invalidity_reasons


@dna_router.post("/analyze", summary="DNA Sequence Analysis")
def analysis(dna: DNASequence, options: DNAAnalysisOptions = Query(),validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        return validity
    res_dict=analyze_dna(dna.seq,options)
    response=DNAAnalysisResponse.model_validate(res_dict)
    return response
