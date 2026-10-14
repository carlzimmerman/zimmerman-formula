"""CFG785 -- young tidal dwarfs: joint fill fraction f of the law's cold-energy halo; predictions N (f=0), L (f=1), C (clock).
Criteria: FROZEN_CRITERIA.md (427afbae9).  Data: real_research/data/tidal_dwarfs/lelli2015_tdg.csv + CFG441 tierB_arp72c.csv.
Run: python3 cfg785.py   (CFG785_MUTATE=1: V_circ := V_model(f=1)).  Seconds.
kappa = 1/2 FITTED; not theory closed.
"""
import csv
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("CFG785_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


Gk = 4.30091e-6                     # kpc (km/s)^2 / Msun
U = 1e6 / 3.0857e19                 # (km/s)^2/kpc -> m/s^2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
nu_s = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y)
f_ = lambda r, k: float(r[k])

G7 = []
for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
    G7.append(dict(name=r["Object"], i=f_(r, "i_deg"), R=f_(r, "R_out_kpc"), Vc=f_(r, "V_circ_kms"), eV=f_(r, "e_V_circ_kms"),
                   Vrot=f_(r, "V_rot_kms"), sHI=f_(r, "sigma_HI_kms"), Mb=f_(r, "M_bar_1e8") * 1e8, eMb=f_(r, "e_M_bar_1e8") * 1e8,
                   Mmol=f_(r, "M_mol_1e8") * 1e8, t=f_(r, "tmerg_over_torb") * f_(r, "t_orb_Gyr"),
                   VL={"canonical": f_(r, "V_EFE1_kms"), "alt": f_(r, "V_EFE2_kms")},
                   VLiso={"canonical": f_(r, "V_ISO1_kms"), "alt": f_(r, "V_ISO2_kms")}))
for r in csv.DictReader(open(os.path.join(HERE, "..", "CFG441_old_tdgs_tidal_origin", "data", "tierB_arp72c.csv"))):
    Mb = f_(r, "M_bar_1e8") * 1e8; R = f_(r, "R_out_kpc")
    VN2 = Gk * Mb / R
    VL = {ft: math.sqrt(VN2 * nu_s(VN2 / R * U / a0)) for ft, a0 in A0.items()}
    G7.append(dict(name=r["object"], i=f_(r, "i_deg"), R=R, Vc=f_(r, "V_circ_kms"), eV=7.5, Vrot=f_(r, "V_circ_kms"), sHI=0.0,
                   Mb=Mb, eMb=f_(r, "e_M_bar_1e8") * 1e8, Mmol=0.0, t=f_(r, "age_Myr") / 1e3, VL=VL, VLiso=VL))


def fit(gals, foot, iso=False, di=0.0, kmol=1.0, press="circ", mut=False):
    F = np.linspace(-0.5, 2.0, 2501)
    chi = np.zeros_like(F)
    for g in gals:
        Mb = g["Mb"] + (kmol - 1.0) * g["Mmol"]
        VN2 = Gk * Mb / g["R"]
        VL = (g["VLiso"] if iso else g["VL"])[foot] * (Mb / g["Mb"]) ** 0.25
        Vo = {"circ": g["Vc"], "rot": g["Vrot"], "iso": math.sqrt(g["Vrot"] ** 2 + 2 * g["sHI"] ** 2)}[press]
        if di:
            Vo = Vo * math.sin(math.radians(g["i"])) / math.sin(math.radians(min(max(g["i"] + di, 15.0), 89.0)))
        Vm = np.sqrt(np.maximum(VN2 + F * (VL ** 2 - VN2), 1e-6))
        if mut:
            Vo = math.sqrt(VL ** 2)
        dV_dM = (Gk / g["R"]) / (2 * Vm)                                 # dV/dM_bar through V_N^2 (law term rescales ~M^1/2 too)
        var = g["eV"] ** 2 + (dV_dM * g["eMb"]) ** 2
        chi += (Vo - Vm) ** 2 / var
    i = int(np.argmin(chi))
    L = np.exp(-0.5 * (chi - chi[i])); L /= L.sum()
    c = np.cumsum(L)
    q = lambda p: float(np.interp(p, c, F))
    sig = (q(0.84) - q(0.16)) / 2
    return dict(f=float(F[i]), lo=q(0.16), hi=q(0.84), u95=q(0.95), sig=sig, chi_min=float(chi[i]),
                chi_f0=float(np.interp(0.0, F, chi)), chi_f1=float(np.interp(1.0, F, chi)))


P("CFG785  young tidal dwarfs: fill fraction of the law's cold-energy halo" + ("  [MUTATE]" if MUT else ""))
six = G7[:6]
k1 = fit(six, "canonical", mut=False)
P(f"  K1 Newton chi^2 (six, f = 0) = {k1['chi_f0']:.3f} (record 1.095); K2 law chi^2 (six, f = 1, V_EFE1) = {k1['chi_f1']:.2f} (record 10.55)")
RES = {"lane": "CFG785", "mutate": MUT, "K1": k1["chi_f0"], "K2": k1["chi_f1"], "fits": {}}
variants = {"primary": {}, "ISO law": dict(iso=True), "i+10": dict(di=10.0), "i-10": dict(di=-10.0), "Xco x0.5": dict(kmol=0.5),
            "Xco x2": dict(kmol=2.0), "no AD (V_rot)": dict(press="rot"), "full AD": dict(press="iso")}
for foot in A0:
    for lab, kw in variants.items():
        r = fit(G7, foot, mut=MUT, **kw)
        RES["fits"][f"{foot}|{lab}"] = r
        P(f"  {foot:9s} {lab:14s}: f = {r['f']:+.2f} [{r['lo']:+.2f}, {r['hi']:+.2f}]  95% upper {r['u95']:+.2f}  chi2 min/f0/f1 {r['chi_min']:.1f}/{r['chi_f0']:.1f}/{r['chi_f1']:.1f}")
# jackknife
jk = [fit([g for k, g in enumerate(G7) if k != j], "canonical", mut=MUT)["u95"] for j in range(len(G7))]
P(f"  jackknife 95% upper limits (drop one): " + " ".join(f"{x:+.2f}" for x in jk))
# clock predictions
tmean = float(np.mean([g["t"] for g in G7]))
fc = {tau: float(np.mean([1 - math.exp(-g["t"] / tau) for g in G7])) for tau in (0.7, 3.5)}
P(f"  clock prediction (mean over the 7, ages {', '.join(f'{g['t']:.2f}' for g in G7)} Gyr): f = {fc[0.7]:.2f} (tau 0.7) / {fc[3.5]:.2f} (tau 3.5)")
if not MUT:
    keys = [k for k in RES["fits"] if k.startswith("canonical|") and "ISO" not in k]
    allN = all(RES["fits"][k]["u95"] < 0.25 and (1 - RES["fits"][k]["f"]) / max(RES["fits"][k]["hi"] - RES["fits"][k]["f"], 1e-9) >= 3 for k in keys) and max(jk) < 0.25
    pr = RES["fits"]["canonical|primary"]
    lawS = pr["f"] / max(pr["f"] - pr["lo"], 1e-9) >= 3 and abs(1 - pr["f"]) / max(pr["hi"] - pr["f"], pr["f"] - pr["lo"]) < 2
    clk = any(abs(fc[t] - pr["f"]) / pr["sig"] < 2 for t in fc) and abs(pr["f"]) / pr["sig"] >= 2 and abs(1 - pr["f"]) / pr["sig"] >= 2
    cls = "NO CAPTURE SUPPORTED" if allN else ("LAW SUPPORTED" if lawS else ("CLOCK" if clk else "NOT DECIDED"))
    P(f"\n  CLASS: {cls}   (primary f = {pr['f']:+.2f} +- {pr['sig']:.2f}; f=1 at {(1 - pr['f']) / pr['sig']:.1f} sigma; clock {fc[0.7]:.2f}/{fc[3.5]:.2f})")
    RES["class"] = cls
else:
    pr = RES["fits"]["canonical|primary"]
    P(f"  MUTATE: f_hat {pr['f']:.3f} (must be 1.00 +- 0.02): {'bites' if abs(pr['f'] - 1) <= 0.02 else 'DID NOT BITE'}")
RES["jackknife_u95"] = jk; RES["clock"] = fc
json.dump(RES, open(os.path.join(HERE, f"cfg785_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg785{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
