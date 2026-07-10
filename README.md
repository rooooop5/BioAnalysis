# 🧬 BioAnalysis

A FastAPI-based REST API for DNA sequence analysis, manipulation, and transcription — built around rule-based models of the **Central Dogma of Molecular Biology** (DNA → RNA → Protein).

> ⚠️ **Educational / Prototyping Tool — Not for Production Genomics**
>
> BioAnalysis implements simplified, rule-based biological logic intended for learning and prototyping. The core operations (complement, transcription, translation) are biologically accurate for clean, well-formed sequences. However, the higher-level features — promoter detection, terminator prediction, and the full transcription pipeline — use heuristic consensus-sequence matching and scoring models that **do not generalise to real genomic data**.
>
> Specifically:
> - The validator rejects anything that isn't a clean uppercase `ATGC` string, so **real FASTA files** (with headers, lowercase masking, ambiguity codes like `N`, `R`, `Y`, multi-line sequences) **will fail validation entirely**.
> - Promoter detection uses a single hardcoded Sigma-70 consensus pattern. Real genomes have enormous promoter diversity; this will produce many false negatives and some false positives even on bacterial sequences.
> - Terminator scoring is a weighted heuristic. It will miss many real terminators and flag spurious ones, especially in GC-rich genomes or sequences with repetitive elements.
> - There is no handling of open reading frames, introns, splice sites, or any eukaryotic gene structure.

---

## Features

| Category | Operations | Biological accuracy |
|---|---|---|
| **Validation** | Rejects non-ATGC characters, whitespace, digits, empty strings | ✅ Correct for clean sequences — ❌ rejects all real FASTA input |
| **Analysis** | GC fraction, per-base counts, sequence length | ✅ Accurate for clean input |
| **Complement / Reverse complement** | Watson-Crick base pairing (A↔T, G↔C) | ✅ Accurate |
| **Transcription** | DNA → mRNA (T→U), coding or template strand | ✅ Accurate for clean input; no intron or splice-site awareness |
| **Translation** | Codons → amino acids via standard genetic code | ✅ Accurate; no ORF detection, stop-codon read-through, or alternative codes |
| **Promoter detection** | Fuzzy regex match of Sigma-70 −35/−10 consensus boxes | ⚠️ Rule-based heuristic |
| **Terminator detection** | Weighted scoring of hairpin stem + poly-T tail | ⚠️ Heuristic — not validated against experimental terminator databases |
| **Pipeline** | Chain any combination of the above steps in a single request | — |

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Sequence Operations | [BioPython](https://biopython.org/) |
| Data Validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Pattern Matching | `regex` (fuzzy matching for promoter/terminator motifs) |
| Linting | [Ruff](https://docs.astral.sh/ruff/) |

---

## Project Structure

```
BioAnalysis/
├── app/
│   ├── main.py                        # FastAPI app, CORS middleware, global error handler
│   ├── bio/
│   │   ├── basic_dna_services.py      # Core DNA operations (validate, analyze, complement, transcribe, translate)
│   │   └── central_dogma_services.py  # Promoter/terminator detection, dsDNA transcription
│   ├── pipelines/
│   │   └── dna_engine.py              # Pipeline executor — chains steps with shared DNAPipelineContext
│   ├── router/
│   │   ├── dna_routes.py              # /dna/* endpoints
│   │   └── central_dogma_routes.py    # /central-dogma/* endpoints
│   └── schemas/
│       ├── dna_schemas.py             # Pydantic models and enums for single-stranded DNA
│       └── ds_dna_schemas.py          # Models for dsDNA, Sigma70 promoter, rho-independent terminator
```

### Architecture layers

```
HTTP Layer       (app/router/)       — request/response only, no business logic
      ↓
Orchestration    (app/pipelines/)    — multi-step pipeline with shared context & early-stop
      ↓
Business Logic   (app/bio/)          — pure functions, no HTTP knowledge
      ↓
Data Models      (app/schemas/)      — Pydantic models, enums, dataclasses, type safety
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/rooooop5/BioAnalysis.git
cd BioAnalysis
pip install -r requirements.txt
```

### Running the server

```bash
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`.  
Interactive Swagger docs: `http://localhost:8000/docs`  
ReDoc: `http://localhost:8000/redoc`

---

## API Reference

All endpoints accept `Content-Type: application/json` and return JSON.  
Request body for all DNA endpoints: `{ "seq": "<DNA string>" }`

### DNA Operations — `/dna`

#### `POST /dna/check-validity`
Validate a DNA sequence.

```bash
curl -X POST http://localhost:8000/dna/check-validity \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGCGTACG"}'
```
```json
{
  "detail": "DNA sequence is valid",
  "is_valid": true,
  "invalidity_reason": []
}
```

Possible `invalidity_reason` codes:

| Code | Meaning |
|---|---|
| `INVALID_CHARACTER_PRESENT` | Only A, T, G, C are allowed |
| `CONTAINS_WHITESPACE` | No spaces, tabs, or newlines |
| `NON_STRING_INPUT` | Digits detected in input |
| `EMPTY_SEQUENCE` | Empty string provided |

---

#### `POST /dna/analyze`
Compute GC fraction, nucleotide counts, and sequence length. Validation is enforced automatically.

```bash
curl -X POST http://localhost:8000/dna/analyze \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGCGTACG"}'
```
```json
{
  "length": 9,
  "gc_fraction": 0.5556,
  "nucleotide_count": {"A": 2, "T": 2, "G": 3, "C": 2},
  "is_valid": true
}
```

---

#### `POST /dna/complement`
Returns the Watson-Crick complement (A↔T, G↔C).

```bash
curl -X POST http://localhost:8000/dna/complement \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGC"}'
```
```json
{
  "original": "ATGC",
  "complement": "TACG"
}
```

---

#### `POST /dna/reverse-complement`
Returns the reverse complement of the sequence.

```bash
curl -X POST http://localhost:8000/dna/reverse-complement \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGC"}'
```
```json
{
  "original": "ATGC",
  "reverse_complement": "GCAT"
}
```

---

#### `POST /dna/transcribe?strand_type=CODING|TEMPLATE`
Transcribes DNA to mRNA (T→U). Requires a `strand_type` query parameter.

- `CODING` — non-template / sense strand (directly substitutes T→U)
- `TEMPLATE` — takes the reverse complement first, then transcribes

```bash
curl -X POST "http://localhost:8000/dna/transcribe?strand_type=CODING" \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGCGTACG"}'
```
```json
{
  "dna_strand": "ATGCGTACG",
  "dna_strand_type": "CODING",
  "transcribed_rna": "AUGCGUACG"
}
```

---

#### `POST /dna/translate`
Translates a DNA coding sequence to a protein. Sequence length must be a multiple of 3.

```bash
curl -X POST http://localhost:8000/dna/translate \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGGCTATGCGT"}'
```
```json
{
  "dna_strand": "ATGGCTATGCGT",
  "translated_protein": "MAMR"
}
```

---

#### `POST /dna/pipeline?steps=...&strand_type=CODING|TEMPLATE`
Execute multiple operations in sequence on one DNA input. Pass `steps` as repeated query parameters.

Available steps: `VALIDATE`, `COMPLEMENT`, `REVERSE COMPLEMENT`, `TRANSCRIBE`, `TRANSLATE`, `ANALYZE`

Validation is always prepended if not explicitly included. The pipeline halts on validation failure.

```bash
curl -X POST "http://localhost:8000/dna/pipeline?steps=VALIDATE&steps=TRANSCRIBE&steps=TRANSLATE&strand_type=CODING" \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGGCTATGCGT"}'
```
```json
{
  "VALIDATE":   { "detail": "DNA sequence is valid", "is_valid": true, "invalidity_reason": [] },
  "TRANSCRIBE": { "dna_strand": "ATGGCTATGCGT", "dna_strand_type": "CODING", "transcribed_rna": "AUGGCUAUGCGU" },
  "TRANSLATE":  { "dna_strand": "ATGGCTATGCGT", "translated_protein": "MAMR" }
}
```

---

### Central Dogma — `/central-dogma`

These endpoints accept double-stranded DNA. The forward (5′→3′) strand is provided; the reverse strand is derived internally.

#### `POST /central-dogma/find-promoter`
Scans both strands for a Sigma-70 promoter using fuzzy matching of the −35 (`TTGACA`) and −10 (`TATAAT`) consensus boxes (1 substitution allowed each), separated by a 16–18 bp spacer.

```bash
curl -X POST http://localhost:8000/central-dogma/find-promoter \
  -H "Content-Type: application/json" \
  -d '{"seq": "TTGACATAAATACCTTAACGGAGTATACATGCGTACG"}'
```
```json
{
  "found": true,
  "coding_strand": "TTGACATAAATACCTTAACGGAGTATACATGCGTACG",
  "promoter_start": 0,
  "promoter_end": 24
}
```

---

#### `POST /central-dogma/transcription`
Transcribes the coding strand if a valid promoter is detected. Returns the mRNA sequence, or `"Not"` if no promoter is found.

```bash
curl -X POST http://localhost:8000/central-dogma/transcription \
  -H "Content-Type: application/json" \
  -d '{"seq": "TTGACATAAATACCTTAACGGAGTATACATGCGTACG"}'
```
```json
{ "mRNA": "AUGCGUACG" }
```

---

#### `POST /central-dogma/find-transcription-terminator`
Detects rho-independent (intrinsic) transcription terminators. Scores candidates by stem length, GC content, loop length, poly-T tail length, and stem mismatches. Returns the highest-scoring terminator and the extracted transcriptable region.

```bash
curl -X POST http://localhost:8000/central-dogma/find-transcription-terminator \
  -H "Content-Type: application/json" \
  -d '{"seq": "ATGCGTACGATCGATCGATCGATTTTTTTTTGCGTACGATCGATCG"}'
```
```json
{
  "found": true,
  "terminator": {
    "score": 0.74,
    "start": 18,
    "end": 36,
    "poly_t": "TTTTTTTT",
    "stem": { "left_stem": "ATCGAT", "right_stem": "ATCGAT" },
    "loop_length": 3
  }
}
```

---

## Error Handling

All endpoints return consistent error shapes via a global exception handler:

```json
{
  "error": {
    "status_code": 400,
    "message": "Bad request, DNA sequence invalid",
    "path": "/dna/analyze"
  }
}
```

Invalid DNA sequences return `400 Bad Request`. Validation is a dependency for all analysis and transformation endpoints, so they will reject invalid input before any processing occurs.

---

## Terminator Scoring

The rho-independent terminator scoring model weights four structural features:

| Feature | Weight |
|---|---|
| Stem length | 59% |
| Stem GC fraction | 26% |
| Poly-T tail length | 9% |
| Loop length (shorter is stronger) | 5% |
| Stem mismatch penalty | −40% of mismatch fraction |

Minimum requirements: stem GC ≥ 65%, stem lengths 6–10 bp, loop lengths 3–8 nt, poly-T tail with ≤ 1–2 substitutions.

---

## Known Limitations & Biological Accuracy

This section documents where the implementation diverges from real biology, so you know exactly what the tool can and cannot do.

### Input format

The validator accepts only clean, uppercase, unambiguous  strings with no whitespace. This means:

- **FASTA files will not work.** The `>header` line, lowercase soft-masking (`atgc`), IUPAC ambiguity codes (`N`, `R`, `Y`, `W`, `S`, `M`, `K`, `H`, `B`, `V`, `D`), and multi-line sequences all fail validation before any processing occurs.
- **Real sequencing output** (Illumina reads, assembled contigs, RefSeq records) nearly always contains at least some of the above.

To use real data you would need to pre-process it: strip FASTA headers, uppercase the sequence, replace or filter ambiguous bases, and join multi-line records.

### Promoter detection

The promoter finder matches a single Sigma-70 consensus pattern ( at −35 and  at −10, separated by 16–18 bp, each allowing 1 substitution). This is a rough model of *E. coli* housekeeping promoters. In practice:

- The −35/−10 spacing is variable in real operons and the consensus degeneracy is much higher than 1 substitution.
- Sigma factors other than σ70 (σ54, σ32, σ38, etc.) have completely different consensus sequences and are not detected.
- Eukaryotic promoters (TATA box, Inr, BRE, DPE, etc.) are entirely absent from this model.
- The tool scans the forward and reverse strand independently using the same pattern, which is a reasonable simplification but will miss promoters embedded in complex regulatory architectures.

For real bacterial promoter prediction, tools like [BPROM](http://www.softberry.com/), [MEME](https://meme-suite.org/), or [Prokka](https://github.com/tseemann/prokka) are appropriate.

### Terminator detection

Rho-independent terminators are detected by scanning for a poly-T tail (6–8 T's, ≤ 1–2 substitutions) and then searching upstream for an inverted repeat (hairpin stem of 6–10 bp, GC ≥ 65%, loop of 3–8 nt). A score is computed from four weighted features (stem length, GC content, loop length, poly-T length) minus a mismatch penalty.

Limitations:

- The scoring weights are manually assigned, not trained on experimental data. There is no calibrated score threshold — the tool returns the single best-scoring candidate regardless of whether it would function as a terminator in vivo.
- Rho-dependent terminators (which rely on the Rho helicase protein and specific *rut* sites) are not modelled at all.
- In GC-rich genomes, many non-terminator hairpins will score highly. In AT-rich genomes, weak terminators may be missed.
- No correction is made for sequence context, upstream secondary structure, or transcription speed.

For production terminator prediction, see [TransTermHP](http://transterm.ccb.jhu.edu/) or [ARNold](https://rna.igmors.u-psud.fr/toolbox/arnold/).

### Transcription and translation

The core mechanics (T→U substitution, reverse-complement of the template strand, codon table lookup) are biologically correct for clean prokaryotic coding sequences. However:

- There is no ORF detection. The tool transcribes or translates whatever sequence you give it, starting from position 0.
- There is no handling of the Shine-Dalgarno sequence or ribosome binding site.
- Stop codons are translated to  by BioPython — there is no endpoint-specific handling of premature stops or read-through.
- Eukaryotic mRNA processing (5′ capping, 3′ polyadenylation, splicing) is not modelled.
- Alternative genetic codes (mitochondrial, ciliate, etc.) are not supported; the standard table is always used.

### What the pipeline actually models

The  endpoint chains individual operations on a single input sequence using a shared context object (). Each step is an independent function; there is no state carried between steps beyond the sequence itself and an early-stop flag triggered by validation failure. The pipeline is a convenience wrapper, not a biological simulation.

---

## Development

```bash
# Lint
ruff check .

# Format
ruff format .
```

Ruff configuration is in `ruff.toml`.

---

## Use Cases

- Bioinformatics education and prototyping
- Backend engine for DNA visualization or annotation tools
- Teaching demonstrations of the Central Dogma of Molecular Biology
- Research prototyping for promoter/terminator discovery pipelines