from pydantic import BaseModel,Field

#----model of the dna seq request-----
class DNASequence(BaseModel):
    seq:str


#-----model for the query params-------
class DNAAnalysisOptions(BaseModel):
    gc_content:bool
    nucleotide_count:bool
    reverse_compliment:bool
    


class DNAAnalysisResponse(BaseModel):
    gc_content:float|None
    nucleotide_count:dict|None
    reverse_compliment:str|None
    validity:bool|None

#-----function signature for Shubh: def analyze_dna(seq:DNASequence,options:DNAAnalysisOptions)->DNAAnalysisResponse
#----- reponse model not designed yet------