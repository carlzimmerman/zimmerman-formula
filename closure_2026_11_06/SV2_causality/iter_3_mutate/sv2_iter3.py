"""SV2 iter_3: MUTATE of the repair class (sign flips). Criteria: iter_3_mutate/FROZEN_CRITERIA.md (7d31bb0ac2).
Kappa = 1/2 FITTED; not theory closed. Single thread. From the repo root:
    nice -n 15 python3 closure_2026_11_06/SV2_causality/iter_3_mutate/sv2_iter3.py   -> sv2_iter3.json / .out
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mpmath as mp
import sv2_common as C

mp.mp.dps = 40
D = Path(__file__).resolve().parent
T0 = time.time()
cv, Gv = C.cv, C.Gv
K = 4 * mp.pi * Gv
beta = mp.mpf("1.4e-15"); alpha = 2 * beta; bl = alpha            # window edge member (alpha = 2 beta, c_k = c)
out = {"criteria": "7d31bb0ac2", "member": {"alpha": float(alpha), "beta": float(beta), "beta+lambda": float(bl)},
       "note": "kappa = 1/2 FITTED; not theory closed"}
res = {}
ok = True
for fname, F in C.FOOT.items():
    Pi = mp.mpf(F["rho0"]) * C.Msun / C.pc ** 3
    x = mp.mpf(F["x"]); Ls = mp.mpf(F["Lstar_pc"]) * C.pc
    gam = K * Ls ** 2 / 2
    r = {}
    for dn, f in (("e", (1 + x) ** 2), ("perp", 1 + x)):
        akin = lambda k, a: 1 / (K * f + gam * k * k) + a / (2 * K)
        # M1: alpha -> -alpha
        kg_closed = mp.sqrt(2) * mp.sqrt(2 / alpha - f) / Ls          # 1/(f + Ls^2 k^2/2) = alpha/2
        kg_num = mp.findroot(lambda k: akin(k, -alpha), kg_closed)
        m1 = bool(akin(2 * kg_num, -alpha) < 0 and akin(kg_num / 2, -alpha) > 0 and akin(kg_num / 2, alpha) > 0
                  and akin(10 * kg_num, alpha) > 0)
        r[dn] = {"k_ghost_per_m": mp.nstr(kg_num, 8), "k_ghost_closed_form": mp.nstr(kg_closed, 8),
                 "ghost_scale_m": mp.nstr(1 / kg_num, 6), "M1_ghost_appears_only_when_flipped": m1}
        ok &= m1
    # M2: beta+lambda -> -(beta+lambda)
    l2 = bl * cv ** 2 / (2 * K)
    kgr = mp.sqrt(Pi / l2)                                            # = sqrt(2 K Pi / (|b+l| c^2))
    grad = lambda k, s: Pi + s * l2 * k * k
    m2 = bool(grad(2 * kgr, -1) < 0 and grad(kgr / 2, -1) > 0 and grad(10 * kgr, +1) > 0)
    # growth rate of the unstable mode at 10 k_grad (omega^2 < 0), using the kinetic coefficient at that k (perp)
    k10 = 10 * kgr
    om2 = grad(k10, -1) / (1 / (K * (1 + x) + gam * k10 ** 2) + alpha / (2 * K))
    # M3: instantaneous mode stays under both flips
    an = lambda a: 2 * x / (a * (1 + x) ** 2 + 2)
    m3 = bool(an(-alpha) > 0 and an(alpha) > 0)
    r.update({"k_grad_per_m": mp.nstr(kgr, 8), "grad_scale_m": mp.nstr(1 / kgr, 6), "grad_scale_pc": float(1 / kgr / C.pc),
              "M2_gradient_instability_only_when_flipped": m2,
              "growth_rate_at_10k_grad_per_s": mp.nstr(mp.sqrt(-om2), 6) if om2 < 0 else None,
              "M3_anisotropy_alpha_flipped": mp.nstr(an(-alpha), 12), "M3_anisotropy_member": mp.nstr(an(alpha), 12),
              "M3_instantaneous_kept": m3})
    ok &= m2 and m3
    res[fname] = r
out["flips"] = res
out["Lean_MUTATE_twins"] = "SV2_causality_MUTATE.out and SV2_repair_MUTATE.out: every planted claim fails (exit 1); read in the README"
out["label"] = "BITES" if ok else "DOES NOT BITE"
out["runtime_s"] = round(time.time() - T0, 2)
(D / "sv2_iter3.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
L = [f"SV2 iter_3 (criteria 7d31bb0ac2): member alpha = 2 beta = {float(alpha):.2e}, beta + lambda = {float(bl):.2e}"]
for fn, r in res.items():
    L.append(f"{fn}: M1 alpha flipped: ghost above k = {r['e']['k_ghost_per_m']} (e) / {r['perp']['k_ghost_per_m']} (perp) 1/m, "
             f"scale {r['e']['ghost_scale_m']} m; healthy member ghost-free: {r['e']['M1_ghost_appears_only_when_flipped'] and r['perp']['M1_ghost_appears_only_when_flipped']}")
    L.append(f"   M2 beta+lambda flipped: gradient-unstable above k = {r['k_grad_per_m']} 1/m (scale {r['grad_scale_pc']:.3g} pc), "
             f"growth at 10 k_grad {r['growth_rate_at_10k_grad_per_s']} 1/s; only when flipped {r['M2_gradient_instability_only_when_flipped']}")
    L.append(f"   M3 anisotropy (alpha flipped) {r['M3_anisotropy_alpha_flipped']}, member {r['M3_anisotropy_member']}: instantaneous kept {r['M3_instantaneous_kept']}")
L.append(f"LABEL {out['label']}; runtime {out['runtime_s']} s")
(D / "sv2_iter3.out").write_text("\n".join(L) + "\n")
print("\n".join(L))
