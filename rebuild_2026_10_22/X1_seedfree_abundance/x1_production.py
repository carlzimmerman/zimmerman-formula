"""X1 E1 production analysis (queued 64/128/256^3 runs): coherent-fraction convergence, cumulants, hand-over criterion.
Windowed f0 = trailing 100-tau mean (A3 item 2). Writes x1_production_results.json."""
import json
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
THR = [1, 2, 3, 5, 10, 20, 50, 100]
out = {}
for f in sorted((HERE/'lattice').glob('*.json')):
    if not (f.stem.startswith('X1_E1') or f.stem.startswith('P64_TW_p50_s1') or f.stem.startswith('P64_CSA')): continue
    d = json.loads(f.read_text()); rr = d['rows']; t = np.array([r['tau'] for r in rr])
    def w(key, T, f=lambda r, k: r[k]):
        s = [f(r, key) for r in rr if T-100 < r['tau'] <= T]; return float(np.mean(s)) if s else None
    exk = lambda r, k: r[k][2]/r[k][0]**2
    taus = [T for T in (100, 500, 1000, 2000, 3000, 4000, 10000, 20000) if T <= t[-1]+1]
    out[f.stem] = dict(N=d['spec']['N'], variant=d['spec']['variant'], tau_end=float(t[-1]),
                       f0=dict((str(T), w('f0_phi', T)) for T in taus), f0X_end=rr[-1]['f0_x'],
                       g4=dict((str(T), w('g4', T)) for T in taus), exkurt=dict((str(T), w('cum_re', T, exk)) for T in taus),
                       frac_low_n16={str(T): float(np.interp(np.log(16), np.log(THR), [r for r in rr if r['tau'] <= T][-1]['frac_low'])) for T in taus},
                       Ephi_end=rr[-1]['Ephi_phys'], energy_residual=d['energy_residual'], wall_s=d['wall_s'])
(HERE/'x1_production_results.json').write_text(json.dumps(out, indent=1))
for k, v in out.items():
    print(k, 'N', v['N'], 'tau', v['tau_end'], 'f0', {a: round(b, 3) for a, b in v['f0'].items()}, 'g4', {a: round(b, 3) for a, b in v['g4'].items()},
          'n<16', {a: round(b, 2) for a, b in v['frac_low_n16'].items()}, 'f0X', round(v['f0X_end'], 5), 'res', f"{v['energy_residual']:.1e}")
