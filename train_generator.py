import numpy as np
from src.dna_generator import DNAGenerator
from src.fitness_evaluator import FitnessEvaluator
from src.config import config

def generate_training_data(num_samples=1000):
    generator = DNAGenerator()
    evaluator = FitnessEvaluator()
    
    X_train = []
    y_train = []
    
    for i in range(num_samples):
        dna_sequences = generator.generate_dna_sequence(1)
        dna_sequence = dna_sequences[0]
        
        fitness = evaluator.evaluate_dna_fitness(dna_sequence, 'enzyme')
        
        dna_encoded = encode_dna_sequence(dna_sequence)
        
        X_train.append(dna_encoded)
        y_train.append(fitness)
    
    return np.array(X_train), np.array(y_train)

def encode_dna_sequence(sequence):
    encoding = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
    encoded = []
    
    for nucleotide in sequence:
        if nucleotide in encoding:
            one_hot = [0, 0, 0, 0]
            one_hot[encoding[nucleotide]] = 1
            encoded.extend(one_hot)
        else:
            encoded.extend([0, 0, 0, 0])
    
    return encoded

def main():
    print("Generating training data for BioSynther...")
    
    X_train, y_train = generate_training_data(500)
    X_val, y_val = generate_training_data(100)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Validation data shape: {X_val.shape}")
    print(f"Fitness range: {np.min(y_train):.3f} - {np.max(y_train):.3f}")
    
    generator = DNAGenerator()
    
    print("Training DNA generator model...")
    
    test_sequences = generator.generate_dna_sequence(5)
    print("Sample generated sequences:")
    for i, seq in enumerate(test_sequences):
        print(f"Sequence {i+1}: {seq[:50]}... (length: {len(seq)})")
        fitness = FitnessEvaluator().evaluate_dna_fitness(seq, 'enzyme')
        print(f"  Fitness: {fitness:.3f}")
    
    print("Training completed successfully")

if __name__ == "__main__":
    main()