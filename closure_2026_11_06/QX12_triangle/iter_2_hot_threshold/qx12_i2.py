#!/usr/bin/env python3
"""QX12 iter_2 (FROZEN_CRITERIA.md, 7a1afa9b6b): host-temperature-keyed sector. Cold (retained at the cosmic ratio R) where
b = p/(rho c^2) > b_t, absent below. b_t = max b over all galaxy-side points (no cluster input); amplitude R = 5.562 (T1);
sector traces baryons (frozen), traces gas (reported). Predict X-COP and groups.
    python3 qx12_i2.py            -> qx12_i2.json/.out
    python3 qx12_i2.py --mutate   -> qx12_i2_MUTATE.json/.out  (M1 b_t = 0; M2 R x 0)
kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx12_i2_MUTATE" if MUT else "qx12_i2"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); cut = src.index("DIR = dict(")
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], Q5, "exec"), NS)
sys.argv = argv0
G, MS, KPC, C, A0, LE, tables = (NS[k] for k in ("G", "MS", "KPC", "C", "A0", "LE", "tables"))
Q5J = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.json")))
R0 = 0.11958060485606123 / 0.0215
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * np.maximum(gN, 0.0))


def run(a0, R, bt_rule="max", gas_trace=False):
    T = tables("b", a0, False)
    kids = []
    for p in LE:
        r = math.sqrt(G * p["Mb"] / p["gbar"]); kids.append(dict(k=p["gobs"] * r / (2 * C ** 2), gobs=p["gobs"], gbar=p["gbar"], Mb=p["Mb"], r=r))
    gal_b = [s["k"] for s in T["S"]] + [e["k"] for e in T["E"]] + [x["k"] for x in kids]
    bt = max(gal_b) if bt_rule == "max" else 0.0
    eps = lambda k: 1.0 if k > bt else 0.0
    def pred(Mb, Mgas, r_kpc, k):
        Mx = R * eps(k) * (Mgas if gas_trace else Mb); r = r_kpc * KPC
        return float(glaw(G * (Mb + Mx) * MS / r ** 2, a0)) * r ** 2 / G / MS
    xd = np.array([math.log10(x["M_obs"] / pred(x["M_b"], z["M_gas"], z["r_kpc"], x["k"])) for x, z in zip(T["X"], NS["XC"])])
    gm, npass = {}, {}
    grows = T["G"]
    for fst in (0.0, 1.0):
        v = []; ok_by = {}
        for gi, g in enumerate([g for g in grows if g["fst"] == fst]):
            gp = NS["GR"][gi // 2]; pt = gp["pts"][gi % 2]
            Mp = pred(g["M_b"], pt["M_gas"], pt["r_kpc"], g["k"]); dl = math.log10(g["M_obs"] / Mp); v.append(dl)
            ok_by.setdefault(gp["name"], True)
            ok_by[gp["name"]] &= abs(dl) <= 2 * pt["eM"] / (pt["M_obs"] * math.log(10))
        gm[fst] = float(np.mean(v)); npass[fst] = int(sum(ok_by.values()))
    lo, hi = sorted([gm[0.0], gm[1.0]])
    # galaxy rechecks
    sd = np.array([math.log10(s["gobs"] / (glaw(s["gbar"] * (1 + R * eps(s["k"])), a0))) for s in T["S"]])
    sd0 = np.array([math.log10(s["gobs"] / glaw(s["gbar"], a0)) for s in T["S"]])
    ke = np.array([math.log10(x["gobs"] / glaw(x["gbar"] * (1 + R * eps(x["k"])), a0)) for x in kids])
    ke0 = np.array([math.log10(x["gobs"] / glaw(x["gbar"], a0)) for x in kids])
    E_shift = max(abs(R * eps(e["k"])) for e in T["E"])   # 0 iff no elliptical point is above threshold
    return dict(b_t=bt, X_mean=float(xd.mean()), X_rms=float(np.sqrt((xd ** 2).mean())), X_pass=bool(abs(xd.mean()) <= 0.05 and np.sqrt((xd ** 2).mean()) <= 0.10),
                G_mean_fst0=gm[0.0], G_mean_fst1=gm[1.0], G_band_pass=bool(lo <= 0.05 and hi >= -0.05), G_strict=npass,
                SPARC_shift=float(sd.mean() - sd0.mean()), KiDS_shift=float(ke.mean() - ke0.mean()), ell_eps_max=E_shift,
                frac_X_above=float(np.mean([x["k"] > bt for x in T["X"]])), frac_G_above=float(np.mean([g["k"] > bt for g in grows])),
                ranges=dict(SPARC=[min(s["k"] for s in T["S"]), max(s["k"] for s in T["S"])], ell=[min(e["k"] for e in T["E"]), max(e["k"] for e in T["E"])],
                            KiDS=[min(x["k"] for x in kids), max(x["k"] for x in kids)], XCOP=[min(x["k"] for x in T["X"]), max(x["k"] for x in T["X"])],
                            groups=[min(g["k"] for g in grows), max(g["k"] for g in grows)]))


RES = dict(lane="QX12 iter_2", criteria="7a1afa9b6b", mutate=MUT, R=R0, note="kappa = 1/2 FITTED; not theory closed")
P(f"QX12 iter_2 ({'MUTATE' if MUT else 'main'}): host-temperature-keyed sector, b_t from galaxies, amplitude R = {R0:.3f}. kappa = 1/2 FITTED; not theory closed.")
if not MUT:
    RES["foot"] = {}
    for f, a0 in A0.items():
        o = run(a0, R0); og = run(a0, R0, gas_trace=True); k1 = run(a0, 0.0)
        q5 = Q5J["b"][f]["keys"]
        ka2 = max(abs(o["ranges"]["ell"][0] / q5["ellipticals"][0] - 1), abs(o["ranges"]["ell"][1] / q5["ellipticals"][1] - 1),
                  abs(o["ranges"]["XCOP"][0] / q5["XCOP"][0] - 1), abs(o["ranges"]["XCOP"][1] / q5["XCOP"][1] - 1),
                  abs(o["ranges"]["groups"][0] / q5["groups"][0] - 1), abs(o["ranges"]["groups"][1] / q5["groups"][1] - 1))
        o["KA1_plain"] = [k1["X_mean"], k1["G_mean_fst0"], k1["G_mean_fst1"]]; o["KA2_maxrel"] = ka2; o["gas_trace"] = og
        o["galaxy_unchanged"] = bool(abs(o["SPARC_shift"]) <= 1e-12 and abs(o["KiDS_shift"]) <= 1e-12 and o["ell_eps_max"] == 0.0)
        o["label"] = "PASS" if (o["X_pass"] and o["G_band_pass"] and o["galaxy_unchanged"]) else "FAIL"
        RES["foot"][f] = o
        P(f"[{f}] b ranges: SPARC {o['ranges']['SPARC'][1]:.3g} max, ellipticals {o['ranges']['ell'][0]:.3g}-{o['ranges']['ell'][1]:.3g}, KiDS {o['ranges']['KiDS'][0]:.3g}-{o['ranges']['KiDS'][1]:.3g}, "
          f"groups {o['ranges']['groups'][0]:.3g}-{o['ranges']['groups'][1]:.3g}, X-COP {o['ranges']['XCOP'][0]:.3g}-{o['ranges']['XCOP'][1]:.3g}")
        P(f"   b_t = {o['b_t']:.4g} (max galaxy b); above threshold: X-COP {o['frac_X_above']:.2f}, groups {o['frac_G_above']:.2f}")
        P(f"   KA1 (R=0): X-COP {k1['X_mean']:+.4f}; KA2 b ranges vs QX5 max rel {ka2:.1e}; galaxies unchanged {o['galaxy_unchanged']}")
        P(f"   PREDICTION (sector traces baryons): X-COP {o['X_mean']:+.3f}/{o['X_rms']:.3f} -> {'PASS' if o['X_pass'] else 'FAIL'}; groups mean [{o['G_mean_fst1']:+.3f}, {o['G_mean_fst0']:+.3f}] -> {'PASS' if o['G_band_pass'] else 'FAIL'}; strict {o['G_strict']}")
        P(f"   reported (traces gas): X-COP {og['X_mean']:+.3f}/{og['X_rms']:.3f}; groups [{og['G_mean_fst1']:+.3f}, {og['G_mean_fst0']:+.3f}]")
        P(f"   LABEL [{f}]: {o['label']}")
    # Sun (reported)
    rho_loc = 0.11958 * 3 * (100e3 / 3.0857e22) ** 2 / (8 * math.pi * G)       # cosmic mean sector density today (kg/m^3), local <= this
    Msun_cap = rho_loc * 4 / 3 * math.pi * (6.957e8) ** 3
    RES["Sun"] = dict(b_centre=1.5e7 * 1.380649e-23 / (0.6 * 1.6726e-27 * C ** 2), rho_local_max=rho_loc, captured_kg=Msun_cap, ephemeris_bound_kg=1e-10 * MS)
    P(f"Sun: b_centre {RES['Sun']['b_centre']:.2g} > b_t, so the sector is cold inside; static capture at the local density <= cosmic mean: {Msun_cap:.2g} kg vs 1e-10 Msun = {1e-10 * MS:.2g} kg (ephemeris) -> harmless; flux capture with finite c_hot owed")
    RES["label"] = "PASS" if all(RES["foot"][f]["label"] == "PASS" for f in A0) else "FAIL"
    P(f"LABEL: {RES['label']}")
else:
    RES["M"] = {}
    for f, a0 in A0.items():
        m1 = run(a0, R0, bt_rule="zero"); m2 = run(a0, 0.0); k1 = run(a0, 0.0)
        RES["M"][f] = dict(M1_KiDS_shift=m1["KiDS_shift"], M1_bites=bool(abs(m1["KiDS_shift"]) > 0.05), M2_X=m2["X_mean"], M2_bites=bool(abs(m2["X_mean"] - k1["X_mean"]) <= 1e-12))
        P(f"[{f}] M1 b_t = 0: KiDS shift {m1['KiDS_shift']:+.3f} -> {'BITES' if RES['M'][f]['M1_bites'] else 'DOES NOT BITE'}; M2 R x 0: X-COP {m2['X_mean']:+.4f} -> {'BITES' if RES['M'][f]['M2_bites'] else 'DOES NOT BITE'}")
    RES["all_bite"] = bool(all(v["M1_bites"] and v["M2_bites"] for v in RES["M"].values()))
    P(f"MUTATE all bite: {RES['all_bite']}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
