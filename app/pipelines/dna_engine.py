from typing import List
from app.bio.dna_services import analyze_dna,dna_validity,rev_complement,transcription,complement,translation
from app.schemas.dna_schemas import DNAPipelineContext,DNASequence,DNAPipelineSteps,Strand
def validation_step(ctx:DNAPipelineContext):
    dna=str(ctx.dna)
    return dna_validity(dna)
def complement_step(ctx:DNAPipelineContext):
    return complement(ctx.dna)

def reverse_complement_step(ctx:DNAPipelineContext):
    return rev_complement(ctx.dna)

def transcription_step(ctx:DNAPipelineContext):
    return transcription(ctx.dna,ctx.strand_type)

def translation_step(ctx:DNAPipelineContext):
    return translation(ctx.dna)

def analyzation_step(ctx:DNAPipelineContext):
    return analyze_dna(ctx.dna,ctx.analysis_options)
    

mapping={DNAPipelineSteps.validate:validation_step,DNAPipelineSteps.reverse_complement:reverse_complement_step,DNAPipelineSteps.complement:complement_step,DNAPipelineSteps.transcribe:transcription_step,DNAPipelineSteps.translate:translation_step,DNAPipelineSteps.analyze:analyzation_step}
def dna_engine(ctx:DNAPipelineContext,steps_list):
    for step in steps_list:
        biofunction=mapping[step]
        ctx.result=biofunction(ctx)
        print(ctx.result)
      



