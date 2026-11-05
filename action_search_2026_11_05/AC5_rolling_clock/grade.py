"""AC5 grade: apply FROZEN_CRITERIA.md (63b0c9ca2c) lines to main, M1 and M2 outputs. Run from the repository root.
Kappa = 1/2 FITTED; not theory closed."""
import json, sys
from pathlib import Path
D = Path('action_search_2026_11_05/AC5_rolling_clock')
load = lambda m: json.loads((D / 'evidence' / m / 'result.json').read_text())
main, m1, m2 = load('main'), load('m1_drop_kdot'), load('m2_flipped')
key = lambda r: (r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k'])

power = {key(r): r['R'] for r in m2['rows']}
power_met = any(R >= 1e3 for R in power.values())
eps_with_power = sorted({k[0] for k, R in power.items() if R >= 1e3})
m1_bites = any(r['omega_drift_max'] > 1e-6 for r in m1['rows'])

rows = main['rows']
all_conv = all(r['converged'] for r in rows)
omega_ok = all(r['omega_drift_max'] <= 1e-6 for r in rows)
ints_ok = all(r['all_integrations_ok'] for r in rows)
fail = any(r['R'] >= 1e3 and r['converged'] for r in rows)
maxR = max(r['R'] for r in rows)
if fail:
    label = 'FAIL'
elif not power_met:
    label = 'NO VERDICT (no power: M2 never reached R >= 1e3)'
elif not (all_conv and omega_ok and ints_ok):
    label = 'NO VERDICT (numerics)'
elif maxR <= 10:
    label = 'PASS'
else:
    label = 'UNDECIDED'
out = dict(label=label, max_R_main=maxR, witness_max_R_main=max(r['R'] for r in rows if r['witness']),
           all_converged=all_conv, nonconverged=[key(r) for r in rows if not r['converged']],
           omega_line_met=omega_ok, integrations_ok=ints_ok,
           power_gate_met=power_met, eps_phi_with_power=eps_with_power,
           m2_R_by_witness={','.join(k): R for k, R in power.items()},
           m1_bites=m1_bites, m1_max_drift=max(r['omega_drift_max'] for r in m1['rows']),
           eps_end_main_witnesses={','.join(key(r)): r['rtol_1e-11']['candidate']['eps_end'] for r in rows if r['witness']},
           note='kappa = 1/2 FITTED; not theory closed')
(D / 'evidence' / 'GRADE.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
