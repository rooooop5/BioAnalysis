🧬 DNA Processing API

A modular DNA sequence processing API built with FastAPI, Pydantic, and BioPython.
This project models biological workflows inspired by the Central Dogma of Molecular Biology, focusing on clean backend architecture and pipeline-based execution.

⸻

📌 Objective

Build a backend system that:
	•	Validates DNA sequences
	•	Performs biological transformations and analysis
	•	Supports single-step endpoints and multi-step pipelines
	•	Demonstrates clean architecture and separation of concerns

Focus is on software design and pipeline workflows, rather than computational complexity.

⸻

🚀 Features
	•	DNA sequence validation
	•	Complement & reverse complement
	•	Transcription (DNA → RNA)
	•	Translation (DNA → Protein)
	•	DNA sequence analysis:
	•	GC fraction
	•	Nucleotide count
	•	Pipeline execution with shared context
	•	Reusable validation using FastAPI dependency injection

⸻

🧠 Architecture

API Endpoint
      ↓
Dependency / Validation Layer
      ↓
DNA Engine (Pipeline Executor)
      ↓
Bio Functions (BioPython)

Design Principles
	•	Separation of concerns: DNA engine is independent of HTTP logic
	•	Validation controlled at API layer
	•	Shared execution state via pipeline context
	•	Pipeline stops execution if validation fails

⸻

📦 Core Models

class DNASequence(BaseModel):
    seq: str

class Strand(str, Enum):
    CODING = "CODING"
    TEMPLATE = "TEMPLATE"

class DNAPipelineSteps(str, Enum):
    VALIDATE = "VALIDATE"
    REVERSE_COMPLEMENT = "REVERSE COMPLEMENT"
    COMPLEMENT = "COMPLEMENT"
    TRANSCRIBE = "TRANSCRIBE"
    TRANSLATE = "TRANSLATE"
    ANALYZE = "ANALYZE"

class InvocationSource(str, Enum):
    PIPELINE = "PIPELINE"
    ENDPOINT = "ENDPOINT"

DNAInvalidReasons = Literal[
    "INVALID_CHARACTER_PRESENT",
    "CONTAINS_WHITESPACE",
    "NON_STRING_INPUT",
    "EMPTY_SEQUENCE",
    "SEQUENCE_TOO_SHORT",
    "LENGTH_NOT_MULTIPLE_OF_THREE"
]


⸻

🔗 Pipeline Execution
	•	Accepts a list of pipeline steps
	•	Executes sequentially
	•	Shares state via pipeline context
	•	Stops if validation fails

Example:
VALIDATE → TRANSCRIBE → TRANSLATE → ANALYZE

⸻

🧪 Tech Stack
	•	FastAPI
	•	Pydantic
	•	BioPython
	•	Python 3.10+

⸻

🎓 Academic Scope
	•	Minor project submissions
	•	Bioinformatics coursework
	•	Backend architecture demos
	•	Learning pipeline & workflow design

⸻

🔮 Future Enhancements
	•	RNA & protein pipelines
	•	Mutation simulation
	•	Central Dogma execution presets
	•	Async pipeline execution
	•	Improved error standardization

⸻

📌 Summary

This project demonstrates modeling biological workflows using modern backend patterns such as:
	•	Dependency injection
	•	Pipeline engines
	•	Shared execution context

…while keeping biological logic and API concerns cleanly separated.