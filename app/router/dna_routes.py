from typing import List

from fastapi import APIRouter, Query, Depends,HTTPException
from app.bio.dna_services import analyze_dna,dna_validity,rev_complement,transcription,complement,translation
from app.schemas.dna_schemas import DNAAnalysisOptions, DNAAnalysisResponse, DNASequence,DNAValidityResponse,DNAReverseComplementResponse,Strand,DNATranscriptionResponse,DNAComplementResponse,DNAPipelineSteps

dna_invalid_exception=HTTPException(status_code=400,detail="Bad request, DNA sequence invalid")

pipeline_steps={DNAPipelineSteps.validate:dna_validity,DNAPipelineSteps.reverse_complement:rev_complement,DNAPipelineSteps.complement:complement,DNAPipelineSteps.transcribe:transcription,DNAPipelineSteps.translate:translation,DNAPipelineSteps.analyze:analyze_dna}

dna_router = APIRouter(prefix="/dna")


@dna_router.post(
    "/check-validity",
    response_model=DNAValidityResponse,
    summary="DNA Sequence Validity Check",tags=["DNA - Validity"]
)
def check_validity(dna: DNASequence):
    reasons_dict=dna_validity(dna)
    response=DNAValidityResponse.model_validate(reasons_dict)
    return response


@dna_router.post("/analyze",response_model=DNAAnalysisResponse,summary="DNA Sequence Analysis",tags=["DNA - Analysis"])
def analysis(dna: DNASequence, options: DNAAnalysisOptions = Query(),validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    res_dict=analyze_dna(dna.seq,options)
    response=DNAAnalysisResponse.model_validate(res_dict)
    return response

@dna_router.post("/complement",response_model=DNAComplementResponse,tags=["DNA - Transformation"])
def dna_complement(dna:DNASequence,validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    return complement(dna.seq)



@dna_router.post("/reverse-complement",summary="Reverse Complement",tags=["DNA - Transformation"])
def reverse_complement(dna:DNASequence,validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    res_dict=rev_complement(dna.seq)
    response=DNAReverseComplementResponse.model_validate(res_dict)
    return response
    
@dna_router.post("/transcribe",tags=["DNA - Transcription and Translation"])
def transcribe(dna:DNASequence,strand_type:Strand=Query(),validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    res_dict=transcription(dna.seq,strand_type)
    response=DNATranscriptionResponse.model_validate(res_dict)
    return response
@dna_router.post("/translate",tags=["DNA - Transcription and Translation"])
def translate(dna:DNASequence,validity:DNAValidityResponse=Depends(dna_validity)):
    if not validity["is_valid"]:
        raise dna_invalid_exception
    return translation(dna.seq)

@dna_router.post("/pipeline")
def pipeline(dna:DNASequence,steps:List[DNAPipelineSteps]=Query(),strand_type:Strand=Query()):
    res={}
    if DNAPipelineSteps.validate not in steps:
        steps.insert(0,DNAPipelineSteps.validate)
    for step in steps:
        if step==DNAPipelineSteps.validate:
            validitiy_response=dna_validity(dna)
            res["validity"]=validitiy_response
            if not validitiy_response["is_valid"]:
                res["detail"]="Pipeline stopped due to invalid dna"
                return res
        if step==DNAPipelineSteps.reverse_complement:
            res["reverse_complement"]=(rev_complement(dna.seq))
        if step==DNAPipelineSteps.complement:
            res["complement"]=(complement(dna.seq))
        if step==DNAPipelineSteps.transcribe:
            res["transcribe"]=(transcription(dna.seq,strand_type))
        if step==DNAPipelineSteps.translate:
            res["translate"]=(translation(dna.seq))
        if step==DNAPipelineSteps.analyze:
            options=DNAAnalysisOptions.model_validate({"gc_fraction":True,"nucleotide_count":True})
            res["analyze"]=(analyze_dna(dna.seq,options))
    return res
        
           
