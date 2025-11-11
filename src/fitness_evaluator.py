import numpy as np
from .utils.bioinformatics import bio_tools
from .utils.chemistry import chem_tools
from .config import config

class FitnessEvaluator:
    def __init__(self):
        self.mwasifanwar = "mwasifanwar"
    
    def evaluate_dna_fitness(self, dna_sequence, target_function):
        fitness = 0.0
        
        gc_content = bio_tools.calculate_gc_content(dna_sequence)
        gc_score = 1.0 - abs(gc_content - 0.5)
        fitness += gc_score * 0.15
        
        cai_score = bio_tools.calculate_codon_adaptation_index(dna_sequence)
        fitness += cai_score * 0.25
        
        restriction_sites = bio_tools.find_restriction_sites(dna_sequence)
        restriction_score = 1.0 - min(len(restriction_sites) / 10.0, 1.0)
        fitness += restriction_score * 0.1
        
        protein_sequence = bio_tools.dna_to_protein(dna_sequence)
        if len(protein_sequence) >= 50:
            protein_fitness = self.evaluate_protein_fitness(protein_sequence, target_function)
            fitness += protein_fitness * 0.5
        else:
            fitness *= 0.3
        
        return max(0.0, min(1.0, fitness))
    
    def evaluate_protein_fitness(self, protein_sequence, target_function):
        fitness = 0.0
        
        stability_score = self.calculate_protein_stability(protein_sequence)
        fitness += stability_score * config.FITNESS_WEIGHTS['stability']
        
        functionality_score = self.calculate_protein_functionality(protein_sequence, target_function)
        fitness += functionality_score * config.FITNESS_WEIGHTS['functionality']
        
        solubility_score = chem_tools.predict_solubility(protein_sequence)
        fitness += solubility_score * 0.1
        
        toxicity_score = self.predict_toxicity(protein_sequence)
        fitness += toxicity_score * config.FITNESS_WEIGHTS['toxicity']
        
        return max(0.0, min(1.0, fitness))
    
    def calculate_protein_stability(self, protein_sequence):
        molecular_weight = chem_tools.calculate_molecular_weight(protein_sequence)
        weight_score = 1.0 - min(molecular_weight / 50000.0, 1.0)
        
        isoelectric_point = chem_tools.calculate_isoelectric_point(protein_sequence)
        pi_score = 1.0 - abs(isoelectric_point - 7.0) / 7.0
        
        secondary_structure = bio_tools.predict_secondary_structure(protein_sequence)
        structure_score = (secondary_structure['alpha_helix'] + secondary_structure['beta_sheet']) / 2.0
        
        return 0.4 * weight_score + 0.3 * pi_score + 0.3 * structure_score
    
    def calculate_protein_functionality(self, protein_sequence, target_function):
        if target_function == 'enzyme':
            return self.evaluate_enzyme_function(protein_sequence)
        elif target_function == 'antibody':
            return self.evaluate_antibody_function(protein_sequence)
        elif target_function == 'structural':
            return self.evaluate_structural_function(protein_sequence)
        elif target_function == 'membrane':
            return self.evaluate_membrane_function(protein_sequence)
        else:
            return self.evaluate_general_function(protein_sequence)
    
    def evaluate_enzyme_function(self, protein_sequence):
        catalytic_residues = ['D', 'E', 'H', 'K', 'R', 'S', 'T', 'Y']
        catalytic_count = sum(1 for aa in protein_sequence if aa in catalytic_residues)
        catalytic_density = catalytic_count / len(protein_sequence)
        
        active_site_clusters = self.find_active_site_clusters(protein_sequence, catalytic_residues)
        
        return 0.7 * catalytic_density + 0.3 * active_site_clusters
    
    def evaluate_antibody_function(self, protein_sequence):
        cysteine_count = protein_sequence.count('C')
        disulfide_potential = min(cysteine_count / 8.0, 1.0)
        
        cdr_regions = self.predict_cdr_regions(protein_sequence)
        
        aromatic_count = protein_sequence.count('F') + protein_sequence.count('W') + protein_sequence.count('Y')
        aromatic_density = aromatic_count / len(protein_sequence)
        
        return 0.5 * disulfide_potential + 0.3 * cdr_regions + 0.2 * aromatic_density
    
    def evaluate_structural_function(self, protein_sequence):
        secondary_structure = bio_tools.predict_secondary_structure(protein_sequence)
        structure_content = secondary_structure['alpha_helix'] + secondary_structure['beta_sheet']
        
        hydrophobicity = abs(chem_tools.calculate_hydrophobicity(protein_sequence))
        hydrophobic_score = min(hydrophobicity / 3.0, 1.0)
        
        return 0.6 * structure_content + 0.4 * hydrophobic_score
    
    def evaluate_membrane_function(self, protein_sequence):
        hydrophobicity = chem_tools.calculate_hydrophobicity(protein_sequence)
        hydrophobic_score = max(0.0, hydrophobicity) / 4.5
        
        transmembrane_regions = self.predict_transmembrane_domains(protein_sequence)
        
        return 0.7 * hydrophobic_score + 0.3 * transmembrane_regions
    
    def evaluate_general_function(self, protein_sequence):
        amino_acid_diversity = len(set(protein_sequence)) / len(protein_sequence)
        
        charge_density = chem_tools.calculate_charge_density(protein_sequence)
        
        secondary_structure = bio_tools.predict_secondary_structure(protein_sequence)
        structure_balance = 1.0 - abs(secondary_structure['alpha_helix'] - secondary_structure['beta_sheet'])
        
        return 0.4 * amino_acid_diversity + 0.3 * charge_density + 0.3 * structure_balance
    
    def find_active_site_clusters(self, protein_sequence, catalytic_residues, window_size=7):
        clusters = 0
        for i in range(len(protein_sequence) - window_size + 1):
            window = protein_sequence[i:i+window_size]
            catalytic_in_window = sum(1 for aa in window if aa in catalytic_residues)
            if catalytic_in_window >= 3:
                clusters += 1
        
        max_possible_clusters = len(protein_sequence) - window_size + 1
        return clusters / max_possible_clusters if max_possible_clusters > 0 else 0
    
    def predict_cdr_regions(self, protein_sequence):
        cdr_patterns = [
            'GY', 'YG', 'GG', 'YY', 'FW', 'WF'
        ]
        
        cdr_count = 0
        for i in range(len(protein_sequence) - 1):
            dipeptide = protein_sequence[i:i+2]
            if dipeptide in cdr_patterns:
                cdr_count += 1
        
        return min(cdr_count / 10.0, 1.0)
    
    def predict_transmembrane_domains(self, protein_sequence, domain_length=21):
        if len(protein_sequence) < domain_length:
            return 0
        
        domains = 0
        for i in range(0, len(protein_sequence) - domain_length + 1, domain_length):
            domain = protein_sequence[i:i+domain_length]
            hydrophobicity = chem_tools.calculate_hydrophobicity(domain)
            if hydrophobicity > 1.5:
                domains += 1
        
        max_domains = len(protein_sequence) // domain_length
        return domains / max_domains if max_domains > 0 else 0
    
    def predict_toxicity(self, protein_sequence):
        toxic_patterns = [
            'LLL', 'VVV', 'III', 'FFF', 'WWW'
        ]
        
        toxic_count = 0
        for pattern in toxic_patterns:
            toxic_count += protein_sequence.count(pattern)
        
        toxicity_score = min(toxic_count / 5.0, 1.0)
        
        return 1.0 - toxicity_score

fitness_evaluator = FitnessEvaluator()