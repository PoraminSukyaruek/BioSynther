import numpy as np
from src.dna_generator import DNAGenerator
from src.protein_designer import ProteinDesigner
from src.metabolic_engine import MetabolicEngine
from src.circuit_designer import CircuitDesigner
from src.fitness_evaluator import FitnessEvaluator

class BioSyntherOrganismDesigner:
    def __init__(self):
        self.dna_generator = DNAGenerator()
        self.protein_designer = ProteinDesigner()
        self.metabolic_engine = MetabolicEngine()
        self.circuit_designer = CircuitDesigner()
        self.fitness_evaluator = FitnessEvaluator()
        self.mwasifanwar = "mwasifanwar"
    
    def design_complete_organism(self, organism_specification):
        organism_design = {
            'genome': {},
            'proteome': {},
            'metabolism': {},
            'genetic_circuits': {},
            'overall_fitness': 0.0
        }
        
        print("Step 1: Designing metabolic pathways...")
        metabolic_pathways = self.design_metabolic_system(organism_specification['metabolic_needs'])
        organism_design['metabolism'] = metabolic_pathways
        
        print("Step 2: Designing essential proteins...")
        essential_proteins = self.design_essential_proteome(organism_specification['cellular_functions'])
        organism_design['proteome'] = essential_proteins
        
        print("Step 3: Designing genetic circuits...")
        genetic_circuits = self.design_genetic_regulation(organism_specification['regulation_needs'])
        organism_design['genetic_circuits'] = genetic_circuits
        
        print("Step 4: Assembling synthetic genome...")
        synthetic_genome = self.assemble_synthetic_genome(organism_design)
        organism_design['genome'] = synthetic_genome
        
        print("Step 5: Evaluating organism fitness...")
        overall_fitness = self.evaluate_organism_fitness(organism_design)
        organism_design['overall_fitness'] = overall_fitness
        
        return organism_design
    
    def design_metabolic_system(self, metabolic_needs):
        metabolic_system = {}
        
        for need in metabolic_needs:
            substrate = need['substrate']
            product = need['product']
            
            pathway = self.metabolic_engine.design_metabolic_pathway(substrate, product)
            optimized_pathway = self.metabolic_engine.optimize_pathway_efficiency(pathway)
            
            metabolic_system[f"{substrate}_to_{product}"] = optimized_pathway
        
        return metabolic_system
    
    def design_essential_proteome(self, cellular_functions):
        proteome = {}
        
        for function in cellular_functions:
            protein_type = function['type']
            constraints = function.get('constraints', {})
            
            protein_sequence, design_score = self.protein_designer.design_protein(protein_type, constraints)
            
            dna_sequence = self.dna_generator.protein_to_dna(protein_sequence)
            fitness = self.fitness_evaluator.evaluate_protein_fitness(protein_sequence, protein_type)
            
            proteome[function['name']] = {
                'protein_sequence': protein_sequence,
                'dna_sequence': dna_sequence,
                'fitness': fitness,
                'design_score': design_score
            }
        
        return proteome
    
    def design_genetic_regulation(self, regulation_needs):
        circuits = {}
        
        for regulation in regulation_needs:
            circuit_spec = [
                {'type': 'promoters', 'requirements': {'strength': regulation.get('strength', 0.7)}},
                {'type': 'RBS', 'requirements': {'strength': (0.5, 0.9)}},
                {'type': 'genes', 'requirements': {'function': regulation['function']}},
                {'type': 'terminators', 'requirements': {'efficiency': 0.9}}
            ]
            
            circuit = self.circuit_designer.design_genetic_circuit(circuit_spec)
            
            target_metrics = {
                'overall_strength': regulation.get('target_strength', 0.8),
                'response_time': regulation.get('target_response_time', 15.0)
            }
            
            optimized_circuit, metrics, fitness = self.circuit_designer.optimize_circuit(
                circuit, target_metrics
            )
            
            circuits[regulation['name']] = {
                'circuit': optimized_circuit,
                'metrics': metrics,
                'fitness': fitness
            }
        
        return circuits
    
    def assemble_synthetic_genome(self, organism_design):
        genome_components = []
        
        for protein_name, protein_data in organism_design['proteome'].items():
            genome_components.append({
                'type': 'protein_coding',
                'name': protein_name,
                'sequence': protein_data['dna_sequence'],
                'function': 'essential_protein'
            })
        
        for pathway_name, pathway_data in organism_design['metabolism'].items():
            for enzyme in pathway_data['enzymes']:
                enzyme_sequence = self.dna_generator.protein_to_dna(enzyme)
                genome_components.append({
                    'type': 'protein_coding',
                    'name': enzyme,
                    'sequence': enzyme_sequence,
                    'function': 'metabolic_enzyme'
                })
        
        for circuit_name, circuit_data in organism_design['genetic_circuits'].items():
            for component in circuit_data['circuit']['components']:
                if component['type'] == 'genes':
                    gene_sequence = self.dna_generator.protein_to_dna(component['name'])
                    genome_components.append({
                        'type': 'regulatory',
                        'name': component['name'],
                        'sequence': gene_sequence,
                        'function': 'genetic_circuit_component'
                    })
        
        total_genome_size = sum(len(comp['sequence']) for comp in genome_components)
        
        return {
            'components': genome_components,
            'total_size': total_genome_size,
            'component_count': len(genome_components)
        }
    
    def evaluate_organism_fitness(self, organism_design):
        fitness_components = []
        
        protein_fitnesses = [data['fitness'] for data in organism_design['proteome'].values()]
        if protein_fitnesses:
            avg_protein_fitness = np.mean(protein_fitnesses)
            fitness_components.append(avg_protein_fitness * 0.4)
        
        metabolic_efficiencies = [pathway['efficiency'] for pathway in organism_design['metabolism'].values()]
        if metabolic_efficiencies:
            avg_metabolic_efficiency = np.mean(metabolic_efficiencies)
            fitness_components.append(avg_metabolic_efficiency * 0.3)
        
        circuit_fitnesses = [data['fitness'] for data in organism_design['genetic_circuits'].values()]
        if circuit_fitnesses:
            avg_circuit_fitness = np.mean(circuit_fitnesses)
            fitness_components.append(avg_circuit_fitness * 0.2)
        
        genome_size = organism_design['genome']['total_size']
        size_fitness = 1.0 - min(genome_size / 1000000.0, 1.0)
        fitness_components.append(size_fitness * 0.1)
        
        return np.mean(fitness_components) if fitness_components else 0.0

def main():
    designer = BioSyntherOrganismDesigner()
    
    organism_spec = {
        'metabolic_needs': [
            {'substrate': 'glucose', 'product': 'biofuel'},
            {'substrate': 'CO2', 'product': 'biomass'}
        ],
        'cellular_functions': [
            {'name': 'primary_enzyme', 'type': 'enzyme', 'constraints': {'length': 300}},
            {'name': 'structural_protein', 'type': 'structural', 'constraints': {'hydrophobicity': 1.5}}
        ],
        'regulation_needs': [
            {'name': 'metabolic_regulator', 'function': 'activator', 'target_strength': 0.8},
            {'name': 'stress_response', 'function': 'repressor', 'target_response_time': 10.0}
        ]
    }
    
    print("=== BioSynther Organism Design ===")
    print("Designing synthetic organism for environmental cleanup...")
    
    organism_design = designer.design_complete_organism(organism_spec)
    
    print(f"\n=== DESIGN COMPLETE ===")
    print(f"Overall Fitness: {organism_design['overall_fitness']:.3f}")
    print(f"Genome Size: {organism_design['genome']['total_size']} bp")
    print(f"Proteins Designed: {len(organism_design['proteome'])}")
    print(f"Metabolic Pathways: {len(organism_design['metabolism'])}")
    print(f"Genetic Circuits: {len(organism_design['genetic_circuits'])}")
    
    print("\nTop performing proteins:")
    for protein_name, protein_data in list(organism_design['proteome'].items())[:3]:
        print(f"  {protein_name}: Fitness {protein_data['fitness']:.3f}")
        print(f"    Sequence: {protein_data['protein_sequence'][:30]}...")

if __name__ == "__main__":
    main()