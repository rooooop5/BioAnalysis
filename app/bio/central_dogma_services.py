import regex
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
from app.schemas.ds_dna_schemas import DoubleStrandedDNA, Sigma70Promoter, RhoIndependentTerminator,TerminatorHit


def find_promoter(dna: DoubleStrandedDNA):
    promoter_pattern = Sigma70Promoter.minus_35 + Sigma70Promoter.gap + Sigma70Promoter.minus_10
    if regex.search(pattern=promoter_pattern, string=dna.forward_strand):
        print('Promoter is on forward strand')
        return {'found': True, 'coding_strand': dna.forward_strand}
    if regex.search(pattern=promoter_pattern, string=dna.reverse_strand):
        return {'found': True, 'coding_strand': dna.reverse_strand}
    return {'found': False, 'coding_strand': None}


# class TerminatorHit():
#     def __init__(terminator_strength)
def terminator_strength(stem_tuple,loop_len,poly_t_match):
    left_stem,right_stem=stem_tuple
    right_stem_rc=str(Seq(right_stem).reverse_complement())
    stem_len_score=(len(left_stem+right_stem)/20)*0.59
    gc_fraction_score=gc_fraction((left_stem+right_stem))*0.26
    loop_len_score=(len(RhoIndependentTerminator.loop_length)-RhoIndependentTerminator.loop_length.index(loop_len))/6*0.06
    poly_t_len_score=len(poly_t_match.group())/8*0.09
    stem_mismatches=sum(1 for left_base,right_base in zip(left_stem,right_stem_rc) if left_base!=right_base)
    stem_mismatch_penalty=(stem_mismatches/len(left_stem))
    terminator_strength=stem_len_score+gc_fraction_score+loop_len_score+poly_t_len_score-stem_mismatch_penalty
    return terminator_strength
    
    

def find_stem(dna, poly_t_match):
    stem_pairs_and_loop_lens=[]
    for stem_len in RhoIndependentTerminator.stem_length:
        allowed_mismatch=(stem_len-min(RhoIndependentTerminator.stem_length))//2
        right_stem = dna[(poly_t_match.start() - stem_len) : poly_t_match.start()]
        ideal_left_stem=str(Seq(right_stem).reverse_complement())
        ideal_left_stem_pattern="("+ideal_left_stem+")"+f"{{s<={allowed_mismatch}}}"
        for loop_len in RhoIndependentTerminator.loop_length:
            loop_start_idx = poly_t_match.start() - stem_len - loop_len
            left_stem = dna[loop_start_idx - stem_len : loop_start_idx]
            if (regex.match(pattern=ideal_left_stem_pattern,string=left_stem)):
                if (gc_fraction(Seq(left_stem+right_stem)))>=RhoIndependentTerminator.min_stem_gc_fraction:
                    stem_pairs_and_loop_lens.append(((left_stem,right_stem),(loop_len)))            
    return stem_pairs_and_loop_lens       


def find_poly_tail(dna):
    valid_poly_tails = []
    min_required_upstream = 2 * min(RhoIndependentTerminator.stem_length) + min(RhoIndependentTerminator.loop_length)
    for poly_t_pattern in RhoIndependentTerminator.poly_tail_pattern:
        for scan_pos in range(len(dna)):
            poly_t_match = regex.search(pattern=poly_t_pattern, string=dna, pos=scan_pos)
            if poly_t_match:
                if "G" not in (poly_t_match.group()) and "C" not in (poly_t_match.group()):
                    if poly_t_match.start() - min_required_upstream >= 0:
                        valid_poly_tails.append(poly_t_match)
            scan_pos = scan_pos + 1
    return valid_poly_tails



def find_terminator(dna:DoubleStrandedDNA):
    dna=dna.forward_strand
    all_terminators=[]
    valid_poly_tails=find_poly_tail(dna)
    for poly_t in valid_poly_tails:
        stem_and_loop=find_stem(dna,poly_t)
        if len(stem_and_loop)>0:
            for stem,loop_len in stem_and_loop:
                score=terminator_strength(stem,loop_len,poly_t)
                terminator_hit=TerminatorHit(score,poly_t,loop_len,stem,)
                all_terminators.append(terminator_hit)
    if not all_terminators:
        return {"found":False,"terminator":{}}
    best = max(all_terminators,key=lambda terminator: terminator.score)
    return {"found":True,"terminator":best.to_dict()}


def ds_transcription(transciptable_dna: str):
    return {'mRNA': str(Seq(transciptable_dna).transcribe())}
