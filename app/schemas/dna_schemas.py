from typing import List, Literal,Optional

from pydantic import BaseModel

DNAInvalidReasons = Literal[
    "invalid character(s) present",
    "contains whitespace",
    "non string input",
    "empty sequence",
    "sequence too short",
    "length not multiple of three"
]


# ----model of the dna seq request-----
class DNASequence(BaseModel):
    seq: str


# -----model for the query params-------
class DNAAnalysisOptions(BaseModel):
    gc_content: bool
    nucleotide_count: bool
    reverse_compliment: bool


class DNAAnalysisResponse(BaseModel):
    length:int
    gc_fraction: Optional[float]=None
    nucleotide_count: Optional[dict]=None
    reverse_compliment: Optional[str]=None
    is_valid: bool


# -----function signature for Shubh: def analyze_dna(seq:DNASequence,options:DNAAnalysisOptions)->dict


class DNAValidityResponse(BaseModel):
    is_valid: bool
    invalidity_reason: List[DNAInvalidReasons] | None = None
