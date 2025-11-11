import numpy as np
from .utils.bioinformatics import bio_tools
from .utils.chemistry import chem_tools
from .config import config

class ProteinDesigner:
    def __init__(self):
        self.mwasifanwar = "mwasifanwar"
    
    def design_protein(self, target_function, constraints=None):
        if constraints is None:
            constraints = {}
        
        target_length = constraints.get('length', config.PROTEIN_SEQUENCE_LENGTH)
        target_hydrophobicity = constraints.get('hydrophobicity', 0)
        target_charge = constraints.get('charge', 0)
        
        best_sequence = None
        best_score = -float('inf')
        
        for _ in range(100):
            candidate = self.generate_random_protein(target_length)
            score = self.evaluate_protein_design(candidate, target_function, constraints)
            
            if score > best_score:
                best_sequence = candidate
                best_score = score
        
        return best_sequence, best_score
    
    def generate_random_protein(self, length):
        return ''.join(np.random.choice(list(config.AMINO_ACIDS), length))
    
    def evaluate_protein_design(self, protein_sequence, target_function, constraints):
        score = 0.0
        
        stability_score = self.calculate_stability(protein_sequence)
        score += stability_score * 0.3
        
        functionality_score = self.predict_functionality(protein_sequence, target_function)
        score += functionality_score * 0.4
        
        solubility_score = chem_tools.predict_solubility(protein_sequence)
        score += solubility_score * 0.2
        
        if 'hydrophobicity' in constraints:
            actual_hydrophobicity = chem_tools.calculate_hydrophobicity(protein_sequence)
            hydrophobicity_match = 1 - abs(actual_hydrophobicity - constraints['hydrophobicity']) / 4.5
            score += hydrophobicity_match * 0.1
        
        return score
    
    def calculate_stability(self, protein_sequence):
        secondary_structure = bio_tools.predict_secondary_structure(protein_sequence)
        
        alpha_content = secondary_structure['alpha_helix']
        beta_content = secondary_structure['beta_sheet']
        
        structure_balance = 1 - abs(alpha_content - beta_content)
        
        hydrophobicity = abs(chem_tools.calculate_hydrophobicity(protein_sequence))
        hydrophobicity_score = 1 - min(hydrophobicity / 3.0, 1.0)
        
        return 0.6 * structure_balance + 0.4 * hydrophobicity_score
    
    def predict_functionality(self, protein_sequence, target_function):
        if target_function == 'enzyme':
            return self.predict_enzyme_function(protein_sequence)
        elif target_function == 'antibody':
            return self.predict_antibody_function(protein_sequence)
        elif target_function == 'membrane_protein':
            return self.predict_membrane_protein_function(protein_sequence)
        else:
            return self.predict_general_function(protein_sequence)
    
    def predict_enzyme_function(self, protein_sequence):
        catalytic_residues = ['D', 'E', 'H', 'K', 'R', 'S', 'T', 'Y']
        catalytic_count = sum(1 for aa in protein_sequence if aa in catalytic_residues)
        catalytic_density = catalytic_count / len(protein_sequence)
        
        flexibility_score = self.calculate_flexibility(protein_sequence)
        
        return 0.7 * catalytic_density + 0.3 * flexibility_score
    
    def predict_antibody_function(self, protein_sequence):
        cysteine_count = protein_sequence.count('C')
        disulfide_potential = min(cysteine_count / 8, 1.0)
        
        aromatic_count = protein_sequence.count('F') + protein_sequence.count('W') + protein_sequence.count('Y')
        aromatic_density = aromatic_count / len(protein_sequence)
        
        return 0.6 * disulfide_potential + 0.4 * aromatic_density
    
    def predict_membrane_protein_function(self, protein_sequence):
        hydrophobicity = chem_tools.calculate_hydrophobicity(protein_sequence)
        hydrophobic_score = max(0, hydrophobicity) / 4.5
        
        transmembrane_regions = self.predict_transmembrane_regions(protein_sequence)
        
        return 0.8 * hydrophobic_score + 0.2 * transmembrane_regions
    
    def predict_general_function(self, protein_sequence):
        diversity = len(set(protein_sequence)) / len(protein_sequence)
        secondary_structure = bio_tools.predict_secondary_structure(protein_sequence)
        structure_score = (secondary_structure['alpha_helix'] + secondary_structure['beta_sheet']) / 2
        
        return 0.5 * diversity + 0.5 * structure_score
    
    def calculate_flexibility(self, protein_sequence):
        flexible_residues = ['G', 'A', 'S', 'T']
        flexible_count = sum(1 for aa in protein_sequence if aa in flexible_residues)
        return flexible_count / len(protein_sequence)
    
    def predict_transmembrane_regions(self, protein_sequence, window_size=19):
        if len(protein_sequence) < window_size:
            return 0
        
        hydrophobic_windows = 0
        for i in range(len(protein_sequence) - window_size + 1):
            window = protein_sequence[i:i+window_size]
            hydrophobicity = chem_tools.calculate_hydrophobicity(window)
            if hydrophobicity > 1.0:
                hydrophobic_windows += 1
        
        return hydrophobic_windows / (len(protein_sequence) - window_size + 1)

protein_designer = ProteinDesigner()