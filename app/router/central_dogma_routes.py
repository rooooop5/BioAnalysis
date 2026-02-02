from fastapi import APIRouter
from app.schemas.ds_dna_schemas import DoubleStrandedDNA,FindPromoterResponse,TerminatorHitResponse
from app.schemas.dna_schemas import DNASequence
from app.bio.central_dogma_services import find_promoter,ds_transcription,find_terminator,extract_transcriptable_dna
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
    
@cd_router.post("/find-transcription-terminator")
def find_transcription_terminator_endpoint(dna:DNASequence):
    ds_dna=DoubleStrandedDNA(seq=dna)
    terminator=find_terminator(ds_dna)
    #return TerminatorHitResponse.model_validate(terminator)
    return extract_transcriptable_dna(ds_dna)