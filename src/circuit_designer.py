import numpy as np
from .config import config

class CircuitDesigner:
    def __init__(self):
        self.genetic_parts = self.load_genetic_parts()
        self.mwasifanwar = "mwasifanwar"
    
    def load_genetic_parts(self):
        parts = {
            'promoters': {
                'strong': {'strength': 0.9, 'leakiness': 0.1},
                'medium': {'strength': 0.6, 'leakiness': 0.05},
                'weak': {'strength': 0.3, 'leakiness': 0.02},
                'inducible': {'strength': 0.8, 'leakiness': 0.01}
            },
            'RBS': {
                'strong': {'strength': 0.95},
                'medium': {'strength': 0.7},
                'weak': {'strength': 0.4}
            },
            'genes': {
                'GFP': {'function': 'reporter', 'size': 720},
                'RFP': {'function': 'reporter', 'size': 675},
                'LacI': {'function': 'repressor', 'size': 1080},
                'TetR': {'function': 'repressor', 'size': 630},
                'AraC': {'function': 'activator', 'size': 870}
            },
            'terminators': {
                'strong': {'efficiency': 0.98},
                'weak': {'efficiency': 0.85}
            }
        }
        return parts
    
    def design_genetic_circuit(self, circuit_specification):
        circuit = {
            'components': [],
            'connections': [],
            'performance_metrics': {}
        }
        
        for component_spec in circuit_specification:
            component = self.select_genetic_part(component_spec)
            circuit['components'].append(component)
        
        circuit['connections'] = self.define_circuit_topology(circuit['components'])
        circuit['performance_metrics'] = self.calculate_circuit_performance(circuit)
        
        return circuit
    
    def select_genetic_part(self, specification):
        part_type = specification['type']
        requirements = specification.get('requirements', {})
        
        available_parts = self.genetic_parts[part_type]
        
        best_part = None
        best_score = -float('inf')
        
        for part_name, part_properties in available_parts.items():
            score = self.evaluate_part_fitness(part_properties, requirements)
            
            if score > best_score:
                best_part = part_name
                best_score = score
        
        return {
            'type': part_type,
            'name': best_part,
            'properties': available_parts[best_part]
        }
    
    def evaluate_part_fitness(self, part_properties, requirements):
        score = 0.0
        
        for req_key, req_value in requirements.items():
            if req_key in part_properties:
                property_value = part_properties[req_key]
                
                if isinstance(req_value, tuple):
                    min_val, max_val = req_value
                    if min_val <= property_value <= max_val:
                        score += 1.0
                    else:
                        distance = min(abs(property_value - min_val), abs(property_value - max_val))
                        score += max(0, 1 - distance)
                else:
                    similarity = 1 - abs(property_value - req_value) / max(property_value, req_value)
                    score += similarity
        
        return score / len(requirements) if requirements else 1.0
    
    def define_circuit_topology(self, components):
        connections = []
        
        promoters = [c for c in components if c['type'] == 'promoters']
        genes = [c for c in components if c['type'] == 'genes']
        
        for i, promoter in enumerate(promoters):
            if i < len(genes):
                connections.append({
                    'from': promoter['name'],
                    'to': genes[i]['name'],
                    'type': 'regulatory'
                })
        
        return connections
    
    def calculate_circuit_performance(self, circuit):
        metrics = {}
        
        total_strength = 1.0
        total_leakiness = 0.0
        
        for component in circuit['components']:
            if component['type'] == 'promoters':
                total_strength *= component['properties']['strength']
                total_leakiness += component['properties']['leakiness']
            elif component['type'] == 'RBS':
                total_strength *= component['properties']['strength']
        
        metrics['overall_strength'] = total_strength
        metrics['total_leakiness'] = min(total_leakiness, 1.0)
        metrics['signal_to_noise'] = total_strength / (total_leakiness + 0.001)
        
        response_time = self.calculate_response_time(circuit)
        metrics['response_time'] = response_time
        
        robustness = self.calculate_circuit_robustness(circuit)
        metrics['robustness'] = robustness
        
        return metrics
    
    def calculate_response_time(self, circuit):
        base_time = 10.0
        
        promoter_count = sum(1 for c in circuit['components'] if c['type'] == 'promoters')
        gene_count = sum(1 for c in circuit['components'] if c['type'] == 'genes')
        
        complexity_factor = (promoter_count + gene_count) / 5.0
        
        average_strength = np.mean([
            c['properties']['strength'] 
            for c in circuit['components'] 
            if 'strength' in c['properties']
        ])
        
        response_time = base_time * complexity_factor / (average_strength + 0.1)
        
        return response_time
    
    def calculate_circuit_robustness(self, circuit):
        robustness_score = 1.0
        
        component_count = len(circuit['components'])
        if component_count > config.MAX_CIRCUIT_COMPONENTS:
            robustness_score *= 0.8
        
        connection_count = len(circuit['connections'])
        if connection_count < component_count - 1:
            robustness_score *= 0.9
        
        promoter_strengths = [
            c['properties']['strength'] 
            for c in circuit['components'] 
            if c['type'] == 'promoters'
        ]
        
        if promoter_strengths:
            strength_variance = np.var(promoter_strengths)
            if strength_variance > 0.1:
                robustness_score *= 0.85
        
        return robustness_score
    
    def optimize_circuit(self, initial_circuit, target_metrics, max_iterations=50):
        current_circuit = initial_circuit
        current_metrics = self.calculate_circuit_performance(current_circuit)
        current_fitness = self.calculate_circuit_fitness(current_metrics, target_metrics)
        
        for iteration in range(max_iterations):
            candidate_circuit = self.mutate_circuit(current_circuit)
            candidate_metrics = self.calculate_circuit_performance(candidate_circuit)
            candidate_fitness = self.calculate_circuit_fitness(candidate_metrics, target_metrics)
            
            if candidate_fitness > current_fitness:
                current_circuit = candidate_circuit
                current_metrics = candidate_metrics
                current_fitness = candidate_fitness
        
        return current_circuit, current_metrics, current_fitness
    
    def mutate_circuit(self, circuit):
        import copy
        mutated_circuit = copy.deepcopy(circuit)
        
        mutation_type = np.random.choice(['add', 'remove', 'modify'])
        
        if mutation_type == 'add' and len(mutated_circuit['components']) < config.MAX_CIRCUIT_COMPONENTS:
            new_component_type = np.random.choice(list(self.genetic_parts.keys()))
            new_component = self.select_genetic_part({
                'type': new_component_type,
                'requirements': {}
            })
            mutated_circuit['components'].append(new_component)
        
        elif mutation_type == 'remove' and len(mutated_circuit['components']) > 1:
            remove_index = np.random.randint(len(mutated_circuit['components']))
            mutated_circuit['components'].pop(remove_index)
        
        elif mutation_type == 'modify':
            modify_index = np.random.randint(len(mutated_circuit['components']))
            component = mutated_circuit['components'][modify_index]
            new_component = self.select_genetic_part({
                'type': component['type'],
                'requirements': {}
            })
            mutated_circuit['components'][modify_index] = new_component
        
        mutated_circuit['connections'] = self.define_circuit_topology(mutated_circuit['components'])
        
        return mutated_circuit
    
    def calculate_circuit_fitness(self, actual_metrics, target_metrics):
        fitness = 0.0
        
        for metric, target_value in target_metrics.items():
            if metric in actual_metrics:
                actual_value = actual_metrics[metric]
                
                if metric == 'response_time':
                    fitness += 1.0 / (1.0 + abs(actual_value - target_value))
                else:
                    fitness += 1.0 - min(abs(actual_value - target_value), 1.0)
        
        return fitness / len(target_metrics)

circuit_designer = CircuitDesigner()