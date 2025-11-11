import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.metabolic_engine import MetabolicEngine

def test_metabolic_engineering():
    engine = MetabolicEngine()
    
    print("Testing metabolic pathway design:")
    
    pathway = engine.design_metabolic_pathway('glucose', 'biofuel')
    
    print(f"Pathway from glucose to biofuel:")
    print(f"  Steps: {len(pathway['steps'])}")
    print(f"  Efficiency: {pathway['efficiency']:.3f}")
    print(f"  Enzymes required: {pathway['enzymes']}")
    
    optimized_pathway = engine.optimize_pathway_efficiency(pathway, target_efficiency=0.9)
    print(f"Optimized efficiency: {optimized_pathway['efficiency']:.3f}")
    
    flux = engine.calculate_pathway_flux(optimized_pathway, substrate_concentration=1.0)
    print(f"Pathway flux: {flux:.3f}")
    
    print("Metabolic engineering test completed successfully")

if __name__ == "__main__":
    test_metabolic_engineering()