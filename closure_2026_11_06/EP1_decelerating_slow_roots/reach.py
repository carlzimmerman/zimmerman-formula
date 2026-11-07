"""EP1 REACHED / NOT REACHED: eps_phi(z) = (1+z) rho_phi'(z) / (2 rho_tot(z)) on CFG689's measured rho_DE(z) (primary,
BAO+SN, curvature free; committed cfg689.json). Lines: CRITERIA.md (d8fc918584). Kappa = 1/2 FITTED; not theory closed."""
import json
from pathlib import Path
import numpy as np
D = Path('closure_2026_11_06/EP1_decelerating_slow_roots')
c = json.loads(Path('campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json').read_text())['BAO+SN']
nodes = np.array(c['P2']['nodes_free']); sd = np.array(c['posterior']['node_std']); Z = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33])
wk, wb, wc = c['P2']['pbest'][6:9]
wk_bound = abs(c['posterior']['omega_k'][0]) + 2 * c['posterior']['omega_k'][1]
z = np.round(np.arange(0, 2.33 + 1e-9, 0.001), 6)
rho_lo = (wb + wc) * (1 + z) ** 3 - wk_bound * (1 + z) ** 2          # radiation, neutrinos, rho_DE dropped (raises the bound)
assert np.all(rho_lo > 0)
idx = np.clip(np.searchsorted(Z, z, side='right') - 1, 0, len(Z) - 2)
slope_best = (nodes[idx + 1] - nodes[idx]) / (Z[idx + 1] - Z[idx])
slope_worst = ((nodes[idx + 1] + 2 * sd[idx + 1]) - (nodes[idx] - 2 * sd[idx])) / (Z[idx + 1] - Z[idx])
eb = (1 + z) * slope_best / (2 * rho_lo); ew = (1 + z) * slope_worst / (2 * rho_lo)
# exact-best (reported): full E^2 with the best nodes, still without radiation/neutrinos
rho_best = (wb + wc) * (1 + z) ** 3 + wk * (1 + z) ** 2 + np.interp(z, Z, nodes)
ex = (1 + z) * slope_best / (2 * rho_best)
iw, ib = int(np.argmax(ew)), int(np.argmax(eb))
label = 'NOT REACHED on the measured span' if ew.max() < 2 else ('REACHED' if eb.max() >= 2 else 'NOT DECIDED by the record data')
out = dict(label=label, line=2.0, worst_max=float(ew.max()), worst_at_z=float(z[iw]), margin_worst=float(2 - ew.max()),
           bound_best_max=float(eb.max()), bound_best_at_z=float(z[ib]), best_full_E2_max=float(ex.max()), best_full_E2_at_z=float(z[int(np.argmax(ex))]),
           best_full_E2_min=float(ex.min()), negative_slope_intervals=[[float(Z[i]), float(Z[i + 1])] for i in range(5) if nodes[i + 1] < nodes[i]],
           per_interval=[dict(z=[float(Z[i]), float(Z[i + 1])], worst_max=float(ew[idx == i].max()), best_max=float(eb[idx == i].max()))
                         for i in range(5)],
           inputs=dict(nodes=nodes.tolist(), node_sd=sd.tolist(), omega_b=wb, omega_c=wc, omega_k_best=wk, omega_k_bound=wk_bound),
           fixture_family=dict(lambda_=2.0, attractor_eps_phi=2.0, eps_total_min=2.0, q_min=1.0, accelerates=False),
           necessary_condition_beyond_2p33='Omega_phi >= 2/3 and w_phi >= 1/3 (eps_phi = (3/2) Omega_phi (1 + w_phi) = 2, w_phi <= 1, Omega_phi <= 1)',
           note='kappa = 1/2 FITTED; not theory closed')
# POST-DATA (reported only, not the frozen label): keep rho_DE in rho_tot at its own node - 2 sd lower bound (clipped at 0)
rho_lo_pd = rho_lo + np.clip(np.interp(z, Z, nodes - 2 * sd), 0, None)
ew_pd = (1 + z) * slope_worst / (2 * rho_lo_pd)
out['post_data_worst_with_rhoDE_kept'] = dict(max=float(ew_pd.max()), at_z=float(z[int(np.argmax(ew_pd))]), below_2=bool(ew_pd.max() < 2))
(D / 'REACH.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('inputs',)}, indent=1))
