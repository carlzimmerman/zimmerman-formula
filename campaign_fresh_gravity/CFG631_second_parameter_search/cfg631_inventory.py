"""CFG631 step 0: per-galaxy property inventory (coverage counts only; NO law residual is computed or read here).
SPARC (Lelli+16 MRT + rotmod), WALLABY DR2 (CFG537 build, executed unedited up to its forecast section), KiDS f30 lenses
(CFG531/585 lens table + KiDS bright-sample LePhare columns). Cross-matches by position only.
Run: nice -n 10 python3 cfg631_inventory.py > cfg631_inventory.out
"""
import os, io, re, json, gzip, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def unit(a, d):
    a, d = np.radians(np.asarray(a, float)), np.radians(np.asarray(d, float))
    return np.stack([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)], axis=-1)


def nearest(u, U):
    s = np.degrees(np.arccos(np.clip(U @ u, -1, 1))) * 3600
    i = int(np.argmin(s)); return i, float(s[i])


# ---------------- shared catalogues
RC3 = []
for line in open(os.path.join(DATA, "rc3_devaucouleurs1991_colors.tsv")):
    p = line.rstrip("\n").split("\t")
    if len(p) < 12:
        continue
    a, d = fnum(p[0]), fnum(p[1])
    if np.isfinite(a) and np.isfinite(d):
        RC3.append(dict(ra=a, dec=d, T=fnum(p[5]), BT=fnum(p[6]), BV=fnum(p[8]), BVo=fnum(p[10]), UB=fnum(p[11])))
U3 = unit([r["ra"] for r in RC3], [r["dec"] for r in RC3])
D1 = {}
with gzip.open(os.path.join(EXT, "alfalfa_sdss", "durbala2020_table1.dat.gz"), "rt") as f:
    for ln in f:
        D1[int(ln[0:6])] = (fnum(ln[30:40]), fnum(ln[41:49]))
D2 = {}
with gzip.open(os.path.join(EXT, "alfalfa_sdss", "durbala2020_table2.dat.gz"), "rt") as f:
    for ln in f:
        D2[int(ln[0:6])] = dict(gi=fnum(ln[30:35]), sfr22=fnum(ln[78:83]), sfrn=fnum(ln[89:94]))
DK = [k for k in D1 if k in D2]
UD = unit([D1[k][0] for k in DK], [D1[k][1] for k in DK])

# ---------------- SPARC
keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
TAB = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) == 19:
        try:
            TAB[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError:
            pass
S = [n for n, t in TAB.items() if t["Q"] <= 2 and t["Inc"] >= 30 and os.path.exists(os.path.join(DATA, "sparc_data", f"{n}_rotmod.dat"))]
pos = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
env = {r.split(",")[0]: r.strip().split(",") for r in open(os.path.join(DATA, "sparc_a0_environment_table.csv")).readlines()[1:]}
cw = {r.split(",")[0]: r.strip().split(",") for r in open(os.path.join(DATA, "sparc_cosmicweb_match.csv")).readlines()[1:]}
cnt = dict(N=len(S), pos=0, rc3_BV=0, rc3_BVo=0, rc3_BT=0, durbala_gi=0, durbala_sfr=0, env_2mrs=0, env_2mpp=0, cweb_class=0, bulge=0)
fD = {}
for n in S:
    t = TAB[n]
    fD[int(t["fD"])] = fD.get(int(t["fD"]), 0) + 1
    d = np.loadtxt(os.path.join(DATA, "sparc_data", f"{n}_rotmod.dat"), comments="#")
    cnt["bulge"] += int(np.any(d[:, 5] > 0))
    p = pos.get(n)
    if p and p.get("ra") is not None:
        cnt["pos"] += 1; u = unit(p["ra"], p["dec"])
        i, s = nearest(u, U3)
        if s <= 30:
            cnt["rc3_BV"] += np.isfinite(RC3[i]["BV"]); cnt["rc3_BVo"] += np.isfinite(RC3[i]["BVo"]); cnt["rc3_BT"] += np.isfinite(RC3[i]["BT"])
        j, s2 = nearest(u, UD)
        if s2 <= 30:
            q = D2[DK[j]]; cnt["durbala_gi"] += np.isfinite(q["gi"]); cnt["durbala_sfr"] += np.isfinite(q["sfr22"]) or np.isfinite(q["sfrn"])
    if n in env:
        cnt["env_2mrs"] += env[n][7] == "1"; cnt["env_2mpp"] += env[n][10] not in ("", "nan")
    if n in cw:
        cnt["cweb_class"] += cw[n][11] not in ("",)
P("=" * 90); P("CFG631 step 0 — property inventory (coverage only)"); P("=" * 90)
P(f"SPARC (Q<=2, Inc>=30, rotmod present): N {cnt['N']}")
P(f"  in MRT for all: T (Hubble type), distance + method fD {dict(sorted(fD.items()))} (1 Hubble flow, 2 TRGB, 3 Cepheid, 4 UMa, 5 SN), Inc, L[3.6],"
  " R_eff, SB_eff, R_d, SB_d, M_HI, R_HI, V_flat")
P(f"  rotmod: bulge component present in {cnt['bulge']}; gas fraction from M_HI (HI only; no H2 on disk)")
P(f"  RC3 (30\"): B-V_T {cnt['rc3_BV']}, (B-V)_T^0 {cnt['rc3_BVo']}, B_T {cnt['rc3_BT']} (of {cnt['pos']} with positions)")
P(f"  ALFALFA-SDSS Durbala+20 (30\"): g-i {cnt['durbala_gi']}, SFR (22um or NUV) {cnt['durbala_sfr']}")
P(f"  environment: 2MRS usable {cnt['env_2mrs']}, 2M++ density {cnt['env_2mpp']} (sparc_a0_environment_table, 122 rows); cosmic-web class {cnt['cweb_class']}")
P("  NOT on disk for SPARC: metallicity, H2 masses, ages; SFR only via the northern ALFALFA overlap")

# ---------------- WALLABY (CFG537 head executed unedited; no residual computed)
SRC = os.path.join(LANES, "CFG537_outer_excess_independent", "cfg537_wallaby.py")
src = open(SRC).read(); cut = "# ================================================================== power forecast"
os.environ.pop("CFG537_MUTATE", None)
ns = {"__file__": SRC, "__name__": "cfg537_head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src.split(cut)[0], SRC, "exec"), ns)
GALS, best, wise = ns["GALS"], ns["best"], ns["wise"]
import csv
w12 = {}
for r in csv.DictReader(open(os.path.join(EXT, "wallaby_dr2", "allwise_wallaby_dr2.csv"))):
    a, b = fnum(r.get("w1mpro")), fnum(r.get("w2mpro"))
    w12[r["wallaby_name"]] = a - b
wc = dict(N=len(GALS), BV=0, BVo=0, BT=0, W12=0, inc=0, nout2=0)
for g in GALS:
    r = best[g["name"]]; u = unit(fnum(r["RA_model"]), fnum(r["DEC_model"]))
    i, s = nearest(u, U3)
    if s <= 30:
        wc["BV"] += np.isfinite(RC3[i]["BV"]); wc["BVo"] += np.isfinite(RC3[i]["BVo"]); wc["BT"] += np.isfinite(RC3[i]["BT"])
    wc["W12"] += np.isfinite(w12.get(g["name"], np.nan)); wc["inc"] += np.isfinite(fnum(r["Inc_model"])); wc["nout2"] += g["nout"] >= 2
P(f"\nWALLABY DR2 (CFG537 build): N {wc['N']} (outer band >=2 rings: {wc['nout2']})")
P("  in build: T (RC3), Hubble-flow distance only (dist_h), M_HI, K-band L (2MASS), K-band R_eff -> R_d, f_gas, M_b")
P(f"  kinematic catalogue inclination {wc['inc']}; RC3 B-V_T {wc['BV']}, (B-V)_T^0 {wc['BVo']}, B_T {wc['BT']}; AllWISE W1-W2 {wc['W12']}")
P("  NOT on disk: SFR, H2, metallicity, bulge decomposition, environment counts")

# ---------------- KiDS f30 lenses
P("\nKiDS f30 lenses (CFG531/585 machinery; stacked lensing, no per-galaxy residual):")
P("  on disk: log M* (lens table), type (u-r > 2), LePhare absolute mags u,g,r,i,Z,Y,J,H,Ks (colours u-r, g-r, r-Ks), SFR_BEST (sSFR),")
P("  photo-z, r-band apparent mag; CFG509 companion counts (environment). NOT on disk: sizes, Sersic index, surface brightness, metallicity, HI/H2")
from astropy.io import fits
Lp = fits.open(os.path.join(DATA, "lensing_rar", "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
sfr = np.asarray(Lp["SFR_BEST"], float)
P(f"  LePhare rows {len(sfr)}; SFR_BEST finite {int(np.isfinite(sfr).sum())} (sentinel <= -90: {int((sfr <= -90).sum())})")
json.dump(dict(sparc=cnt, sparc_fD=fD, wallaby=wc), open(os.path.join(HERE, "cfg631_inventory.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg631_inventory.out"), "w").write("\n".join(OUT) + "\n")
