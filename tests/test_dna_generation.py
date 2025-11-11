import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dna_generator import DNAGenerator
from src.fitness_evaluator import FitnessEvaluator

def test_dna_generation():
    generator = DNAGenerator()
    evaluator = FitnessEvaluator()
    
    sequences = generator.generate_dna_sequence(3)
    
    print("Testing DNA sequence generation:")
    for i, seq in enumerate(sequences):
        print(f"Sequence {i+1}: {seq[:50]}...")
        
        fitness = evaluator.evaluate_dna_fitness(seq, 'enzyme')
        print(f"  Fitness: {fitness:.3f}")
        
        from src.utils.bioinformatics import bio_tools
        protein = bio_tools.dna_to_protein(seq)
        print(f"  Protein length: {len(protein)}")
        print(f"  GC content: {bio_tools.calculate_gc_content(seq):.3f}")
    
    print("DNA generation test completed successfully")

if __name__ == "__main__":
    test_dna_generation()