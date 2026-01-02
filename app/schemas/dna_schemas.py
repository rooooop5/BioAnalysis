from pydantic import BaseModel,Field

#----model of the dna seq request-----
class DNASequence(BaseModel):
    seq:str


#-----model for the query params-------
class DNAAnalysisOptions(BaseModel):
    gc_content:bool
    nucleotide_count:bool
    reverse_compliment:bool
    check_validity:bool

#-----function signature for Shubh: def analyze_dna(seq:DNASequence,options:DNAAnalysisOptions)
#----- reponse model not designed yet------
