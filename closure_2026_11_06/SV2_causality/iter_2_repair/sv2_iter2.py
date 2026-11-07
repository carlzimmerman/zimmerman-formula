"""SV2 iter_2: can the standard khronometric terms remove the instantaneous mode? Criteria: iter_2_repair/FROZEN_CRITERIA.md
(7d31bb0ac2). Kappa = 1/2 FITTED; not theory closed. Single thread. From the repo root:
    nice -n 15 python3 closure_2026_11_06/SV2_causality/iter_2_repair/sv2_iter2.py    -> sv2_iter2.json / .out
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sympy as sp
from sympy.calculus.euler import euler_equations
import mpmath as mp
import sv2_common as C

D = Path(__file__).resolve().parent
T0 = time.time()
out = {"criteria": "7d31bb0ac2", "note": "kappa = 1/2 FITTED; not theory closed"}

# ---------------------------------------------------------------- derivation: EL of L2, plane waves, dispersion
t, X, Y, Z = sp.symbols("t x y z", real=True)
K, gam, Pi, al, l2, xb = sp.symbols("K gamma Pi alpha lambda2", positive=True) + (sp.Symbol("x_bg", nonnegative=True),)
al = sp.Symbol("alpha", real=True); l2 = sp.Symbol("lambda2", real=True)   # signs free here; health graded below
co = (X, Y, Z)
sig = sp.Function("sigma")(t, X, Y, Z)
P = [sp.Function(f"P{i}")(t, X, Y, Z) for i in (1, 2, 3)]
Mt = (1 + xb) * (sp.eye(3) + xb * sp.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]]))
Xi = -sp.diff(sig, t)                                            # phi frozen: homogeneous leaf modes
gXi = [sp.diff(Xi, c) for c in co]
divP = sum(sp.diff(P[i], co[i]) for i in range(3))
lap = lambda f: sum(sp.diff(f, c, 2) for c in co)
Pv = sp.Matrix(P)
L2 = (sum(P[i] * gXi[i] for i in range(3)) - gam / 2 * divP ** 2 - K / 2 * (Pv.T * Mt * Pv)[0]
      - Pi / 2 * sum(sp.diff(sig, c) ** 2 for c in co)
      + al / (4 * K) * sum(g ** 2 for g in gXi) - l2 / 2 * lap(sig) ** 2)
eqs = euler_equations(L2, [sig] + P, [t, X, Y, Z])
w = sp.Symbol("omega", positive=True)
kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
amp = sp.symbols("A0 A1 A2 A3")
ph = sp.exp(sp.I * (kx * X + ky * Y + kz * Z - w * t))
subs = {sig: amp[0] * ph, P[0]: amp[1] * ph, P[1]: amp[2] * ph, P[2]: amp[3] * ph}
rows = []
for e in eqs:
    ex = sp.expand(sp.simplify((e.lhs - e.rhs).subs(subs).doit() / ph))
    rows.append([sp.expand(ex.coeff(a)) for a in amp])
Mlin = sp.Matrix(rows)
det = sp.factor(Mlin.det())
w2 = sp.Symbol("w2", positive=True)
detw = sp.expand(det.subs(w, sp.sqrt(w2)))
roots = [r for r in sp.solve(detw, w2) if r != 0]
assert len(roots) == 1, roots
om2 = sp.simplify(roots[0])
# expected closed form (criteria): (Pi + lambda'' k^2)/(1/Z + alpha/(2K)), Z = K f + gamma k^2
kk2 = kx ** 2 + ky ** 2 + kz ** 2
kMk = (sp.Matrix([kx, ky, kz]).T * Mt.inv() * sp.Matrix([kx, ky, kz]))[0]
Zs = K * kk2 / kMk + gam * kk2
expected = (Pi + l2 * kk2) / (1 / Zs + al / (2 * K))
form_ok = sp.simplify(om2 - expected) == 0
out["derivation"] = {"omega2": str(om2), "matches_closed_form": bool(form_ok),
                     "P_equations_contain_omega": bool(any(r.has(w) for r in rows[1:] for r in r[1:]))}

# ---------------------------------------------------------------- R1: k -> 0 limit, e vs perp
s = sp.Symbol("s", positive=True)
o_e = sp.limit(om2.subs({kx: 0, ky: 0, kz: s}), s, 0)
o_p = sp.limit(om2.subs({kx: s, ky: 0, kz: 0}), s, 0)
aniso = sp.factor(sp.simplify(o_e / o_p - 1))
aniso_x0 = sp.simplify(aniso.subs(xb, 0))
# positivity on the healthy region alpha >= 0, x > 0
ap = sp.Symbol("a_p", nonnegative=True); xp = sp.Symbol("x_p", positive=True)
aniso_h = sp.factor(aniso.subs({al: ap, xb: xp}))
aniso_pos = bool(aniso_h.is_positive)
out["R1"] = {"omega0^2_along_e": str(sp.factor(o_e)), "omega0^2_perp": str(sp.factor(o_p)),
             "omega0e/omega0perp - 1": str(aniso), "independent_of_lambda": not aniso.has(l2),
             "positive_for_all_alpha>=0_x>0 (sympy)": aniso_pos,
             "control_x0_value": str(aniso_x0), "control_x0_REMOVED_CANDIDATE": aniso_x0 == 0,
             "label": "KEPT" if aniso_pos else "UNDECIDED"}

# ---------------------------------------------------------------- R2: c_k
ck_e = sp.limit(om2.subs({kx: 0, ky: 0, kz: s}) / s ** 2, s, sp.oo)
ck_p = sp.limit(om2.subs({kx: s, ky: 0, kz: 0}) / s ** 2, s, sp.oo)
cc, bl = sp.symbols("c beta_plus_lambda", positive=True)
ck_std = sp.simplify(ck_e.subs(l2, bl * cc ** 2 / (2 * K)))
out["R2"] = {"c_k^2_e": str(ck_e), "c_k^2_perp": str(ck_p), "isotropic": bool(sp.simplify(ck_e - ck_p) == 0),
             "in_standard_units": str(ck_std),
             "known_answer_(beta+lambda)c^2/alpha": bool(sp.simplify(ck_std - bl * cc ** 2 / al) == 0),
             "alpha_0_limit": str(sp.limit(om2.subs({al: 0, kx: 0, ky: 0, kz: s}) / s ** 2, s, sp.oo))}

# ---------------------------------------------------------------- R3: health (kinetic, gradient)
akin = sp.simplify(1 / Zs + al / (2 * K))
out["R3"] = {"kinetic_coefficient": str(akin),
             "kinetic_large_k_limit": str(sp.limit(akin.subs({kx: 0, ky: 0, kz: s}), s, sp.oo)),
             "gradient_coefficient": "Pi + lambda'' k^2",
             "rule": "alpha >= 0 and beta+lambda >= 0 healthy for all k; alpha < 0 ghost and beta+lambda < 0 gradient-unstable at large k (Lean SV2_repair)"}

# ---------------------------------------------------------------- R1b: lambda channel and alpha channel sizes
mp.mp.dps = 50
cv, Gv = C.cv, C.Gv
Kn = 4 * mp.pi * Gv
R1b = {}
for fname, F in C.FOOT.items():
    Pi_v = mp.mpf(F["rho0"]) * C.Msun / C.pc ** 3
    x = mp.mpf(F["x"])
    rr = []
    for dn, dvec in C.DIRS.items():
        xo = [mp.mpf(1e10) * mp.mpf(c) for c in dvec]
        res = C.response(xo, x, mp.mpf(1), Pi_v, Gv, cv, mp.mpf(1000), mp.mpf(1), C.e_s, want=("dv", "dvlap"))
        dv = [mp.re(c) for c in res["dv"]]; dl = [mp.re(c) for c in res["dvlap"]]
        ndv = mp.sqrt(sum(c * c for c in dv)); ndl = mp.sqrt(sum(c * c for c in dl))
        per_unit = ndl * cv ** 2 / (2 * Kn)                      # |dv_lambda| per unit (beta+lambda)
        floor = C.EPS * mp.sqrt(sum(c * c for c in res["dvlap_abs"]))
        rr.append({"dir": dn, "abs_dv_AC18": float(ndv), "abs_dv_lambda_per_unit_beta+lambda": float(per_unit),
                   "ratio_per_unit": float(per_unit / ndv), "dvlap_over_floor": float(ndl / floor),
                   "ratio_at_beta+lambda=2.8e-15": float(per_unit * mp.mpf("2.8e-15") / ndv)})
    fmax = (1 + x) ** 2
    R1b[fname] = {"t_s": 1, "r_m": 1e10, "rows": rr,
                  "alpha_channel_symbol_rel_bound_at_alpha_2.5e-5": float(mp.mpf("2.5e-5") * fmax / 2),
                  "alpha_channel_symbol_rel_bound_at_alpha_2.8e-15": float(mp.mpf("2.8e-15") * fmax / 2),
                  "scale_(c t_dyn/r)^2/2": float((cv / mp.sqrt(Kn * Pi_v) / mp.mpf(1e10)) ** 2 / 2)}
out["R1b"] = R1b

# ---------------------------------------------------------------- R4: window (literature formulas, provisional)
out["R4_window"] = {"beta": "(-6e-15, 1.4e-15) from c_T^2 = 1/(1-beta), GW170817 -3e-15 < c_T - 1 < 7e-16",
                    "alpha_minus_2beta": "|alpha - 2 beta| <= 2.5e-5 from alpha1 = 4(alpha-2beta)/(beta-1), |alpha1| <= 1e-4 (LLR)",
                    "alpha2": "proportional to (alpha - 2 beta) (literature); zero on that line",
                    "health": "alpha >= 0, beta + lambda >= 0",
                    "finite_c_k": "alpha > 0; c_k^2 = (beta+lambda) c^2/alpha; c_k <= c needs beta+lambda <= alpha",
                    "edge_alpha=2beta": "alpha <= 2.8e-15 on the alpha = 2 beta line; alpha <= 2.5e-5 off it (alpha1 only)",
                    "status": "LITERATURE, not re-derived on the v3s equations; the R1 verdict does not use it"}

# ---------------------------------------------------------------- R5: static law
yv = sp.Symbol("y", positive=True)
r5_bl = sp.simplify(lap(sp.Function("s0")(t)) ** 2) == 0     # beta, lambda terms on static leaves (v = 0)
mp.mp.dps = 30
dmax = mp.mpf(0); mu_min = mp.inf
alpha_e = mp.mpf("2.5e-5")
for i in range(601):
    gn = mp.mpf(10) ** (-3 + 6 * mp.mpf(i) / 600)               # g_N / a0 with measured G
    y0 = (gn + mp.sqrt(gn * gn + 4 * gn)) / 2                   # mu(y) y = g_N
    f = lambda yy: (yy / (1 + yy) - alpha_e / 2) * yy - gn * (1 - alpha_e / 2)
    y1 = mp.findroot(f, y0)
    dmax = max(dmax, abs(mp.log10(y1 / y0)))
    mu_min = min(mu_min, y1 / (1 + y1) - alpha_e / 2)
out["R5"] = {"beta_lambda_static_zero": bool(r5_bl), "alpha_edge": 2.5e-5,
             "max_dex_change_of_g_GN_absorbed": float(dmax), "min_mu_minus_alpha/2": float(mu_min),
             "pass_0.01_dex": bool(dmax <= 0.01 and mu_min > 0),
             "footings": "identical in y = g/a0 (a0 is only the scale): canonical and alt both carry this number"}

# ---------------------------------------------------------------- label
R1_kept = out["R1"]["label"] == "KEPT"
out["label"] = "NO REPAIR IN CLASS" if R1_kept else "UNDECIDED (see R1)"
out["controls_ok"] = bool(form_ok and out["R1"]["control_x0_REMOVED_CANDIDATE"] and out["R2"]["known_answer_(beta+lambda)c^2/alpha"])
out["runtime_s"] = round(time.time() - T0, 1)
(D / "sv2_iter2.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
L = ["SV2 iter_2 (criteria 7d31bb0ac2)",
     f"derivation: omega^2 matches (Pi + lambda'' k^2)/(1/Z + alpha/2K): {form_ok}; P eqs carry omega: {out['derivation']['P_equations_contain_omega']}",
     f"R1: omega0^2(e) = {out['R1']['omega0^2_along_e']}; omega0^2(perp) = {out['R1']['omega0^2_perp']}",
     f"    anisotropy = {aniso}; lambda-free {out['R1']['independent_of_lambda']}; positive for alpha>=0, x>0: {aniso_pos}; x=0 control -> {aniso_x0} (REMOVED-CANDIDATE {aniso_x0 == 0}); R1 {out['R1']['label']}",
     f"R2: c_k^2 (e) = {ck_e}, (perp) = {ck_p}; standard units {ck_std}; known answer {out['R2']['known_answer_(beta+lambda)c^2/alpha']}; alpha = 0: {out['R2']['alpha_0_limit']}",
     f"R3: kinetic {akin}; large-k {out['R3']['kinetic_large_k_limit']}"]
for fn, b in R1b.items():
    L.append(f"R1b {fn} (t 1 s, r 1e10 m): (c t_dyn/r)^2/2 = {b['scale_(c t_dyn/r)^2/2']:.3e}; alpha-channel symbol bound {b['alpha_channel_symbol_rel_bound_at_alpha_2.5e-5']:.2e} (alpha 2.5e-5), {b['alpha_channel_symbol_rel_bound_at_alpha_2.8e-15']:.2e} (alpha 2.8e-15)")
    for r in b["rows"]:
        L.append(f"   {r['dir']:7s} |dv_AC18| {r['abs_dv_AC18']:.3e}  |dv_lambda|/unit(beta+lambda) {r['abs_dv_lambda_per_unit_beta+lambda']:.3e}  ratio/unit {r['ratio_per_unit']:.3e}  at 2.8e-15: {r['ratio_at_beta+lambda=2.8e-15']:.3e}  floor-ratio {r['dvlap_over_floor']:.1e}")
L.append(f"R5: beta/lambda static zero {r5_bl}; alpha 2.5e-5 max change {float(dmax):.2e} dex, min(mu - alpha/2) {float(mu_min):.2e}; pass {out['R5']['pass_0.01_dex']}")
L.append(f"LABEL {out['label']}; controls ok {out['controls_ok']}; runtime {out['runtime_s']} s")
(D / "sv2_iter2.out").write_text("\n".join(L) + "\n")
print("\n".join(L))
