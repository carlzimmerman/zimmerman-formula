"""CFG154 POST-HOC (not frozen; written after cfg154_plane.py failed C4 and C5b): diagnoses of the two control misses.

Nothing here re-pins a frozen line.  By the frozen rule, C4's miss voids H2, R2, R4 and R5; this script only asks WHY
the controls missed and whether the misses reach the numbers that decide the readings.
  P1  C4's failing cell (m = 10 eV, alpha = 0.1), B-, yhat(0.1) = 1: solver B at rtol 1e-10 / 1e-12 against solver C at
      nsub = 6, 12, 24, 48 (which solver is off, and does the gap close as the RK4 step shrinks?).
  P2  C5b per eps: where does |E(nsub=12) - E(nsub=6)| exceed 1e-3, and what is E* there?
  P3  the search repeated at nsub = 12 on the lattice points (H2) and on log eps in [-1, 1] (R2's minimum).
kappa = 1/2 is FITTED.  Nothing here says the data favour either model, or that the theory is closed.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg154_common import (A0, MASSES, MPL, MSUN_EV, X_EVAL, Report, SolverB, eps_of, lam_tie, r_M_nat, search,
                           solver_C, target)

rep = Report('cfg154_plane_POSTHOC')
rep.p('POST-HOC diagnosis; not a frozen check.  N_a = 1 (derived in cfg154_headline S3 and cfg154_plane).')

# ---------------------------------------------------------------- P1
rep.banner('P1. C4\'s failing cell: which solver is off?')
a0c = A0['canonical']
mv, alv = 10.0, 0.1
lam = lam_tie(alv, a0c, 1.0)
p1 = []
for Mv in MASSES:
    eps = eps_of(mv, alv, Mv, a0c)
    rM_n = r_M_nat(Mv, a0c)
    J_M = alv * Mv * MSUN_EV / (16 * math.pi * mv * rM_n ** 2 * MPL)
    T = target(Mv, ('point', None), a0c)
    RB = {}
    for rt in (1e-10, 1e-12):
        B = SolverB(mv, alv, lam, Mv, ('point', None), a0c, 'B-')
        o = B.solve(0.1 * rM_n, 1.0 * J_M, 0.0, X_EVAL * rM_n, 40.0 * rM_n, rtol=rt)
        RB[rt] = o['rho_SI'] / T['rho_c']
    row = {'M': Mv, 'eps': eps, 'B_rtol_change': float(np.max(np.abs(RB[1e-12] / RB[1e-10] - 1)))}
    for ns in (6, 12, 24, 48):
        c = solver_C(np.array([eps]), np.array([1.0]), 'B-', nsub=ns, keep_eval=True)
        row[f'C{ns}_vs_B12'] = float(np.max(np.abs(c['Rev'][0] / RB[1e-12] - 1)))
    row['R_range'] = [float(RB[1e-12].min()), float(RB[1e-12].max())]
    p1.append(row)
    rep.p(f'M_b = {Mv:.0e} eps = {eps:.4e}: solver B rtol 1e-10 -> 1e-12 changes R by {row["B_rtol_change"]:.1e}; '
          f'solver C vs B(1e-12): nsub 6 {row["C6_vs_B12"]:.2e}, 12 {row["C12_vs_B12"]:.2e}, '
          f'24 {row["C24_vs_B12"]:.2e}, 48 {row["C48_vs_B12"]:.2e}; R spans {row["R_range"][0]:.3e} .. {row["R_range"][1]:.3e}')
rep.num('P1', p1)

# ---------------------------------------------------------------- P2 + P3 (lattice)
rep.banner('P2. C5b per eps (the frozen search, re-run identically, then its best solutions at twice the steps)')
M_GRID = 10.0 ** (-3 + 0.5 * np.arange(13))
A_GRID = 10.0 ** (-2 + 0.5 * np.arange(9))
LINE = 10.0 ** (-9.5 + 0.05 * np.arange(361))
key = lambda e: round(math.log10(e), 6)
cells, uniq, lat = {}, {}, set()
for foot, a0v in A0.items():
    for m_ in M_GRID:
        for a_ in A_GRID:
            cells[(foot, m_, a_)] = [eps_of(m_, a_, Mv, a0v) for Mv in MASSES]
for e in LINE:
    uniq.setdefault(key(e), e)
for es in cells.values():
    for e in es:
        uniq.setdefault(key(e), e)
        lat.add(key(e))
keys = sorted(uniq)
all_eps = np.array([uniq[k] for k in keys])
res = search(all_eps)
dE = np.full(all_eps.size, np.nan)
for b in ('B-', 'B+a', 'B+b'):
    idx = [i for i, k in enumerate(keys) if res['best_branch'][i] == b]
    if idx:
        c12 = solver_C(all_eps[idx], res['best_y'][idx], b, nsub=12)
        dE[idx] = np.abs(c12['E'] - res['best_E'][idx])
bad = np.where(dE > 1e-3)[0]
rep.p(f'|dE| > 1e-3 at {bad.size} of {all_eps.size} eps; their log eps: '
      + (', '.join(f'{math.log10(all_eps[i]):.2f}' for i in bad) if bad.size else 'none'))
rep.p('   of those, the smallest E* is ' + (f'{min(res["best_E"][i] for i in bad):.4g}' if bad.size else 'n/a')
      + '; the largest |dE| where E* < 2 is '
      + f'{np.nanmax(np.where(res["best_E"] < 2, dE, np.nan)):.2e}')
for lo, hi in ((-9.6, -2), (-2, 2), (2, 4.6), (4.6, 7.6), (7.6, 9)):
    sel = [(math.log10(e) >= lo) and (math.log10(e) < hi) for e in all_eps]
    sel = np.array(sel)
    if sel.any():
        rep.p(f'   log eps in [{lo}, {hi}): max |dE| = {np.nanmax(dE[sel]):.2e}; E* range '
              f'{np.min(res["best_E"][sel]):.4g} .. {np.max(res["best_E"][sel]):.4g}')
rep.num('P2', {'log_eps': np.log10(all_eps), 'Estar': res['best_E'], 'dE': dE})

rep.banner('P3. The search at nsub = 12 (twice the steps): the lattice (H2) and log eps in [-1, 1] (R2\'s minimum)')
lat_keys = sorted(lat)
lat_eps = np.array([uniq[k] for k in lat_keys])
r12 = search(lat_eps, nsub=12)
E12 = dict(zip(lat_keys, r12['best_E']))
E6 = dict(zip(keys, res['best_E']))
changed, bw = 0, {}
for (foot, m_, a_), es in cells.items():
    v6 = max(E6[key(e)] for e in es)
    v12 = max(E12[key(e)] for e in es)
    changed += int((v6 <= 0.10) != (v12 <= 0.10))
    bw[foot] = min(bw.get(foot, np.inf), v12)
rep.p(f'lattice at nsub = 12: min single-mass E* = {min(E12.values()):.4f}; cells passing: '
      f'{sum(1 for es in cells.values() if max(E12[key(e)] for e in es) <= 0.10)}; verdicts changed vs nsub = 6: {changed}; '
      f'best worst-mass error ' + ', '.join(f'{f} {v:.4f}' for f, v in bw.items()))
near = 10.0 ** np.linspace(-1, 1, 41)
rn6 = search(near, nsub=6)
rn12 = search(near, nsub=12)
k6, k12 = int(np.argmin(rn6['best_E'])), int(np.argmin(rn12['best_E']))
rep.p(f'log eps in [-1, 1] (41 values): min E* nsub 6 = {rn6["best_E"][k6]:.5f} at eps = {near[k6]:.4f} '
      f'({rn6["best_branch"][k6]}, yhat(0.1) = {rn6["best_y"][k6]:.5g}); nsub 12 = {rn12["best_E"][k12]:.5f} at eps = '
      f'{near[k12]:.4f}; max |dE*| over the 41 values = {np.max(np.abs(rn12["best_E"] - rn6["best_E"])):.2e}')
rep.num('P3', {'lattice_min_Estar_nsub12': min(E12.values()), 'verdicts_changed': changed, 'best_worst': bw,
               'near_min_nsub6': rn6['best_E'][k6], 'near_min_nsub12': rn12['best_E'][k12],
               'near_eps_nsub6': near[k6], 'near_max_dE': float(np.max(np.abs(rn12['best_E'] - rn6['best_E'])))})
rep.p('kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.')
rep.write(0)
