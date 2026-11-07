"""SV2 iter_1: is AC18's outside-cone signal physical? Criteria: iter_1_physical/FROZEN_CRITERIA.md (7d31bb0ac2).

Kappa = 1/2 FITTED; not theory closed. Single thread. From the repo root:
    nice -n 15 python3 closure_2026_11_06/SV2_causality/iter_1_physical/sv2_iter1.py          -> sv2_iter1.json/.out
    SV2_MUTATE=1 nice -n 15 python3 ...                                                      -> sv2_iter1_MUTATE.*
"""
import json, os, sys, time, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sympy as sp
import mpmath as mp
import sv2_common as C

MUTATE = os.environ.get("SV2_MUTATE") == "1"
D = Path(__file__).resolve().parent
T0 = time.time()
mp.mp.dps = 50
out = {"mode": "MUTATE_hyperbolic_leaf" if MUTATE else "main", "criteria": "7d31bb0ac2",
       "note": "kappa = 1/2 FITTED; not theory closed"}
cv, Gv = C.cv, C.Gv
K = 4 * mp.pi * Gv
m, vsv = mp.mpf(1000), mp.mpf(1)


def tidal(res):
    """E_ij = 4 pi G (4 Q_ij - delta_ij dq), real part; floor from the sum of |terms|."""
    Q = [[mp.re(res["Q"][i][j]) for j in range(3)] for i in range(3)]
    Qa = res["Q_abs"]
    dq = sum(Q[l][l] for l in range(3)); dqa = sum(Qa[l][l] for l in range(3))
    E = [[4 * mp.pi * Gv * (4 * Q[i][j] - (dq if i == j else 0)) for j in range(3)] for i in range(3)]
    Ea = [[4 * mp.pi * Gv * (4 * Qa[i][j] + (dqa if i == j else 0)) for j in range(3)] for i in range(3)]
    return E, Ea, dq


def maxabs(M):
    return max(abs(M[i][j]) for i in range(3) for j in range(3))


# ---------------------------------------------------------------- Q1 / Q2 rows
F1_coef = {}
A = {}
for fname, F in C.FOOT.items():
    Pi_v = mp.mpf(F["rho0"]) * C.Msun / C.pc ** 3
    xb = mp.mpf(F["x"])
    rows = []
    for tsec, rm in C.GRID:
        tsec, rm = mp.mpf(tsec), mp.mpf(rm)
        for dn, dvec in C.DIRS.items():
            xo = [rm * mp.mpf(c) for c in dvec]
            row = {"t_s": float(tsec), "r_m": float(rm), "dir": dn, "ct_over_r": float(cv * tsec / rm)}
            if MUTATE:
                cmax = cv / mp.sqrt(1 + xb)
                t_arr = min(tq + (rm - cv * tq) / cmax for tq in [tsec * j / 200 for j in range(201)])
                zero = tsec < t_arr
                row.update({"mutant_earliest_arrival_s": float(t_arr), "E_max_abs": 0.0 if zero else None,
                            "D1": not zero, "D2": not zero})
                rows.append(row); continue
            r1 = C.response(xo, xb, tsec, Pi_v, Gv, cv, m, vsv, C.e_s)
            r2 = C.response(xo, xb, tsec, Pi_v, Gv, cv, m, vsv, [-c for c in C.e_s])
            E1, Ea1, dq1 = tidal(r1)
            E2, Ea2, dq2 = tidal(r2)
            floor1 = C.EPS * maxabs(Ea1)
            diff = [[E1[i][j] - E2[i][j] for j in range(3)] for i in range(3)]
            floor2 = C.EPS * (maxabs(Ea1) + maxabs(Ea2))
            ev = mp.eigsy(mp.matrix(E1))[0]
            evmax = max(abs(ev[i]) for i in range(3))
            dvd = [mp.re(c) for c in r1["dv_dip"]]
            ndvd = mp.sqrt(sum(c * c for c in dvd))
            ndv = mp.sqrt(sum(mp.re(c) ** 2 for c in r1["dv"]))
            coefC = ndvd * rm ** 5 / (K * Pi_v * Gv * m * cv ** 2 * vsv * tsec ** 6)
            F1_coef.setdefault((fname, dn), []).append(coefC)
            row.update({"E_ij_s^-2": [[mp.nstr(E1[i][j], 6) for j in range(3)] for i in range(3)],
                        "E_eig_max_abs_s^-2": float(evmax), "E_max_abs": float(maxabs(E1)),
                        "E_over_floor": float(maxabs(E1) / floor1),
                        "E_flip_diff_over_floor": float(maxabs(diff) / floor2),
                        "strain_1m_pair_after_t": float(evmax * tsec ** 2 / 2),
                        "dq_kg_m3": mp.nstr(dq1, 6), "c2_dq_J_m3": mp.nstr(cv ** 2 * dq1, 6),
                        "abs_dv_m_s": float(ndv), "dipole_coef_C": mp.nstr(coefC, 25),
                        "D1": bool(maxabs(E1) > 1e6 * floor1), "D2": bool(maxabs(diff) > 1e6 * floor2)})
            rows.append(row)
    td = 1 / mp.sqrt(4 * mp.pi * Gv * Pi_v)
    A[fname] = {"Pi_kg_m3": mp.nstr(Pi_v, 6), "x_bg": float(xb), "t_dyn_s": mp.nstr(td, 6),
                "t_dyn_Myr": float(td / (mp.mpf("3.15576e13"))), "rows": rows}
out["Q1_rows"] = A

# ---------------------------------------------------------------- F1, F2, F3 (main mode)
if not MUTATE:
    f1 = {}
    for (fname, dn), cs in F1_coef.items():
        spread = max(abs(c - cs[0]) / abs(cs[0]) for c in cs)
        f1[f"{fname}:{dn}"] = {"C": mp.nstr(cs[0], 12), "rel_spread_over_cells": float(spread)}
    F1_ok = all(v["rel_spread_over_cells"] <= 1e-20 for v in f1.values())
    # F2: Pi -> 2 Pi at (1 s, 1e10 m)
    f2 = []
    for fname, F in C.FOOT.items():
        Pi_v = mp.mpf(F["rho0"]) * C.Msun / C.pc ** 3; xb = mp.mpf(F["x"])
        for dn, dvec in C.DIRS.items():
            xo = [mp.mpf(1e10) * mp.mpf(c) for c in dvec]
            a = C.response(xo, xb, mp.mpf(1), Pi_v, Gv, cv, m, vsv, C.e_s, want=("dv",))
            b = C.response(xo, xb, mp.mpf(1), 2 * Pi_v, Gv, cv, m, vsv, C.e_s, want=("dv",))
            na = mp.sqrt(sum(mp.re(c) ** 2 for c in a["dv"])); nb = mp.sqrt(sum(mp.re(c) ** 2 for c in b["dv"]))
            f2.append({"footing": fname, "dir": dn, "ratio": mp.nstr(nb / na, 25), "dev": float(abs(nb / na - 2))})
    F2_ok = all(r["dev"] <= 1e-20 for r in f2)
    gam = sp.symbols("gamma", positive=True)
    F3_ok = bool(sp.expand(gam * C.k2 * C.ghat).is_polynomial(C.kx, C.ky, C.kz))
    Cmax = {fn: max(abs(c) for (f, d), cs in F1_coef.items() if f == fn for c in cs) for fn in C.FOOT}
    bound = {}
    for fname, F in C.FOOT.items():
        Pi_v = mp.mpf(F["rho0"]) * C.Msun / C.pc ** 3
        td = 1 / mp.sqrt(4 * mp.pi * Gv * Pi_v)
        bound[fname] = {"C_max": mp.nstr(Cmax[fname], 8),
                        "bound_formula": "|dv| <= C_max (t/t_dyn)^2 G m v_s/(c^3 t)  (r > c t, leading order, t << t_dyn)",
                        "bound_at_t_1s_m_s": mp.nstr(Cmax[fname] * (1 / td) ** 2 * Gv * m * vsv / cv ** 3, 6)}
    out["F1"] = f1; out["F2"] = f2; out["F3_gamma_part_polynomial_local"] = bool(F3_ok)
    out["F_bound"] = bound
    FORCED = bool(F1_ok and F2_ok and F3_ok)
    out["FORCED"] = FORCED

# ---------------------------------------------------------------- KA1 / KA2
out["KA1_x0_H_offorigin_zero"] = bool(sp.simplify(C.H.subs(C.xs, 0)) == 0)
out["KA2_Pi0_g_zero"] = bool(sp.simplify(C.ghat.subs(C.Pi_, 0)) == 0)

# ---------------------------------------------------------------- Q3 paradox sweep (P2, P3)
def fib_dirs(n):
    pts = []
    for i in range(n):
        zz = 1 - 2 * (i + mp.mpf(1) / 2) / n
        rr = mp.sqrt(1 - zz * zz); ph = i * mp.pi * (3 - mp.sqrt(5))
        pts.append((rr * mp.cos(ph), rr * mp.sin(ph), zz))
    return pts

dirs26 = fib_dirs(26)
min_ratio = mp.inf; n_backward = 0; n_loops = 0
for wb in ["0", "0.5", "0.9", "0.99", "0.999999"]:
    wmag = mp.mpf(wb)
    for wd in dirs26:
        w = [wmag * c for c in wd]                         # emitter velocity / c, khronon frame
        for nd in dirs26:
            L = mp.mpf(1)
            # instantaneous leg at tau = 0 from emitter (origin) to relay at L n; luminal return to x_e(t) = w c t
            # solve |w t - L n| = t (c = 1): (1 - w^2) t^2 + 2 (w.n) L t - L^2 = 0, positive root
            wn = sum(w[i] * nd[i] for i in range(3)); w2 = sum(c * c for c in w)
            if w2 == 0:
                tstar = L
            else:
                tstar = (-wn * L + mp.sqrt((wn * L) ** 2 + (1 - w2) * L ** 2)) / (1 - w2)
            n_loops += 1
            min_ratio = min(min_ratio, tstar / L)
            # boosted observer comoving with the emitter: time of the instantaneous leg's arrival event
            if w2 > 0:
                g = 1 / mp.sqrt(1 - w2)
                dtp = -g * wn * L
                if dtp < 0:
                    n_backward += 1
P2_ok = bool(min_ratio > 0 and n_backward > 0)
vrel = mp.mpf(220e3)
P3 = float(1 - (vrel / cv) ** 2)
out["Q3"] = {"P2_loops": n_loops, "P2_min_tstar_c_over_L": mp.nstr(min_ratio, 15),
             "P2_analytic_min_1_over_(1+|w|)": mp.nstr(1 / (1 + mp.mpf("0.999999")), 15),
             "P2_backward_instantaneous_legs_found": n_backward, "P2_ok": P2_ok,
             "P3_1_minus_vrel2_over_c2": P3, "P3_ok": P3 > 0,
             "P1": "Lean SV2_causality.lean (graded from its .out in the README)"}

# ---------------------------------------------------------------- labels
def lab(rows):
    # the "ct/r = 0.03" cell of the criteria is (t 1 s, r 1e10 m), ct/r = 0.02998 (first run matched 0.03 to 1e-9: slip, disclosed)
    g = [r for r in rows if r["t_s"] == 1 and r["r_m"] == 1e10]
    assert len(g) == 6
    return any(r["D1"] for r in g), any(r["D1"] and r["D2"] for r in g)

per = {}
for fname, F in A.items():
    d1, d12 = lab(F["rows"])
    per[fname] = "PHYSICAL" if d12 else "HARMLESS-BY-STRUCTURE"
labs = set(per.values())
label = labs.pop() if len(labs) == 1 else "SPLIT"
out["label_per_footing"] = per
out["label"] = label
out["runtime_s"] = round(time.time() - T0, 1)

suffix = "_MUTATE" if MUTATE else ""
(D / f"sv2_iter1{suffix}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
L = [f"SV2 iter_1 {out['mode']}  (criteria 7d31bb0ac2)"]
for fname, F in A.items():
    L.append(f"{fname}: Pi {F['Pi_kg_m3']} kg/m3, x {F['x_bg']}, t_dyn {F['t_dyn_Myr']:.2f} Myr")
    for r in F["rows"]:
        if MUTATE:
            L.append(f"  t {r['t_s']:g} r {r['r_m']:.0e} {r['dir']:7s} mutant arrival {r['mutant_earliest_arrival_s']:.3g} s  D1 {r['D1']}")
        else:
            L.append(f"  t {r['t_s']:g} r {r['r_m']:.0e} {r['dir']:7s} ct/r {r['ct_over_r']:.2f} |E|max {r['E_max_abs']:.3e} s^-2 "
                     f"eig {r['E_eig_max_abs_s^-2']:.3e} floor-ratio {r['E_over_floor']:.1e} flip-diff/floor {r['E_flip_diff_over_floor']:.1e} "
                     f"strain(1 m, t) {r['strain_1m_pair_after_t']:.2e} c2dq {r['c2_dq_J_m3']} J/m3 D1 {r['D1']} D2 {r['D2']}")
if not MUTATE:
    L.append(f"F1 coefficient spread max {max(v['rel_spread_over_cells'] for v in out['F1'].values()):.1e}; "
             f"F2 Pi-linearity dev max {max(r['dev'] for r in out['F2']):.1e}; F3 gamma part local {out['F3_gamma_part_polynomial_local']}; FORCED {out['FORCED']}")
    for fn, b in out["F_bound"].items():
        L.append(f"  {fn}: C_max {b['C_max']}, bound at t = 1 s: {b['bound_at_t_1s_m_s']} m/s")
L.append(f"KA1 {out['KA1_x0_H_offorigin_zero']}  KA2 {out['KA2_Pi0_g_zero']}")
q = out["Q3"]
L.append(f"Q3: {q['P2_loops']} loops, min t* c/L {q['P2_min_tstar_c_over_L']} (analytic {q['P2_analytic_min_1_over_(1+|w|)']}), "
         f"backward legs seen {q['P2_backward_instantaneous_legs_found']}, P2 {q['P2_ok']}; P3 1-v^2/c^2 = {q['P3_1_minus_vrel2_over_c2']:.9f}")
L.append(f"label per footing {per}; LABEL {label}; runtime {out['runtime_s']} s")
(D / f"sv2_iter1{suffix}.out").write_text("\n".join(L) + "\n")
print("\n".join(L))
