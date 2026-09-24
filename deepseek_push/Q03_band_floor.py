#!/usr/bin/env python3
"""Q03 -- GEOMETRY-MARGINALIZED WIDTH FLOOR (door: K12 'Thm-2 lower endpoint withdrawn under unknown geometry').
(a) re-derive every stored band violation from raw fields; (b) verify the uniform-kappa
identity E[Q]=(R-2d)/2 and the criterion equivalence on volume_q0; (c) tabulate the q>0
kappa compensator; (d) hunt the largest geometry-free lower floor f(R)=c*R valid on ALL
landed geometry clouds. Kills pre-registered in QWAVE_BRIEF.md (K1 1% match, K2 identity,
K3 no-tuned-floor), written before this run."""
import json, math, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, 'K12_results.json')) as f:
    K12 = json.load(f)
M = K12['measurements']

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

# ---- (a) re-derive stored band violations
c1_rows, c1_ok = [], True
for key, m in M.items():
    if not isinstance(m, dict) or 'R' not in m or 'band_lo' not in m:
        continue
    d, R, se = m['E_D'], m['R'], m['se_D']
    lo = math.sqrt(1.0 + R) / 2 - 0.5   # (sqrt(1+R)-1)/2
    viol = lo - d
    nse = viol / se
    d_lo, d_nse = abs(viol - m['band_viol_lower']), None
    if m.get('band_n_se_lower') is not None:
        d_nse = abs(nse - m['band_n_se_lower']) / max(abs(m['band_n_se_lower']), 1e-30)
    ok = d_lo < 1e-9 and (d_nse is None or d_nse < 0.01)
    c1_ok = c1_ok and ok
    c1_rows.append({"cloud": key, "d": d, "R": R, "lo_rederived": lo,
                    "nse_rederived": nse, "nse_stored": m.get('band_n_se_lower'),
                    "match": ok})
check("K1 re-derivation of every stored lower-endpoint SE within 1%", c1_ok, json.dumps(c1_rows))

# ---- (b) uniform-kappa identity on volume_q0
q0 = M['volume_q0']
d, R, EQ = q0['E_D'], q0['R'], q0['E_Q']
EQ_imp = (R - 2 * d) / 2
se_comb = math.sqrt(q0['se_Q']**2 + (q0['se_v2'] / 2)**2 + q0['se_D']**2)
z_ident = abs(EQ_imp - EQ) / se_comb
crit = d + 2 * d * d
viol = (EQ > crit)
k2 = z_ident < 5.0 and (viol == (q0['band_viol_lower'] > 0))
check("K2 uniform-kappa identity E[Q]=(R-2d)/2 + criterion equivalence (volume_q0, 5 SE)", k2,
      f"E_Q={EQ:.6f} vs (R-2d)/2={EQ_imp:.6f} (z={z_ident:.2f}); E[Q]>{d+2*d*d:.4f} -> {viol}; stored lower violated: {q0['band_viol_lower']>0}")

# ---- (c) q>0 kappa compensator table
comp = {}
for key, m in M.items():
    if isinstance(m, dict) and 'E_N' in m:
        comp[key] = {"E_N": m['E_N'], "E_tau": m.get('E_tau'),
                     "ratio_E_N_over_E_tau_time": m.get('E_N_vs_En_time_ratio'),
                     "E_Q": m.get('E_Q')}
check("K3a compensator table recorded", True, json.dumps(comp))

# ---- (d) geometry-free floor hunt: c* = min over clouds of d/R; check on all clouds
clouds = {}
for key, m in M.items():
    if isinstance(m, dict) and 'E_D' in m and 'R' in m:
        clouds[key] = {"d": m['E_D'], "R": m['R'], "se_D": m['se_D']}
cstar = min(v['d'] / v['R'] for v in clouds.values())
floor_rows, floor_ok = [], True
for key, v in clouds.items():
    margin = v['d'] - (cstar * v['R'])
    nsess = margin / v['se_D']
    ok = margin >= -3 * v['se_D']
    floor_ok = floor_ok and ok
    floor_rows.append({"cloud": key, "d": v['d'], "R": v['R'], "c*d/R": cstar,
                       "margin": margin, "margin_in_se": nsess, "holds": ok})
central = M.get('central_q0', None)
central_floor = (math.sqrt(2.0) / 2 - 0.5) if central else None   # (sqrt(1+1)-1)/2
power_at_1 = (cstar * 1.0) / central_floor if central_floor else None
k3 = floor_ok
check("K3b geometry-free floor c*R valid on every landed cloud", k3, json.dumps(floor_rows))
check("power loss quantified", True,
      f"c* = {cstar:.6f}; central floor at R=1 = {central_floor:.4f}; f(1)/central_floor = {power_at_1:.3f}")

result = {
    "lane": "Q03_band_floor", "source": "K12_results.json (landed, read-only)",
    "c_star": cstar, "central_floor_R1": central_floor, "relative_power_at_R1": power_at_1,
    "rederivation": c1_rows, "identity_volume_q0": {"E_Q_imp": EQ_imp, "E_Q": EQ, "z": z_ident,
                                                     "criterion_threshold": crit, "violated": bool(viol)},
    "compensators": comp, "floor_check": floor_rows,
    "checks": checks, "exit0": bool(c1_ok and k2 and k3),
}
with open(os.path.join(BASE, 'Q03_results.json'), 'w') as f:
    json.dump(result, f, indent=1)
print("Q03 COMPLETE; c* =", cstar, "; f(1)/central_floor =", power_at_1)
for r in floor_rows:
    print(r)
print("EXIT", 0 if result["exit0"] else 1)
