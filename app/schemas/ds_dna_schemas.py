from pydantic import BaseModel
from enum import Enum
from app.schemas.dna_schemas import DNASequence,StrandTranscriptionRole
from Bio.Seq import Seq


class Sigma70Promoter:
    minus_35: str = r'(TTGACA){s<=1,i<=0,d<=0}'
    minus_10: str = r'(TATAAT){s<=1,i<=0,d<=0}'
    gap: str = r'.{16,18}'

class StrandPolarity(str, Enum):
    forward = '5_3'
    reverse = '3_5'

class FindPromoterResponse(BaseModel):
    found:bool
    coding_strand:str|None
    
class DoubleStrandedDNA:
    def __init__(self, seq: DNASequence):
        self.forwardSeq: str = seq.seq
        self.polarity: StrandPolarity = StrandPolarity.forward.value

    @property
    def forward_strand(self):
        return self.forwardSeq

    @property
    def reverse_strand(self):
        return (str(Seq(self.forwardSeq).reverse_complement()))