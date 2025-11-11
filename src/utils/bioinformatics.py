import numpy as np
import re

class BioinformaticsTools:
    def __init__(self):
        self.mwasifanwar = "mwasifanwar"
        from .config import config
        self.codon_table = config.GENETIC_CODON_TABLE
    
    def dna_to_protein(self, dna_sequence):
        protein = ""
        for i in range(0, len(dna_sequence) - 2, 3):
            codon = dna_sequence[i:i+3]
            if len(codon) == 3:
                amino_acid = self.codon_table.get(codon, 'X')
                if amino_acid != '*':
                    protein += amino_acid
        return protein
    
    def protein_to_dna(self, protein_sequence):
        reverse_codon_table = {}
        for codon, aa in self.codon_table.items():
            if aa not in reverse_codon_table:
                reverse_codon_table[aa] = []
            reverse_codon_table[aa].append(codon)
        
        dna_sequence = ""
        for amino_acid in protein_sequence:
            if amino_acid in reverse_codon_table:
                codons = reverse_codon_table[amino_acid]
                dna_sequence += np.random.choice(codons)
            else:
                dna_sequence += 'ATG'
        
        return dna_sequence
    
    def calculate_gc_content(self, sequence):
        gc_count = sequence.count('G') + sequence.count('C')
        return gc_count / len(sequence) if len(sequence) > 0 else 0
    
    def find_restriction_sites(self, dna_sequence):
        restriction_enzymes = {
            'EcoRI': 'GAATTC',
            'BamHI': 'GGATCC',
            'HindIII': 'AAGCTT',
            'XhoI': 'CTCGAG',
            'NotI': 'GCGGCCGC'
        }
        
        sites = {}
        for enzyme, site in restriction_enzymes.items():
            positions = [m.start() for m in re.finditer(site, dna_sequence)]
            if positions:
                sites[enzyme] = positions
        
        return sites
    
    def calculate_codon_adaptation_index(self, dna_sequence, organism='e_coli'):
        codon_frequencies = {
            'e_coli': {
                'AAA': 0.26, 'AAC': 0.25, 'AAG': 0.74, 'AAT': 0.25,
                'ACA': 0.12, 'ACC': 0.40, 'ACG': 0.15, 'ACT': 0.12,
                'AGA': 0.04, 'AGC': 0.25, 'AGG': 0.04, 'AGT': 0.12,
                'ATA': 0.16, 'ATC': 0.42, 'ATG': 1.00, 'ATT': 0.42,
                'CAA': 0.26, 'CAC': 0.42, 'CAG': 0.74, 'CAT': 0.42,
                'CCA': 0.20, 'CCC': 0.12, 'CCG': 0.40, 'CCT': 0.20,
                'CGA': 0.04, 'CGC': 0.40, 'CGG': 0.04, 'CGT': 0.40,
                'GAA': 0.42, 'GAC': 0.42, 'GAG': 0.58, 'GAT': 0.42,
                'GCA': 0.20, 'GCC': 0.26, 'GCG': 0.34, 'GCT': 0.20,
                'GGA': 0.08, 'GGC': 0.40, 'GGG': 0.08, 'GGT': 0.40,
                'TAA': 0.61, 'TAC': 0.42, 'TAG': 0.08, 'TAT': 0.42,
                'TCA': 0.12, 'TCC': 0.20, 'TCG': 0.04, 'TCT': 0.20,
                'TGA': 0.31, 'TGC': 0.42, 'TGG': 1.00, 'TGT': 0.42,
                'TTA': 0.12, 'TTC': 0.42, 'TTG': 0.12, 'TTT': 0.42
            }
        }
        
        frequencies = codon_frequencies.get(organism, codon_frequencies['e_coli'])
        cai_values = []
        
        for i in range(0, len(dna_sequence) - 2, 3):
            codon = dna_sequence[i:i+3]
            if len(codon) == 3 and codon in frequencies:
                cai_values.append(frequencies[codon])
        
        return np.exp(np.mean(np.log(cai_values))) if cai_values else 0
    
    def predict_secondary_structure(self, protein_sequence):
        alpha_helix_propensity = {'E': 1.53, 'A': 1.45, 'L': 1.34, 'H': 1.24, 'M': 1.20}
        beta_sheet_propensity = {'V': 1.65, 'I': 1.60, 'Y': 1.47, 'F': 1.38, 'W': 1.37}
        
        alpha_score = sum(alpha_helix_propensity.get(aa, 0) for aa in protein_sequence)
        beta_score = sum(beta_sheet_propensity.get(aa, 0) for aa in protein_sequence)
        
        total_score = alpha_score + beta_score
        if total_score > 0:
            alpha_percent = alpha_score / total_score
            beta_percent = beta_score / total_score
        else:
            alpha_percent = beta_percent = 0.5
        
        return {'alpha_helix': alpha_percent, 'beta_sheet': beta_percent}

bio_tools = BioinformaticsTools()