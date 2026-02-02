from typing import List
from fastapi import APIRouter, Query, Depends, Body
from app.schemas.dna_schemas import (
    DNAAnalysisResponse,
    DNASequence,
    DNAValidityResponse,
    DNAPipelineContext,
    DNAReverseComplementResponse,
    StrandTranscriptionRole,
    DNATranscriptionResponse,
    DNAComplementResponse,
    DNAPipelineSteps,
    DNATranslationResponse,
    InvocationSource,
    dna_invalid_exception,
)
from app.pipelines.dna_engine import dna_engine
from app.schemas.ds_dna_schemas import DoubleStrandedDNA, FindPromoterResponse
from app.bio.central_dogma_services import find_promoter

dna_router = APIRouter(prefix='/dna')


def check_validity(dna: DNASequence):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.validate])
    if not ctx.result['is_valid']:
        raise dna_invalid_exception


@dna_router.post(
    '/check-validity',
    response_model=DNAValidityResponse,
    summary='DNA Sequence Validity Check',
    tags=['DNA - Validity'],
)
def validation_endpoint(dna: DNASequence):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.validate])
    response = DNAValidityResponse.model_validate(ctx.result)
    return response


@dna_router.post(
    '/analyze', response_model=DNAAnalysisResponse, summary='DNA Sequence Analysis', tags=['DNA - Analysis']
)
def analysis_endpoint(dna: DNASequence = Body(), _: DNAValidityResponse = Depends(check_validity)):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.analyze])
    response = DNAAnalysisResponse.model_validate(ctx.result)
    return response


@dna_router.post('/complement', response_model=DNAComplementResponse, tags=['DNA - Transformation'])
def complement_endpoint(dna: DNASequence, validity: DNAValidityResponse = Depends(check_validity)):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.complement])
    response = DNAComplementResponse.model_validate(ctx.result)
    return response


@dna_router.post('/reverse-complement', summary='Reverse Complement', tags=['DNA - Transformation'])
def reverse_complement_endpoint(dna: DNASequence, validity: DNAValidityResponse = Depends(check_validity)):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.reverse_complement])
    response = DNAReverseComplementResponse.model_validate(ctx.result)
    return response


@dna_router.post('/transcribe', tags=['DNA - Transcription and Translation'])
def transcription_endpoint(
    dna: DNASequence,
    strand_type: StrandTranscriptionRole = Query(),
    validity: DNAValidityResponse = Depends(check_validity),
):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint, strand_type=strand_type)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.transcribe])
    response = DNATranscriptionResponse.model_validate(ctx.result)
    return response


@dna_router.post('/translate', tags=['DNA - Transcription and Translation'])
def translation_endpoint(dna: DNASequence, validity: DNAValidityResponse = Depends(check_validity)):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.endpoint)
    dna_engine(ctx=ctx, steps_list=[DNAPipelineSteps.translate])
    response = DNATranslationResponse.model_validate(ctx.result)
    return response


@dna_router.post('/pipeline')
def pipeline(
    dna: DNASequence,
    steps: List[DNAPipelineSteps] = Query(),
    strand_type: StrandTranscriptionRole = Query(default=None),
):
    ctx = DNAPipelineContext(dna=dna, invocation_source=InvocationSource.pipeline, strand_type=strand_type)
    dna_engine(ctx=ctx, steps_list=steps)
    return ctx.result
