#!/usr/bin/env python3
"""KR2 POST-FREEZE section (requested by the orchestrator after KR1 landed, 38b8f7749f; NOT part of the frozen label):
KR1 found that for any convex K(Q) the kernel mass M^2 = Q^2 K''/2 is a function of the sector's own LOCAL density. This
script asks, with KR1's own relation (kr1.py's DBI members D0-D3 and M_at_density, executed read-only), what M the dust
carries at the local densities of KR2's columns, and whether each column's frozen mu_K(0) window survives once M is local.
    python3 kr2_local.py  -> kr2_local.json / kr2_local.out
Local dust densities are stated relative to today's mean K-dust density (the same ratio for baryons when the dust is at
R x the baryons). One thread. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
p = os.path.join(REPO, "closure_2026_11_08", "KR1_running_k_mass", "kr1.py")
src = open(p).read(); cut = src.index("# ------------------------------------------------------------------ KA1 / KA2 / KA3")
NS = {"__file__": p, "__name__": "kr1_prefix"}; a = sys.argv; sys.argv = [p]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], p, "exec"), NS)
sys.argv = a
KR1J = json.load(open(os.path.join(REPO, "closure_2026_11_08", "KR1_running_k_mass", "kr1.json")))
KR2J = json.load(open(os.path.join(HERE, "kr2.json")))
B = json.load(open(os.path.join(HERE, "parts", "battery.json"))); K = json.load(open(os.path.join(HERE, "parts", "kids.json")))
bg, lam_fix, M_at_density, SET, MEMBERS = NS["bg"], NS["lam_fix"], NS["M_at_density"], NS["SET"], NS["MEMBERS"]
FOOTS = ("canonical", "alt"); RHOC_H2 = 2.775e11                  # Msun / Mpc^3 per h^2
F1A = json.load(open(os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit", "f1a.json")))
RF = {f: float(F1A[f]["R_B2"]) for f in FOOTS}
KDJ = json.load(open(os.path.join(REPO, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
FX = {f: KDJ["footings"][f]["uniform_f_diag"]["Xcop_f_need"] for f in FOOTS}
RES = dict(lane="KR2", section="POST-FREEZE local-M (not the frozen label)", kr1_result="38b8f7749f", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})

# known answer: KR1's recorded M_ta at the turnaround density 149.85 for every member, and M_table at z 3
ka = []
for f in FOOTS:
    for m, mu in MEMBERS.items():
        I0 = SET[f]["I0"]; lam = KR1J["footings"][f][m]["lam"]
        Mta, _ = M_at_density(mu, lam, I0, KR1J["footings"][f][m]["GC"]["rho_ta_over_rho0"])
        ka.append(abs(Mta / KR1J["footings"][f][m]["GC"]["M_ta"] - 1))
RES["KA_kr1_Mta"] = dict(max_rel=max(ka), pass_=bool(max(ka) <= 1e-9))
P(f"KA: KR1's M_ta reproduced at rho 149.85 x mean, 4 members x 2 footings: max rel {max(ka):.1e} -> {'PASS' if max(ka) <= 1e-9 else 'FAIL'}")

# local densities (ratio to today's mean dust density = ratio to today's mean baryon density for dust at R x baryons)
for f in FOOTS:
    ob = SET[f]["ob"]; rhob0 = ob * RHOC_H2                                              # Msun/Mpc^3 (h cancels)
    rows = {}
    # SPARC / any captured galaxy: turnaround density (KR1 GC; the lowest density a captured galaxy's dust reaches)
    rows["C1 SPARC turnaround (KR1 GC)"] = 149.85
    # KiDS: dust R x M* enclosed within r (mean), bins of KX1, r 100 and 300 kpc (upper bound on the stack's dust density)
    for lm in (9.4, 10.45, 10.7, 10.9):
        for r in (0.1, 0.3):
            rows[f"C5 KiDS lm {lm} mean inside {int(r*1e3)} kpc (dust R x M*)"] = RF[f] * 10 ** lm / (4 / 3 * math.pi * r ** 3) / (RF[f] * rhob0)
    # X-COP: dust at the need F_X x M_last in the cored isothermal r_c 100 kpc (KQ1 M3 install), mean inside 100 kpc and 0.25 R500
    rows_x = []
    if "XI" not in globals():
        kp = os.path.join(REPO, "closure_2026_11_07", "KQ1_kq_dust_cluster_core", "kq1.py"); s2 = open(kp).read(); c2 = s2.index("def cored_shape(rc)")
        N2 = {"__file__": kp, "__name__": "kq1_prefix"}; a = sys.argv; sys.argv = [kp]
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(s2[:c2], kp, "exec"), N2)
        sys.argv = a
        globals()["XI"] = {n: (N2["XINFO"][n]["Mlast"], N2["XINFO"][n]["tl"], N2["XINFO"][n]["r500"]) for n in N2["XN"]}
    m = lambda x: x - math.atan(x)
    for n, (Ml, tl, r5) in XI.items():
        for lab, rk in (("100 kpc", 100.0), ("0.25 R500", 0.25 * r5)):
            Md = FX[f] * Ml * m(rk / 100.0) / m(tl / 100.0); rows_x.append((n, lab, Md / (4 / 3 * math.pi * (rk / 1e3) ** 3) / (RF[f] * rhob0)))
    for lab in ("100 kpc", "0.25 R500"):
        v = [x[2] for x in rows_x if x[1] == lab]; rows[f"C2 X-COP need profile, mean inside {lab} (min over 7)"] = min(v)
    # groups: GB1 group totals are on disk only through GB1; the turnaround density applies to any captured group (lower bound)
    rows["C3 groups turnaround (KR1 GC convention)"] = 149.85
    # hosts: R500 mean density is 500 rho_crit; dust at fair share -> 500 / Omega_m x mean
    Om = (SET[f]["ob"] + SET[f]["od"]) / SET[f]["h"] ** 2
    rows["C6 hosts mean inside R500 (500 rho_crit)"] = 500.0 / Om
    out = {}
    for lab, ratio in rows.items():
        Ms = {}
        for mname, mu in MEMBERS.items():
            lam = KR1J["footings"][f][mname]["lam"]; Ms[mname] = M_at_density(mu, lam, SET[f]["I0"], ratio)[0]
        out[lab] = dict(density_over_mean=ratio, M_by_member=Ms, M_min=min(Ms.values()), M_max=max(Ms.values()), jeans_kpc_max=2 * math.pi / min(Ms.values()) * 1e3)
    # does each column's frozen window survive with M local? window (grid mu, reading B, amount R) vs the M the column's dust carries
    W = KR2J["footings"][f]["windows"]
    def survives(col, keys):
        w = W[col]
        if not w: return dict(window=w, survives=False, why="frozen window already empty")
        Mmin = min(out[k]["M_min"] for k in keys)
        return dict(window=[w[0], w[-1]], M_local_min=Mmin, survives=bool(Mmin <= w[-1]), why=f"local M >= {Mmin:.4g} vs window top {w[-1]:.4g}")
    surv = {"C1": survives("C1", ["C1 SPARC turnaround (KR1 GC)"]),
            "C2": survives("C2", [k for k in out if k.startswith("C2")]),
            "C3": survives("C3", ["C3 groups turnaround (KR1 GC convention)"]),
            "C5": survives("C5", [k for k in out if k.startswith("C5")]),
            "C6": survives("C6", ["C6 hosts mean inside R500 (500 rho_crit)"])}
    today = KR2J["footings"][f]["today_window"]
    RES["footings"][f] = dict(densities=out, xcop_rows=rows_x, survives=surv, today_window=today,
                              today_survives=bool(today and all(v["survives"] for v in surv.values())))
    P(f"=== {f}")
    for lab, o in out.items():
        P(f"  {lab}: rho/mean {o['density_over_mean']:.4g} -> M {o['M_min']:.4g}-{o['M_max']:.4g} Mpc^-1 (Jeans 2 pi/M <= {o['jeans_kpc_max']:.3g} kpc)")
    for c, v in surv.items(): P(f"  {c}: frozen window {v['window'] if v['window'] else 'empty'}; {v['why']} -> {'SURVIVES' if v['survives'] else 'DOES NOT SURVIVE'}")
    P(f"  today window {today if today else 'empty'} -> with local M: {'SURVIVES' if RES['footings'][f]['today_survives'] else 'DOES NOT SURVIVE'}")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, "kr2_local.json"), "w"), indent=1)
open(os.path.join(HERE, "kr2_local.out"), "w").write("\n".join(OUT) + "\n")
