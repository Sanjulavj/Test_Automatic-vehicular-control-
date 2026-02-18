


import numpy as np
from pathlib import Path


class SocialCompatibilityEvaluator:

    def __init__(self, config):
        self.config = config
        self.results = {}
        self.expert_data = None
    
    def load_expert_data(self, expert_path='expert_demonstrations.npz'):
        """Load human driving demonstrations for comparison"""
        print(f"Loading expert data from: {expert_path}")
        data = np.load(expert_path, allow_pickle=True)
        self.expert_data = {
            'observations': data['observations'],
            'actions': data['actions']
        }
        print(f"  Loaded {len(self.expert_data['actions'])} expert samples\n")




def main():
    """Run social compatibility evaluation"""
    import sys
    
    # Get results directory from command line
    if len(sys.argv) > 1:
        results_path = Path(sys.argv[1])
    else:
        results_path = Path('results/gail_test')
        print("⚠️  No results path provided, using default: results/gail_test")
        print("   Usage: python evaluate_social_compatibility.py <results_directory>")
    
    print(f"\n🔍 Evaluating models in: {results_path}\n")
    
    # Base configuration
    base_config = {
        'obs_tail': True,
        'obs_next_cross_platoons': 1,
        'directions': '4way',
        'multi_flowrate': False,
        'enter_length': False,
        'short_exit': False,
        'av_frac': 0.15,
        'depart_speed': 0,
        'max_speed': 13,
        'max_dist': 100,
        'max_accel': 1.5,
        'max_decel': 3.5,
        'sim_step': 0.5,
        'generic_type': True,
        'n_actions': 3,
        'handcraft': False,
        'handcraft_tl': None,
        'flow_rate': 700,
        'length': 100,
        'n_rows': 1,
        'n_cols': 1,
        'speed_mode': 1,
        'act_type': 'accel_discrete',
        'low': -1,
        'alg': 'PG',
        'gamma': 0.99,
        'collision_coef': 5,
        'rew_type': 'outflow',
        'res': str(results_path),
    }
    
    # Create evaluator
    evaluator = SocialCompatibilityEvaluator(base_config)
    
    # Load expert data for comparison
    evaluator.load_expert_data('expert_demonstrations.npz')
    
    # Find models in the specified directory
    results_dir = results_path / 'models'
    if results_dir.exists():
        # Sort models by step number
        models = sorted(
            results_dir.glob('model-*.pth'),
            key=lambda x: int(x.stem.split('-')[1])
        )
        
        if len(models) > 0:
            print(f"✅ Found {len(models)} models")
            print(f"   First model:  {models[0].name} (step {models[0].stem.split('-')[1]})")
            print(f"   Latest model: {models[-1].name} (step {models[-1].stem.split('-')[1]})")
            print()
            
            # Evaluate first (base/untrained) model
            base_model = str(models[0])
            evaluator.evaluate_model(base_model, 'Base_RL', n_episodes=5)
            
            # Evaluate latest (trained) model
            gail_model = str(models[-1])
            evaluator.evaluate_model(gail_model, 'GAIL_Trained', n_episodes=5)
            
            # Generate comparison
            evaluator.compare_models()
            
            print("\n" + "="*80)
            print("✅ EVALUATION COMPLETE!")
            print("="*80)
            print("\n📁 Generated files:")
            print("   📊 results/social_compatibility_comparison.csv")
            print("   📈 results/eval_Base_RL_trajectories.npz")
            print("   📈 results/eval_Base_RL_stats.csv")
            print("   📈 results/eval_GAIL_Trained_trajectories.npz")
            print("   📈 results/eval_GAIL_Trained_stats.csv")
            print()
        else:
            print(f"❌ No model files found in: {results_dir}")
            print("   Expected files like: model-0.pth, model-10.pth, etc.")
    else:
        print(f"❌ Models directory not found: {results_dir}")
        print(f"   Make sure training was completed in: {results_path}")




if __name__ == '__main__':
    main()




