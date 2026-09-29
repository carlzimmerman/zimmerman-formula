"""CFG154 plane: the secondary check -- CFG122's G1.1 (point mass) on a coarse (m, alpha) plane with my own search.

Frozen criteria: ../CFG154_FROZEN_CRITERIA.md (sha256 printed first).  Runs, in order:
  C4  solver B (physical units, brentq, solve_ivp) against solver C (dimensionless, closed-form roots, RK4);
  C6  the search finds a known answer (target replaced by solver C's own B- solution at eps = 1, yhat(0.1) = 10^0.568);
  the search E*(eps) on the union of the R2 line (log eps = -9.5 .. 8.5 step 0.05) and the plane's lattice points;
  H2  cells of m in {1e-3 .. 1e3} eV x alpha in {1e-2 .. 1e2} (0.5-dex steps), both footings;
  R2  E*(eps) per branch and overall, with the declared reading (i)/(ii)/(iii);
  R5  E* at the lattice points with mu(0.1) = 0.01;
  C5b each eps's best solution re-run with twice the steps.
Exit 1 on H2 DISAGREE (or undecided) or on a failed control.
kappa = 1/2 is FITTED.  Nothing here says the data favour either model, or that the theory is closed.
"""
import math
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg154_common import (A0, BRANCHES, MASSES, MPL, MSUN_EV, X_EVAL, Report, SolverB, eps_of, lam_tie, r_M_nat,
                           search, solver_C, target)

rep = Report('cfg154_plane')

# N_a of the tie, re-derived here so that this script stands alone (the same algebra as cfg154_headline S3)
m_, Lam_, al_, MPl_, M_, r_ = sp.symbols('m Lambda alpha M_Pl M r', positive=True)
kap_ = al_ * M_ / (8 * sp.pi * MPl_ * r_ ** 2)
N_a = sp.simplify((al_ * Lam_ / MPl_ * sp.sqrt(kap_)) ** 2 / (M_ / (8 * sp.pi * MPl_ ** 2 * r_ ** 2) * al_ ** 3 * Lam_ ** 2 / MPl_))
N_A = float(N_a)
rep.p(f'N_a (a_phi^2 = N_a (alpha^3 Lambda^2/M_Pl) g_N in the gradient limit) = {N_a}')

# =====================================================================================================================
rep.banner('C4. THE REDUCTION: solver B (physical units) against solver C (only eps enters)')
a0c = A0['canonical']
worst_c4 = 0.0
c4_rows = []
for mv, alv in ((1.0, 1.0), (0.1, 10.0), (10.0, 0.1)):
    lam = lam_tie(alv, a0c, N_A)
    for Mv in MASSES:
        eps = eps_of(mv, alv, Mv, a0c)
        rM_n = r_M_nat(Mv, a0c)
        J_M = alv * Mv * MSUN_EV / (16 * math.pi * mv * rM_n ** 2 * MPL)
        T = target(Mv, ('point', None), a0c)
        for br, yh0 in (('B-', 1.0), ('B+a', 1e3 + 40.0 * eps)):
            B = SolverB(mv, alv, lam, Mv, ('point', None), a0c, br)
            o = B.solve(0.1 * rM_n, yh0 * J_M, 0.0, X_EVAL * rM_n, 40.0 * rM_n, rtol=1e-10)
            R_B = o['rho_SI'] / T['rho_c']
            c = solver_C(np.array([eps]), np.array([yh0]), br, keep_eval=True)
            R_C = c['Rev'][0]
            xe = min(c['xedge'][0], o['r_edge'] / rM_n)
            sel = (X_EVAL <= min(30.0, 0.9 * xe)) & np.isfinite(R_B) & np.isfinite(R_C)
            if sel.sum() == 0:
                d = float('nan')
                note = 'no overlap (fold before 0.111 r_M)'
            else:
                d = float(np.max(np.abs(R_B[sel] / R_C[sel] - 1)))
                worst_c4 = max(worst_c4, d)
                note = f'{sel.sum()} points up to x = {X_EVAL[sel][-1]:.3f}'
            c4_rows.append({'m': mv, 'alpha': alv, 'M': Mv, 'branch': br, 'eps': eps, 'yhat0': yh0, 'max_dev': d,
                            'x_edge_C': c['xedge'][0], 'x_edge_B': o['r_edge'] / rM_n, 'note': note})
            rep.p(f'C4 m = {mv:5g} eV, alpha = {alv:5g}, M_b = {Mv:.0e}, {br:4s} eps = {eps:.4e}, yhat(0.1) = {yh0:.4e}: '
                  f'max |R_B/R_C - 1| = {d:.2e} ({note}); x_edge C {c["xedge"][0]:.4g}, B {o["r_edge"] / rM_n:.4g}')
c4ok = rep.check('C4 solver B = solver C to 1e-6 over [0.1, min(30, 0.9 x_edge)]', worst_c4 <= 1e-6,
                 f'worst max |R_B/R_C - 1| = {worst_c4:.2e} over {sum(np.isfinite(r["max_dev"]) for r in c4_rows)} '
                 f'compared runs')
rep.num('C4_rows', c4_rows)
rep.num('C4_worst', worst_c4)

# =====================================================================================================================
rep.banner('C6. THE SEARCH CAN FIND A KNOWN ANSWER')
y_fake = 10.0 ** 0.568
cf = solver_C(np.array([1.0]), np.array([y_fake]), 'B-', keep_eval=True)
fake = cf['Rev'][0]
s6 = search([1.0], fake=fake)
c6ok = rep.check('C6 target := solver C B- solution at eps = 1, yhat(0.1) = 10^0.568; the search returns E* <= 0.005',
                 s6['best_E'][0] <= 0.005, f'E* = {s6["best_E"][0]:.3e} ({s6["best_branch"][0]}, yhat(0.1) = '
                 f'{s6["best_y"][0]:.5g}; true {y_fake:.5g})')
rep.num('C6_Estar', s6['best_E'][0])

# =====================================================================================================================
rep.banner('THE SEARCH: E*(eps) on the R2 line and on the plane\'s lattice points (point mass, 3 branches)')
M_GRID = 10.0 ** (-3 + 0.5 * np.arange(13))
A_GRID = 10.0 ** (-2 + 0.5 * np.arange(9))
LINE = 10.0 ** (-9.5 + 0.05 * np.arange(361))
cells = {}
for foot, a0v in A0.items():
    for mv in M_GRID:
        for alv in A_GRID:
            cells[(foot, mv, alv)] = [eps_of(mv, alv, Mv, a0v) for Mv in MASSES]
key = lambda e: round(math.log10(e), 6)
uniq = {}
for e in LINE:
    uniq.setdefault(key(e), e)
lattice = {}
for (foot, mv, alv), es in cells.items():
    for e in es:
        uniq.setdefault(key(e), e)
        lattice.setdefault(foot, set()).add(key(e))
keys = sorted(uniq)
all_eps = np.array([uniq[k] for k in keys])
rep.p(f'{len(LINE)} line values + lattice values ({", ".join(f"{f}: {len(v)}" for f, v in lattice.items())}) '
      f'-> {all_eps.size} distinct eps; {len(cells)} cells')
res = search(all_eps)
Estar = dict(zip(keys, res['best_E']))
Ebr = {b: dict(zip(keys, res['branch'][b]['best_E'])) for b in BRANCHES}
bestb = dict(zip(keys, res['best_branch']))
besty = dict(zip(keys, res['best_y']))

# ---- H2
rep.banner('H2 [SECONDARY]. G1.1 ON THE COARSE PLANE')
h2 = {}
for foot in A0:
    npass = nmarg = 0
    per_mass_pass = [0, 0, 0, 0]
    best_worst, best_cell = np.inf, None
    for (f2, mv, alv), es in cells.items():
        if f2 != foot:
            continue
        Es = [Estar[key(e)] for e in es]
        for i, E in enumerate(Es):
            per_mass_pass[i] += int(E <= 0.10)
        if max(Es) < best_worst:
            best_worst, best_cell = max(Es), (mv, alv, Es)
        if max(Es) < 0.095:
            npass += 1
        elif max(Es) <= 0.105:
            nmarg += 1
    h2[foot] = {'pass': npass, 'marginal': nmarg, 'per_mass_pass': per_mass_pass, 'best_worst_mass_E': best_worst,
                'best_cell': best_cell}
    rep.p(f'H2 {foot}: {npass} of {sum(1 for c in cells if c[0] == foot)} cells pass, {nmarg} marginal; '
          f'cells passing per mass (1e9..1e12): {per_mass_pass}; best worst-mass error {best_worst:.4f} at m = '
          f'{best_cell[0]:.3g} eV, alpha = {best_cell[1]:.3g} (per mass ' + ', '.join(f'{v:.4f}' for v in best_cell[2]) + ')')
tot_pass = sum(v['pass'] for v in h2.values())
tot_marg = sum(v['marginal'] for v in h2.values())
status = 'AGREE' if (tot_pass == 0 and tot_marg == 0) else ('DISAGREE' if tot_pass > 0 else 'UNDECIDED (marginal)')
rep.p(f'H2 status: {status} (CFG122: 0/3600 cells; best worst-mass error 0.896 / 0.894 on its finer plane)')
rep.num('H2', h2)
rep.num('H2_status', status)

# ---- R2
rep.banner('R2 (reported). E*(eps): can even one mass be fitted, at any (m, alpha)?')
lineE = np.array([Estar[key(e)] for e in LINE])
for b in BRANCHES:
    arr = np.array([Ebr[b][key(e)] for e in LINE])
    k = int(np.argmin(arr))
    rep.p(f'R2 branch {b:4s}: min over the line E* = {arr[k]:.4f} at eps = {LINE[k]:.4e}')
k = int(np.argmin(lineE))
rep.p(f'R2 overall: min E* = {lineE[k]:.4f} at eps = {LINE[k]:.4e} ({bestb[key(LINE[k])]}, yhat(0.1) = '
      f'{besty[key(LINE[k])]:.5g})')
rep.p('R2 E*(eps) every 0.5 dex:')
for i in range(0, 361, 10):
    kk = key(LINE[i])
    rep.p(f'   log eps = {math.log10(LINE[i]):6.2f}: E* = {Estar[kk]:.4f} ({bestb[kk]}, yhat(0.1) = {besty[kk]:.4g}); '
          + ', '.join(f'{b} {Ebr[b][kk]:.4f}' for b in BRANCHES))
all_single = [Estar[k2] for k2 in keys]
any_single = any(E <= 0.10 for E in all_single)
four = any(all(lineE[i + 10 * j] <= 0.10 for j in range(4)) for i in range(361 - 30))
reading = '(iii)' if four else ('(ii)' if any_single else '(i)')
rep.p(f'R2 reading {reading}: ' + {
    '(i)': 'E* > 0.10 for every eps -- no single mass can be fitted at any (m, alpha); the G1.1 FAIL does not need '
           'the mass spread; 31.6 is a second, separate failure.',
    '(ii)': 'some single masses pass, but no eps0 passes at all four of eps0 x {1, 10^1/2, 10, 10^3/2}: the mass '
            'spread decides.',
    '(iii)': 'some eps0 passes at all four: that predicts passing cells (compare H2).'}[reading])
rep.p(f'R2 smallest single-mass E* anywhere (line + lattice): {min(all_single):.4f}; count of eps with E* <= 0.10: '
      f'{sum(E <= 0.10 for E in all_single)}')
rep.num('R2_reading', reading)
rep.num('R2_min_Estar', float(min(all_single)))
rep.num('R2_line', {'log_eps': np.log10(LINE), 'Estar': lineE,
                    'Estar_branch': {b: [Ebr[b][key(e)] for e in LINE] for b in BRANCHES},
                    'best_branch': [bestb[key(e)] for e in LINE], 'best_yhat0': [besty[key(e)] for e in LINE]})

# ---- R5
rep.banner('R5 (reported). H2 SENSITIVITY: mu(0.1) = 0.01 instead of 0 at the lattice points')
lat_keys = sorted(set().union(*lattice.values()))
lat_eps = np.array([uniq[k2] for k2 in lat_keys])
res5 = search(lat_eps, mu0=0.01)
dE = np.array(res5['best_E']) - np.array([Estar[k2] for k2 in lat_keys])
E5 = dict(zip(lat_keys, res5['best_E']))
changed = 0
for (foot, mv, alv), es in cells.items():
    v0 = max(Estar[key(e)] for e in es) <= 0.10
    v1 = max(E5[key(e)] for e in es) <= 0.10
    changed += int(v0 != v1)
rep.p(f'R5: max |dE*| = {np.max(np.abs(dE)):.4e} over {lat_eps.size} lattice eps; cell verdicts changed: {changed}')
rep.num('R5_max_dE', float(np.max(np.abs(dE))))
rep.num('R5_cells_changed', changed)

# ---- C5b
rep.banner('C5b. RESOLUTION: each eps\'s best solution with twice the steps')
worst5 = 0.0
for b in BRANCHES:
    idx = [i for i, k2 in enumerate(keys) if bestb[k2] == b]
    if not idx:
        continue
    c12 = solver_C(all_eps[idx], res['best_y'][idx], b, nsub=12)
    worst5 = max(worst5, float(np.max(np.abs(c12['E'] - res['best_E'][idx]))))
c5ok = rep.check('C5b twice the steps changes E by <= 1e-3', worst5 <= 1e-3, f'max |dE| = {worst5:.2e}')
rep.num('C5b_worst', worst5)

# =====================================================================================================================
rep.banner('SUMMARY')
for c in rep.checks:
    rep.p(f'  {"PASS" if c["pass"] else "FAIL"}  [{c["kind"]}] {c["name"]}')
rep.p(f'  H2: {status}')
exit_code = 0 if (c4ok and c5ok and c6ok and status == 'AGREE') else 1
rep.p('kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.')
rep.write(exit_code)
sys.exit(exit_code)
