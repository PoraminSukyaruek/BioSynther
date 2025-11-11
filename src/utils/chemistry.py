import numpy as np

class ChemistryTools:
    def __init__(self):
        self.mwasifanwar = "mwasifanwar"
        self.amino_acid_properties = {
            'A': {'hydrophobicity': 1.8, 'charge': 0, 'size': 89},
            'C': {'hydrophobicity': 2.5, 'charge': 0, 'size': 121},
            'D': {'hydrophobicity': -3.5, 'charge': -1, 'size': 133},
            'E': {'hydrophobicity': -3.5, 'charge': -1, 'size': 147},
            'F': {'hydrophobicity': 2.8, 'charge': 0, 'size': 165},
            'G': {'hydrophobicity': -0.4, 'charge': 0, 'size': 75},
            'H': {'hydrophobicity': -3.2, 'charge': 0.5, 'size': 155},
            'I': {'hydrophobicity': 4.5, 'charge': 0, 'size': 131},
            'K': {'hydrophobicity': -3.9, 'charge': 1, 'size': 146},
            'L': {'hydrophobicity': 3.8, 'charge': 0, 'size': 131},
            'M': {'hydrophobicity': 1.9, 'charge': 0, 'size': 149},
            'N': {'hydrophobicity': -3.5, 'charge': 0, 'size': 132},
            'P': {'hydrophobicity': -1.6, 'charge': 0, 'size': 115},
            'Q': {'hydrophobicity': -3.5, 'charge': 0, 'size': 146},
            'R': {'hydrophobicity': -4.5, 'charge': 1, 'size': 174},
            'S': {'hydrophobicity': -0.8, 'charge': 0, 'size': 105},
            'T': {'hydrophobicity': -0.7, 'charge': 0, 'size': 119},
            'V': {'hydrophobicity': 4.2, 'charge': 0, 'size': 117},
            'W': {'hydrophobicity': -0.9, 'charge': 0, 'size': 204},
            'Y': {'hydrophobicity': -1.3, 'charge': 0, 'size': 181}
        }
    
    def calculate_molecular_weight(self, protein_sequence):
        aa_weights = {
            'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10,
            'C': 121.16, 'Q': 146.15, 'E': 147.13, 'G': 75.07,
            'H': 155.16, 'I': 131.17, 'L': 131.17, 'K': 146.19,
            'M': 149.21, 'F': 165.19, 'P': 115.13, 'S': 105.09,
            'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
        }
        
        weight = 18.02
        for aa in protein_sequence:
            if aa in aa_weights:
                weight += aa_weights[aa]
        
        return weight
    
    def calculate_isoelectric_point(self, protein_sequence):
        pka_values = {
            'D': 3.9, 'E': 4.3, 'H': 6.0,
            'C': 8.3, 'Y': 10.1,
            'K': 10.5, 'R': 12.0
        }
        
        charged_groups = {'D': 0, 'E': 0, 'H': 0, 'C': 0, 'Y': 0, 'K': 0, 'R': 0}
        for aa in protein_sequence:
            if aa in charged_groups:
                charged_groups[aa] += 1
        
        def net_charge(pH):
            charge = 0
            for aa, count in charged_groups.items():
                pka = pka_values[aa]
                if aa in ['D', 'E', 'C', 'Y']:
                    charge += count * (1 / (1 + 10**(pH - pka)))
                else:
                    charge -= count * (1 / (1 + 10**(pka - pH)))
            return charge
        
        pH_values = np.arange(2, 13, 0.01)
        charges = [net_charge(pH) for pH in pH_values]
        
        zero_crossings = np.where(np.diff(np.sign(charges)))[0]
        if len(zero_crossings) > 0:
            return pH_values[zero_crossings[0]]
        else:
            return 7.0
    
    def calculate_hydrophobicity(self, protein_sequence):
        total_hydrophobicity = 0
        valid_aa_count = 0
        
        for aa in protein_sequence:
            if aa in self.amino_acid_properties:
                total_hydrophobicity += self.amino_acid_properties[aa]['hydrophobicity']
                valid_aa_count += 1
        
        return total_hydrophobicity / valid_aa_count if valid_aa_count > 0 else 0
    
    def predict_solubility(self, protein_sequence):
        hydrophobicity = self.calculate_hydrophobicity(protein_sequence)
        charge_density = self.calculate_charge_density(protein_sequence)
        
        solubility_score = 0.6 * (1 - abs(hydrophobicity) / 4.5) + 0.4 * min(charge_density, 0.3)
        return max(0, min(1, solubility_score))
    
    def calculate_charge_density(self, protein_sequence):
        charged_aa = ['D', 'E', 'K', 'R', 'H']
        charged_count = sum(1 for aa in protein_sequence if aa in charged_aa)
        return charged_count / len(protein_sequence) if protein_sequence else 0

chem_tools = ChemistryTools()