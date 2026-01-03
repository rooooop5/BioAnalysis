from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
from app.schemas.dna_schemas import DNASequence,DNAAnalysisOptions,DNAAnalysisResponse,DNAInvalidReasons
import re

# DNAInvalidReasons = Literal[
#     "invalid character",
#     "contains whitespace",
#     "non string input",
#     "empty sequence",
#     "sequence too short",
#     "length not multiple of three"
# ]
def dna_validity(dna:DNASequence):
    req=dna.seq
    is_valid=True
    invalidity_reason=[]
    if re.findall(r"[^ATGC]",req):
        invalidity_reason.append("invalid character(s) present")
        is_valid=False
    if re.search(r"\s",req):
        invalidity_reason.append("contains whitespace")
        is_valid=False
    if re.search(r"\d",req):
        invalidity_reason.append("non string input")
        is_valid=False
    if len(req)==0:
        invalidity_reason.append("empty sequence")
        is_valid=False
    return {"is_valid":is_valid,"invalidity_reason":invalidity_reason}

    
def analyze_dna(req:str,options:DNAAnalysisOptions):
    dna=Seq(req)
    res={}
    res["length"]=len(dna)
    if options.gc_content:
        res["gc_content"]=gc_fraction(dna)
    if options.nucleotide_count:
        base_counts={}
        base_counts["A"]=dna.count("A")
        base_counts["T"]=dna.count("T")
        base_counts["G"]=dna.count("G")
        base_counts["C"]=dna.count("C")
        res["nucleotide_count"]=base_counts
    if options.reverse_compliment:
        res["reverse_compliment"]=str(dna.reverse_complement())
    res["is_valid"]=True
    return res
