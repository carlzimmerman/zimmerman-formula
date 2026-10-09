#!/usr/bin/env python3
"""CFG535 T1: within-sample delta(z) slope of the Ubler+17 KMOS3D bTFR sample (criteria FROZEN_CRITERIA.md section 5).
Usage: python3 cfg535_t1_ubler_dz.py [MUTATE]   (MUTATE writes *_MUTATE outputs).  kappa = 1/2 FITTED; no verdict words beyond the frozen gate."""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
TAG = "_MUTATE" if MUT else ""
SEED, NBOOT, TSIG = 535, 10000, 0.19
FOOT = {"canonical": H.A0C, "alt": H.A0A}
KERN = {"nu_mono": H.NU, "nu_plain": lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))}

u = pd.read_csv(os.path.join(REPO, "data_assembly/high_z_tf_tables/ubler2017.csv"))
c = pd.read_csv(os.path.join(REPO, "data_assembly/kmos3d_phibss/kmos3d_catalog.csv"))
c = c[(c.Z > 0) & (c.LMSTAR > 0)].reset_index(drop=True)
out = {"lane": "CFG535 T1", "mutate": MUT, "controls": {}}

# C1
nb = [int((u.z < 1.3).sum()), int(((u.z >= 1.3) & (u.z < 1.8)).sum()), int((u.z >= 1.8).sum())]
out["controls"]["C1"] = {"rows": len(u), "split": nb, "pass": len(u) == 135 and nb == [65, 24, 46]}

# match (CFG90 rule)
rows = []
for i, r in u.iterrows():
    dd = np.hypot((c.Z - r.z) / 0.002, (c.LMSTAR - r.logMstar) / 0.02)
    j = dd.idxmin()
    if dd[j] > 1.0:
        continue
    Re = c.loc[j, "RHALF"] * H.kpc_per_arcsec(r.z)
    rows.append(dict(i=i, kid=c.loc[j, "ID"], z=r.z, Ms=10 ** r.logMstar, Mg=10 ** r.logMbar - 10 ** r.logMstar, Re=Re, V=r.vcirc_max_kms))
D = pd.DataFrame(rows)
D = D[D.Re > 0].reset_index(drop=True)
out["n_matched"] = len(D)

# C2 against CFG90
p90 = pd.read_csv(os.path.join(CFG, "CFG90_a0z_rederivation/cfg90_per_object.csv"))
k90 = p90[p90.survey == "KMOS3D"].copy()
k90["i"] = k90.name.str.split(":").str[0].str[1:].astype(int)
m = D.merge(k90[["i", "kid", "Re"]], on="i", suffixes=("", "_90"))
ids_equal = set(D.i) == set(k90.i) and (m.kid.astype(str) == m.kid_90.astype(str)).all()
rr = (m.Re / m.Re_90 - 1).abs().max() if len(m) else float("nan")
out["controls"]["C2"] = {"n_cfg90": len(k90), "n_here": len(D), "ids_equal": bool(ids_equal), "max_Re_frac_diff": float(rr),
                         "pass": bool(ids_equal and rr < 0.03)}

zmed = float(np.median(D.z))
RGRID = np.linspace(0.5, 5.0, 91)  # in R_d


def vpred(Ms, Mg, Re, z, a0, nu, gas_fac=1.0, tilt=0.0, ratio=1.0):
    Mg = Mg * 10 ** (tilt * (z - zmed))
    Rd = Re / H.XN
    R = RGRID[None, :] * Rd[:, None]
    v2 = H.disc_v2(Ms[:, None], Re[:, None], R) + H.disc_v2(Mg[:, None], gas_fac * Re[:, None], R)
    gN = v2 / R * H.G2SI
    a = a0 * ratio[:, None]
    vc2 = v2 * nu(gN / a)
    return np.sqrt(vc2.max(axis=1))


def ratios(law, z):
    return np.array([H.LAWS[law](zz) for zz in z])


z = D.z.values; Ms = D.Ms.values; Mg = D.Mg.values; Re = D.Re.values; Vobs = D.V.values.astype(float)
R_FL, R_H, R_PX = ratios("FLAT", z), ratios("H(z)", z), ratios("PROXY", z)


def slope(x, y):
    x0 = x - x.mean()
    return float((x0 * (y - y.mean())).sum() / (x0 ** 2).sum())


rng = np.random.default_rng(SEED)
BOOT = rng.integers(0, len(D), size=(NBOOT, len(D)))


def boot_slope(x, y):
    xb, yb = x[BOOT], y[BOOT]
    x0 = xb - xb.mean(1, keepdims=True)
    return (x0 * (yb - yb.mean(1, keepdims=True))).sum(1) / (x0 ** 2).sum(1)


cells = {}
for fn, a0 in FOOT.items():
    for kn, nu in KERN.items():
        for gf in (1.0, 1.5):
            key = f"{fn}|{kn}|gas{gf}"
            vp = {L: vpred(Ms, Mg, Re, z, a0, nu, gf, ratio=r) for L, r in (("FLAT", R_FL), ("H(z)", R_H), ("PROXY", R_PX))}
            V = Vobs * (vp["H(z)"] / vp["FLAT"]) if MUT else Vobs
            res = {}
            for L in vp:
                d = np.log10(V / vp[L])
                b = slope(z, d)
                sb = float(np.std(boot_slope(z, d)))
                bp = slope(z, np.log10(V / vpred(Ms, Mg, Re, z, a0, nu, gf, tilt=+TSIG, ratio={"FLAT": R_FL, "H(z)": R_H, "PROXY": R_PX}[L])))
                bm = slope(z, np.log10(V / vpred(Ms, Mg, Re, z, a0, nu, gf, tilt=-TSIG, ratio={"FLAT": R_FL, "H(z)": R_H, "PROXY": R_PX}[L])))
                ss = abs(bp - bm) / 2
                st = math.hypot(sb, ss)
                sel = (z >= 1.3) & (z <= 2.1)
                res[L] = {"b": b, "sigma_boot": sb, "sigma_sys_gas_tilt": ss, "sigma_tot": st, "b_over_sigma_tot": b / st,
                          "median_delta": float(np.median(d)), "subset_z13_21": {"n": int(sel.sum()), "b": slope(z[sel], d[sel]),
                                                                                 "median_delta": float(np.median(d[sel]))}}
            sep = res["FLAT"]["b"] - res["H(z)"]["b"]
            Pi = abs(sep) / res["FLAT"]["sigma_tot"]
            # C3 noiseless
            c3f = slope(z, np.log10(vp["FLAT"] / vp["FLAT"]))
            c3r = slope(z, np.log10(vp["H(z)"] / vp["H(z)"]))
            cells[key] = {"laws": res, "sep_flat_minus_rival": sep, "Pi": Pi, "C3": [c3f, c3r],
                          "y_median_flat_at_Vmax": None}
out["cells"] = cells
out["controls"]["C3"] = {"pass": all(abs(v["C3"][0]) < 1e-10 and abs(v["C3"][1]) < 1e-10 for v in cells.values())}
prim = [k for k in cells if k.endswith("gas1.0")]
diag = all(cells[k]["Pi"] >= 3 for k in prim)
out["gate"] = {"primary_cells": prim, "Pi": {k: cells[k]["Pi"] for k in prim}, "DIAGNOSTIC": diag,
               "label": "DIAGNOSTIC" if diag else "NON-DIAGNOSTIC"}
if diag:
    out["law_status"] = {L: ("DISFAVOURED" if all(abs(cells[k]["laws"][L]["b_over_sigma_tot"]) > 3 for k in prim)
                             else "CONSISTENT" if all(abs(cells[k]["laws"][L]["b_over_sigma_tot"]) < 2 for k in prim) else "MIXED")
                         for L in ("FLAT", "H(z)")}
out["hand_estimates"] = {
    "HE-T1a_Pi_lt3_every_cell": all(v["Pi"] < 3 for v in cells.values()),
    "HE-T1b_sep_in_0.02_0.05": all(0.02 <= abs(v["sep_flat_minus_rival"]) <= 0.05 for v in cells.values()),
    "HE-T1c_sys_ge_boot": all(v["laws"]["FLAT"]["sigma_sys_gas_tilt"] >= v["laws"]["FLAT"]["sigma_boot"] for v in cells.values())}
out["z_median"] = zmed

if MUT:
    main = json.load(open(os.path.join(HERE, "cfg535_t1_results.json")))
    det = {}
    for k in cells:
        shift = cells[k]["laws"]["FLAT"]["b"] - main["cells"][k]["laws"]["FLAT"]["b"]
        exp = main["cells"][k]["sep_flat_minus_rival"]
        det[k] = {"shift": shift, "expected": exp, "detected": abs(shift - exp) <= 0.05 * abs(exp)}
    out["M1"] = {"cells": det, "DETECTED": all(v["detected"] for v in det.values())}

json.dump(out, open(os.path.join(HERE, f"cfg535_t1_results{TAG}.json"), "w"), indent=1, default=float)
print(f"CFG535 T1{TAG}: n_matched {len(D)}  z_med {zmed:.3f}")
print("controls:", {k: v["pass"] for k, v in out["controls"].items()})
for k, v in cells.items():
    L = v["laws"]
    print(f"{k:28s} b_FLAT {L['FLAT']['b']:+.4f} b_H {L['H(z)']['b']:+.4f} b_PX {L['PROXY']['b']:+.4f} | sep {v['sep_flat_minus_rival']:+.4f} "
          f"boot {L['FLAT']['sigma_boot']:.4f} sys {L['FLAT']['sigma_sys_gas_tilt']:.4f} Pi {v['Pi']:.2f} | "
          f"T_FLAT {L['FLAT']['b_over_sigma_tot']:+.2f} T_H {L['H(z)']['b_over_sigma_tot']:+.2f} | subset b_F {L['FLAT']['subset_z13_21']['b']:+.3f} n {L['FLAT']['subset_z13_21']['n']}")
print("gate:", out["gate"]["label"], {k: round(x, 2) for k, x in out["gate"]["Pi"].items()})
print("hand estimates:", out["hand_estimates"])
if MUT:
    print("M1 DETECTED:", out["M1"]["DETECTED"], {k: (round(v["shift"], 4), round(v["expected"], 4)) for k, v in out["M1"]["cells"].items()})
