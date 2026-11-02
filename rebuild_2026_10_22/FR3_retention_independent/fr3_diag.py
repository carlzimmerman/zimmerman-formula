#!/usr/bin/env python3
"""FR3 diagnostics, POST-RESULT, no label: dz outliers; XXL overlap Umetsu vs Okabe mass, E16 vs eRASS1 gas; eFEDS report-only row. python3 -I."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); sys.path.insert(0, HERE)
import numpy as np
from astropy.io import fits
import fr3_parse as FP
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
h = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
E = {str(n).strip().split("J")[-1]: i for i, n in enumerate(h["NAME"])}; eMg, eM, eR, eZ, eRA, eDE, eZt = np.array(h["MGAS500"], float) * 1e11, np.array(h["M500"], float) * 1e13, np.array(h["R500"], float), np.array(h["BEST_Z"], float), np.array(h["RA"], float), np.array(h["DEC"], float), h["BEST_Z_TYPE"]
ok = FP.okabe(); P("Okabe z vs eRASS1 BEST_Z, |dz| > 0.02")
for r in ok:
    if r["id"] in E and abs(r["z"] - eZ[E[r["id"]]]) > .02: i = E[r["id"]]; P(f"  {r['id']}{r['flag']} z {r['z']:.3f} BEST_Z {eZ[i]:.3f} {str(eZt[i]).strip()} M500_WL {r['M500']} lg Mg {math.log10(eMg[i]) if eMg[i] > 0 else float('nan'):.2f}")
def sep(a, b, c, d):
    a, b, c, d = map(np.radians, (a, b, c, d)); return np.degrees(np.arccos(np.clip(np.sin(b) * np.sin(d) + np.cos(b) * np.cos(d) * np.cos(a - c), -1, 1)))
U = FP.tsv(os.path.join(HERE, "data", "umetsu20_table2.tsv"))["J/ApJ/890/148/table2"]; X = {int(r["XLSSC"]): r for r in list(FP.tsv(os.path.join(REPO, "_external_data", "gs4", "xxl100", "xxl100gc.tsv")).values())[0]}
P("\nXXL (E16 + Umetsu) x eRASS1, 3 arcmin, |dz| <= 0.03, lg ratios at eRASS1's R500 with slope 1.05 for the gas")
Rho = lambda z: 3 * (70e3 / 3.0857e22) ** 2 * (.3 * (1 + z) ** 3 + .7) / (8 * math.pi * 6.674e-11); MR = lambda Rk, z: 500 * Rho(z) * 4 / 3 * math.pi * (Rk * 3.0857e19) ** 3 / 1.989e30
rows = []
for r in U:
    x = X.get(int(r["XLSSC"]));
    if x is None: continue
    ra, de, z = FP.fl(r["RAJ2000"]), FP.fl(r["DEJ2000"]), FP.fl(r["z"]); d = sep(ra, de, eRA, eDE) * 60; j = np.where((d <= 3) & (np.abs(eZ - z) <= .03) & (eMg > 0))[0]
    if not len(j): continue
    i = j[np.argmin(d[j])]; me = MR(FP.fl(x["r500MT"]) * 1e3, z); mg = FP.fl(x["Mgas500"]) * 1e13
    if mg > 0: rows.append(dict(x=int(r["XLSSC"]), z=z, mu=FP.fl(r["M500"]) * 1e14, su=FP.fl(r["e_M500"]) * 1e14, me=me, mc=eM[i], g_E=mg, g_e=eMg[i], R=eR[i], Re=FP.fl(x["r500MT"]) * 1e3, name=str(h["NAME"][i]).strip().split("J")[-1], gatC=mg * (eR[i] / (FP.fl(x["r500MT"]) * 1e3)) ** 1.05))
P(f"  N {len(rows)}"); O = {r["id"]: r for r in ok}
if rows:
    Mg = np.array([r["gatC"] for r in rows]); ge = np.array([r["g_e"] for r in rows]); P(f"  E16 gas moved to eRASS1's R500 vs eRASS1 MGAS500: median lg ratio {np.median(np.log10(Mg / ge)):+.3f} +- {1.25 * np.std(np.log10(Mg / ge)) / math.sqrt(len(Mg)):.3f}")
    mus = np.array([r["mu"] for r in rows]); mc = np.array([r["mc"] for r in rows]); me = np.array([r["me"] for r in rows]); P(f"  lg <Umetsu M500> / <eRASS1 M500>: {math.log10(mus.sum() / mc.sum()):+.3f}; lg <E16 r500MT mass> / <eRASS1 M500>: {math.log10(me.sum() / mc.sum()):+.3f}; lg <Umetsu>/<E16>: {math.log10(mus.sum() / me.sum()):+.3f}")
    both = [r for r in rows if r["name"] in O and O[r["name"]]["M500"] is not None]
    for r in both: P(f"  XLSSC {r['x']} {r['name']} z {r['z']:.3f}: Okabe {O[r['name']]['M500']:.2f} Umetsu {r['mu'] / 1e14:.2f} +- {r['su'] / 1e14:.2f}, E16 {r['me'] / 1e14:.2f}, eRASS1 {r['mc'] / 1e14:.2f}; gas eRASS1 {r['g_e'] / 1e13:.2f}, E16 at that R {r['gatC'] / 1e13:.2f}")
    if both: oks = np.array([O[r['name']]['M500'] for r in both]) * 1e14; us = np.array([r['mu'] for r in both]); P(f"  overlap Okabe vs Umetsu, N {len(both)}: lg <Okabe>/<Umetsu> {math.log10(oks.sum() / us.sum()):+.3f}")
# eFEDS report only
Ch = {r["Name"]: r for r in list(FP.tsv(os.path.join(HERE, "data", "chiu22.tsv")).values())[0]}; BH = list(FP.tsv(os.path.join(REPO, "real_research", "data", "efeds_bahar2022_table2.tsv")).values())[0]; ccRA = np.array([FP.fl(r["_RA"]) for r in Ch.values()]); ccDE = np.array([FP.fl(r["_DE"]) for r in Ch.values()]); cR = list(Ch.values())
def DAk(z, Om=.3089, H0=67.74): zz = np.linspace(0, z, 400); return 299792.458 / H0 * np.trapz(1 / np.sqrt(Om * (1 + zz) ** 3 + 1 - Om), zz) / (1 + z)
R = []
for r in BH:
    ra, de, z, Mg, Rm = FP.fl(r["RAJ2000"]), FP.fl(r["DEJ2000"]), FP.fl(r["z"]), FP.fl(r["Mgas500"]), FP.fl(r["R500"])
    if r.get("l_Mgas500", "") not in ("",) or not (Mg > 0 and Rm > 0) or z > .5: continue
    d = sep(ra, de, ccRA, ccDE) * 3600; j = int(np.argmin(d))
    if d[j] > 30: continue
    q = cR[j]; lm = FP.fl(q["logM500R0.2B"]); s = FP.fl(q["e_logM500R0.2B"])
    if not np.isfinite(lm): continue
    Rk = Rm / 60 * math.pi / 180 * DAk(z) * 1e3; h = 67.74 / 70; R.append(dict(z=z, mg=Mg * 1e12 * h ** 2.5, m=10 ** lm / .7, mB=MR(Rk * h, z), s=s))
P(f"\neFEDS report only, N {len(R)}, Chiu lg M500 treated as M h (h 0.7); Bahar gas moved to h 0.7")
m = np.array([r["m"] for r in R]); g = np.array([r["mg"] for r in R]); mB = np.array([r["mB"] for r in R]); sel = (np.log10(g) >= 12.75) & (np.log10(g) < 13.58); xx = math.log10(m[sel].mean()); dd = math.log10(m[sel].mean() / mB[sel].mean()) / 3; gg = g[sel].mean() * 10 ** (1.05 * dd); y = math.log10(6.2715 * gg / m[sel].mean()); P(f"  gas bin N {int(sel.sum())}: x {xx:.3f}, lg <M Chiu>/<M from Bahar R500> {3 * dd:+.3f}, lg Y {y:+.3f}; H {-.121 + .219 * (xx - 14.5):+.3f}, W {-.321 + .263 * (xx - 14.5):+.3f}. Same reading with no h conversion of Chiu: x {xx + math.log10(.7):.3f}. Report only; M from count rate, not a test")
open(os.path.join(HERE, "fr3_diag.out"), "w").write("\n".join(OUT) + "\n")
