#!/usr/bin/env python3
"""UX3: GM1's Okabe x eRASS1 selection written to ux3_okabe.json, read only. M in Msun h 0.7, R in m. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np
from astropy.io import fits
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); sys.path.insert(0, os.path.join(RB, "FR3_retention_independent")); import fr3_parse as FP
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); names = [str(x).strip() for x in X["name"]]
h_ = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; EN = [str(n).strip() for n in h_["NAME"]]; S = {n.split("J")[-1]: i for i, n in enumerate(EN)}; eMg = np.array(h_["MGAS500"], float); eM = np.array(h_["M500"], float) * 1e13
AL, BE, GA, DE_ = .079, .965, .665, -.258
def tt(M, z): F = math.log((1 + z) / 1.21); return 1e14 * math.exp((math.log(M / 1e14) - AL - GA * F) / (BE + DE_ * F))
def Rho(z): return 3 * (70e3 / 3.0857e22) ** 2 * (.3 * (1 + z) ** 3 + .7) / (8 * math.pi * 6.674e-11)
def RD(M, z, D): return (3 * M * 1.989e30 / (4 * math.pi * D * Rho(z))) ** (1 / 3)
O = {}
for r in FP.okabe():
    if r["id"] not in S or r["flag"] == "*" or r["z"] > .5 or r["M500"] is None or not eMg[S[r["id"]]] > 0: continue
    n = EN[S[r["id"]]]
    if n in names: M5, M2 = r["M500"] * 1e14, r["M200"] * 1e14; O[n] = dict(z=r["z"], M500=M5, M200=M2, R500_m=RD(M5, r["z"], 500), R200_m=RD(M2, r["z"], 200), s=.5 * (r["up"] + r["dn"]) * 1e14, cf=tt(M5, r["z"]) / M5, Mcat=float(eM[S[r["id"]]]))
json.dump(O, open(os.path.join(HERE, "ux3_okabe.json"), "w"), indent=0); print("N", len(O))
