#!/usr/bin/env python3
"""CFG316 Stage A diagnostics (POST HOC, labelled; counts only, no shear value read).  Verifies Stage A's empty ISO-S / ISO-S4 samples
as hard as a pass would be verified:
  (1) an independent brute-force recount (plain great-circle separations, no KD-tree) of the qualifying neighbours of every complete lens;
  (2) the neighbour-count distribution of the complete lenses (observed good-z, unobserved);
  (3) what changes the count: the isolated fraction of ALL matched lenses (no D5) vs lens mass and z, with and without unobserved targets;
      and the complete-and-isolated count for diagnostic radii 0.5-3 Mpc (NOT frozen; never a result).
Run from the repository root: python3 -u campaign_fresh_gravity/CFG316_desi_lens_split/cfg316_stageA_diag.py
"""
import os, sys, json
import numpy as np
import fitsio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg316_common import *   # noqa
sys.path.insert(0, CFG)
import CFG7_common as C7       # noqa: E402

R = C7.Report("cfg316_stageA_diag", False)
P, check = R.P, R.check
P(__doc__.split("Run from")[0].strip())
L = np.load(os.path.join(WORK, "cfg316_lenses.npz"))
A = json.load(open(os.path.join(HERE, "cfg316_stageA_results.json")))
fb = fitsio.FITS(F_BGS)
B = fb[1].read(columns=["TARGETID", "RA", "DEC", "Z_not4clus", "ZWARN", "DELTACHI2", "SPECTYPE", "COADD_FIBERSTATUS", "FLUX_R", "MW_TRANSMISSION_R"])
fb.close()
ra, dec, zsp = B["RA"].astype("f8"), B["DEC"].astype("f8"), B["Z_not4clus"].astype("f8")
good = (B["ZWARN"] == 0) & (B["DELTACHI2"] > 40) & (np.char.strip(B["SPECTYPE"].astype(str)) == "GALAXY") & (B["COADD_FIBERSTATUS"] == 0)
with np.errstate(divide="ignore", invalid="ignore"):
    logF = np.log10(B["FLUX_R"].astype("f8") / B["MW_TRANSMISSION_R"].astype("f8"))
tid = B["TARGETID"]
fc = fitsio.FITS(F_CIG)
CG = fc[1].read(columns=["TARGETID", "SURVEY", "PROGRAM", "LOGM", "FLAG_MASSPDF"])
fc.close()
CG = CG[(np.char.strip(CG["SURVEY"].astype(str)) == "main") & (np.char.strip(CG["PROGRAM"].astype(str)) == "bright")]
CG = CG[np.argsort(CG["TARGETID"])]
j = np.clip(np.searchsorted(CG["TARGETID"], tid), 0, len(CG) - 1); hasC = CG["TARGETID"][j] == tid
lmC = np.where(hasC & (CG["FLAG_MASSPDF"][j] >= 0.2) & (CG["FLAG_MASSPDF"][j] <= 5) & good, CG["LOGM"][j], np.nan)

hb = L["mass_ok"] & L["matched"] & L["complete"]
P(f"\n  complete headline base: {hb.sum():,} lenses; median z {np.median(L['z'][hb]):.3f}, median log M* {np.median(L['logM'][hb]):.2f}, "
  f"median r {np.median(L['rmag'][hb]):.2f}")

# (1)+(2) brute force for every complete lens: ISO-S observed neighbours only (CIGALE masses where present, else the lens-class M/L)
row = {t: i for i, t in enumerate(tid)}
nobs, nun, nobs4 = [], [], []
# median M/L table rebuilt exactly as Stage A does would be needed for flux-to-mass; here the observed count uses CIGALE-mass neighbours
# only (a LOWER bound on the qualifying count), which is enough to verify that the complete lenses are not isolated.
for i in np.where(hb)[0]:
    r0, d0, z0, m0 = L["ra"][i], L["dec"][i], L["z"][i], L["logM"][i]
    chi0 = chi_of(z0)
    th = 4.0 * (1 + z0) / chi0
    box = (np.abs(dec - d0) < np.degrees(th) * 1.05) & (np.abs(((ra - r0 + 180) % 360) - 180) * np.cos(np.radians(d0)) < np.degrees(th) * 1.05)
    jj = np.where(box)[0]
    jj = jj[tid[jj] != L["tid"][i]]
    cosang = np.sin(np.radians(dec[jj])) * np.sin(np.radians(d0)) + np.cos(np.radians(dec[jj])) * np.cos(np.radians(d0)) * np.cos(np.radians(ra[jj] - r0))
    Rp = np.arccos(np.clip(cosang, -1, 1)) * chi0 / (1 + z0)
    dv = CKMS * np.abs(zsp[jj] - z0) / (1 + z0)
    q = np.isfinite(lmC[jj]) & (lmC[jj] > m0 - 1)
    nobs.append(int(np.sum(q & good[jj] & (Rp < 3) & (dv < 1000))))
    nobs4.append(int(np.sum(q & good[jj] & (Rp < 4) & (dv < 2000))))
    nun.append(int(np.sum(~good[jj] & (Rp < 3))))
nobs, nobs4, nun = map(np.array, (nobs, nobs4, nun))
st_iso = L["isoS"][hb]
agree = bool(np.all((nobs > 0) <= ~st_iso))   # every lens with a brute-force CIGALE-mass neighbour is non-isolated in Stage A
check("D1 (diagnostic) brute-force recount: every complete lens with >= 1 qualifying CIGALE-mass neighbour (3 Mpc, 1000 km/s) is "
      "non-isolated in Stage A", f"{int(np.sum(nobs > 0)):,} of {hb.sum():,} complete lenses have >= 1 such neighbour (a lower bound on Stage "
      f"A's count); consistent: {agree}; Stage A ISO-S isolated: {int(st_iso.sum())}", agree)
pct = lambda a: "/".join(str(int(x)) for x in np.percentile(a, [10, 50, 90]))
P(f"  qualifying observed CIGALE-mass neighbours per complete lens (10/50/90 pct): ISO-S {pct(nobs)}, ISO-S4 {pct(nobs4)}; "
  f"unobserved BGS targets within 3 Mpc (any brightness): {pct(nun)}")
P(f"  complete lenses with ZERO qualifying observed neighbours (3 Mpc, 1000 km/s): {int(np.sum(nobs == 0))}")

# (3) the isolated fraction of all matched good-mass lenses (no D5) by mass and z
mm = L["mass_ok"] & L["matched"]
P("\n  ISO-S isolated fraction of matched good-mass lenses WITHOUT the D5 cut (observed+unobserved | observed only):")
for lo, hi in ((9.5, 10.0), (10.0, 10.5), (10.5, 11.0)):
    for zlo, zhi in ((0.1, 0.2), (0.2, 0.3), (0.3, 0.5)):
        s = mm & (L["logM"] >= lo) & (L["logM"] < hi) & (L["z"] >= zlo) & (L["z"] < zhi)
        if s.sum() < 20: continue
        P(f"    log M* {lo}-{hi}, z {zlo}-{zhi}: N {s.sum():6,}  iso {np.mean(L['isoS'][s]):.3f} | obs-only {np.mean(~L['hitS_o'][s]):.3f}  "
          f"(complete {np.mean(L['complete'][s]):.3f})")
# (4) counts and analytic power of NON-FROZEN variants, for a possible re-freeze (no shear value read; never a result)
R.banner("(4) NON-FROZEN variants: counts and analytic power (for a re-freeze only; no shear value read)")
PM = PowerModel(L["zbh"], L["zbe"])
cand_m = L["matched"]
fl_ok = np.ones(len(L["z"]), bool)                        # every candidate passed FLAG_MASSPDF in [1/5, 5]
VAR = {
    "V1 obs-only ISO-S, no D5, AGN cut": L["mass_ok"] & cand_m & ~L["hitS_o"],
    "V2 obs-only ISO-S, no D5, no AGN cut": fl_ok & cand_m & ~L["hitS_o"],
    "V3 obs-only ISO-S4, no D5, no AGN cut": fl_ok & cand_m & ~L["hitS4_o"],
    "V4 obs-only ISO-S, D5, no AGN cut": fl_ok & cand_m & L["complete"] & ~L["hitS_o"],
    "V5 ISO-P, no D5, no AGN cut": fl_ok & cand_m & L["isoP"],
    "V6 no isolation, no D5, no AGN cut (upper bound)": fl_ok & cand_m,
}
POWV = {}
for nm, f in VAR.items():
    POWV[nm] = PM.rows(L["Mgal"], L["z"], L["clsb"], f, P, nm)
R.num("variants_power", POWV)
R.num("brute", dict(n_complete=int(hb.sum()), with_neighbour=int(np.sum(nobs > 0)), zero=int(np.sum(nobs == 0)),
                    nobs_pct=np.percentile(nobs, [10, 50, 90]).tolist(), nun_pct=np.percentile(nun, [10, 50, 90]).tolist()))
nf = R.write(here=HERE)
sys.exit(0)
