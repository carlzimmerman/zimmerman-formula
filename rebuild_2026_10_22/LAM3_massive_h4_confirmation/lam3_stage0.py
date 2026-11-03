"""LAM3 stage 0 (criteria d5c434a268): build the SAMI sample, check DA and NSA conventions against DynPop, F1/F2.
Run: python3 -I lam3_stage0.py. Seconds, single thread. kappa = 1/2 FITTED; not theory closed."""
import os, csv, glob, json, math, numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "_external_data")
SD = os.path.join(EXT, "lam3_sami_dr3_2026_11_03"); QD = os.path.join(EXT, "lam3_sdss_2026_11_03"); OUT = []; RES = {"lane": "LAM3", "stage": 0}
def P(s=""): print(s, flush=True); OUT.append(s)
def unit(ra, dec):
    r, d = np.radians(ra), np.radians(dec); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
def match(ra1, de1, ra2, de2, arcsec):
    d, i = cKDTree(unit(ra2, de2)).query(unit(ra1, de1), distance_upper_bound=2 * math.sin(math.radians(arcsec / 3600) / 2))
    return np.isfinite(d), np.minimum(i, len(ra2) - 1)
def DA(z):  # flat Omega_m 0.3, h 0.7, Mpc: classifier feature only (criteria)
    return 299792.458 / 70 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x)**3 + 0.7), 0, z)[0] / (1 + z)
fl = lambda v: float(v) if v not in ("", "null", None) else np.nan

# ---- SAMI ----
kin = {r["CATID"]: r for r in csv.DictReader(open(os.path.join(SD, "stelkin.csv")))}
mge = {}
for r in csv.DictReader(open(os.path.join(SD, "mge.csv"))):
    if r["CATID"] not in mge or r["photometry"] == "SDSS": mge[r["CATID"]] = r  # SDSS row where a galaxy has two
pos = {}
for f in ("pos_gama", "pos_clusters", "pos_filler"):
    for r in csv.DictReader(open(os.path.join(SD, f + ".csv"))): pos.setdefault(r["CATID"], (float(r["RA_OBJ"]), float(r["DEC_OBJ"])))
ids = [c for c in kin if c in mge and c in pos]
lam = np.array([fl(kin[c]["LAMBDAR_RE_MGE"]) for c in ids]); eps = np.array([fl(mge[c]["epsMGE_Re"]) for c in ids])
epsLW = np.array([fl(mge[c]["epsMGE_LW"]) for c in ids]); re_as = np.array([fl(mge[c]["ReMGE"]) for c in ids])
ra = np.array([pos[c][0] for c in ids]); de = np.array([pos[c][1] for c in ids])
ok = np.isfinite(lam) & np.isfinite(eps) & (eps >= 0) & np.isfinite(re_as) & (re_as > 0)
P(f"SAMI: Stelkin {len(kin)}, with MGE and position {len(ids)}, finite lambda/eps/Re {int(ok.sum())}")
dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
inMaNGA, jd = match(ra, de, dp["obj_ra"], dp["obj_dec"], 3.0)
P(f"Independence: {int((ok & inMaNGA).sum())} SAMI galaxies within 3\" of a DynPop galaxy, removed")

# ---- SDSS spectra + NSA ----
def rows(pat):
    out = []
    for fn in sorted(glob.glob(os.path.join(QD, pat))):
        L = open(fn).read().splitlines()
        if len(L) > 2: out += list(csv.DictReader(L[1:]))
    return out
S = rows("spec_ra*.csv"); N = rows("nsa_ra*.csv")
sra = np.array([float(r["ra"]) for r in S]); sde = np.array([float(r["dec"]) for r in S])
nra = np.array([float(r["ra"]) for r in N]); nde = np.array([float(r["dec"]) for r in N])
hs, js = match(ra, de, sra, sde, 1.0); hn, jn = match(ra, de, nra, nde, 3.0)
P(f"SDSS SpecObj rows {len(S)}, NSA rows {len(N)}; SAMI with spectrum <=1\" {int((ok & hs).sum())}, with NSA <=3\" {int((ok & hn).sum())}")
g = lambda k: np.array([fl(S[j][k]) if h else np.nan for h, j in zip(hs, js)])
gn = lambda k: np.array([fl(N[j][k]) if h else np.nan for h, j in zip(hn, jn)])
z, vd, vde, sn = g("z"), g("velDisp"), g("velDispErr"), g("snMedian"); ew = -g("h_alpha_eqw")
mass = gn("sersic_mass"); logm = np.where(mass > 0, np.log10(np.clip(mass, 1e-30, None)), np.nan) + 0.310

# ---- convention checks on the MaNGA overlap (these galaxies are then removed) ----
ov = ok & inMaNGA & hn
dpm = dp["nsa_sersic_mass"][jd[ov]].astype(float); dpm = np.where(dpm > 100, np.log10(np.clip(dpm, 1, None)), dpm)
dm = (logm[ov] - 0.310) - dpm
P(f"Check NSA mass vs DynPop's on {int(ov.sum())} overlap galaxies: median d log M* {np.nanmedian(dm):+.4f}, |d| > 0.01 in {int((np.abs(dm) > 0.01).sum())}")
zz = dp["z"].astype(float); dd = dp["DA"].astype(float); pick = np.flatnonzero(np.isfinite(zz) & (zz > 0) & np.isfinite(dd))[::20]
rat = np.array([DA(zz[i]) / dd[i] for i in pick]); dac = abs(np.median(rat) - 1) <= 0.01
P(f"Check DA(flat 0.3, h 0.7) / DynPop DA on {len(pick)} DynPop galaxies: median {np.median(rat):.4f}, 5-95 % {np.percentile(rat, 5):.4f}-{np.percentile(rat, 95):.4f}: {'OK' if dac else 'MISMATCH'}")
RES["checks"] = dict(nsa_dlogm_median=float(np.nanmedian(dm)), n_overlap=int(ov.sum()), DA_ratio_median=float(np.median(rat)), DA_ok=bool(dac))

# ---- cuts ----
slow = lam < 0.31 * np.sqrt(np.clip(eps, 0, None))
qual = (sn >= 20) & (vd >= 100) & (vde / vd < 0.10)
base = ok & ~inMaNGA & hs & hn & np.isfinite(logm) & qual & np.isfinite(ew)
poor = base & (ew < 3); prim = poor & (logm > 11.17); sec = poor & (vd > 10**2.327)
for nm, m in (("quality + spectrum + NSA, independent", ok & ~inMaNGA & hs & hn & qual), ("  with galSpecLine", base),
              ("gas-poor", poor), ("PRIMARY log M* > 11.17", prim), ("SECONDARY velDisp > 212", sec)):
    P(f"{nm}: N {int(m.sum())}, slow {int((m & slow).sum())}")
def hm(A, n1, n2):
    q1, q2 = A / (2 - A), 2 * A * A / (1 + A)
    return math.sqrt((A * (1 - A) + (n1 - 1) * (q1 - A * A) + (n2 - 1) * (q2 - A * A)) / (n1 * n2))
n, ns = int(prim.sum()), int((prim & slow).sum()); f1 = n >= 150 and ns >= 40
sa = hm(0.75, ns, n - ns) if ns and n - ns else float("inf"); f2 = sa <= 0.020
P(f"F1 primary N {n} (>= 150), slow {ns} (>= 40): {'PASS' if f1 else 'FAIL'}")
P(f"F2 Hanley-McNeil sigma(AUC) at 0.75: {sa:.4f} (<= 0.020): {'PASS' if f2 else 'FAIL'}")
n2, ns2 = int(sec.sum()), int((sec & slow).sum()); P(f"   row: secondary sigma(AUC) {hm(0.75, ns2, n2 - ns2) if ns2 and n2 - ns2 else float('inf'):.4f}")
v = "PASS" if f1 and f2 else ("STOP: NOT FEASIBLE" if not f1 else "STOP: NOT POWERED")
P(f"STAGE 0: {v}"); RES.update(F1=dict(n=n, n_slow=ns, pass_=bool(f1)), F2=dict(sigma_auc=sa, pass_=bool(f2)), verdict=v)
idx = np.flatnonzero(base)
with open(os.path.join(HERE, "lam3_sample.csv"), "w") as fo:
    fo.write("catid,specobjid,plate,mjd,fiberID,run2d,gas_poor,slow,primary,secondary\n")
    for i in idx:
        r = S[js[i]]; fo.write(f"{ids[i]},{r['specobjid']},{r['plate']},{r['mjd']},{r['fiberID']},{r['run2d']},{int(poor[i])},{int(slow[i])},{int(prim[i])},{int(sec[i])}\n")
open(os.path.join(HERE, "lam3_stage0.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "lam3_stage0.json"), "w"), indent=1, default=float)
