import os
import json
import numpy as np
import runpy

def simulate_photon_path_radial(A, epsilon, seed, max_events=10000):
    """Simulate a single photon path in unit sphere with radial opacity kappa(r)=A/(epsilon^2+r^2)."""
    rng = np.random.default_rng(seed)
    
    # Initial state: s=0, z=0, t=0
    s = 0.0
    z = 0.0
    t = 0.0
    
    for _ in range(max_events):
        # Free flight: compute exit distance
        arg = z*z + 1.0 - s
        if arg < 0:
            arg = 0.0   # Clamp for roundoff
        l_exit = -z + np.sqrt(arg)
        
        # Draw optical depth E ~ Exp(1)
        E = rng.exponential(1.0)
        
        # Optical depth along flight: tau(l) = A/b * [atan((z+l)/b) - atan(z/b)]
        b = np.sqrt(epsilon*epsilon + s - z*z)
        
        # Check if E is larger than optical depth to exit
        tau_exit = A / b * (np.arctan((z + l_exit) / b) - np.arctan(z / b)) if b > 0 else np.inf
        
        if E >= tau_exit:
            # Escape
            t_new = t + l_exit
            z_new = z + l_exit
            T = t_new
            Z = z_new
            D = T - Z
            return D, Z, T
        else:
            # Invert for l: E = A/b * [atan((z+l)/b) - atan(z/b)]
            # atan((z+l)/b) = atan(z/b) + b*E/A
            # (z+l)/b = tan(atan(z/b) + b*E/A)
            # l = b*tan(atan(z/b) + b*E/A) - z
            angle = np.arctan(z / b) + b * E / A
            l = b * np.tan(angle) - z
            
            # Assert 0 <= l < l_exit up to roundoff
            if l < 0 or l >= l_exit:
                # Allow small roundoff clamps
                if l < 0 and l > -1e-10:
                    l = 0.0
                elif l >= l_exit and l < l_exit + 1e-10:
                    l = l_exit - 1e-10
                else:
                    raise Exception(f"Geometry violation: l={l}, l_exit={l_exit}")
            
            t_new = t + l
            z_new = z + l
            s_new = s + 2*z*l + l*l
            
            # Thomson scattering: mu in [-1,1] with density (1+mu^2)/2
            while True:
                mu = rng.uniform(-1, 1)
                if rng.uniform() < (1 + mu*mu)/2:
                    break
            
            phi = rng.uniform(0, 2*np.pi)
            
            # New z after scattering
            perp_arg = s_new - z_new*z_new
            if perp_arg < 0:
                perp_arg = 0.0   # Clamp for roundoff
            perp = np.sqrt(perp_arg)
            z = z_new*mu + perp*np.sqrt(1-mu*mu)*np.cos(phi)
            s = s_new
            t = t_new
    
    raise Exception("Path did not complete")

def simulate_photon_path_uniform(k, seed, max_events=10000):
    """Simulate a single photon path in unit sphere with uniform opacity k."""
    rng = np.random.default_rng(seed)
    
    # Initial state: s=0, z=0, t=0
    s = 0.0
    z = 0.0
    t = 0.0
    
    for _ in range(max_events):
        # Free flight: compute exit distance
        arg = z*z + 1.0 - s
        if arg < 0:
            arg = 0.0   # Clamp for roundoff
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
            while True:
                mu = rng.uniform(-1, 1)
                if rng.uniform() < (1 + mu*mu)/2:
                    break
            
            phi = rng.uniform(0, 2*np.pi)
            
            # New z after scattering
            perp_arg = s_new - z_new*z_new
            if perp_arg < 0:
                perp_arg = 0.0   # Clamp for roundoff
            perp = np.sqrt(perp_arg)
            z = z_new*mu + perp*np.sqrt(1-mu*mu)*np.cos(phi)
            s = s_new
            t = t_new
    
    raise Exception("Path did not complete")

def main():
    mode = os.environ.get('ORCH_MODE', 'main')
    
    # Load inputs
    inputs = json.load(open(os.environ['ORCH_INPUTS']))
    
    # Set parameters
    d = 4.0
    epsilon = 0.125
    A = 2 * d / np.log((1 + epsilon*epsilon) / (epsilon*epsilon))
    k_uniform = 8.0
    
    # Seed ranges
    if mode == 'main':
        seed_start = 9500000
        n_paths = 8000
    elif mode == 'positive':
        seed_start = 9600000
        n_paths = 8000
    elif mode == 'negative':
        seed_start = 9700000
        n_paths = 8000
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    D_values = []
    Z_values = []
    T_values = []
    
    for i in range(n_paths):
        path_seed = seed_start + i
        
        if mode == 'negative':
            D, Z, T = simulate_photon_path_uniform(k_uniform, path_seed)
        else:
            D, Z, T = simulate_photon_path_radial(A, epsilon, path_seed)
        
        D_values.append(D)
        Z_values.append(Z)
        T_values.append(T)
    
    D_arr = np.array(D_values)
    Z_arr = np.array(Z_values)
    T_arr = np.array(T_values)
    
    # Compute B = D^2 - (7/5)*d^2
    B = D_arr**2 - (7/5)*d*d
    
    # Statistics
    mean_D = np.mean(D_arr)
    std_D = np.std(D_arr, ddof=1)
    se_D = std_D / np.sqrt(n_paths)
    
    mean_B = np.mean(B)
    std_B = np.std(B, ddof=1)
    se_B = std_B / np.sqrt(n_paths)
    
    # Counterexample predicate
    counterexample = bool((mean_B < -6 * se_B) and (abs(mean_D - d) <= 6 * se_D))
    
    # Additional measurements
    var_D = np.var(D_arr, ddof=1)
    cv2 = var_D / (d*d)
    mean_B_over_se_B = mean_B / se_B if se_B > 0 else 0.0
    
    # Unscattered fraction
    tau_rad = A / epsilon * np.arctan(1 / epsilon) if mode != 'negative' else k_uniform
    unscattered_frac = np.exp(-tau_rad)
    
    checks = {
        'counterexample': counterexample
    }
    
    measurements = {
        'mode': mode,
        'seed_start': seed_start,
        'n_paths': n_paths,
        'mean_D': float(mean_D),
        'std_D': float(std_D),
        'se_D': float(se_D),
        'mean_B': float(mean_B),
        'std_B': float(std_B),
        'se_B': float(se_B),
        'var_D': float(var_D),
        'cv2': float(cv2),
        'mean_B_over_se_B': float(mean_B_over_se_B),
        'tau_rad': float(tau_rad),
        'unscattered_frac': float(unscattered_frac),
        'A': float(A),
        'epsilon': float(epsilon),
        'd': float(d)
    }
    
    print(json.dumps({
        'protocol': 2,
        'complete': True,
        'checks': checks,
        'measurements': measurements
    }))

if __name__ == '__main__':
    main()