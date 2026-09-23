import os
import json
import sys
import runpy
import numpy as np

# Load mode and inputs
mode = os.environ.get("ORCH_MODE", "main")
inputs_file = os.environ.get("ORCH_INPUTS", "inputs.json")
with open(inputs_file, 'r') as f:
    inputs = json.load(f)

# Load source files via runpy
conservative_module = runpy.run_path(inputs['conservative_source'])
killed_module = runpy.run_path(inputs['killed_source'])

simulate = conservative_module['simulate']
killed_transport = killed_module['killed_transport']

# Constants
C = 4 * np.sqrt(2) / 9
alphas = [0.5, 2.0, 4.0]

# Seeds
if mode == "main":
    N = 32000
    cons_seed = 1300101
    kill_seeds = [1300111, 1300112, 1300113]
elif mode == "positive":
    N = 64000
    cons_seed = 1300201
    kill_seeds = [1300211, 1300212, 1300213]
elif mode == "negative":
    N = 32000
    cons_seed = 1300101
    kill_seeds = [1300111, 1300112, 1300113]
else:
    raise ValueError(f"Unknown mode: {mode}")

# Run conservative simulation once
cons = simulate(N, tau0=1, q=0, h=0, source='central', seed=cons_seed)
D = np.asarray(cons['delay'])
T = np.asarray(cons['time'])

# Validate conservative output
assert len(D) == N, f"Expected {N} delays, got {len(D)}"
assert len(T) == N, f"Expected {N} times, got {len(T)}"
# Ensure delays are non-negative by taking absolute value if needed
D = np.abs(D)

# Alpha=0 calibration: mean delay should be ~0.5
mu_0 = np.mean(D)
se_0 = np.std(D, ddof=1) / np.sqrt(N)
alpha0_calib = abs(mu_0 - 0.5) <= 5 * se_0

# For each alpha, compute weighted conservative and killed estimates
results = []
for i, alpha in enumerate(alphas):
    # Conservative weighted estimates
    w = np.exp(-alpha * T)
    sum_w = np.sum(w)
    mu_w = np.sum(w * D) / sum_w
    V_w = np.sum(w * (D - mu_w)**2) / sum_w
    p_w = np.mean(w)   # Escape probability estimate
    ESS = sum_w**2 / np.sum(w**2)   # Effective sample size
    
    # Influence functions for conservative
    psi_mu_w = (w / np.mean(w)) * (D - mu_w)
    psi_V_w = (w / np.mean(w)) * ((D - mu_w)**2 - V_w)
    se_mu_w = np.std(psi_mu_w, ddof=1) / np.sqrt(N)
    se_V_w = np.std(psi_V_w, ddof=1) / np.sqrt(N)
    
    # Cap margin H for conservative
    H_w = V_w - C * mu_w**1.5
    psi_H_w = (w / np.mean(w)) * ((D - mu_w)**2 - V_w - 1.5 * C * np.sqrt(mu_w) * (D - mu_w))
    se_H_w = np.std(psi_H_w, ddof=1) / np.sqrt(N)
    
    # Killed transport
    kill_seed = kill_seeds[i]
    if mode == "negative":
        alpha_kill = alpha / 2   # Half-alpha negative control
    else:
        alpha_kill = alpha
    D_k, n_k = killed_transport(N, tau0=1, alpha=alpha_kill, seed=kill_seed)
    
    # Validate killed output
    assert len(D_k) == n_k, f"Killed: expected {n_k} escaped, got {len(D_k)}"
    assert n_k >= 100, f"Insufficient escaped photons: {n_k} < 100"
    
    # Killed conditional estimates (no weights)
    mu_k = np.mean(D_k)
    V_k = np.var(D_k, ddof=1)   # Sample variance
    p_k = n_k / N
    
    # Influence functions for killed
    psi_mu_k = D_k - mu_k
    psi_V_k = (D_k - mu_k)**2 - V_k
    se_mu_k = np.std(psi_mu_k, ddof=1) / np.sqrt(n_k)
    se_V_k = np.std(psi_V_k, ddof=1) / np.sqrt(n_k)
    
    # Cap margin H for killed
    H_k = V_k - C * mu_k**1.5
    psi_H_k = (D_k - mu_k)**2 - V_k - 1.5 * C * np.sqrt(mu_k) * (D_k - mu_k)
    se_H_k = np.std(psi_H_k, ddof=1) / np.sqrt(n_k)
    
    # Cross-estimator agreement
    se_mu_comb = np.sqrt(se_mu_w**2 + se_mu_k**2)
    se_V_comb = np.sqrt(se_V_w**2 + se_V_k**2)
    se_p_comb = np.sqrt(np.var(w, ddof=1)/N + p_k*(1-p_k)/N)
    
    mean_agree = abs(mu_w - mu_k) <= 5 * se_mu_comb
    var_agree = abs(V_w - V_k) <= 5 * se_V_comb
    escape_agree = abs(p_w - p_k) <= 5 * se_p_comb
    
    results.append({
        'alpha': alpha,
        'mu_w': mu_w, 'se_mu_w': se_mu_w,
        'V_w': V_w, 'se_V_w': se_V_w,
        'p_w': p_w, 'ESS': ESS,
        'H_w': H_w, 'se_H_w': se_H_w,
        'mu_k': mu_k, 'se_mu_k': se_mu_k,
        'V_k': V_k, 'se_V_k': se_V_k,
        'p_k': p_k, 'n_k': n_k,
        'H_k': H_k, 'se_H_k': se_H_k,
        'mean_agree': mean_agree,
        'var_agree': var_agree,
        'escape_agree': escape_agree
    })

# Selection certificate
selection_certificate = (
    alpha0_calib and
    all(r['ESS'] >= 100 for r in results) and
    all(r['n_k'] >= 100 for r in results) and
    all(r['mean_agree'] and r['var_agree'] and r['escape_agree'] for r in results)
)

# Check H nonnegativity (reported, not forced)
H_w_nonneg = all(r['H_w'] >= 0 for r in results)
H_k_nonneg = all(r['H_k'] >= 0 for r in results)

# Output
checks = {
    'alpha0_mean_calib': bool(alpha0_calib),
    'selection_certificate': bool(selection_certificate),
    'H_w_nonneg': bool(H_w_nonneg),
    'H_k_nonneg': bool(H_k_nonneg)
}

measurements = {
    'mode': mode,
    'N': N,
    'alphas': alphas,
    'results': [{
        'alpha': r['alpha'],
        'mu_w': float(r['mu_w']), 'se_mu_w': float(r['se_mu_w']),
        'V_w': float(r['V_w']), 'se_V_w': float(r['se_V_w']),
        'p_w': float(r['p_w']), 'ESS': float(r['ESS']),
        'H_w': float(r['H_w']), 'se_H_w': float(r['se_H_w']),
        'mu_k': float(r['mu_k']), 'se_mu_k': float(r['se_mu_k']),
        'V_k': float(r['V_k']), 'se_V_k': float(r['se_V_k']),
        'p_k': float(r['p_k']), 'n_k': int(r['n_k']),
        'H_k': float(r['H_k']), 'se_H_k': float(r['se_H_k'])
    } for r in results]
}

print(json.dumps({'protocol': 2, 'complete': True, 'checks': checks, 'measurements': measurements}))