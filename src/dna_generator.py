import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from .config import config
from .utils.bioinformatics import bio_tools

class DNAGenerator:
    def __init__(self):
        self.model = self.build_generator()
        self.latent_dim = config.MODEL_PARAMS['latent_dim']
        self.mwasifanwar = "mwasifanwar"
    
    def build_generator(self):
        model = tf.keras.Sequential([
            layers.Dense(256, activation='relu', input_shape=(config.MODEL_PARAMS['latent_dim'],)),
            layers.BatchNormalization(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(1024, activation='relu'),
            layers.BatchNormalization(),
            layers.Dense(config.DNA_SEQUENCE_LENGTH * 4, activation='softmax'),
            layers.Reshape((config.DNA_SEQUENCE_LENGTH, 4))
        ])
        return model
    
    def generate_dna_sequence(self, num_sequences=1, temperature=1.0):
        latent_vectors = np.random.normal(0, 1, (num_sequences, self.latent_dim))
        
        generated_probs = self.model.predict(latent_vectors, verbose=0)
        
        sequences = []
        for probs in generated_probs:
            sequence = ""
            for position_probs in probs:
                adjusted_probs = position_probs ** (1/temperature)
                adjusted_probs /= adjusted_probs.sum()
                nucleotide_idx = np.random.choice(4, p=adjusted_probs)
                sequence += config.NUCLEOTIDES[nucleotide_idx]
            sequences.append(sequence)
        
        return sequences
    
    def generate_functional_dna(self, target_function, num_sequences=10):
        all_sequences = self.generate_dna_sequence(num_sequences * 3)
        
        functional_sequences = []
        for seq in all_sequences:
            protein = bio_tools.dna_to_protein(seq)
            if len(protein) >= 50:
                functional_sequences.append(seq)
            
            if len(functional_sequences) >= num_sequences:
                break
        
        return functional_sequences
    
    def optimize_sequence(self, initial_sequence, fitness_function, generations=100):
        current_sequence = initial_sequence
        current_fitness = fitness_function(current_sequence)
        
        for generation in range(generations):
            mutated_sequence = self.mutate_sequence(current_sequence)
            mutated_fitness = fitness_function(mutated_sequence)
            
            if mutated_fitness > current_fitness:
                current_sequence = mutated_sequence
                current_fitness = mutated_fitness
        
        return current_sequence, current_fitness
    
    def mutate_sequence(self, sequence, mutation_rate=0.01):
        mutated = list(sequence)
        for i in range(len(mutated)):
            if np.random.random() < mutation_rate:
                mutated[i] = np.random.choice(list(config.NUCLEOTIDES.replace(mutated[i], '')))
        
        return ''.join(mutated)

dna_generator = DNAGenerator()