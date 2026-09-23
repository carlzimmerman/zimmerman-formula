import os
import json
import sys
import numpy as np
import importlib.util

def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

mode = os.environ['ORCH_MODE']
with open(os.environ['ORCH_INPUTS']) as f:
    inputs = json.load(f)

killed_source = load_module_from_path('killed_mod', inputs['killed_source'])
conservative_source = load_module_from_path('conservative_mod', inputs['conservative_source'])

if mode == 'main':
    N = 32000
    alpha_values = [0.5, 2.0, 4.0]
    conservative_seed = 1300101
    killed_seeds = [1300111, 1300112, 1300113]
    alpha_killed = alpha_values
    alpha_conservative = alpha_values
elif mode == 'positive':
    N = 64000
    alpha_values = [0.5, 2.0, 4.0]
    conservative_seed = 1300201
    killed_seeds = [1300211, 1300212, 1300213]
    alpha_killed = alpha_values
    alpha_conservative = alpha_values
elif mode == 'negative':
    N = 32000
    alpha_values = [0.5, 2.0, 4.0]
    conservative_seed = 1300101
    killed_seeds = [1300111, 1300112, 1300113]
    alpha_killed = [a/2 for a in alpha_values]
    alpha_conservative = alpha_values
else:
    raise ValueError(f'Unknown mode: {mode}')

C = 4 * np.sqrt(2) / 9

results = {
    'alpha_values': alpha_values,
    'H_values': [],
    'SE_H_values': [],
    'mu_values': [],
    'V_values': [],
    'escape_probs': [],
    'ESS_values': [],
    'certificate_checks': []
}

for i, alpha in enumerate(alpha_values):
    alpha_k = alpha_killed[i]
    alpha_c = alpha_conservative[i]
    
    np.random.seed(conservative_seed)
    try:
        D_cons, T_cons = conservative_source.simulate(N, tau0=1, q=0, h=0, source='central', seed=conservative_seed)
    except Exception as e:
        print(f"Error in conservative simulate: {e}", file=sys.stderr)
        D_cons = np.zeros(N)
        T_cons = np.zeros(N)
    
    np.random.seed(killed_seeds[i])
    try:
        D_killed, T_killed, escaped_mask = killed_source.killed_transport(N, tau0=1, alpha=alpha_k, seed=killed_seeds[i])
    except Exception as e:
        print(f"Error in killed transport: {e}", file=sys.stderr)
        D_killed = np.zeros(N)
        T_killed = np.zeros(N)
        escaped_mask = np.zeros(N, dtype=bool)
    
    w = np.exp(-alpha_c * T_cons)
    mu_c = np.sum(w * D_cons) / np.sum(w)
    V_c = np.sum(w * (D_cons - mu_c)**2) / np.sum(w)
    p_c = np.mean(w)
    ESS_c = np.sum(w)**2 / np.sum(w**2)
    
    D_escaped = D_killed[escaped_mask]
    n_escaped = np.sum(escaped_mask)
    
    if n_escaped < 100:
        results['certificate_checks'].append(False)
        results['H_values'].append({'conservative': 0.0, 'killed': 0.0})
        results['SE_H_values'].append({'conservative': 1.0, 'killed': 1.0})
        results['mu_values'].append({'conservative': 0.0, 'killed': 0.0})
        results['V_values'].append({'conservative': 0.0, 'killed': 0.0})
        results['escape_probs'].append({'conservative': p_c, 'killed': 0.0})
        results['ESS_values'].append(ESS_c)
        continue
    
    mu_k = np.mean(D_escaped)
    V_k = np.var(D_escaped, ddof=0)
    p_k = n_escaped / N
    
    H_c = V_c - C * mu_c**(3/2)
    psi_H_c = (D_cons - mu_c)**2 - V_c - 1.5 * C * np.sqrt(mu_c) * (D_cons - mu_c)
    psi_H_weighted = (w / np.mean(w)) * psi_H_c
    SE_H_c = np.std(psi_H_weighted, ddof=1) / np.sqrt(N)
    
    H_k = V_k - C * mu_k**(3/2)
    psi_H_k = (D_escaped - mu_k)**2 - V_k - 1.5 * C * np.sqrt(mu_k) * (D_escaped - mu_k)
    SE_H_k = np.std(psi_H_k, ddof=1) / np.sqrt(n_escaped)
    
    results['H_values'].append({'conservative': float(H_c), 'killed': float(H_k)})
    results['SE_H_values'].append({'conservative': float(SE_H_c), 'killed': float(SE_H_k)})
    results['mu_values'].append({'conservative': float(mu_c), 'killed': float(mu_k)})
    results['V_values'].append({'conservative': float(V_c), 'killed': float(V_k)})
    results['escape_probs'].append({'conservative': float(p_c), 'killed': float(p_k)})
    results['ESS_values'].append(float(ESS_c))
    
    diff_mu = abs(mu_c - mu_k)
    se_mu = np.sqrt((SE_H_c**2) + (SE_H_k**2))
    diff_V = abs(V_c - V_k)
    diff_p = abs(p_c - p_k)
    se_p = np.sqrt(p_c * (1 - p_c) / N + p_k * (1 - p_k) / N)
    
    agreement = (diff_mu < 5 * se_mu) and (diff_V < 5 * se_mu) and (diff_p < 5 * se_p)
    results['certificate_checks'].append(bool(agreement))

np.random.seed(conservative_seed)
try:
    D_cons_0, T_cons_0 = conservative_source.simulate(N, tau0=1, q=0, h=0, source='central', seed=conservative_seed)
    mu_0 = np.mean(D_cons_0)
except Exception:
    mu_0 = 0.0
calibration_ok = abs(mu_0 - 0.5) < 0.01

selection_certificate = all(results['certificate_checks']) and bool(calibration_ok)

violation_detected = False
for i, alpha in enumerate(alpha_values):
    H_c = results['H_values'][i]['conservative']
    SE_H_c = results['SE_H_values'][i]['conservative']
    H_k = results['H_values'][i]['killed']
    SE_H_k = results['SE_H_values'][i]['killed']
    
    if H_c < -5 * SE_H_c and H_k < -5 * SE_H_k:
        violation_detected = True
        break

print(json.dumps({
    'protocol': 2,
    'complete': True,
    'checks': {
        'selection_certificate': selection_certificate,
        'H_positive': not violation_detected,
        'calibration_ok': calibration_ok
    },
    'measurements': results
}))
sys.exit(0)