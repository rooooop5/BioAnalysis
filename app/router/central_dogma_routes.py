from fastapi import APIRouter
from app.schemas.ds_dna_schemas import DoubleStrandedDNA,FindPromoterResponse
from app.schemas.dna_schemas import DNASequence
from app.bio.central_dogma_services import find_promoter,ds_transcription
cd_router=APIRouter(prefix="/central-dogma")

@cd_router.post('/find-promoter')
def find_promoter_endpoint(dna:DNASequence):
    ds_dna=DoubleStrandedDNA(seq=dna)
    result=find_promoter(ds_dna)
    response=FindPromoterResponse.model_validate(result)
    return response

@cd_router.post('/transcription')
def ds_transcription_endpoint(dna:DNASequence):
    ds_dna=DoubleStrandedDNA(seq=dna)
    result=find_promoter(ds_dna)
    if result["found"]:
        return ds_transcription(result["coding_strand"])
    else:
        return "Not"