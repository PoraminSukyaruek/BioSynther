import os

class Config:
    DNA_SEQUENCE_LENGTH = 1000
    PROTEIN_SEQUENCE_LENGTH = 300
    MAX_CIRCUIT_COMPONENTS = 15
    
    GENETIC_CODON_TABLE = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
        'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W'
    }
    
    AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'
    NUCLEOTIDES = 'ATCG'
    
    MODEL_PARAMS = {
        'learning_rate': 0.001,
        'batch_size': 32,
        'epochs': 200,
        'latent_dim': 128
    }
    
    FITNESS_WEIGHTS = {
        'expression_level': 0.3,
        'stability': 0.25,
        'functionality': 0.35,
        'toxicity': -0.1
    }
    
    DATA_PATHS = {
        'genetic_parts': 'data/genetic_parts/',
        'protein_templates': 'data/protein_templates/',
        'metabolic_pathways': 'data/metabolic_pathways/',
        'organisms': 'data/organisms/'
    }

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = DevelopmentConfig()