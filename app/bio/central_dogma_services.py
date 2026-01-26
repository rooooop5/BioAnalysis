import regex
from Bio.Seq import Seq
from app.schemas.ds_dna_schemas import DoubleStrandedDNA, Sigma70Promoter,FindPromoterResponse

def find_promoter(dna: DoubleStrandedDNA):
    promoter_pattern = Sigma70Promoter.minus_35 + Sigma70Promoter.gap + Sigma70Promoter.minus_10
    if regex.search(pattern=promoter_pattern, string=dna.forward_strand):
        print('Promoter is on forward strand')
        return {'found':True,"coding_strand":dna.forward_strand}
    if regex.search(pattern=promoter_pattern, string=dna.reverse_strand):
        return {'found':True,"coding_strand":dna.reverse_strand}
    return {'found':False,'coding_strand':None}

def ds_transcription(transciptable_dna:str):
    return {"mRNA":str(Seq(transciptable_dna).transcribe())}
