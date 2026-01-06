from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
from app.schemas.dna_schemas import DNASequence,DNAAnalysisOptions,Strand
import re

# DNAInvalidReasons = Literal[
#     "invalid character",
#     "contains whitespace",
#     "non string input",
#     "empty sequence",
#     "sequence too short",
#     "length not multiple of three"
# ]
def dna_validity(dna:DNASequence)->dict:
    seq=dna.seq
    is_valid=True
    invalidity_reason=[]
    if re.findall(r"[^ATGC]",seq):
        invalidity_reason.append("invalid character(s) present")
        is_valid=False
    if re.search(r"\s",seq):
        invalidity_reason.append("contains whitespace")
        is_valid=False
    if re.search(r"\d",seq):
        invalidity_reason.append("non string input")
        is_valid=False
    if len(seq)==0:
        invalidity_reason.append("empty sequence")
        is_valid=False
    return {"detail":"DNA sequence is invalid","is_valid":is_valid,"invalidity_reason":invalidity_reason}

    
def analyze_dna(seq:str,options:DNAAnalysisOptions)->dict:
    dna=Seq(seq)
    res={}
    res["length"]=len(dna)
    if options.gc_fraction:
        res["gc_fraction"]=gc_fraction(dna)
    if options.nucleotide_count:
        base_counts={}
        base_counts["A"]=dna.count("A")
        base_counts["T"]=dna.count("T")
        base_counts["G"]=dna.count("G")
        base_counts["C"]=dna.count("C")
        res["nucleotide_count"]=base_counts
    if options.reverse_compliment:
        res["reverse_compliment"]=str(dna.reverse_complement())
    res["is_valid"]=dna_validity(dna)
    return res

def rev_compliment(seq:str)->dict:
    dna=Seq(seq)
    res={}
    res["original"]=seq
    res["reverse_compliment"]=str(dna.reverse_complement())
    return res

def transcription(seq:str,strand_type:Strand)->dict:
    dna=Seq(seq)
    res={}
    res["dna_strand"]=seq
    res["dna_strand_type"]=strand_type
    if strand_type==Strand.CODING:
        transcribed_rna=dna.transcribe()
    else:
        transcribed_rna=dna.reverse_complement().transcribe()
    res["transcribed_rna"]=str(transcribed_rna)
    return res
