import regex
from Bio.Seq import Seq
from app.schemas.ds_dna_schemas import DoubleStrandedDNA, Sigma70Promoter, RhoIndependentTerminator


def find_promoter(dna: DoubleStrandedDNA):
    promoter_pattern = Sigma70Promoter.minus_35 + Sigma70Promoter.gap + Sigma70Promoter.minus_10
    if regex.search(pattern=promoter_pattern, string=dna.forward_strand):
        print('Promoter is on forward strand')
        return {'found': True, 'coding_strand': dna.forward_strand}
    if regex.search(pattern=promoter_pattern, string=dna.reverse_strand):
        return {'found': True, 'coding_strand': dna.reverse_strand}
    return {'found': False, 'coding_strand': None}


def find_stem(dna, match_obj):
    for stem_len in RhoIndependentTerminator.stem_length:
        allowed_mismatch=stem_len-min(RhoIndependentTerminator.stem_length)//2
        right_stem = dna[(match_obj.start() - stem_len) : match_obj.start()]
        ideal_left_stem=str(Seq(right_stem).reverse_complement())
        ideal_left_stem_pattern=ideal_left_stem+f"{{s<={allowed_mismatch}}}"
        print(stem_len,ideal_left_stem_pattern) 
        for loop_len in RhoIndependentTerminator.loop_length:
            loop_start_idx = match_obj.start() - stem_len - loop_len
            left_stem = dna[loop_start_idx - stem_len : loop_start_idx]


def find_poly_tail(dna):
    valid_poly_tails = []
    min_required_upstream = 2 * min(RhoIndependentTerminator.stem_length) + min(RhoIndependentTerminator.loop_length)
    for poly_t_pattern in RhoIndependentTerminator.poly_tail_pattern:
        for scan_pos in range(len(dna)):
            poly_t_match = regex.search(pattern=poly_t_pattern, string=dna, pos=scan_pos)
            if poly_t_match:
                if poly_t_match.start() - min_required_upstream > 0:
                    valid_poly_tails.append(poly_t_match)
            scan_pos = scan_pos + 1


def find_transcription_terminator(dna):
    pass


def ds_transcription(transciptable_dna: str):
    return {'mRNA': str(Seq(transciptable_dna).transcribe())}
