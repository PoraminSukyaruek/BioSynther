import numpy as np
import networkx as nx
from .config import config

class MetabolicEngine:
    def __init__(self):
        self.metabolic_pathways = self.load_metabolic_pathways()
        self.mwasifanwar = "mwasifanwar"
    
    def load_metabolic_pathways(self):
        pathways = {
            'glycolysis': {
                'inputs': ['glucose', 'ATP'],
                'outputs': ['pyruvate', 'ATP', 'NADH'],
                'enzymes': ['hexokinase', 'phosphofructokinase', 'pyruvate_kinase'],
                'efficiency': 0.85
            },
            'TCA_cycle': {
                'inputs': ['acetyl-CoA', 'NAD+', 'ADP'],
                'outputs': ['ATP', 'NADH', 'FADH2', 'CO2'],
                'enzymes': ['citrate_synthase', 'isocitrate_dehydrogenase', 'alpha_ketoglutarate_dehydrogenase'],
                'efficiency': 0.78
            },
            'fatty_acid_synthesis': {
                'inputs': ['acetyl-CoA', 'NADPH', 'ATP'],
                'outputs': ['palmitate', 'NADP+', 'ADP'],
                'enzymes': ['acetyl-CoA_carboxylase', 'fatty_acid_synthase'],
                'efficiency': 0.72
            },
            'photosynthesis': {
                'inputs': ['CO2', 'H2O', 'light'],
                'outputs': ['glucose', 'O2'],
                'enzymes': ['RuBisCO', 'PSI', 'PSII'],
                'efficiency': 0.65
            }
        }
        return pathways
    
    def design_metabolic_pathway(self, substrate, product, max_steps=6):
        pathway = {
            'steps': [],
            'efficiency': 0.0,
            'enzymes': [],
            'intermediates': []
        }
        
        current_compound = substrate
        steps = 0
        
        while current_compound != product and steps < max_steps:
            possible_reactions = self.find_possible_reactions(current_compound)
            
            if not possible_reactions:
                break
            
            best_reaction = max(possible_reactions, key=lambda x: x['efficiency'])
            
            pathway['steps'].append(best_reaction)
            pathway['enzymes'].extend(best_reaction['enzymes'])
            pathway['intermediates'].append(best_reaction['output'])
            
            current_compound = best_reaction['output']
            steps += 1
        
        if pathway['steps']:
            pathway['efficiency'] = np.prod([step['efficiency'] for step in pathway['steps']])
        
        return pathway
    
    def find_possible_reactions(self, compound):
        possible_reactions = []
        
        for pathway_name, pathway_info in self.metabolic_pathways.items():
            if compound in pathway_info['inputs']:
                reaction = {
                    'pathway': pathway_name,
                    'input': compound,
                    'output': pathway_info['outputs'][0],
                    'enzymes': pathway_info['enzymes'],
                    'efficiency': pathway_info['efficiency']
                }
                possible_reactions.append(reaction)
        
        synthetic_reactions = self.generate_synthetic_reactions(compound)
        possible_reactions.extend(synthetic_reactions)
        
        return possible_reactions
    
    def generate_synthetic_reactions(self, compound):
        synthetic_reactions = []
        
        reaction_templates = [
            {
                'type': 'oxidation',
                'input_pattern': 'alcohol',
                'output_pattern': 'aldehyde',
                'efficiency': 0.8,
                'enzymes': ['alcohol_dehydrogenase']
            },
            {
                'type': 'reduction',
                'input_pattern': 'aldehyde',
                'output_pattern': 'alcohol',
                'efficiency': 0.75,
                'enzymes': ['aldehyde_reductase']
            },
            {
                'type': 'methylation',
                'input_pattern': 'amine',
                'output_pattern': 'methylated_amine',
                'efficiency': 0.7,
                'enzymes': ['methyltransferase']
            }
        ]
        
        compound_type = self.classify_compound(compound)
        
        for template in reaction_templates:
            if compound_type == template['input_pattern']:
                synthetic_reaction = {
                    'pathway': f'synthetic_{template["type"]}',
                    'input': compound,
                    'output': f'{compound}_{template["output_pattern"]}',
                    'enzymes': template['enzymes'],
                    'efficiency': template['efficiency']
                }
                synthetic_reactions.append(synthetic_reaction)
        
        return synthetic_reactions
    
    def classify_compound(self, compound):
        if 'alcohol' in compound.lower() or 'ol' in compound:
            return 'alcohol'
        elif 'aldehyde' in compound.lower() or 'al' in compound:
            return 'aldehyde'
        elif 'amine' in compound.lower():
            return 'amine'
        elif 'acid' in compound.lower():
            return 'acid'
        else:
            return 'generic'
    
    def optimize_pathway_efficiency(self, pathway, target_efficiency=0.9):
        current_efficiency = pathway['efficiency']
        
        while current_efficiency < target_efficiency and len(pathway['steps']) > 0:
            least_efficient_step = min(pathway['steps'], key=lambda x: x['efficiency'])
            
            alternative_reactions = self.find_possible_reactions(least_efficient_step['input'])
            if alternative_reactions:
                best_alternative = max(alternative_reactions, key=lambda x: x['efficiency'])
                
                if best_alternative['efficiency'] > least_efficient_step['efficiency']:
                    pathway['steps'].remove(least_efficient_step)
                    pathway['steps'].append(best_alternative)
                    
                    pathway['enzymes'] = []
                    for step in pathway['steps']:
                        pathway['enzymes'].extend(step['enzymes'])
                    
                    current_efficiency = np.prod([step['efficiency'] for step in pathway['steps']])
                else:
                    break
            else:
                break
        
        pathway['efficiency'] = current_efficiency
        return pathway
    
    def calculate_pathway_flux(self, pathway, substrate_concentration):
        if not pathway['steps']:
            return 0.0
        
        min_efficiency = min(step['efficiency'] for step in pathway['steps'])
        flux = substrate_concentration * min_efficiency
        
        return flux

metabolic_engine = MetabolicEngine()