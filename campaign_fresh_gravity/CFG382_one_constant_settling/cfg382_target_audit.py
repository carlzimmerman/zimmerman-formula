"""CFG382 POST-RUN target audit (labelled; the frozen PARTIAL stands): put groups and clusters on ONE definition (A: (M_tot - M_b - M_ph)/(5.364 M_b))
and ONE hydrostatic-bias treatment, then re-compare the CFG382 predictions (0.722 groups / 0.714 clusters)."""
import json, os, sys, math
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..")); import CFG4_common as C4
G, MSUN, KPC = 6.674e-8, 1.989e33, 3.0857e21; a0 = 9.3603e-9
def defA(Mhse, Mb, b):
    gN = G * Mb * MSUN / (Rk * KPC) ** 2
    Mph = (C4.nu_mono(np.array([gN / a0]))[0] - 1) * Mb
    return (Mhse / (1 - b) - Mb - Mph) / (5.364 * Mb)
xdir = os.path.join(REPO, "real_research", "data", "xcop"); r5 = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
BS = (0.0, 0.1, 0.2, 0.3)
cl = {b: [] for b in BS}
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r5 or not os.path.exists(os.path.join(d, f"{nm}_mstar.fits")):
        continue
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data; fg = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"].data
    ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
    Rk = r5[nm]["R500"] * 1000
    Mh = float(np.interp(Rk, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float)))
    Mg = float(np.exp(np.interp(0.0, np.log(np.asarray(fg["RADIUS"], float)), np.log(np.asarray(fg["MGAS"], float)))))
    Ms = float(np.exp(np.interp(np.log(Rk), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
    for b in BS:
        cl[b].append(defA(Mh, Mg + Ms, b))
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], [x for x in rows[1:] if len(x) > 5]
grp = {b: [] for b in BS}
for x in rows:
    Rk = float(x[hdr.index("R500_kpc")]); Mh = float(x[hdr.index("M500_1e13")]) * 1e13; Mg = float(x[hdr.index("Mgas500_1e12")]) * 1e12
    Mb = Mg * 1.10                                   # stars := 0.10 M_gas (declared bracket-free placeholder; groups have no stellar profiles here)
    for b in BS:
        grp[b].append(defA(Mh, Mb, b))
print("Definition A, same hydrostatic bias b for both (median; 16-84%):")
out = {}
for b in BS:
    g, c = np.array(grp[b]), np.array(cl[b])
    out[b] = dict(groups=float(np.median(g)), clusters=float(np.median(c)))
    print(f"  b = {b:.1f}: groups {np.median(g):.3f} [{np.percentile(g,16):.2f}-{np.percentile(g,84):.2f}]  clusters {np.median(c):.3f} [{np.percentile(c,16):.2f}-{np.percentile(c,84):.2f}]"
          f"  | CFG382 predicts 0.722 / 0.714 -> {'both within 0.15' if abs(np.median(g)-0.722)<=0.15 and abs(np.median(c)-0.714)<=0.15 else 'not both'}")
json.dump({str(k): v for k, v in out.items()}, open(os.path.join(HERE, "cfg382_target_audit_results.json"), "w"), indent=1)
