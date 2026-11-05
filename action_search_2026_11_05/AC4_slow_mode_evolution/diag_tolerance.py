"""AC4 diagnostic (not graded): tolerance ladder on the one witness that missed the frozen 1e-4 R line.
Does not change the frozen label. Run from the repository root."""
import sys, json
sys.argv = ['evolve.py', '--out', '/dev/null']
src = open('action_search_2026_11_05/AC4_slow_mode_evolution/evolve.py').read().split('rows = json.loads')[0]
ns = {}; exec(src, ns); fn = ns['build'](False)
out = []
for rtol in (1e-9, 1e-10, 1e-11, 1e-12, 1e-13):
    c = ns['run_case'](fn, 2.0, 0.9, 0.001, 100.0, 1.0, rtol, False)
    g = ns['run_case'](fn, 2.0, 0.9, 0.001, 100.0, 0.0, rtol, False)
    row = dict(rtol=rtol, R_I=c['max_I'] / g['max_I'], R_II=c['max_II'] / g['max_II'],
               cand_max=[c['max_I'], c['max_II']], gr_max=[g['max_I'], g['max_II']], drift=max(c['omega_drift'], g['omega_drift']))
    out.append(row); print(json.dumps(row), flush=True)
json.dump(out, open('action_search_2026_11_05/AC4_slow_mode_evolution/evidence_diag_tolerance.json', 'w'), indent=1)
