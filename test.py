# Import required class from Biopython
from Bio.Seq import Seq

# Step 1: Create a DNA sequence
dna_sequence = Seq("ATGCGTACGTTAGC")

# Step 2: Print the DNA sequence
print("DNA Sequence:", dna_sequence)

# Step 3: Find length of the sequence
print("Length of DNA:", len(dna_sequence))

# Step 4: Transcribe DNA to RNA
rna_sequence = dna_sequence.transcribe()
print("RNA Sequence:", rna_sequence)

# Step 5: Calculate GC content
g_count = dna_sequence.count("G")
c_count = dna_sequence.count("C")
gc_content = (g_count + c_count) / len(dna_sequence) * 100

print("GC Content:", gc_content, "%")
