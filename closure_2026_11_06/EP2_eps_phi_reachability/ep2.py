"""EP2: eps_phi(z) = (1+z) rho_DE'(z) / (2 rho_tot(z)) with rho_DE kept in rho_tot, on the record's histories, both
footings. Lines: CRITERIA.md (c9fe71ac87). Kappa = 1/2 FITTED; not theory closed. Run from the repo root.
python3 ep2.py -> EP2.json; KA1 re-evaluates EP1's frozen bound with this code."""
import json, math
from pathlib import Path
import numpy as np
D = Path('closure_2026_11_06/EP2_eps_phi_reachability')
c = json.loads(Path('campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json').read_text())['BAO+SN']
Z = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]); KEYS = ['0.0', '0.4', '0.7', '1.0', '1.5', '2.33']
A0 = {'canonical': 9.360324825027975e-11, 'alt': 1.1312035414413022e-10}
C_ = 299792458.0; H100 = 100e3 / 3.0856775814913673e22; KAPPA = 0.5
WM = 0.02236 + 0.1202; WR = 2.47e-5 * (1 + 0.2271 * 3.044)
z = np.round(np.arange(0, 2.33 + 1e-9, 0.001), 6)
zl = np.concatenate([z, np.geomspace(2.331, 1100, 2000)])
idx = np.clip(np.searchsorted(Z, z, side='right') - 1, 0, len(Z) - 2)


def omega_de0(f): return (8 * math.pi / 3) * (A0[f] / (KAPPA * C_)) ** 2 / H100 ** 2


def eps_lin(lo, hi, wm=WM, wr=WR, wk=0.0, drop_de=False, zz=z, ii=idx, ZZ=Z):
    """rho_DE linear on each interval from lo[i] (at Z[i]) to hi[i+1] (at Z[i+1]), clipped at 0; exact eps_phi."""
    slope = (hi[ii + 1] - lo[ii]) / (ZZ[ii + 1] - ZZ[ii])
    rde = np.clip(lo[ii] + slope * (zz - ZZ[ii]), 0, None)
    rt = wm * (1 + zz) ** 3 + wr * (1 + zz) ** 4 + wk * (1 + zz) ** 2 + (0 if drop_de else rde)
    return (1 + zz) * slope / (2 * rt)


def summ(e, zz=z):
    i = int(np.argmax(e)); return dict(max=float(e.max()), at_z=float(zz[i]), min=float(e.min()), reached=bool(e.max() >= 2))


out = dict(note='kappa = 1/2 FITTED; not theory closed', omega_m=WM, omega_r=WR)
# KA1: EP1's frozen bound and its numbers
nodes = np.array(c['P2']['nodes_free']); sd = np.array(c['posterior']['node_std']); wk, wb, wc = c['P2']['pbest'][6:9]
wkb = abs(c['posterior']['omega_k'][0]) + 2 * c['posterior']['omega_k'][1]
r1 = json.loads(Path('closure_2026_11_06/EP1_decelerating_slow_roots/REACH.json').read_text())
slope_w = ((nodes[idx + 1] + 2 * sd[idx + 1]) - (nodes[idx] - 2 * sd[idx])) / (Z[idx + 1] - Z[idx])
slope_b = (nodes[idx + 1] - nodes[idx]) / (Z[idx + 1] - Z[idx])
rlo = (wb + wc) * (1 + z) ** 3 - wkb * (1 + z) ** 2
k1 = dict(worst_max=float(((1 + z) * slope_w / (2 * rlo)).max()), bound_best_max=float(((1 + z) * slope_b / (2 * rlo)).max()),
          best_full_E2_max=float(((1 + z) * slope_b / (2 * ((wb + wc) * (1 + z) ** 3 + wk * (1 + z) ** 2 + np.interp(z, Z, nodes)))).max()),
          post_data=float(((1 + z) * slope_w / (2 * (rlo + np.clip(np.interp(z, Z, nodes - 2 * sd), 0, None)))).max()))
ref = dict(worst_max=r1['worst_max'], bound_best_max=r1['bound_best_max'], best_full_E2_max=r1['best_full_E2_max'],
           post_data=r1['post_data_worst_with_rhoDE_kept']['max'])
k1rel = max(abs(k1[x] - ref[x]) / abs(ref[x]) for x in ref)
out['KA1'] = dict(values=k1, EP1=ref, max_rel=k1rel, pass_=bool(k1rel <= 1e-12))
# H-CFG689 (footing-free): best and self-consistent worst-case history
out['H-CFG689'] = dict(best=summ(eps_lin(nodes, nodes, wm=wb + wc, wr=WR, wk=wk)),
                       worst=summ(eps_lin(nodes - 2 * sd, nodes + 2 * sd, wm=wb + wc, wr=WR, wk=wk - 2 * c['posterior']['omega_k'][1])))
a0q = {k: np.array(c['P3']['a0_node_q'][k]) for k in KEYS}
q = np.array([a0q[k] for k in KEYS])          # rows nodes, cols quantiles 2.5 16 50 84 97.5
F = {}
for f in A0:
    w0 = omega_de0(f); med0 = q[0, 2]
    rmed = w0 * (q[:, 2] / med0) ** 2; rlo_ = w0 * (q[:, 0] / med0) ** 2; rhi = w0 * (q[:, 4] / med0) ** 2
    flat = np.zeros_like(zl)                     # rho_DE' = 0 exactly
    w_ = lambda zz: -0.838 - 0.62 * zz / (1 + zz)
    rcpl = w0 * (1 + zl) ** (3 * (1 + -0.838 + -0.62)) * np.exp(-3 * -0.62 * zl / (1 + zl))
    ecpl = 3 * (1 + w_(zl)) * rcpl / (2 * (WM * (1 + zl) ** 3 + WR * (1 + zl) ** 4 + rcpl))
    # M1 planted kination clock
    A = WM / 64; rk = w0 + A * (1 + zl) ** 6
    em1 = (1 + zl) * 6 * A * (1 + zl) ** 5 / (2 * (WM * (1 + zl) ** 3 + WR * (1 + zl) ** 4 + rk))
    # M2: native median with slope x100 on [0.4, 0.7] (worst-case rule)
    hi2 = rhi.copy(); lo2 = rlo_.copy(); hi2[2] = lo2[1] + 100 * (rhi[2] - rlo_[1])
    F[f] = dict(omega_DE0=w0, **{'H-flat': dict(max=float(np.abs(flat).max()), reached=False, exact_zero=True),
                'H-native': dict(median=summ(eps_lin(rmed, rmed)), worst=summ(eps_lin(rlo_, rhi)),
                                 beyond_2p33='held constant: eps_phi = 0'),
                'H-CPL(reported)': dict(**summ(ecpl, zl), phantom_z=[float(zl[ecpl < 0].min()) if np.any(ecpl < 0) else None]),
                'MUTATE_M1_kination': summ(em1, zl), 'MUTATE_M2_slope100': summ(eps_lin(lo2, hi2))})
out['footings'] = F
out['KA2_flat_zero'] = all(F[f]['H-flat']['max'] == 0.0 for f in F)
out['KA3_reported'] = dict(omega_DE0_canonical=F['canonical']['omega_DE0'], CFG689_node0=float(nodes[0]))
graded = [out['H-CFG689']['best'], out['H-CFG689']['worst']] + [F[f]['H-native'][k] for f in F for k in ('median', 'worst')]
reached = any(g['reached'] for g in graded)
m1 = all(F[f]['MUTATE_M1_kination']['reached'] for f in F)
if not (out['KA1']['pass_'] and out['KA2_flat_zero'] and m1): label = 'NO VERDICT'
elif reached: label = 'REACHED (EP1 witness grade decides)'
else: label = 'NOT REACHED'
out.update(label=label, max_graded=max(g['max'] for g in graded), MUTATE_M1_bites=m1,
           MUTATE_M2_bites=all(F[f]['MUTATE_M2_slope100']['reached'] for f in F))
(D / 'EP2.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
