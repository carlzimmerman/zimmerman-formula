#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG306 (PAPER40 referee): is CFG304's single-dish flux offset representative of CFG301's 47 discs?  Referee diagnostic, not frozen.

  S1  property distributions of CFG304's matched pairs (23 all codes, 15 code 1) against CFG301's 47: z, log M_HI, SNR_3D, W50, HI angular
      diameter (size relation at the catalogue distance), and the number of catalogued MIGHTEE neighbours in an Arecibo beam.
  S2  R_cat (catalogue/ALFALFA log flux ratio) against those properties (Spearman, all 23 and code 1), and the linear extrapolation of R_cat
      in log SNR_3D and in z to the 47's medians (bootstrap) -- an illustration of how far the 47 lie outside the calibrating pairs.
  S3  an order-of-magnitude bound on ALFALFA confusion by HI sources below MIGHTEE's catalogue (mean cosmic HI density in an Arecibo
      beam x velocity window, with an overdensity factor), against the HI mass the offset requires.
Writes cfg306_flux_scale.out and cfg306_flux_scale_results.json.
"""
import os, sys, json, math
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
LOG, NUM = [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


cat = pd.read_csv(os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv"), dtype={"ID_catalogue": str})
JA = json.load(open(os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_stageA_results.json")))["numbers"]
pairs = pd.read_csv(os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_matched_pairs.csv"))
S47 = cat[cat.ID_catalogue.isin(JA["survivor_ids"])].copy()
H0, OM = 70.0, 0.3


def DA(z):
    from scipy.integrate import quad
    dc = 299792.458 / H0 * quad(lambda x: 1 / math.sqrt(OM * (1 + x) ** 3 + 1 - OM), 0, z)[0]
    return dc / (1 + z)


def theta_hi(lmhi, z):
    dhi_kpc = 10 ** (0.506 * lmhi - 3.293)
    return dhi_kpc / (DA(z) * 1e3) * 206265.0


def n_neigh(ra, de, z, r_arcmin=3.5, dv=400.0):
    sep = np.hypot((cat.RA_deg - ra) * np.cos(np.radians(de)), cat.Dec_deg - de) * 60
    dcz = np.abs(cat.z_HI - z) * 299792.458
    return int(((sep <= r_arcmin) & (dcz <= dv)).sum() - 1)


for T in (S47,):
    T["theta_HI"] = [theta_hi(l, z) for l, z in zip(T.log_M_HI, T.z_HI)]
    T["nn"] = [n_neigh(r, d_, z) for r, d_, z in zip(T.RA_deg, T.Dec_deg, T.z_HI)]
pairs = pairs.merge(cat[["ID_catalogue", "W_50_km_s", "incl_deg"]].rename(columns={"ID_catalogue": "ID"}), on="ID", how="left")
pairs["theta_HI"] = [theta_hi(l, z) for l, z in zip(pairs.log_M_HI, pairs.z_HI)]
pairs["nn"] = [n_neigh(r, d_, z) for r, d_, z in zip(pairs.RA_deg, pairs.Dec_deg, pairs.z_HI)]
c1 = pairs[pairs.hi_code == 1]
P("S1 PROPERTIES (median [16-84%])")
props = {}
for nm, col47, colp in (("z", "z_HI", "z_HI"), ("log M_HI", "log_M_HI", "log_M_HI"), ("SNR_3D", "SNR_3D", "SNR_3D"), ("W50", "W_50_km_s", "W_50_km_s"),
                        ("theta_HI arcsec", "theta_HI", "theta_HI"), ("MIGHTEE neighbours in 3.5' x 400 km/s", "nn", "nn")):
    row = {}
    for lab, v in (("47", S47[col47].values), ("pairs 23", pairs[colp].values), ("code1 15", c1[colp].values)):
        v = np.asarray(v, float)
        row[lab] = [float(np.median(v)), float(np.percentile(v, 16)), float(np.percentile(v, 84))]
    props[nm] = row
    P(f"  {nm:38s} 47: {row['47'][0]:.3f} [{row['47'][1]:.3f}-{row['47'][2]:.3f}]   23 pairs: {row['pairs 23'][0]:.3f} [{row['pairs 23'][1]:.3f}-{row['pairs 23'][2]:.3f}]   "
      f"15 code-1: {row['code1 15'][0]:.3f} [{row['code1 15'][1]:.3f}-{row['code1 15'][2]:.3f}]")
ov = {nm: float(np.mean((S47[c].values >= pairs[c].min()) & (S47[c].values <= pairs[c].max()))) for nm, c in (("z", "z_HI"), ("SNR_3D", "SNR_3D"), ("log M_HI", "log_M_HI"))}
P(f"  fraction of the 47 inside the pairs' range: z {ov['z']:.2f}, SNR_3D {ov['SNR_3D']:.2f}, log M_HI {ov['log M_HI']:.2f}")
NUM["S1"] = dict(props=props, frac47_inside_pairs_range=ov, n47_with_alfalfa_pair=int(S47.ID_catalogue.isin(pairs.ID).sum()))
P(f"  the 47 with an ALFALFA pair: {NUM['S1']['n47_with_alfalfa_pair']}")

P("\nS2 R_cat TRENDS AND EXTRAPOLATION")
rng = np.random.default_rng(3064)
S2 = {}
for lab, T in (("all 23", pairs), ("code 1 (15)", c1)):
    R = T.R_cat_OPT.values
    for nm, x in (("log SNR_3D", np.log10(T.SNR_3D.values)), ("z", T.z_HI.values), ("log M_HI", T.log_M_HI.values), ("theta_HI", T.theta_HI.values), ("W50", T.W_50_km_s.values)):
        r_, p_ = spearmanr(R, x)
        S2[f"{lab} | {nm}"] = dict(rho=float(r_), p=float(p_))
        P(f"  {lab:12s} Spearman(R_cat, {nm:10s}) rho {r_:+.2f}  p {p_:.2f}")
    for nm, x, x47 in (("log SNR_3D", np.log10(T.SNR_3D.values), float(np.median(np.log10(S47.SNR_3D)))), ("z", T.z_HI.values, float(np.median(S47.z_HI)))):
        ext = []
        for _ in range(4000):
            i = rng.integers(0, len(T), len(T))
            if np.ptp(x[i]) == 0:
                continue
            b = np.polyfit(x[i], R[i], 1); ext.append(np.polyval(b, x47))
        b0 = np.polyfit(x, R, 1)
        q = np.percentile(ext, [16, 50, 84])
        S2[f"{lab} | extrapolated to the 47's median {nm}"] = dict(slope=float(b0[0]), at_median47=float(np.polyval(b0, x47)), boot=q.tolist(), x47=x47)
        P(f"  {lab:12s} linear R_cat on {nm}: slope {b0[0]:+.3f}; at the 47's median ({x47:.3f}) R_cat {np.polyval(b0, x47):+.3f} (bootstrap 16/50/84 {q[0]:+.3f} / {q[1]:+.3f} / {q[2]:+.3f})")
NUM["S2"] = S2

P("\nS3 ALFALFA CONFUSION BY SUB-CATALOGUE HI (order of magnitude)")
rho_crit = 2.775e11 * (H0 / 100) ** 2
omega_hi = 3.9e-4                                   # ALFALFA HI mass function, Jones et al. 2018 (Omega_HI ~ 3.9e-4): an order-of-magnitude input
rho_hi = omega_hi * rho_crit
zc = float(np.median(c1.z_HI)); da = DA(zc)
r_beam = 3.5 / 2 / 60 * math.pi / 180 * da * (1 + zc)         # comoving radius of the beam (Mpc), half of 3.5'
depth = 2 * 300.0 / H0                                        # +-300 km/s in Hubble flow
vol = math.pi * r_beam ** 2 * depth
m_mean = rho_hi * vol
m_need = float(np.median(10 ** c1.log_M_HI.values) * (10 ** 0.195 - 1))
S3 = dict(z=zc, rho_hi=rho_hi, beam_radius_Mpc=r_beam, volume_Mpc3=vol, M_mean=m_mean, M_needed=m_need, overdensity_needed=m_need / m_mean)
P(f"  at z {zc:.3f}: beam radius {r_beam * 1e3:.0f} kpc, depth {depth:.1f} Mpc, volume {vol:.3f} Mpc^3; mean HI in it {m_mean:.2e} Msun (rho_HI {rho_hi:.2e} Msun/Mpc^3)")
P(f"  HI the -0.195 dex offset needs per galaxy: {m_need:.2e} Msun (median code-1 M_HI x (10^0.195 - 1)) -> overdensity {m_need / m_mean:.0f} of HI that MIGHTEE did not catalogue")
NUM["S3"] = S3

json.dump(dict(lane="CFG306", script=os.path.basename(__file__), note="referee diagnostic; not frozen", numbers=NUM),
          open(os.path.join(HERE, "cfg306_flux_scale_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg306_flux_scale.out"), "w").write(__doc__.strip() + "\n\n" + "\n".join(LOG) + "\n")
print("wrote cfg306_flux_scale.out and cfg306_flux_scale_results.json")
