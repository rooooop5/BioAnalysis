from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
from app.schemas.dna_schemas import StrandTranscriptionRole
import re


def dna_validity(dna: str) -> dict:
    is_valid = True
    invalidity_reason = []
    if not set(dna) <= {'A', 'G', 'C', 'T'}:
        invalidity_reason.append('INVALID_CHARACTER_PRESENT')
        is_valid = False
    if re.search(r'\s', dna):
        invalidity_reason.append('CONTAINS_WHITESPACE')
        is_valid = False
    if re.search(r'\d', dna):
        invalidity_reason.append('NON_STRING_INPUT')
        is_valid = False
    if len(dna) == 0:
        invalidity_reason.append('EMPTY_SEQUENCE')
        is_valid = False
    if is_valid:
        return {'detail': 'DNA sequence is valid', 'is_valid': is_valid, 'invalidity_reason': invalidity_reason}
    else:
        return {'detail': 'DNA sequence is invalid', 'is_valid': is_valid, 'invalidity_reason': invalidity_reason}


def analyze_dna(dna: Seq) -> dict:
    res = {}
    res['length'] = len(dna)
    res['gc_fraction'] = gc_fraction(dna)
    base_counts = {}
    base_counts['A'] = dna.count('A')
    base_counts['T'] = dna.count('T')
    base_counts['G'] = dna.count('G')
    base_counts['C'] = dna.count('C')
    res['nucleotide_count'] = base_counts
    res['is_valid'] = True
    return res


def complement(dna: Seq) -> dict:
    return {'original': str(dna), 'complement': str(dna.complement())}


def rev_complement(dna: Seq) -> dict:
    return {'original': str(dna), 'reverse_complement': str(dna.reverse_complement())}


def transcription(dna: Seq, strand_type: StrandTranscriptionRole) -> dict:
    res = {}
    res['dna_strand'] = str(dna)
    res['dna_strand_type'] = strand_type
    if strand_type == StrandTranscriptionRole.CODING:
        transcribed_rna = dna.transcribe()
    else:
        transcribed_rna = dna.reverse_complement().transcribe()
    res['transcribed_rna'] = str(transcribed_rna)
    return res


def translation(dna: Seq) -> dict:
    res = {}
    res['dna_strand'] = str(dna)
    translated_protein = dna.translate()
    res['translated_protein'] = str(translated_protein)
    return res
