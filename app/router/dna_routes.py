from typing import List
from fastapi import APIRouter, Query, Depends, HTTPException, Body
from app.bio.dna_services import analyze_dna, dna_validity, rev_complement, transcription, complement, translation
from app.schemas.dna_schemas import (
    DNAAnalysisOptions,
    DNAAnalysisResponse,
    DNASequence,
    DNAValidityResponse,
    DNAPipelineContext,
    DNAReverseComplementResponse,
    Strand,
    DNATranscriptionResponse,
    DNAComplementResponse,
    DNAPipelineSteps,
    DNATranslationResponse,
    InvocationSource,
)
from app.pipelines.dna_engine import dna_engine

dna_invalid_exception = HTTPException(status_code=400, detail="Bad request, DNA sequence invalid")


dna_router = APIRouter(prefix="/dna")


@dna_router.post(
    "/check-validity",
    response_model=DNAValidityResponse,
    summary="DNA Sequence Validity Check",
    tags=["DNA - Validity"],
)
def check_validity(dna: DNASequence):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.validate])
    response = DNAValidityResponse.model_validate(ctx.result)
    return response


@dna_router.post(
    "/analyze", response_model=DNAAnalysisResponse, summary="DNA Sequence Analysis", tags=["DNA - Analysis"]
)
def analysis(dna: DNASequence = Body(), validity: DNAValidityResponse = Depends(check_validity)):
    if not validity.is_valid:
        raise dna_invalid_exception
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.analyze])
    response = DNAAnalysisResponse.model_validate(ctx.result)
    return response


@dna_router.post("/complement", response_model=DNAComplementResponse, tags=["DNA - Transformation"])
def dna_complement(dna: DNASequence, validity: DNAValidityResponse = Depends(check_validity)):
    if not validity.is_valid:
        raise dna_invalid_exception
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.complement])
    response = DNAComplementResponse.model_validate(ctx.result)
    return response


@dna_router.post("/reverse-complement", summary="Reverse Complement", tags=["DNA - Transformation"])
def reverse_complement(dna: DNASequence, validity: DNAValidityResponse = Depends(check_validity)):
    if not validity.is_valid:
        raise dna_invalid_exception
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.reverse_complement])
    response = DNAReverseComplementResponse.model_validate(ctx.result)
    return response


@dna_router.post("/transcribe", tags=["DNA - Transcription and Translation"])
def transcribe(
    dna: DNASequence, strand_type: Strand = Query(), validity: DNAValidityResponse = Depends(check_validity)
):
    if not validity.is_valid:
        raise dna_invalid_exception
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint, strand_type=strand_type)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.transcribe])
    response = DNATranscriptionResponse.model_validate(ctx.result)
    return response


@dna_router.post("/translate", tags=["DNA - Transcription and Translation"])
def translate(dna: DNASequence, validity: DNAValidityResponse = Depends(check_validity)):
    if not validity.is_valid:
        raise dna_invalid_exception
    ctx = DNAPipelineContext(
        dna=dna,
        invocation_source=InvocationSource.endpoint,
    )
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.translate])
    response = DNATranslationResponse.model_validate(ctx.result)
    return response


@dna_router.post("/pipeline")
def pipeline(dna: DNASequence, steps: List[DNAPipelineSteps] = Query(), strand_type: Strand = Query(default=None)):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.pipeline, strand_type=strand_type)
    dna_engine(ctx=ctx, steps_list=steps)
    return ctx.result
