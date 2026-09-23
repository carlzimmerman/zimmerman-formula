import os
import json
import runpy
import numpy as np

def main():
    mode = os.environ["ORCH_MODE"]
    inputs = json.load(open(os.environ["ORCH_INPUTS"]))
    
    # Load the audited transport functions
    path = inputs["audited_absorption"]
    ns = runpy.run_path(path)
    killed_transport = ns["killed_transport"]
    conservative_transport = ns["conservative_transport"]
    
    tau0 = 1.0
    alphas = [0.1, 0.5]
    
    # Fixed seeds and N as per task specification
    if mode == "main":
        N = 16000
        seeds = {
            0.1: {"killed": 1200101, "conservative": 1200102},
            0.5: {"killed": 1200111, "conservative": 1200112}
        }
    elif mode == "positive":
        N = 32000
        seeds = {
            0.1: {"killed": 1200201, "conservative": 1200202},
            0.5: {"killed": 1200211, "conservative": 1200212}
        }
    elif mode == "negative":
        N = 16000
        seeds = {
            0.1: {"killed": 1200101, "conservative": 1200102},
            0.5: {"killed": 1200111, "conservative": 1200112}
        }
    else:
        raise ValueError(f"Unknown mode: {mode}")

    results = {}
    checks = {}
    
    for alpha in alphas:
        # Negative control: halve alpha in killed transport only
        killed_alpha = alpha / 2.0 if mode == "negative" else alpha
        
        # Run transports
        D_killed, n_escape = killed_transport(N, tau0, killed_alpha, seed=seeds[alpha]["killed"])
        mu_cons, se_cons, w = conservative_transport(N, tau0, alpha, seed=seeds[alpha]["conservative"])
        
        # Calculate statistics for killed transport
        if len(D_killed) == 0:
            raise RuntimeError("No photons escaped in killed transport")
            
        mu_killed = float(np.mean(D_killed))
        se_killed = float(np.std(D_killed, ddof=1) / np.sqrt(n_escape))
        
        # Combined SE for mean comparison
        combined_se = float(np.sqrt(se_killed**2 + se_cons**2))
        diff_mean = float(mu_killed - mu_cons)
        z_mean = float(diff_mean / combined_se) if combined_se > 0 else float('inf')
        
        # Escape fraction comparison
        p_escape = float(n_escape / N)
        p_expected = float(np.mean(w))
        
        # SE for escape fraction
        # Var(p) approx p(1-p)/N + Var(w)/N (approximation for weighted sum)
        var_w = float(np.var(w, ddof=1))
        se_p = float(np.sqrt(p_escape * (1 - p_escape) / N + var_w / N))
        diff_p = float(p_escape - p_expected)
        z_p = float(diff_p / se_p) if se_p > 0 else float('inf')
        
        # Effective Sample Size (ESS)
        ess = float(np.sum(w)**2 / np.sum(w**2))
        
        results[str(alpha)] = {
            "mu_killed": mu_killed,
            "se_killed": se_killed,
            "mu_cons": mu_cons,
            "se_cons": se_cons,
            "combined_se": combined_se,
            "z_mean": z_mean,
            "p_escape": p_escape,
            "p_expected": p_expected,
            "z_p": z_p,
            "ess": ess,
            "n_escape": n_escape
        }
        
        # Check: agreement within 5 SE for both mean and escape
        # Finite and non-negative D check
        finite_check = bool(np.all(np.isfinite(D_killed)) and np.all(D_killed >= -1e-12))
        
        mean_agreement = bool(abs(z_mean) < 5.0)
        escape_agreement = bool(abs(z_p) < 5.0)
        
        checks[f"agreement_alpha_{alpha}"] = bool(finite_check and mean_agreement and escape_agreement)

    # Output
    output = {
        "protocol": 2,
        "complete": True,
        "checks": checks,
        "measurements": results
    }
    print(json.dumps(output))

if __name__ == "__main__":
    main()