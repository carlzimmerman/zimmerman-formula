"""CFG154 POST-HOC comparison with CFG122 (written after opening CFG122's scripts and outputs; not frozen).

  Q1  Does CFG122's G1.1 depend on (m, alpha) only through eps0 = m^2 r_M(1e9)/(alpha M_Pl)?  Read CFG122's own saved plane
      arrays (cfg122_g1_plane_arrays.npz, point mass): group the 60 x 60 cells by eps0 and test whether the best error per
      (mass, branch) is constant within each group.  CFG122's coverage rule also requires n >= n_c(m, sigma^2) (a thermal
      edge), which depends on m separately, so the answer is not assumed.
  Q2  Why is CFG122's per-mass closest approach 0.805-0.818 while my search finds 0.416?  Run MY solver C on CFG122's own
      per-halo grid (Y(0.1 r_M) = 0, +-10^k m G M/r_M, k = -6..6, i.e. yhat(0.1) = 0, +-2 eps 10^k), no thermal edge.
  Q3  (added after writing Q1/Q2) A bound on CFG122's thermal edge.  My frozen spec said H2's missing thermal edge makes it
      "more permissive"; that is only half right, because an edge at x_edge >= 3 also SHORTENS the scored range.  For any
      solution the error over [0.1, 3] is <= its error over [0.1, x_edge] for every allowed edge (x_edge >= 3), so the best
      error over [0.1, 3] (my two-stage search, all branches, no coverage constraint) is a lower bound on G1.1's error under
      ANY thermal-edge placement.  If it exceeds 0.10 at every eps, no edge can make even one mass pass.
Version history (disclosed): the first run compared absolute within-group spreads in Q1, which runaway solutions (errors of
order 1e25) swamp; its output is kept as cfg154_compare_POSTHOC_FIRSTRUN.out.  Q1 now uses relative spreads in the
verdict-relevant region; Q3 was added in the same revision.
kappa = 1/2 is FITTED.  Nothing here says the data favour either model, or that the theory is closed.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg154_common import A0, BRANCHES, MASSES, MPL, REPO, Report, r_M_nat, search, solver_C

rep = Report('cfg154_compare_POSTHOC')
rep.p('POST-HOC comparison with CFG122; not a frozen check.')
NPZ = os.path.join(REPO, 'campaign_fresh_gravity', 'CFG122_door4_superfluid', 'cfg122_g1_plane_arrays.npz')

# ---------------------------------------------------------------- Q1
rep.banner('Q1. CFG122\'s own plane arrays: is the best error a function of eps0 alone?')
z = np.load(NPZ)
mg, ag = z['mg'], z['ag']
q1 = {}
for foot in ('canonical', 'alt'):
    a0 = A0[foot]
    eps0 = (mg[:, None] ** 2) * r_M_nat(1e9, a0) / (ag[None, :] * MPL)
    keyg = np.round(np.log10(eps0), 6)
    groups = {}
    for i in range(mg.size):
        for j in range(ag.size):
            groups.setdefault(keyg[i, j], []).append((i, j))
    ng = len(groups)
    multi = [g for g in groups.values() if len(g) > 1]
    for Mv in MASSES:
        E = np.stack([z[f'{foot}|point|{Mv}|{br}|bestS'] for br in ('B-', 'B+hi', 'B+lo')])
        ED = np.stack([z[f'{foot}|point|{Mv}|{br}|edgeS'] for br in ('B-', 'B+hi', 'B+lo')])
        kb = np.argmin(np.where(np.isfinite(E), E, np.inf), axis=0)
        best_all = np.take_along_axis(E, kb[None], axis=0)[0]
        edge_at_best = np.take_along_axis(ED, kb[None], axis=0)[0]
        rel, edge_diff, n_rel = [], 0, 0
        for g in multi:
            vals = np.array([best_all[i, j] for i, j in g])
            eds = np.array([edge_at_best[i, j] for i, j in g])
            if np.all(np.isfinite(vals)) and vals.min() < 2.0:
                n_rel += 1
                rel.append(float(vals.max() / vals.min() - 1.0))
                edge_diff += int(eds.max() - eds.min() > 1e-9)
        rel = np.array(rel) if rel else np.array([0.0])
        trunc = float(np.mean(edge_at_best < 30.0 - 1e-9))
        q1[f'{foot}_{Mv:.0e}'] = {'n_groups': ng, 'n_multi': len(multi), 'n_groups_best_below_2': n_rel,
                                  'max_rel_spread_below_2': float(rel.max()), 'n_rel_spread_gt_1e-6': int(np.sum(rel > 1e-6)),
                                  'groups_with_different_edges': edge_diff, 'frac_cells_best_solution_edge_below_30': trunc}
        rep.p(f'{foot:9s} M_b = {Mv:.0e}: {mg.size * ag.size} cells -> {ng} distinct eps0 ({len(multi)} shared by >1 cell). '
              f'In the {n_rel} shared groups whose best error is < 2: largest relative within-group spread {rel.max():.3g}; '
              f'groups differing by > 1e-6: {int(np.sum(rel > 1e-6))}; groups whose best solutions have different edges: {edge_diff}. '
              f'Cells whose best solution is cut by the thermal edge (x_edge < 30): {100 * trunc:.1f}%')
rep.num('Q1', q1)

# ---------------------------------------------------------------- Q2
rep.banner('Q2. My solver C on CFG122\'s own 27-value per-halo grid (no thermal edge), against my two-stage search')
LINE = 10.0 ** (-9.5 + 0.05 * np.arange(361))
ks = np.arange(-6, 7)
best27 = np.full(LINE.size, np.inf)
arg27 = [None] * LINE.size
for br in BRANCHES:
    for i0 in range(0, LINE.size, 61):
        es = LINE[i0:i0 + 61]
        y0 = np.concatenate([[0.0], 10.0 ** ks, -(10.0 ** ks)])
        E = solver_C(np.repeat(es, y0.size), (2.0 * es[:, None] * y0[None, :]).ravel(), br)['E'].reshape(es.size, y0.size)
        for k in range(es.size):
            j = int(np.argmin(E[k]))
            if E[k, j] < best27[i0 + k]:
                best27[i0 + k] = E[k, j]
                arg27[i0 + k] = (br, float(y0[j]))
k27 = int(np.argmin(best27))
rep.p(f'CFG122 grid in my solver: min over eps of the per-mass best error = {best27[k27]:.4f} at eps = {LINE[k27]:.4e} '
      f'({arg27[k27][0]}, Y0/(m G M/r_M) = {arg27[k27][1]:g})')
full = search(LINE[(LINE > 0.1) & (LINE < 30)])
kf = int(np.argmin(full['best_E']))
rep.p(f'my two-stage search, same eps range [0.1, 30]: min E* = {full["best_E"][kf]:.4f} at eps = '
      f'{full["eps"][kf]:.4e} ({full["best_branch"][kf]}, yhat(0.1) = {full["best_y"][kf]:.5g}, i.e. Y0/(m G M/r_M) = '
      f'{full["best_y"][kf] / (2 * full["eps"][kf]):.4g})')
for le in (-0.5, 0.0, 0.15, 0.5):
    e = 10.0 ** le
    i = int(np.argmin(np.abs(np.log10(LINE) - le)))
    rep.p(f'   log eps = {le:5.2f}: CFG122 grid {best27[i]:.4f} ({arg27[i][0]}, Y0 = {arg27[i][1]:g} m G M/r_M)')
rep.num('Q2', {'min_grid27': best27[k27], 'eps_grid27': LINE[k27], 'min_fine': full['best_E'][kf],
               'eps_fine': full['eps'][kf]})

# ---------------------------------------------------------------- Q3
rep.banner('Q3. Lower bound under any thermal edge: the best single-mass error scored only over [0.1, 3]')
from cfg154_common import GRID, X_EVAL, local_minima, refine_points  # noqa: E402
SEL3 = X_EVAL <= 3.0


def E_range(eps, y0, branch):
    c = solver_C(eps, y0, branch, keep_eval=True)
    R = c['Rev'][:, SEL3]
    E = np.nanmax(np.abs(R - 1.0), axis=1)
    return np.where(c['xedge'] < 3.0, np.inf, E)


best3 = np.full(LINE.size, np.inf)
arg3 = [None] * LINE.size
for br in BRANCHES:
    for i0 in range(0, LINE.size, 20):
        es = LINE[i0:i0 + 20]
        E1 = E_range(np.repeat(es, GRID.size), np.tile(GRID, es.size), br).reshape(es.size, GRID.size)
        ee, yy, ow = [], [], []
        for k in range(es.size):
            for jm in local_minima(E1[k]):
                pts = refine_points(jm)
                ee.append(np.full(pts.size, es[k]))
                yy.append(pts)
                ow.append(np.full(pts.size, k))
        E2 = E_range(np.concatenate(ee), np.concatenate(yy), br) if ee else np.array([])
        yy = np.concatenate(yy) if yy else np.array([])
        ow = np.concatenate(ow) if ow else np.array([], int)
        for k in range(es.size):
            j = int(np.argmin(E1[k]))
            cand = [(E1[k, j], GRID[j])]
            s = ow == k
            if s.any():
                j2 = int(np.argmin(E2[s]))
                cand.append((E2[s][j2], yy[s][j2]))
            e_best, y_best = min(cand, key=lambda t: t[0])
            if e_best < best3[i0 + k]:
                best3[i0 + k] = e_best
                arg3[i0 + k] = (br, float(y_best))
k3 = int(np.argmin(best3))
rep.p(f'min over eps of the best single-mass error over [0.1, 3] = {best3[k3]:.4f} at eps = {LINE[k3]:.4e} '
      f'({arg3[k3][0]}, yhat(0.1) = {arg3[k3][1]:.5g}); count of eps with E <= 0.10: {int(np.sum(best3 <= 0.10))}')
for i in range(0, LINE.size, 20):
    rep.p(f'   log eps = {math.log10(LINE[i]):6.2f}: best over [0.1, 3] = {best3[i]:.4f} ({arg3[i][0]})')
rep.p('   (a lower bound on G1.1 under any thermal edge with x_edge >= 3; the edge also removes solutions, which only raises it)')
rep.num('Q3', {'min_E_0.1_to_3': best3[k3], 'eps_at_min': LINE[k3], 'branch': arg3[k3][0], 'yhat0': arg3[k3][1],
               'n_eps_le_0.10': int(np.sum(best3 <= 0.10)), 'log_eps': np.log10(LINE), 'E3': best3})
rep.p('kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.')
rep.write(0)
