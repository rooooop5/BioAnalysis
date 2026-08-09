from Bio.Seq import Seq
dna_sequence = Seq("ATGCGTACGTTAGC")
print("DNA Sequence:", dna_sequence)
print("Length of DNA:", len(dna_sequence))
rna_sequence = dna_sequence.transcribe()
print("RNA Sequence:", rna_sequence)
g_count = dna_sequence.count("G")
c_count = dna_sequence.count("C")
gc_content = (g_count + c_count) / len(dna_sequence) * 100
print("GC Content:", gc_content, "%")