from app.schemas.dna_schemas import DNAPipelineContext
from app.bio.dna_services import dna_validity
def validation_step(ctx:DNAPipelineContext):
    dna=ctx.dna
    return dna_validity(dna)

def complement_step(ctx:DNAPipelineContext):
    pass

def reverse_complement_step(ctx:DNAPipelineContext):
    pass

def transcription_step(ctx:DNAPipelineContext):
    pass

def translation_step(ctx:DNAPipelineContext):
    pass

def analyzation_step(ctx:DNAPipelineContext):
    pass

