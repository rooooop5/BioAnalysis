import regex
from Bio.Seq import Seq
from app.schemas.ds_dna_schemas import DoubleStrandedDNA, Sigma70Promoter,RhoIndependentTerminator

def find_promoter(dna: DoubleStrandedDNA):
    promoter_pattern = Sigma70Promoter.minus_35 + Sigma70Promoter.gap + Sigma70Promoter.minus_10
    if regex.search(pattern=promoter_pattern, string=dna.forward_strand):
        print('Promoter is on forward strand')
        return {'found':True,"coding_strand":dna.forward_strand}
    if regex.search(pattern=promoter_pattern, string=dna.reverse_strand):
        return {'found':True,"coding_strand":dna.reverse_strand}
    return {'found':False,'coding_strand':None}

def find_stem(dna,match_obj):
    for each_stem_length in RhoIndependentTerminator.stem_length:
        right_stem=dna[(match_obj.start()-each_stem_length):match_obj.start()]
        for each_loop_len in RhoIndependentTerminator.loop_length:
            loop_start=match_obj.start()-each_stem_length-each_loop_len
            left_stem=dna[loop_start-each_stem_length:loop_start]
            
def find_poly_tail(dna):
    valid_polytails=[]
    for pattern in RhoIndependentTerminator.poly_tail_pattern:
        for start in range(len(dna)):
            match_obj=(regex.search(pattern=pattern,string=dna,pos=start))
            if match_obj:
                if match_obj.start()-(2*min(RhoIndependentTerminator.stem_length)+min(RhoIndependentTerminator.loop_length))>0:
                    valid_polytails.append(match_obj)
            start=start+1
    

      
def find_transcription_terminator(dna):
    pass

def ds_transcription(transciptable_dna:str):
    return {"mRNA":str(Seq(transciptable_dna).transcribe())}
