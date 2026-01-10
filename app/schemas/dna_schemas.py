from typing import List, Literal,Optional
from enum import Enum

from pydantic import BaseModel

DNAInvalidReasons = Literal[
    "INVALID_CHARACTER_PRESENT",
    "CONTAINS_WHITESPACE",
    "NON_STRING_INPUT",
    "EMPTY_SEQUENCE",
    "SEQUENCE_TOO_SHORT",
    "LENGHT_NOT_MULTIPLE_OF_THREE"
]

class Strand(str,Enum):
    CODING='CODING'
    TEMPLATE='TEMPLATE'

class DNAPipelineSteps(str,Enum):
    validate="VALIDATE"
    reverse_complement="REVERSE COMPLEMENT"
    complement="COMPLEMENT"
    transcribe="TRANSCRIBE"
    translate="TRANSLATE"
    analyze="ANALYZE"

# ----model of the dna seq request-----
class DNASequence(BaseModel):
    seq: str


# -----model for the query params-------
class DNAAnalysisOptions(BaseModel):
    gc_fraction: bool
    nucleotide_count: bool


class DNAAnalysisResponse(BaseModel):
    length:int
    gc_fraction: Optional[float]=None
    nucleotide_count: Optional[dict]=None
    is_valid: bool


# -----function signature for Shubh: def analyze_dna(seq:DNASequence,options:DNAAnalysisOptions)->dict

class DNAComplementResponse(BaseModel):
    original:str
    complement:str
class DNAReverseComplementResponse(BaseModel):
    original:str
    reverse_complement:str

class DNATranscriptionResponse(BaseModel):
    dna_strand:str
    dna_strand_type:str
    transcribed_rna:str
class DNAValidityResponse(BaseModel):
    detail:str
    is_valid: bool
    invalidity_reason: Optional[List[DNAInvalidReasons]]=None
