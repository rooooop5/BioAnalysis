from enum import Enum
from typing import List, Literal, Optional
from fastapi import HTTPException
from Bio.Seq import Seq
from pydantic import BaseModel

DNAInvalidReasons = Literal[
    "INVALID_CHARACTER_PRESENT",
    "CONTAINS_WHITESPACE",
    "NON_STRING_INPUT",
    "EMPTY_SEQUENCE",
    "SEQUENCE_TOO_SHORT",
    "LENGHT_NOT_MULTIPLE_OF_THREE",
]


class StrandTranscriptionRole(str, Enum):
    CODING = "CODING"
    TEMPLATE = "TEMPLATE"


class DNAPipelineSteps(str, Enum):
    validate = "VALIDATE"
    reverse_complement = "REVERSE COMPLEMENT"
    complement = "COMPLEMENT"
    transcribe = "TRANSCRIBE"
    translate = "TRANSLATE"
    analyze = "ANALYZE"


class InvocationSource(str, Enum):
    pipeline = "PIPELINE"
    endpoint = "ENDPOINT"


# ----model of the dna seq request-----
class DNASequence(BaseModel):
    seq: str


# -----model for the query params-------
class DNAAnalysisOptions(str, Enum):
    gc_fraction = "GC FRACTION"
    nucleotide_count = "NUCLEOTIDE COUNT"


class DNAAnalysisResponse(BaseModel):
    length: int
    gc_fraction: Optional[float] = None
    nucleotide_count: Optional[dict] = None
    is_valid: bool


# -----function signature for Shubh: def analyze_dna(seq:DNASequence,options:DNAAnalysisOptions)->dict


class DNAComplementResponse(BaseModel):
    original: str
    complement: str

dna_invalid_exception = HTTPException(status_code=400, detail="Bad request, DNA sequence invalid")
class DNAReverseComplementResponse(BaseModel):
    original: str
    reverse_complement: str


class DNATranscriptionResponse(BaseModel):
    dna_strand: str
    dna_strand_type: str
    transcribed_rna: str


class DNATranslationResponse(BaseModel):
    dna_strand: str
    translated_protein: str


class DNAValidityResponse(BaseModel):
    detail: str
    is_valid: bool
    invalidity_reason: Optional[List[DNAInvalidReasons]] = None


class DNAPipelineContext:
    def __init__(
        self,
        dna: DNASequence,
        invocation_source: InvocationSource,
        strand_type: Optional[Strand] = None,
    ):
        self.dna: Seq = Seq(dna.seq)
        self.strand_type: Optional[Strand] = strand_type
        self.invocation_source: InvocationSource = invocation_source
        self.stop_pipeline: bool = False
        self.result: dict = None
        self.error: dict = None
