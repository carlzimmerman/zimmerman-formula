"""Surface-density profiles of the disk-only SPARC galaxies, for the /galaxy-sim page (live disk under the record's law).

Inputs (read-only): real_research/data/sparc_data/*_rotmod.dat (Lelli, McGaugh & Schombert 2016: Rad, Vobs, errV, Vgas, Vdisk, Vbul, SBdisk, SBbul),
  the master table via campaign_fresh_gravity/CFG4_common.load_sparc, the kernel nu_mono and a0 from ai_slop/website/public/data/to_scale.json.
Method:
  stars : Sigma_*(R) = Upsilon_disk * SBdisk(R)   (3.6 um L/pc^2; Upsilon_disk = 0.61, the record's value), truncated at the last tabulated radius.
          These become the live particles; their in-plane force is computed on a grid in the browser.
  gas   : NOT inverted. The gas does not respond in the simulation, so SPARC's own tabulated gas contribution Vgas(R) (signed V|V|, helium included)
          is used directly as a fixed axisymmetric Newtonian field. (A ring inversion to a surface density was tried and is ill-posed.)
  checks: (1) the thin-disk force of Sigma_* with SPARC's exponential-thickness correction (h_z = 0.196 R_d) must reproduce the tabulated Vdisk*sqrt(Upsilon);
          (2) the law g = nu(g_N/a0) g_N on [that stellar force + tabulated gas] must fit Vobs about as well as on SPARC's own tabulated curves.
          Galaxies with any bulge light are skipped (a spherical bulge is not a thin disk), as are curves with fewer than 8 points.
Output: public/data/sparc_sim.json
Run from the repo root: python3 ai_slop/website/scripts/build_sparc_sim.py
"""
import json, os, sys
import numpy as np
from scipy.special import j0, j1

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C  # noqa: E402

OUT = os.path.join(REPO, "ai_slop", "website", "public", "data", "sparc_sim.json")
TS = json.load(open(os.path.join(REPO, "ai_slop", "website", "public", "data", "to_scale.json")))
G = TS["G"]                                  # kpc (km/s)^2 / Msun
A0K = TS["a0"]["canonical"] * TS["a0_unit_conv"]   # a0 in (km/s)^2 / kpc
LY, NU = np.array(TS["kernel"]["log10y"]), np.array(TS["kernel"]["nu"])
UPS = TS["ups"]["disk"]
nu = lambda y: np.interp(np.log10(np.maximum(y, 1e-6)), LY, NU)
PC2KPC2 = 1e6                                # Msun/pc^2 -> Msun/kpc^2

KG = np.geomspace(2e-3, 60.0, 5000)          # k grid, 1/kpc
DKG = np.gradient(KG)

def vc2_thin(Rfine, sig, Robs, hz=0.0):
    """V_c^2(Robs) of an axisymmetric thin disk Sigma(Rfine) [Msun/kpc^2]; exponential vertical profile of scale hz gives a 1/(1+k hz) factor on the midplane potential."""
    w = sig * Rfine * np.gradient(Rfine)
    S = (j0(np.outer(KG, Rfine)) * w).sum(1) / (1.0 + KG * hz)
    f = (KG * S * DKG)[:, None] * j1(np.outer(KG, Robs))
    return 2 * np.pi * G * Robs * f.sum(0)

gals, skipped = [], {"bulge": 0, "short": 0, "no_sb": 0}
for g in C.load_sparc():
    m = g["meta"]
    if m is None:
        continue
    raw = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", g["name"] + "_rotmod.dat"), comments="#")
    R, Vo, eV, Vg, Vd, Vb, SB = (raw[:, i] for i in (0, 1, 2, 3, 4, 5, 6))
    if np.any(np.abs(Vb) > 0):
        skipped["bulge"] += 1; continue
    if len(R) < 8:
        skipped["short"] += 1; continue
    if not np.any(SB > 0):
        skipped["no_sb"] += 1; continue
    Rf = np.linspace(0.0, R.max(), 160)[1:]
    ss = np.interp(Rf, R, UPS * SB)                                             # Msun/pc^2, truncated at the last radius
    hz = 0.196 * m["Rdisk"]
    v2_star = vc2_thin(Rf, ss * PC2KPC2, R, hz)
    v_star = np.sqrt(np.maximum(v2_star, 0))
    ref = Vd * np.sqrt(UPS)
    star_err = float(np.sqrt(np.mean(((v_star - ref) / np.maximum(ref, 5)) ** 2)))   # fractional rms vs SPARC's own stellar curve
    # law on [model stars + SPARC's tabulated gas] vs the observed curve (algebraic RAR form, as the record fits SPARC)
    gN = (v2_star + np.sign(Vg) * Vg ** 2) / R
    gN_tab = (np.sign(Vg) * Vg ** 2 + Vd ** 2 * UPS) / R
    gobs = Vo ** 2 / R
    res = np.log10(np.maximum(gobs, 1e-9)) - np.log10(nu(np.maximum(gN, 1e-9) / A0K) * np.maximum(gN, 1e-9))
    res_tab = np.log10(np.maximum(gobs, 1e-9)) - np.log10(nu(np.maximum(gN_tab, 1e-9) / A0K) * np.maximum(gN_tab, 1e-9))
    gals.append(dict(name=g["name"], D=m["D"], Q=m["Q"], T=m["T"], Rd=m["Rdisk"], Vflat=m["Vflat"], Inc=m["Inc"], L36=m["L36"], MHI=m["MHI"],
                     Mstar=float(2 * np.pi * np.trapz(ss * PC2KPC2 * Rf, Rf)),
                     R=R.round(3).tolist(), Vobs=Vo.round(2).tolist(), eV=eV.round(2).tolist(), Vgas=Vg.round(2).tolist(), Vdisk=(Vd * np.sqrt(UPS)).round(2).tolist(),
                     Rf=Rf.round(4).tolist(), ss=np.round(ss, 4).tolist(),
                     chk=dict(star_frac_rms=round(star_err, 4), law_rms_dex=round(float(np.sqrt(np.mean(res ** 2))), 4), law_tab_rms_dex=round(float(np.sqrt(np.mean(res_tab ** 2))), 4))))
print(f"{len(gals)} disk-only galaxies kept; skipped {skipped}")
se = np.array([x["chk"]["star_frac_rms"] for x in gals]); lr = np.array([x["chk"]["law_rms_dex"] for x in gals]); lt = np.array([x["chk"]["law_tab_rms_dex"] for x in gals])
print(f"stellar thin-disk force vs SPARC Vdisk: median fractional rms {np.median(se):.3f}, 90th pct {np.percentile(se, 90):.3f}")
print(f"law on [model stars + tabulated gas] vs Vobs: median per-galaxy rms {np.median(lr):.3f} dex; on SPARC's own tabulated curves: {np.median(lt):.3f} dex (unweighted per-galaxy medians; the record's 0.10 is weighted over the whole sample)")
json.dump(dict(built_from="SPARC rotmod (Lelli+2016), Upsilon_disk 0.61, record kernel nu_mono, a0 canonical", G=G, a0_kms2_per_kpc=A0K, ups=UPS,
               kernel=dict(log10y=LY[::6].round(3).tolist(), nu=NU[::6].round(5).tolist()),
               summary=dict(n=len(gals), skipped=skipped, star_frac_rms_median=float(np.median(se)), law_rms_dex_median=float(np.median(lr)), law_tab_rms_dex_median=float(np.median(lt))),
               galaxies=gals), open(OUT, "w"), separators=(",", ":"))
print("wrote", OUT, f"{os.path.getsize(OUT) / 1e6:.2f} MB")
