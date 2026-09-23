import os
import json
import numpy as np

def simulate_photon_path(k, seed, max_events=10000):
    """Simulate a single photon path in unit sphere with Thomson scattering."""
    rng = np.random.default_rng(seed)
    
    # Initial state: s=0, z=0, t=0
    s = 0.0
    z = 0.0
    t = 0.0
    
    for _ in range(max_events):
        # Free flight: compute exit distance
        # l_exit = -z + sqrt(z^2 + 1 - s)
        arg = z*z + 1.0 - s
        if arg < 0:
            arg = 0.0  # Clamp for roundoff
        l_exit = -z + np.sqrt(arg)
        
        # Draw scatter length
        l_scatter = rng.exponential(1.0/k)
        
        if l_scatter >= l_exit:
            # Escape
            t_new = t + l_exit
            z_new = z + l_exit
            T = t_new
            Z = z_new
            D = T - Z
            return D, Z, T
        else:
            # Collision
            t_new = t + l_scatter
            z_new = z + l_scatter
            s_new = s + 2*z*l_scatter + l_scatter*l_scatter
            
            # Thomson scattering: mu in [-1,1] with density (1+mu^2)/2
            # Rejection sampling
            while True:
                mu = rng.uniform(-1, 1)
                if rng.uniform() < (1 + mu*mu)/2:
                    break
            
            phi = rng.uniform(0, 2*np.pi)
            
            # New z after scattering
            # z_out = z_new*mu + sqrt(s_new - z_new^2)*sqrt(1-mu^2)*cos(phi)
            perp_arg = s_new - z_new*z_new
            if perp_arg < 0:
                perp_arg = 0.0  # Clamp for roundoff
            perp = np.sqrt(perp_arg)
            z = z_new*mu + perp*np.sqrt(1-mu*mu)*np.cos(phi)
            s = s_new
            t = t_new
    
    # Should not reach here with max_events=10000
    raise Exception("Path did not complete")

def main():
    mode = os.environ.get('ORCH_MODE', 'main')
    
    if mode == 'main':
        seed = 9225200
        k_values = [1.0, 2.0]
        n_paths = 10000
    elif mode == 'positive':
        seed = 9225300
        k_values = [1.0, 2.0]
        n_paths = 10000
    elif mode == 'negative':
        seed = 9225200
        k_values = [1.0, 2.0]
        n_paths = 10000
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    all_results = []
    
    for k in k_values:
        D_values = []
        Z_values = []
        T_values = []
        
        for i in range(n_paths):
            path_seed = seed + i
            D, Z, T = simulate_photon_path(k, path_seed)
            D_values.append(D)
            Z_values.append(Z)
            T_values.append(T)
        
        D_arr = np.array(D_values)
        Z_arr = np.array(Z_values)
        T_arr = np.array(T_values)
        
        # For negative control, substitute T for D
        if mode == 'negative':
            D_for_check = T_arr
        else:
            D_for_check = D_arr
        
        # Compute Y = D^2 + Z^2/3 - 2*k*Z/5
        Y = D_for_check**2 + Z_arr**2/3 - 2*k*Z_arr/5
        
        # Expected value
        expected = 7*k*k/20 + 1/3
        
        # Statistics
        mean_Y = np.mean(Y)
        std_Y = np.std(Y, ddof=1)
        se_Y = std_Y / np.sqrt(n_paths)
        z_score = abs(mean_Y - expected) / se_Y if se_Y > 0 else 0.0
        
        # Check: |mean(Y) - expected| <= 6*SE
        clock_identity = bool(abs(mean_Y - expected) <= 6*se_Y)
        
        # Additional measurements
        mean_D = np.mean(D_arr)
        mean_Z = np.mean(Z_arr)
        mean_T = np.mean(T_arr)
        
        all_results.append({
            'k': k,
            'n_paths': n_paths,
            'mean_Y': float(mean_Y),
            'expected_Y': float(expected),
            'se_Y': float(se_Y),
            'z_score': float(z_score),
            'clock_identity': clock_identity,
            'mean_D': float(mean_D),
            'mean_Z': float(mean_Z),
            'mean_T': float(mean_T)
        })
    
    # Combine results
    all_clock_identities = [r['clock_identity'] for r in all_results]
    clock_identity = all(all_clock_identities)
    
    checks = {
        'clock_identity': clock_identity
    }
    
    measurements = {
        'mode': mode,
        'seed': seed,
        'results': all_results
    }
    
    print(json.dumps({
        'protocol': 2,
        'complete': True,
        'checks': checks,
        'measurements': measurements
    }))

if __name__ == '__main__':
    main()