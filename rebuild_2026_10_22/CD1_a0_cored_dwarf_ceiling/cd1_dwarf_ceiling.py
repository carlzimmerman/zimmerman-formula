"""CD1_a0_cored_dwarf_ceiling -- frozen criteria FROZEN_CRITERIA.md (c99930b2af).

Can X38's a0-cored (rho0 r0 = a0/(2 pi G)) Burkert halos supply the dwarfs' route-E requirement g_obs - g_N at r12,
for ANY core radius?  The fixed-Sigma ceiling is g_h,max = 0.2545 a0.  MUTATE=1 runs the controls (separate outputs).
"""
import csv, json, math, os, sys
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get('MUTATE') == '1'
TAG = '_MUTATE' if MUTATE else ''
G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
OUT = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)

def B(x): return np.log1p(x*x) + 2*np.log1p(x) - 2*np.arctan(x)

# K1
xs = np.logspace(-3, 3, 400001); yy = B(xs)/xs**2; cgrid = float(yy.max())
dB = lambda x: (2*x/(1+x*x) + 2/(1+x) - 2/(1+x*x))/x**2 - 2*B(x)/x**3
xr = brentq(dB, 0.3, 3.0, xtol=1e-14); croot = float(B(xr)/xr**2)
qok = all(abs(quad(lambda r: 4*math.pi*r*r/((r+1)*(r*r+1)), 0, x, epsabs=0, epsrel=1e-12)[0]/(math.pi*B(x)) - 1) < 1e-8 for x in (0.5, 1, 3))
k1 = abs(cgrid - croot) < 1e-6 and qok
C = croot
P(f'CD1_a0_cored_dwarf_ceiling{TAG}  (frozen c99930b2af; A1 K2 check definition)  kappa = 1/2 FITTED; footings never pooled; not theory closed')
P(f'K1 max B/x^2 grid {cgrid:.7f} root {croot:.7f} at x {xr:.5f}; closed form vs quadrature ok {qok}: {"PASS" if k1 else "FAIL"}')
P(f'ceiling g_h,max = (a0/2) * {C:.6f} = {C/2:.6f} a0')

rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'X1_hosted_recount', 'x1_per_system.csv'))))
RES = dict(frozen='c99930b2af', mutate=MUTATE, ceiling_over_a0=C/2, footings={})
checks = [('K1', k1)]
classes = {}
for foot in ('canonical', 'alt'):
    R = [r for r in rows if r['footing'] == foot]
    k3 = len(R) == 89
    a0 = A0[foot]; gmax = C/2*a0
    recs = []; k2hits = 0
    for r in R:
        mstar = 10**float(r['logMstar'])*MSUN; r12 = 4/3*float(r['rh_pc'])*PC
        gN = G*(mstar/2)/r12**2; sig = float(r['sigma'])*1e3
        D = float(r['Delta[Newton]']); sd = float(r['sdMC[Newton]'])
        off = math.log10(3*sig**2/r12/gN) - D                     # A1: raw-sigma vs X1's binary-corrected Delta
        if (float(r['M_V']) <= -7.7 and abs(off) <= 0.035) or (float(r['M_V']) > -7.7 and 0 <= off <= 0.40): k2hits += 1
        if MUTATE == 'a': pass
        recs.append(dict(name=r['name'], host=r['host'], cls=r['cls'], logM=float(r['logMstar']), rh=float(r['rh_pc']), gN=gN, D=D, sd=sd))
    k2 = k2hits == len(R)
    P(f'\n=== [{foot}] a0 {a0:.4e}; ceiling {gmax:.3e} m/s^2; rows {len(R)} (K3 {"PASS" if k3 else "FAIL"}); '
      f'K2 Delta[Newton] reproduced in {k2hits}/{len(R)}: {"PASS" if k2 else "FAIL"}')
    checks += [(f'K2[{foot}]', k2), (f'K3[{foot}]', k3)]
    if not k2:
        P('K2 FAILED: definition mismatch; stopping as frozen'); break

    def grade(recs, mode=None):
        out = []
        for q in recs:
            D, sd = q['D'], q['sd']
            if mode == 'a': D = D/4
            gobs = q['gN']*10**D; gh = gobs - q['gN']
            if mode == 'b': gh = 3*gmax
            if D <= 0 and mode != 'b':
                out.append(dict(q, gh=0.0, S=0.0, z=-np.inf, graded=True, passes=True)); continue
            ratio = (10**D - 1)
            if ratio < 0.1 and mode != 'b':
                out.append(dict(q, gh=gh, S=gh/gmax, z=np.nan, graded=False, passes=None)); continue
            sdh = sd*10**D/ratio if mode != 'b' else sd*10**q['D']/max(10**q['D'] - 1, 0.1)
            z = (math.log10(gh) - math.log10(gmax))/sdh
            out.append(dict(q, gh=gh, S=gh/gmax, z=z, graded=True, passes=z < 2))
        g = [o for o in out if o['graded']]
        fex = np.mean([o['z'] >= 2 for o in g]); medS = float(np.median([o['S'] for o in g]))
        cls = 'DWARFS EXCLUDE FIXED-SIGMA_a0' if fex >= 0.25 else ('CONSISTENT' if fex < 0.05 and medS <= 1 else 'PARTIAL')
        return out, g, float(fex), medS, cls

    if MUTATE:
        _, ga, fa, ma, ca = grade(recs, 'a'); _, gb, fb, mb, cb = grade(recs, 'b')
        P(f'  MUTATE (a) weak discrepancy: frac z>=2 {fa:.3f}, median S {ma:.2f} -> {ca} (must not be EXCLUDE)')
        P(f'  MUTATE (b) g_h = 3 ceiling: frac z>=2 {fb:.3f} -> {cb} (must be EXCLUDE)')
        RES['footings'][foot] = dict(a=ca, b=cb)
        checks.append((f'MUT[{foot}]', ca != 'DWARFS EXCLUDE FIXED-SIGMA_a0' and cb == 'DWARFS EXCLUDE FIXED-SIGMA_a0'))
        continue
    out, g, fex, medS, cls = grade(recs)
    classes[foot] = cls
    S = np.array([o['S'] for o in g])
    P(f'  graded {len(g)} of {len(out)}; fraction z>=2: {fex:.3f}; median S {medS:.2f}; S quantiles 50/84/97.5: '
      + ' / '.join(f'{v:.2f}' for v in np.percentile(S, [50, 84, 97.5])))
    rho_m = spearmanr([o['logM'] for o in g], S); rho_r = spearmanr([o['rh'] for o in g], S)
    P(f'  Spearman S vs logM* {rho_m.statistic:+.2f} (p {rho_m.pvalue:.1e}); vs r_h {rho_r.statistic:+.2f} (p {rho_r.pvalue:.1e})')
    bycls = {}
    for o in g: bycls.setdefault(o['cls'] if not o['cls'].startswith('indiv') else 'indiv:' + o['host'], []).append(o)
    for k, v in sorted(bycls.items()):
        P(f'    {k:28s} n {len(v):3d}  frac z>=2 {np.mean([o["z"] >= 2 for o in v]):.2f}  median S {np.median([o["S"] for o in v]):.2f}')
    P(f'  CLASS [{foot}]: {cls}   (cluster cores per X39 need S ~ 2)')
    worst = sorted(g, key=lambda o: -o['z'])[:8]
    P('  largest z: ' + '; '.join(f'{o["name"]} S {o["S"]:.1f} z {o["z"]:+.1f}' for o in worst))
    RES['footings'][foot] = dict(cls=cls, frac_z2=fex, median_S=medS, S_q=np.percentile(S, [50, 84, 97.5]).tolist(),
                                 spearman_logM=float(rho_m.statistic), spearman_rh=float(rho_r.statistic),
                                 rows=[{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in o.items()} for o in out])

if not MUTATE and len(classes) == 2:
    RES['verdict'] = classes['canonical'] if classes['canonical'] == classes['alt'] else f'UNDECIDED (footings disagree: {classes})'
    P(f'\n=== VERDICT: {RES["verdict"]}')
n = sum(ok for _, ok in checks); P(f'\nchecks {n}/{len(checks)}: ' + ', '.join(f'{k} {"PASS" if ok else "FAIL"}' for k, ok in checks))
RES['checks'] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f'cd1_dwarf_ceiling{TAG}.out'), 'w').write('\n'.join(OUT) + '\n')
json.dump(RES, open(os.path.join(HERE, f'cd1_dwarf_ceiling{TAG}.json'), 'w'), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
