from typing import List, Literal

from pydantic import BaseModel

DNAInvalidReasons = Literal[
    "invalid character",
    "contains whitespace",
    "non string input",
    "empty sequence",
    "sequence too short",
    "length not multiple of three",
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
    gc_content: float | None
    nucleotide_count: dict | None
    reverse_compliment: str | None
    is_valid: bool


# -----function signature for Shubh: def analyze_dna(seq:DNASequence,options:DNAAnalysisOptions)->DNAAnalysisResponse


class DNAValidityResponse(BaseModel):
    is_valid: bool
    error: List[DNAInvalidReasons] | None = None
