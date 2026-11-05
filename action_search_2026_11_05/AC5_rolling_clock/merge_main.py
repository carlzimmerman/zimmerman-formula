"""Merge per-case streaming outputs (evidence/main_parts/*.json) into evidence/main/result.json, same summary as evolve.py."""
import json, glob, os
D = 'action_search_2026_11_05/AC5_rolling_clock/evidence'
rows = []
for f in sorted(glob.glob(f'{D}/main_parts/*.json')):
    rows += json.load(open(f))['rows']
Rs = [r['R'] for r in rows]
summ = dict(mode='main', n_cases=len(rows), max_R=max(Rs), witness_max_R=max(r['R'] for r in rows if r['witness']),
            all_converged=all(r['converged'] for r in rows), all_integrations_ok=all(r['all_integrations_ok'] for r in rows),
            omega_drift_max=max(r['omega_drift_max'] for r in rows), omega_line_met=all(r['omega_drift_max'] <= 1e-6 for r in rows),
            note='kappa = 1/2 FITTED; not theory closed; merged from streaming per-case runs')
os.makedirs(f'{D}/main', exist_ok=True)
json.dump(dict(summary=summ, rows=rows), open(f'{D}/main/result.json', 'w'), indent=1)
print(json.dumps(summ, indent=1))
