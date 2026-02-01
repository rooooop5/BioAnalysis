from pydantic import BaseModel
from enum import Enum
from app.schemas.dna_schemas import DNASequence, StrandTranscriptionRole
from Bio.Seq import Seq
from dataclasses import dataclass


@dataclass
class Sigma70Promoter:
    minus_35: str = r'(TTGACA){s<=1,i<=0,d<=0}'
    minus_10: str = r'(TATAAT){s<=1,i<=0,d<=0}'
    gap: str = r'.{16,18}'


@dataclass
class StrandPolarity(str, Enum):
    forward = '5_3'
    reverse = '3_5'


@dataclass
class RhoIndependentTerminator:
    min_stem_gc_fraction = 0.65
    stem_length = (6, 7, 8, 9, 10)
    poly_tail_pattern = [r'(TTTTTTTT){s<=2}', r'(TTTTTTT){s<=2}', r'(TTTTTT){s<=1}']
    loop_length = (3, 4, 5, 6, 7, 8)

@dataclass
class TranscriptionTerminatorScoringConfig():
    MAX_STEM_LENGTH=2*max(RhoIndependentTerminator.stem_length)
    MAX_LOOP_LENGTH_SCORE=len(RhoIndependentTerminator.loop_length)
    MAX_POLY_T_LENGTH=8 # max allowed length of poly-T tail
    STEM_LENGTH_SCORE_WEIGHT=0.59
    GC_FRACTION_SCORE_WEIGHT=0.26
    POLY_T_LENGTH_SCORE_WEIGHT=0.09
    LOOP_LENGTH_SCORE_WIEGHT=0.05
    
class TerminatorHit:
    def __init__(self, score, poly_t_match, loop_length, stem):
        self.score = score
        self.start = poly_t_match.start() - loop_length - 2 * len(stem[0])
        self.end = poly_t_match.end()
        self.poly_t = poly_t_match.group()
        self.stem = {'left_stem': stem[0], 'right_stem': stem[1]}
        self.loop_length = loop_length

    def to_dict(self):
        return {
            'score': self.score,
            'start': self.start,
            'end': self.end,
            'poly_t': self.poly_t,
            'stem': self.stem,
            'loop_length': self.loop_length,
        }


class TerminatorHitResponse(BaseModel):
    found: bool
    terminator: dict


class FindPromoterResponse(BaseModel):
    found: bool
    coding_strand: str | None


class DoubleStrandedDNA:
    def __init__(self, seq: DNASequence):
        self.forwardSeq: str = seq.seq
        self.polarity: StrandPolarity = StrandPolarity.forward.value

    @property
    def forward_strand(self):
        return self.forwardSeq

    @property
    def reverse_strand(self):
        return str(Seq(self.forwardSeq).reverse_complement())
