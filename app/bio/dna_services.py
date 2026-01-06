from Bio.SeqUtils import gc_fraction
from Bio.Data import CodonTable
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
    if set(seq)<={"A","G","C","T"}:
        invalidity_reason.append("INVALID_CHARACTER_PRESENT")
        is_valid=False
    if re.search(r"\s",seq):
        invalidity_reason.append("CONTAINS_WHITESPACE")
        is_valid=False
    if re.search(r"\d",seq):
        invalidity_reason.append("NON_STRING_INPUT")
        is_valid=False
    if len(seq)==0:
        invalidity_reason.append("EMPTY_SEQUENCE")
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

def complement(seq:str):
    dna=Seq(seq)
    return {"original":seq,"complement":str(dna.complement())}

def rev_complement(seq:str)->dict:
    dna=Seq(seq)
    return {"original":seq,"reverse_complement":str(dna.reverse_complement())}

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
def translation(seq:str):
    dna=Seq(seq)
    res={}
    res["dna_strand"]=seq
    translated_protein=dna.translate()
    res["translated_protein"]=str(translated_protein)
    return res