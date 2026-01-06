from typing import TYPE_CHECKING

from fastapi import APIRouter, Query, Depends,HTTPException
from app.bio.dna_services import analyze_dna,dna_validity,rev_compliment,transcription
from app.schemas.dna_schemas import DNAAnalysisOptions, DNAAnalysisResponse, DNASequence,DNAValidityResponse,DNAReverseCompliment,Strand

dna_invalid_exception=HTTPException(status_code=400,detail="Bad request, DNA sequence invalid")


dna_router = APIRouter(prefix="/dna", tags=["DNA"])


@dna_router.post(
    "/check-validity",
    response_model=DNAValidityResponse,
    summary="DNA Sequence Validity Check",
)
def check_validity(dna: DNASequence):
    reasons_dict=dna_validity(dna)
    response=DNAValidityResponse.model_validate(reasons_dict)
    return response


@dna_router.post("/analyze", summary="DNA Sequence Analysis")
def analysis(dna: DNASequence, options: DNAAnalysisOptions = Query(),validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    res_dict=analyze_dna(dna.seq,options)
    response=DNAAnalysisResponse.model_validate(res_dict)
    return response

@dna_router.post("/reverse-compliment",summary="Reverse Compliment")
def reverse_compliment(dna:DNASequence,validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    res_dict=rev_compliment(dna.seq)
    response=DNAReverseCompliment.model_validate(res_dict)
    return response
    
@dna_router.post("/transcribe")
def transcribe(dna:DNASequence,strand_type:Strand=Query()):
    res_dict=transcription(dna.seq,strand_type)
    return res_dict