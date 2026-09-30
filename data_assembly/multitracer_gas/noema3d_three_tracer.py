#!/usr/bin/env python3
"""Reconstruct CO, dust and [CI] molecular gas masses for the 10 NOEMA3D galaxies from the TABULATED integrated fluxes (paper 2, arXiv:2604.18504 Table 2: S_CO, S_CI, S_dust) using the
conversion recipes STATED in paper 2 Sect. 3.4 (Eq. 1-3): CO: M = alpha_CO * R_1J * L'_CO, L' = 3.25e7 S dv nu_obs^-2 D_L^2 (1+z)^-3, alpha_CO = 4.36, R_14 = 2.4 (CO(4-3), group 1), R_13 = 1.8 (CO(3-2), group 2);
dust: L_nu850 = 4 pi S K D_L^2/(1+z), K as printed (T_d = 25 K, beta = 1.8), alpha_850 = 6.7e12 W/Hz/Msun; [CI](1-0): M = 18.7 * L'_CI.
These are NOT the paper's own tracer masses (the paper tabulates only the CO one, in Table 1): they are this script's reconstruction.  CONTROL: the CO reconstruction is compared with the paper's Table 1 M_mol
for the same galaxies; dust and [CI] are reported only if that control holds (the script prints the residuals; the cosmology is not stated on the pages read, so H0 = 70, Om = 0.3 and Planck18 are both tried).
Unknowns flagged: dust observed frequency = the CO line frequency of the same tuning (the text says all three tracers were observed at similar frequencies: ~1.4 mm group 1, 2 mm group 2), so the dust mass
carries an extra ~0.05 dex frequency uncertainty; no uncertainty on conversion factors is propagated (alpha_CO +-0.9, alpha_850 +-1.7e12, alpha_CI +-0.6 as stated)."""
import csv, math, os, json
import numpy as np
from astropy.cosmology import FlatLambdaCDM, Planck18
import astropy.units as u
HERE = os.path.dirname(os.path.abspath(__file__)); G = list(csv.DictReader(open(os.path.join(HERE, "..", "noema3d", "noema3d_per_galaxy.csv"))))
OBS = {r["id"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "noema3d", "noema3d_observations.csv"))) if r["weighting"] != "Ro5"}
def f(x):
    try: return float(x)
    except: return None
COSMOS = {"H0=70,Om=0.3": FlatLambdaCDM(H0=70, Om0=0.3), "Planck18": Planck18}
Msun = 1.0
def masses(cosmo, g):
    z = float(g["z"]); DL = cosmo.luminosity_distance(z).to(u.Mpc).value; nu_co = float(OBS[g["id"]]["freq_GHz"])
    group1 = "CO4-3" in OBS[g["id"]]["line"]; R1J = 2.4 if group1 else 1.8
    Lp = lambda S, nu: 3.25e7 * S * nu ** -2 * DL ** 2 * (1 + z) ** -3
    out = {}
    S = f(g["S_CO_P2_Jykms"]); out["CO"] = 4.36 * R1J * Lp(S, nu_co) if S else None
    Sci = f(g["S_CI_Jykms"]); out["CI"] = 18.7 * Lp(Sci, 492.161 / (1 + z)) if Sci else None
    Sd = f(g["S_dust_mJy"])
    if Sd:
        nu_rest = nu_co * (1 + z); T = 25.0; beta = 1.8
        K = (353.0 / nu_rest) ** (3 + beta) * ((math.exp(0.04799 * nu_rest / T) - 1) / (math.exp(16.956 / T) - 1))      # h nu/k = 0.04799 K per GHz
        DLm = DL * 3.0857e22; Lnu = 4 * math.pi * Sd * 1e-29 * K * DLm ** 2 / (1 + z)
        out["dust"] = Lnu / 6.7e12
    return out
rows = []; res = {}
for cn, cosmo in COSMOS.items():
    d = []
    for g in G:
        m = masses(cosmo, g); tab = 10 ** float(g["logMmol_CO_P2"])
        d.append(math.log10(m["CO"] / tab))
    res[cn] = d
    print(cn, "log(CO reconstructed / Table 1) per galaxy:", [round(x, 3) for x in d], "median", round(float(np.median(d)), 3), "max|.|", round(max(abs(x) for x in d), 3))
g1 = [i for i, g in enumerate(G) if "CO4-3" in OBS[g["id"]]["line"]]
best = min(res, key=lambda k: float(np.median([abs(res[k][i]) for i in g1]))); print("closer cosmology (median |residual| over the group-1 CO(4-3) galaxies):", best)
cosmo = COSMOS[best]
for g in G:
    m = masses(cosmo, g)
    resid = math.log10(m["CO"] / 10 ** float(g["logMmol_CO_P2"]))
    rows.append(dict(id=g["id"], group="1 (CO(4-3))" if "CO4-3" in OBS[g["id"]]["line"] else "2 (CO(3-2))", CO_control_residual_dex=round(resid, 3), CO_control_pass=int(abs(resid) < 0.03), z=g["z"], logMmol_CO_table1=g["logMmol_CO_P2"], logMmol_CO_reconstructed=round(math.log10(m["CO"]), 3), logMmol_CI_reconstructed=None if not m["CI"] else round(math.log10(m["CI"]), 3),
                     logMmol_dust_reconstructed=None if not m.get("dust") else round(math.log10(m["dust"]), 3), S_CO_Jykms=g["S_CO_P2_Jykms"], S_CI_Jykms=g["S_CI_Jykms"], S_dust_mJy=g["S_dust_mJy"], logMstar_SED=g["logMstar_SED"], cosmology=best))
with open(os.path.join(HERE, "noema3d_three_tracer_reconstruction.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r["id"], r["z"], "CO(tab)", r["logMmol_CO_table1"], "CO(rec)", r["logMmol_CO_reconstructed"], "CI", r["logMmol_CI_reconstructed"], "dust", r["logMmol_dust_reconstructed"])
