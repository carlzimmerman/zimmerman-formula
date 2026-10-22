#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A70 -- IS THE 4.9-SIGMA SLACS LENSING FAILURE REAL?  An evidence re-audit.

Lane A70.  Audits A55_lensing_prediction (the 70-SLACS amplitude failure),
A51_kappa_measured (kappa = 0.371 +- 0.119) and A65_stiffness_origin (L* fitted).

Everything here is computed from files already on disk.  No network.  No number in
report.md is quoted unless this script prints it.

DATA (read-only; sha256 printed):
  real_research/data/slacs_auger2009_lenses.tsv
      Auger+2009 (SLACS IX), VizieR J/ApJ/705/1099.  85 rows, 70 with a usable R_E.
      THE SAME FILE A55 USED (A55's per-lens ratios are reproduced to 1e-6, K9).
  real_research/cross_thread_review_2026_09_26/XR33_data_treu2010_table1.tsv
      Treu+2010 Table 1, 56 SLACS lenses, per-lens IMF mismatch log(alpha) vs Salpeter.
  .../XR33_data_cvd12b_table2.tsv
      Conroy & van Dokkum 2012b Table 2, 35 ETGs, spectroscopic M/L_K / (M/L_K)_MW.
  .../XR33_data_slacsX_auger2010_table1.tsv
      Auger+2010 Table 1, 59 lenses: M_e2, f_DM for Salpeter and Chabrier, gamma_p.
  /Users/carlzimmerman/new_physics/_external_data/etherington2022/src/6_Results.tex
      Etherington+2022 Table 'SLACS mass': 43 SLACS lenses, imaging-only power-law
      slope gamma, R_Ein,eff, EXTERNAL SHEAR gamma_ext.

CONVENTIONS.  SI.  Flat LCDM (0.3, 0.7, h=0.7) everywhere, the SLACS tables' own.
kappa is A51's P3 convention: kappa = a0 sqrt(8 pi/3)/(c H0), H0 = 67.4 km/s/Mpc,
so a0 = kappa * 2.2627e-10 m/s^2 and kappa = 1/2 at a0 = 1.1312e-10.

MUTATIONS.  A70_MUTATE=<name> changes ONE input and must break a named check.
  imf | newton | arcsec | a0shift | treu | dropmassive | shuffle_re
Exit 0 iff every check passes.
"""
import os, sys, json, math, time, hashlib, re
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import gammainc, gammaln
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = (os.environ.get("A70_MUTATE", "") or "").strip()
T0 = time.time()

DATA_SLACS = os.path.join(REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
XR = os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26")
DATA_TREU = os.path.join(XR, "XR33_data_treu2010_table1.tsv")
DATA_CVD = os.path.join(XR, "XR33_data_cvd12b_table2.tsv")
DATA_AUG10 = os.path.join(XR, "XR33_data_slacsX_auger2010_table1.tsv")
DATA_ETH = os.path.join(os.path.dirname(REPO), "_external_data",
                        "etherington2022", "src", "6_Results.tex")
A55JSON = os.path.join(REPO, "deepseek_push", "DS_FINAL_2026_10_21",
                       "A55_lensing_prediction", "a55_results.json")

# ---------------------------------------------------------------- constants
G, C, MSUN = 6.67430e-11, 2.99792458e8, 1.98847e30
PC = 3.0856775814913673e16
KPC = 1.0e3 * PC
ARCSEC = math.pi / (180.0 * 3600.0)
OM, OL, H0_KMS = 0.3, 0.7, 70.0
H0 = H0_KMS * 1.0e3 / (1.0e6 * PC)
H0_67 = 67.4 * 1.0e3 / (1.0e6 * PC)
KAPPA2A0 = C * H0_67 / math.sqrt(8.0 * math.pi / 3.0)     # 2.2627e-10 m/s^2
A0_THEORY = 1.132e-10
A0_CANON = 9.3603e-11
A0_EFF = A0_THEORY
IMF_HEAD = "Fs"
SHAPE_MUT = 0.0

OUT = []
def P(s=""):
    print(s); OUT.append(s)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# ---------------------------------------------------------------- cosmology
if MUT == "cosmo":                       # mutation: a different background
    OM, OL, H0 = 0.35, 0.65, 75.0e3 / (1.0e6 * PC)
_zg = np.linspace(0.0, 6.0, 8001)
_E = np.sqrt(OM * (1.0 + _zg) ** 3 + OL)
_ig = np.concatenate([[0.0], np.cumsum(0.5 * (1.0 / _E[1:] + 1.0 / _E[:-1]) * np.diff(_zg))])

def DC(z):  return (C / H0) * float(np.interp(z, _zg, _ig))
def DA(z):  return DC(z) / (1.0 + z)
def DAls(z1, z2): return (DC(z2) - DC(z1)) / (1.0 + z2)
def SICR(zl, zs): return C * C * DA(zs) / (4.0 * math.pi * G * DA(zl) * DAls(zl, zs))

# ---------------------------------------------------------------- Sersic / PS
B4 = 7.669249934
def b_ser(n): return B4 if n == 4.0 else 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)
def nu_ps(n):
    p = 1.0 - 0.6097 / n + 0.05463 / (n * n)
    return n * (3.0 - p)
def M2D_star(R, Re, n=4.0, M=1.0):
    return M * gammainc(2.0 * n, b_ser(n) * (np.asarray(R) / Re) ** (1.0 / n))
def M3D_star(r, Re, n=4.0, M=1.0):
    return M * gammainc(nu_ps(n), b_ser(n) * (np.asarray(r) / Re) ** (1.0 / n))
def g_law(gN, a0):
    gN = np.asarray(gN, dtype=float)
    return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / np.maximum(gN, 1e-300)))
def F_ph(y): return 0.5 * (np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)) - 1.0)

GLX, GLW = np.polynomial.legendre.leggauss(400)
GLX = 0.5 * (GLX + 1.0); GLW = 0.5 * GLW
def M2D_from_g(R, M3Df, a0, rmax=1.0e6 * KPC):
    if R >= rmax: return 0.0
    U = math.acosh(max(rmax / R, 1.0 + 1e-9))
    u = GLX * U
    r = R * np.cosh(u)
    g = g_law(G * np.asarray(M3Df(r)) / r ** 2, a0)
    return R * R / G * float(np.sum(GLW * g) * U)

# ---------------------------------------------------------------- data loaders
def load_slacs():
    lines = [l.rstrip("\n") for l in open(DATA_SLACS, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    raw = [l.split("\t") for l in lines[hi + 3:] if l.strip() and not l.startswith("#")]
    def f(v):
        try: return float(v.strip())
        except Exception: return float("nan")
    L = []
    for r in raw:
        if len(r) < len(hdr): continue
        d = dict(name=r[col["SDSS"]].strip(), zl=f(r[col["zlens"]]), zs=f(r[col["zsrc"]]),
                 sig=f(r[col["sigma"]]), RE=f(r[col["RE"]]), lME=f(r[col["Mass"]]),
                 Fc=f(r[col["Fc"]]), eFc=f(r[col["e_Fc"]]), Fs=f(r[col["Fs"]]), eFs=f(r[col["e_Fs"]]),
                 lMc=f(r[col["logMc"]]), lMs=f(r[col["logMs"]]),
                 ReV=f(r[col["Re(V)"]]), ReI=f(r[col["Re(I)"]]), ReB=f(r[col["Re(B)"]]),
                 comp=r[col["f_MType"]].strip())
        if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0:
            L.append(d)
    return L, len(raw), hdr

def load_table(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("name")][0]
    hdr = lines[hi].split("\t")
    rows = []
    for l in lines[hi + 1:]:
        if not l.strip() or l.startswith("#"): continue
        r = l.split("\t")
        d = {}
        for k, v in zip(hdr, r):
            try: d[k] = float(v)
            except Exception: d[k] = v.strip()
        rows.append(d)
    return hdr, rows

def parse_etherington():
    s = open(DATA_ETH, encoding="latin-1").read()
    i = s.find("label{table: SLACS mass}")
    blk = s[s.rfind("begin{table", 0, i):i]
    def num(c):
        m = re.findall(r"([0-9]+\.[0-9]+|[0-9]+)", c)
        return float(m[0]) if m else float("nan")
    out = {}
    for line in blk.splitlines():
        m = re.search(r"(J\d{4}[+-]\d{4})", line)
        if not m or "&" not in line: continue
        cells = line.split("&")
        k = [j for j, c in enumerate(cells) if m.group(1) in c][0]
        e = re.findall(r"\+([0-9.]+)", cells[k + 1])
        out[m.group(1)] = dict(thE=num(cells[k + 1]), e_thE=(float(e[0]) if e else float("nan")),
                               gam=num(cells[k + 2]), q=num(cells[k + 3]), gext=num(cells[k + 5]))
    if MUT == "ethcopy":                 # mutation: pretend both pipelines give the same theta_E
        aug = {d["name"]: d for d in L}
        for nm_, v in out.items():
            if nm_ in aug:
                v["thE"] = aug[nm_]["RE"] * KPC / DA(aug[nm_]["zl"]) / ARCSEC
    if MUT == "gextq":                   # mutation: read the axis-ratio column as the shear
        for v in out.values(): v["gext"] = v["q"]
    return out

# ---------------------------------------------------------------- model
L, NRAW, HDR = load_slacs()
if MUT == "dropmassive":
    L = [d for d in L if d["sig"] <= 300.0]
if MUT == "zsrc":                        # mutation: one source moved to a shallow geometry
    L[0]["zs"] = L[0]["zl"] + 0.05
if MUT == "fsx":                         # mutation: a 5% corruption of the Salpeter f* column
    for d in L: d["Fs"] *= 1.05
if MUT == "shuffle_re":
    rng = np.random.default_rng(70)
    vals = np.array([d["ReV"] for d in L])
    perm = rng.permutation(len(vals))
    for d, v in zip(L, vals[perm]): d["ReV"] = float(v)
if MUT == "imf":
    IMF_HEAD = "Fc"
if MUT == "newton":
    A0_EFF = 1e-30
if MUT == "a0shift":
    A0_THEORY *= 1.10; A0_EFF = A0_THEORY
if MUT == "arcsec":
    def Re_kpc(d, band="ReV"): return float(d[band])          # mutation: no arcsec conversion
else:
    def Re_kpc(d, band="ReV"): return d[band] * ARCSEC * DA(d["zl"]) / KPC

_CACHE = {}
def predict(d, a0=A0_THEORY, imf="Fs", band="ReV", n=4.0, boost=1.0, newton=False,
            rmax=1.0e6 * KPC, shape=0.0):
    key = (d["name"], float(a0), imf, band, float(n), round(float(boost), 8), bool(newton),
           round(float(rmax), 3), round(float(shape), 8))
    if key in _CACHE: return _CACHE[key]
    sc = SICR(d["zl"], d["zs"]); ME = 10.0 ** d["lME"]; REo = d["RE"] * KPC; Re = Re_kpc(d, band) * KPC
    A = boost * d[imf] * ME / M2D_star(REo, Re, n)
    if shape:
        A0_ = A
        M3f = lambda r, A0_=A0_, Re=Re, n=n, shape=shape: A0_ * (np.asarray(r) / Re) ** shape * M3D_star(r, Re, n) * MSUN
    else:
        M3f = lambda r: A * M3D_star(r, Re, n) * MSUN
    aa = 1e-30 if newton else a0
    fun = lambda R: M2D_from_g(R, M3f, aa, rmax) - math.pi * R * R * sc
    Rs = np.logspace(math.log10(0.15 * REo), math.log10(10.0 * REo), 60)
    v = np.array([fun(x) for x in Rs])
    idx = np.where(np.diff(np.sign(v)) != 0)[0]
    if len(idx) == 0:
        _CACHE[key] = float("nan"); return float("nan")
    r = brentq(fun, Rs[idx[0]], Rs[idx[0] + 1], xtol=1e-5 * KPC) / KPC
    _CACHE[key] = r
    return r

def ratios(**kw):
    names, rr = [], []
    for d in L:
        if not np.isfinite(d["ReV"]): continue
        r = predict(d, **kw)
        if np.isfinite(r): names.append(d["name"]); rr.append(r / d["RE"])
    return names, np.array(rr)

def stats(rr):
    x = np.asarray(rr); lx = np.log(x); N = len(x)
    sem = lx.std(ddof=1) / math.sqrt(N)
    return dict(N=N, median=float(np.median(x)), mean_ln=float(lx.mean()), sem_ln=float(sem),
                scatter_ln=float(lx.std(ddof=1)), scatter_dex=float(lx.std(ddof=1) / math.log(10.0)),
                sigma=float(abs(lx.mean()) / sem))

CK = []
def ck(cid, what, measured, ok):
    CK.append(dict(id=cid, what=what, measured=str(measured), pass_=bool(ok)))
    P("  [%s] %s  %s: %s" % (cid, "PASS" if ok else "FAIL", what, measured))

RES = dict(lane="A70", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           mutate=MUT or None,
           data=dict(slacs=DATA_SLACS, treu=DATA_TREU, cvd=DATA_CVD, auger2010=DATA_AUG10,
                     etherington=DATA_ETH,
                     sha256_slacs=sha256(DATA_SLACS), sha256_treu=sha256(DATA_TREU),
                     sha256_cvd=sha256(DATA_CVD), sha256_aug10=sha256(DATA_AUG10),
                     sha256_eth=sha256(DATA_ETH)))

A55 = json.load(open(A55JSON))
S55 = A55["slacs"]["salpeter"]
NAMES55 = [x["name"] for x in A55["slacs"]["per_lens_salpeter"]]
RAT55 = {x["name"]: x["ratio"] for x in A55["slacs"]["per_lens_salpeter"]}

P("=" * 118)
P("A70 -- IS THE 4.9-SIGMA SLACS LENSING FAILURE REAL?   (mutation: %s)" % (MUT or "none"))
P("=" * 118)
P("\n  data sha256: slacs %s" % RES["data"]["sha256_slacs"][:16])
P("               treu  %s   cvd %s" % (RES["data"]["sha256_treu"][:16], RES["data"]["sha256_cvd"][:16]))
P("               aug10 %s   eth %s" % (RES["data"]["sha256_aug10"][:16], RES["data"]["sha256_eth"][:16]))

# =====================================================================================
P("\n" + "-" * 118)
P("TASK 1 -- AUDIT THE DATA")
P("-" * 118)

med = lambda k: float(np.median([d[k] for d in L]))
thE = np.array([d["RE"] * KPC / DA(d["zl"]) / ARCSEC for d in L])
P("\n  rows in catalogue %d ; rows with a usable R_E %d" % (NRAW, len(L)))
P("  median: z_l %.4f  z_s %.4f  sigma %.1f km/s  R_E %.3f kpc  theta_E %.4f arcsec  f*_Salp %.4f  f*_Chab %.4f"
  % (med("zl"), med("zs"), med("sig"), med("RE"), float(np.median(thE)), med("Fs"), med("Fc")))
P("  z_l 16-84: %.3f-%.3f (range %.3f-%.3f)   z_s 16-84: %.3f-%.3f (range %.3f-%.3f)"
  % (np.percentile([d["zl"] for d in L], 16), np.percentile([d["zl"] for d in L], 84),
     min(d["zl"] for d in L), max(d["zl"] for d in L),
     np.percentile([d["zs"] for d in L], 16), np.percentile([d["zs"] for d in L], 84),
     min(d["zs"] for d in L), max(d["zs"] for d in L)))
P("  sigma 16-84: %.0f-%.0f (range %.0f-%.0f)"
  % (np.percentile([d["sig"] for d in L], 16), np.percentile([d["sig"] for d in L], 84),
     min(d["sig"] for d in L), max(d["sig"] for d in L)))

ref = A55["slacs"]["median_lens"]
ok1 = (NRAW == 85 and len(L) == 70 and abs(med("zl") - ref["zl"]) < 1e-9
       and abs(med("zs") - ref["zs"]) < 1e-9 and abs(med("sig") - ref["sigma"]) < 1e-9
       and abs(med("RE") - ref["RE"]) < 1e-9)
ck("K1", "census and median lens: my catalogue read vs A55's stored median_lens",
   "rows %d/%d ; medians (%.4f, %.4f, %.1f, %.2f) vs (%.4f, %.4f, %.1f, %.2f)"
   % (NRAW, len(L), med("zl"), med("zs"), med("sig"), med("RE"),
      ref["zl"], ref["zs"], ref["sigma"], ref["RE"]), ok1)
RES["census"] = dict(nraw=NRAW, n_used=len(L), med_zl=med("zl"), med_zs=med("zs"),
                     med_sig=med("sig"), med_RE=med("RE"), med_thE=float(np.median(thE)))

th55 = A55["k18_amplitude_arcsec"]["theta_E_median"]
ck("K2", "theta_E recomputed from R_E and D_A(z_l) vs A55's stored median theta_E",
   "%.4f arcsec vs %.4f arcsec (ratio %.6f)" % (float(np.median(thE)), th55, float(np.median(thE)) / th55),
   abs(float(np.median(thE)) / th55 - 1.0) < 2e-3)

# M_E from geometry -- independent of the tabulated Mass column
dM = np.array([math.log10(max(math.pi * (d["RE"] * KPC) ** 2 * SICR(d["zl"], d["zs"]) / MSUN, 1e-300)) - d["lME"] for d in L])
P("  log M_E(reconstructed from theta_E, z_l, z_s) - log M_E(tabulated): %.4f +- %.4f dex"
  % (dM.mean(), dM.std(ddof=1)))
ck("K3", "Einstein mass from geometry vs the tabulated Mass column (A55 K8: 0.0008 +- 0.0032)",
   "mean %+.4f, scatter %.4f dex" % (dM.mean(), dM.std(ddof=1)),
   abs(dM.mean()) < 5e-3 and abs(dM.std(ddof=1) - 3.2e-3) < 3e-3)
RES["k3_mass_geometry"] = dict(mean=float(dM.mean()), scatter=float(dM.std(ddof=1)))

# R_e parsing: the columns are ARCSEC
conv = np.array([Re_kpc(d, "ReV") / d["ReV"] for d in L])
rVI = np.array([Re_kpc(d, "ReV") / Re_kpc(d, "ReI") for d in L if np.isfinite(d["ReI"]) and d["ReI"] > 0])
expect_conv = ARCSEC * DA(med("zl")) / KPC
re_over = np.array([d["RE"] / Re_kpc(d) for d in L if np.isfinite(d["ReV"])])
P("  R_e(V) conversion kpc/arcsec: median %.4f (D_A*ARCSEC at the median z_l = %.4f); a 2.5\" galaxy is %.1f kpc"
  % (np.median(conv), expect_conv, 2.5 * np.median(conv)))
P("  R_E/R_e(V): median %.3f, 16-84 %.3f-%.3f ; R_e(V)/R_e(I) = %.3f +- %.3f (the two bands' radii differ in the catalogue)"
  % (np.median(re_over), np.percentile(re_over, 16), np.percentile(re_over, 84), np.median(rVI), rVI.std(ddof=1)))
ck("K4", "arcsec->kpc conversion: kpc/arcsec vs D_A*ARCSEC, and R_E/R_e in its physical range",
   "kpc/arcsec %.4f vs %.4f (ratio %.4f) ; R_E/R_e %.3f"
   % (np.median(conv), expect_conv, np.median(conv) / expect_conv, np.median(re_over)),
   abs(np.median(conv) / expect_conv - 1.0) < 0.05 and 0.2 < np.median(re_over) < 0.9)
RES["k4_re_parsing"] = dict(kpc_per_arcsec=float(np.median(conv)), reV_over_reI=float(np.median(rVI)))

# f* internal consistency: Fs/Fc must equal the Salpeter/Chabrier SPS mass ratio
ratio_f = np.array([d["Fs"] / d["Fc"] for d in L])
ratio_m = np.array([10.0 ** (d["lMs"] - d["lMc"]) for d in L])
P("  f*_Salp/f*_Chab median %.4f vs 10^(logM*_Salp-logM*_Chab) median %.4f"
  % (np.median(ratio_f), np.median(ratio_m)))
ck("K5", "two independent IMF columns agree: Fs/Fc vs the SPS mass ratio (Auger abstract: <f*_Chab>=0.4)",
   "Fs/Fc %.4f vs mass ratio %.4f ; median f*_Chab %.4f vs 0.4"
   % (np.median(ratio_f), np.median(ratio_m), med("Fc")),
   abs(np.median(ratio_f) / np.median(ratio_m) - 1.0) < 0.03 and abs(med("Fc") - 0.4) < 0.03)

# is there a per-lens R_E error column?  Is 2% the data's?
errcols = [c for c in HDR if c.strip().lower() in ("e_re", "ere", "e_mass", "emass", "e_m", "e_thetae", "e_theta_e")]
eth = parse_etherington()
match = [d for d in L if d["name"] in eth]
rth = np.array([eth[d["name"]]["thE"] / (d["RE"] * KPC / DA(d["zl"]) / ARCSEC) for d in match])
P("\n  catalogue columns carrying an R_E or Mass uncertainty: %s  (count %d)" % (errcols or "NONE", len(errcols)))
P("  Etherington+2022 / Auger+2009 theta_E, %d common lenses: median ratio %.4f, scatter %.4f (%.1f%%),"
  % (len(match), np.median(rth), rth.std(ddof=1), 100 * rth.std(ddof=1)))
P("    |1-ratio| median %.3f ; A55's assumed per-lens error 0.020" % np.median(np.abs(1 - rth)))
P("  Etherington formal error on theta_E: median %.4f (max %.3f)" % (
    np.nanmedian([eth[d["name"]]["e_thE"] / eth[d["name"]]["thE"] for d in match]),
    np.nanmax([eth[d["name"]]["e_thE"] / eth[d["name"]]["thE"] for d in match])))
ck("K6", "the 2% R_E error is NOT in the data: zero error columns, and the inter-pipeline scatter is larger",
   "err cols %d ; inter-pipeline scatter %.4f = %.1fx the assumed 0.02" % (len(errcols), rth.std(ddof=1), rth.std(ddof=1) / 0.02),
   len(errcols) == 0 and rth.std(ddof=1) > 1.5 * 0.02)
RES["k6_re_error"] = dict(n_err_cols=len(errcols), interpipeline_scatter=float(rth.std(ddof=1)),
                          median_abs_dev=float(np.median(np.abs(1 - rth))))

# geometry / LOS
dls_ds = np.array([DAls(d["zl"], d["zs"]) / DA(d["zs"]) for d in L])
sicr = np.array([SICR(d["zl"], d["zs"]) for d in L])
P("\n  D_ls/D_s: median %.3f, 16-84 %.3f-%.3f, min %.3f ; all z_s>z_l: %s"
  % (np.median(dls_ds), np.percentile(dls_ds, 16), np.percentile(dls_ds, 84), dls_ds.min(),
     all(d["zs"] > d["zl"] for d in L)))
P("  Sigma_cr: median %.3e kg/m^2, 16-84 %.2e-%.2e" % (np.median(sicr), np.percentile(sicr, 16), np.percentile(sicr, 84)))
ck("K7", "lens geometry: every source behind its lens, D_ls/D_s in a sane range, Sigma_cr positive and finite",
   "min D_ls/D_s %.3f, median %.3f, max %.3f ; Sigma_cr median %.2e"
   % (dls_ds.min(), np.median(dls_ds), dls_ds.max(), np.median(sicr)),
   all(d["zs"] > d["zl"] for d in L) and 0.2 < dls_ds.min() and dls_ds.max() < 1.0
   and np.all(np.isfinite(sicr)) and np.all(sicr > 0))
RES["k7_geometry"] = dict(dls_ds_min=float(dls_ds.min()), dls_ds_median=float(np.median(dls_ds)),
                          sicr_median=float(np.median(sicr)))

# no Sersic index in the catalogue; the n=3/6 bracket
ncol = [c for c in HDR if c.lower() in ("n", "nsersic", "sersic", "n_sersic")]
P("\n  Sersic-index columns in the catalogue: %s" % (ncol or "NONE"))
ck("K8", "no per-lens Sersic index exists: n=4 is assumed, and the n=3/6 bracket reproduces A55's 0.877/0.893",
   "n cols %d ; my n=3/6 medians %.4f/%.4f vs A55 %.4f/%.4f"
   % (len(ncol), float(np.median(ratios(a0=A0_EFF, imf=IMF_HEAD, n=3.0)[1])),
      float(np.median(ratios(a0=A0_EFF, imf=IMF_HEAD, n=6.0)[1])),
      A55["k15_nscan"]["3.0"]["median"], A55["k15_nscan"]["6.0"]["median"]),
   len(ncol) == 0 and abs(float(np.median(ratios(a0=A0_EFF, imf=IMF_HEAD, n=3.0)[1])) - A55["k15_nscan"]["3.0"]["median"]) < 5e-3
   and abs(float(np.median(ratios(a0=A0_EFF, imf=IMF_HEAD, n=6.0)[1])) - A55["k15_nscan"]["6.0"]["median"]) < 5e-3)

# external shear (Etherington), the only environment statistic on disk
ge = np.array([v["gext"] for v in eth.values() if np.isfinite(v["gext"])])
dth_ext = 0.5 * ge ** 2
P("\n  external shear gamma_ext (%d lenses): median %.3f, 16-84 %.3f-%.3f, max %.2f, frac>0.1 %.2f, frac>0.2 %.2f"
  % (len(ge), np.median(ge), np.percentile(ge, 16), np.percentile(ge, 84), ge.max(),
     np.mean(ge > 0.1), np.mean(ge > 0.2)))
P("  leading O(gamma_ext^2) shift of theta_E: median %.4f, at gamma=0.2 %.4f -- vs the 0.115 deficit"
  % (np.median(dth_ext), 0.5 * 0.2 ** 2))
P("  fraction with sigma>250 km/s: %.2f ; >300 km/s: %.2f ; >350 km/s: %.2f (no sigma cut in the selection)"
  % (np.mean([d["sig"] > 250 for d in L]), np.mean([d["sig"] > 300 for d in L]), np.mean([d["sig"] > 350 for d in L])))
ck("K9", "environment: external shear is measured and non-zero, but its median O(gamma^2) effect on theta_E is << 11.5%",
   "median gamma_ext %.3f, %.0f%% above 0.1, max %.2f ; median dtheta/theta %.4f, max %.4f, frac>0.02 %.2f"
   % (np.median(ge), 100 * np.mean(ge > 0.1), ge.max(), np.median(dth_ext), dth_ext.max(), np.mean(dth_ext > 0.02)),
   np.median(ge) > 0.02 and np.mean(ge > 0.1) > 0.2 and np.median(dth_ext) < 0.01 and np.mean(dth_ext > 0.02) < 0.15)
RES["k9_environment"] = dict(median_gext=float(np.median(ge)), frac_gt_01=float(np.mean(ge > 0.1)),
                             max_gext=float(ge.max()), max_dtheta_frac=float(dth_ext.max()))

# =====================================================================================
P("\n" + "-" * 118)
P("THE MODEL -- reproduced, then audited")
P("-" * 118)

nm, r_sal = ratios(a0=A0_EFF, imf=IMF_HEAD)
dev = max(abs(r_sal[i] / RAT55[n] - 1.0) for i, n in enumerate(nm))
st_sal = stats(r_sal)
P("\n  my 70-lens Salpeter prediction: median %.4f, <ln> %+.4f +- %.4f, %.2f sigma, scatter %.4f dex"
  % (st_sal["median"], st_sal["mean_ln"], st_sal["sem_ln"], st_sal["sigma"], st_sal["scatter_dex"]))
P("  max relative deviation from A55's stored 70 per-lens ratios: %.2e" % dev)
ck("K10", "the audit uses the same data and the same model: my 70 per-lens ratios vs A55's stored ratios",
   "max |ratio/ratio_A55 - 1| = %.2e" % dev, dev < 1e-6)
ck("K11", "headline reproduced: median, <ln>, sigma vs A55's stored value",
   "median %.4f vs %.4f ; <ln> %+.4f vs %+.4f ; %.2f sigma vs %.2f sigma"
   % (st_sal["median"], S55["median"], st_sal["mean_ln"], S55["mean_ln"], st_sal["sigma"], S55["sigma_offset"]),
   abs(st_sal["median"] - S55["median"]) < 1e-4 and abs(st_sal["mean_ln"] - S55["mean_ln"]) < 1e-4
   and abs(st_sal["sigma"] - S55["sigma_offset"]) < 0.01)
RES["headline"] = st_sal

st_new = stats(ratios(a0=A0_EFF, imf=IMF_HEAD, newton=True)[1])
st_cha = stats(ratios(a0=A0_EFF, imf="Fc")[1])
st_can = stats(ratios(a0=A0_CANON, imf=IMF_HEAD)[1])
P("\n  Newton %.4f (A55 %.4f) ; Chabrier %.4f (A55 %.4f) ; canonical a0 %.4f (A55 %.4f)"
  % (st_new["median"], A55["slacs"]["newton"]["median"], st_cha["median"], A55["slacs"]["chabrier"]["median"],
     st_can["median"], A55["slacs"]["canonical"]["median"]))
ck("K12", "the three control branches (Newton, Chabrier, canonical a0) vs A55's stored values",
   "newton %.4f/%.4f ; chabrier %.4f/%.4f ; canonical %.4f/%.4f"
   % (st_new["median"], A55["slacs"]["newton"]["median"], st_cha["median"], A55["slacs"]["chabrier"]["median"],
      st_can["median"], A55["slacs"]["canonical"]["median"]),
   abs(st_new["median"] - A55["slacs"]["newton"]["median"]) < 1e-4
   and abs(st_cha["median"] - A55["slacs"]["chabrier"]["median"]) < 1e-4
   and abs(st_can["median"] - A55["slacs"]["canonical"]["median"]) < 1e-4)
RES["controls"] = dict(newton=st_new, chabrier=st_cha, canonical=st_can)

# phantom share and the 3D law identity; the c_n slip correction
def M2D_newton(R, M3Df, rmax=1.0e6 * KPC):
    """pure Newtonian projection of a 3D mass profile: (R^2/G) int G M/r^2 dr/sqrt(r^2-R^2)."""
    if R >= rmax: return 0.0
    U = math.acosh(max(rmax / R, 1.0 + 1e-9)); u = GLX * U; r = R * np.cosh(u)
    return R * R * float(np.sum(GLW * np.asarray(M3Df(r)) / r ** 2) * U)

Fs, Fp, Fp2, yv, rel = [], [], [], [], []
defc = []; proj_ratio = []
Fdict = {}
for d in L:
    if not np.isfinite(d["ReV"]): continue
    REo = d["RE"] * KPC; Re = Re_kpc(d) * KPC; ME = 10.0 ** d["lME"]
    A = d[IMF_HEAD] * ME / M2D_star(REo, Re)
    Mb3 = A * M3D_star(REo, Re) * MSUN
    y = G * Mb3 / (A0_EFF * REo ** 2)
    yv.append(y); Fs.append(F_ph(y)); Fdict[d["name"]] = F_ph(y)
    g = float(g_law(G * Mb3 / REo ** 2, A0_EFF))
    rel.append(abs(REo ** 2 * g / G / (Mb3 * (1.0 + F_ph(y))) - 1.0))
    Mst = float(M2D_star(REo, Re, 4.0, A * MSUN))
    proj_ratio.append(M2D_from_g(REo, lambda r, A=A, Re=Re: A * M3D_star(r, Re) * MSUN, 1e-30) / Mst)
    Mph_law = M2D_from_g(REo, lambda r, A=A, Re=Re: A * M3D_star(r, Re) * MSUN, A0_EFF) - Mst
    Mph_proj = M2D_newton(REo, lambda r, A=A, Re=Re: A * M3D_star(r, Re) * F_ph(G * A * M3D_star(r, Re) * MSUN / (A0_EFF * r ** 2)) * MSUN)
    Fp.append(Mph_law / Mst); Fp2.append(Mph_proj / Mst)
    sc_ = SICR(d["zl"], d["zs"])
    defc.append(math.log10((math.pi * REo ** 2 * sc_) / (Mst + Mph_law)))
P("\n  phantom at R_E: y=g_N/a0 median %.2f ; F(y) 3D median %.4f (range %.3f-%.3f) ; share of M_E %.4f"
  % (np.median(yv), np.median(Fs), min(Fs), max(Fs), np.median(np.array(Fs) / (1 + np.array(Fs)))))
P("  Newtonian g-integral projection / analytic projected stellar mass: median %.4f (the projection is not double counting)" % np.median(proj_ratio))
P("  phantom PROJECTED mass inside R_E / stellar projected mass: %.4f (law route) vs %.4f (direct 3D projection)"
  % (np.median(Fp), np.median(Fp2)))
P("  -> projection amplifies the phantom: %.2f x its 3D F(y), because rho_ph ~ r^-2 extends along the LOS"
  % (np.median(Fp) / np.median(Fs)))
P("  mass deficit at FIXED observed R_E: %.4f dex (factor %.3f) ; radius deficit (median) %.4f dex (factor %.3f) ;"
  " A55 quoted 0.108 dex = 2x the radius (M~R^2)" 
  % (np.median(defc), 10 ** np.median(defc), -math.log10(st_sal["median"]), 1 / st_sal["median"]))
P("  A55's 0.108 dex = 2 x the radius deficit, which assumes M_2D ~ R^2; the measured response is R^%.2f"
  % (-st_sal["mean_ln"] / math.log(10) / (np.median(defc))))
# DIAGNOSTIC, not a check: the two routes are algebraically the same model, so no input
# mutation can make them disagree.  Values are reported above and stored in RES["phantom"].
# (A disagreement would be a code bug, which is tested by construction, not by a mutation.)
RES["phantom"] = dict(y_median=float(np.median(yv)), F_median=float(np.median(Fs)),
                      F_min=float(min(Fs)), F_max=float(max(Fs)),
                      share_M_E=float(np.median(np.array(Fs) / (1 + np.array(Fs)))))

# the c_n = B(2n+1)/B(n+1) correction
def Bint(m):
    f = lambda u: u ** (-m) / math.sqrt(u * u - 1.0)
    return quad(f, 1.0, np.inf, limit=400)[0]
cn = {n: Bint(2 * n + 1) / Bint(n + 1) for n in (0.5, 1.0, 1.5, 2.0)}
psi_i = [G * 10.0 ** d["lME"] * MSUN / (d["RE"] * KPC * C * C) for d in L]
psi = float(np.median(psi_i))
slip = float(np.median([cn[1.0] * x for x in psi_i]))
P("\n  c_n = B(2n+1)/B(n+1): " + ", ".join("n=%.1f %.4f" % (k, v) for k, v in cn.items()))
P("  Psi(R_E) = GM_E/(R_E c^2) = %.3e ; delta-alpha/alpha = -c_n Psi = %.3e" % (psi, slip))
P("  correction / deficit = %.2e  (the LOS/slip term cannot double count or explain the 11.5%%)" % (slip / 0.115))
# DIAGNOSTIC, not a check: c_n is an analytic constant, independent of every input.
RES["k14_cn"] = dict(cn={str(k): float(v) for k, v in cn.items()}, psi=float(psi), slip=float(slip))

# the M/L boost: exact vs A55's 1/median^2
def med_at(B):
    return float(np.median(ratios(a0=A0_EFF, imf=IMF_HEAD, boost=B)[1]))
B_req = brentq(lambda B: med_at(B) - 1.0, 1.02, 5.00, xtol=1e-4)
B_inv = 1.0 / st_sal["median"]
B_a55 = 10.0 ** (-2.0 * st_sal["mean_ln"] / math.log(10.0))
P("\n  required single M/L boost: median(R_E,pred/R_E,obs)=1 at B = %.4f" % B_req)
P("  1/median ratio = %.4f ; 1/median^2 = %.4f (A55's 1.283) ; ratio B_req/(1/median) = %.4f"
  % (B_inv, B_inv ** 2, B_req / B_inv))
ck("K13", "A55's 1.28x Salpeter is NOT the M/L that fixes the fit: B_req vs 1/median vs 1/median^2",
   "B_req %.4f ; 1/median %.4f ; 1/median^2 %.4f ; B_req < 1/median^2 by %.0f%%"
   % (B_req, B_inv, B_inv ** 2, 100 * (1 - B_req / B_inv ** 2)),
   abs(B_req / B_inv - 1.0) < 0.06 and B_req < 0.97 * B_inv ** 2)
for ke in (0.02, 0.05, 0.10):
    P("  unsubtracted external convergence kappa_ext=%.2f: theta_E is boosted %.1f%%, so the required B rises to %.3f"
      % (ke, 100 * ((1 - ke) ** -0.5 - 1), B_req / (1 - ke) ** 0.5))
RES["boost"] = dict(B_req=float(B_req), one_over_median=float(B_inv), one_over_median_sq=float(B_inv ** 2),
                    log10_B_req=float(math.log10(B_req)))

# why the boost is 1.17, not 1.28: the response of R_E to a uniform M/L boost
def M2DatRE(d, B):
    REo = d["RE"] * KPC; Re = Re_kpc(d) * KPC
    A = B * d[IMF_HEAD] * 10.0 ** d["lME"] / M2D_star(REo, Re)
    return M2D_from_g(REo, lambda r, A=A, Re=Re: A * M3D_star(r, Re) * MSUN, A0_EFF)
massr, dlnM_dlnB, dlnR_dlnB = [], [], []
dB = 0.10
for d in L:
    if not np.isfinite(d["ReV"]): continue
    REo = d["RE"] * KPC; sc = SICR(d["zl"], d["zs"])
    massr.append((math.log(M2DatRE(d, 1.0) / (math.pi * REo ** 2 * sc)), math.log(predict(d) / d["RE"])))
    dlnM_dlnB.append(math.log(M2DatRE(d, 1.0 + dB) / M2DatRE(d, 1.0)) / math.log(1.0 + dB))
    dlnR_dlnB.append(math.log(predict(d, boost=1.0 + dB) / predict(d, boost=1.0)) / math.log(1.0 + dB))
massr = np.array(massr)
dlnM_dlnB = float(np.median(dlnM_dlnB)); resp = float(np.median(dlnR_dlnB))
slope_mr = float(np.polyfit(massr[:, 0], massr[:, 1], 1)[0])
B_from_resp = math.exp(-st_sal["mean_ln"] / resp)
P("\n  response of R_E to a uniform M/L boost: dlnR/dlnB = %.4f ; dlnM2D/dlnB = %.4f ; ratio %.3f"
  % (resp, dlnM_dlnB, resp / dlnM_dlnB))
P("  population regression dln(R_pred/R_obs)/dln(M2D/M_E) = %.4f (corr %.3f)"
  % (slope_mr, np.corrcoef(massr[:, 0], massr[:, 1])[0, 1]))
sig_logB = (st_sal["sem_ln"] / math.log(10.0)) / resp
P("  the same data measure log10(B) to %.4f dex, i.e. B = %.3f +- %.3f (%.1f%%) -- a 3%% IMF measurement"
  % (sig_logB, B_req, B_req * sig_logB * math.log(10.0), 100 * sig_logB * math.log(10.0)))
P("  B from the response: exp(%.4f/%.4f) = %.4f vs the root-found B_req %.4f"
  % (-st_sal["mean_ln"], resp, B_from_resp, B_req))
ck("K14", "the boost is sub-linear in mass: the response route and the root-found boost agree, and both are < 1/median^2",
   "dlnR/dlnB %.4f ; B_response %.4f vs B_req %.4f ; 1/median^2 %.4f"
   % (resp, B_from_resp, B_req, B_inv ** 2),
   abs(B_from_resp - B_req) < 0.02 and B_from_resp < 0.97 * B_inv ** 2 and 0.7 < resp < 1.0)
RES["k16_boost_response"] = dict(dlnR_dlnB=resp, dlnM_dlnB=dlnM_dlnB, B_from_response=float(B_from_resp),
                                 regression=float(slope_mr), sigma_logB_dex=float(sig_logB),
                                 sigma_B=float(B_req * sig_logB * math.log(10.0)))

# how much of the prediction is just f*?
byall = {d["name"]: d for d in L}
lr = np.log(r_sal); lf = np.log(np.array([byall[x][IMF_HEAD] for x in nm]))
lph = np.log(1.0 + np.array([Fdict[x] for x in nm]))
X1 = np.vstack([np.ones_like(lf), lf]).T
p1 = X1 @ np.linalg.lstsq(X1, lr, rcond=None)[0]
r2 = 1.0 - ((lr - p1) ** 2).sum() / ((lr - lr.mean()) ** 2).sum()
X3 = np.vstack([np.ones_like(lf), lf, lph]).T
p3 = X3 @ np.linalg.lstsq(X3, lr, rcond=None)[0]
r2b = 1.0 - ((lr - p3) ** 2).sum() / ((lr - lr.mean()) ** 2).sum()
P("\n  variance of ln(R_pred/R_obs) explained by ln f* alone: R^2 = %.4f ; adding ln(1+F): %.4f ; residual %.4f dex"
  % (r2, r2b, (lr - p3).std(ddof=3) / math.log(10)))
ck("K15", "the 'prediction' is 95% a restatement of f*_Salp: R^2 of ln f* alone",
   "R^2(f*) %.4f ; R^2(f*, phantom) %.4f ; resid %.4f dex" % (r2, r2b, (lr - p3).std(ddof=3) / math.log(10)),
   r2 > 0.90 and r2b > r2)
RES["k17_variance"] = dict(r2_fstar=float(r2), r2_full=float(r2b), resid_dex=float((lr - p3).std(ddof=3) / math.log(10)))

# =====================================================================================
P("\n" + "-" * 118)
P("TASK 3 -- THE kappa / a0 TENSION")
P("-" * 118)

def med_kap(k, B=1.0):
    return float(np.median(ratios(a0=k * KAPPA2A0, imf=IMF_HEAD, boost=B)[1]))

kaps = [0.252, 0.30, 0.3415, 0.371, 0.4137, 0.45, 0.490, 0.5265, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20]
P("\n  kappa   a0           median R_E,pred/R_E,obs   <ln>")
rows = []
for k in kaps:
    rr = ratios(a0=k * KAPPA2A0, imf=IMF_HEAD)[1]
    P("  %.4f  %.4e   %.4f                 %+.4f" % (k, k * KAPPA2A0, np.median(rr), np.log(rr).mean()))
    rows.append(dict(kappa=k, a0=float(k * KAPPA2A0), median=float(np.median(rr)), mean_ln=float(np.log(rr).mean()),
                     scatter_ln=float(np.log(rr).std(ddof=1))))
RES["kappa_scan"] = rows

h = 1e-3
s_k = (math.log(med_kap(0.5 * math.exp(h))) - math.log(med_kap(0.5 * math.exp(-h)))) / (2 * h)
P("\n  dln(R_E,pred)/dln(kappa) at kappa=0.5: %.4f  (the theory is almost blind to a0 at SLACS accelerations)" % s_k)
P("  response ratio dlnR/dlnB : dlnR/dlnkappa = %.2f : 1" % (0.7775 / s_k))
# DIAGNOSTIC, not a check: the 0.08-0.18 band is physical, not data-derived; see K17 for the
# mutation-sensitive consequence (the flat Delta-chi2 with a free IMF).
RES["dlnR_dlnkappa"] = float(s_k)

kstar = brentq(lambda k: med_kap(k) - 1.0, 0.55, 6.00, xtol=1e-5)
P("  kappa that makes the median ratio exactly 1, with Salpeter fixed: kappa* = %.4f" % kstar)
P("  A51 measured band [0.252, 0.490] ; falsifier band [0.3415, 0.5265] ; kappa* is %.2f%% above the top of the measured band"
  % (100 * (kstar / 0.490 - 1)))
# DIAGNOSTIC, not a check: kappa* is reported; its consequence is carried by K22.
RES["kappa_star_salpeter"] = float(kstar)

r490 = med_kap(0.490); r5265 = med_kap(0.5265)
P("  at kappa=0.490: median %.4f ; at kappa=0.5265: %.4f ; both < 1 (the whole band under-predicts)" % (r490, r5265))
# DIAGNOSTIC, not a check: the band medians are reported above.
RES["kappa_band_medians"] = dict(k490=float(r490), k5265=float(r5265))

# Delta chi2 with Salpeter fixed: full per-lens likelihood vs the mean/SEM route
sem = st_sal["sem_ln"]
sig_k_mean = 0.5 * sem / abs(s_k)
s_tot_dex = math.sqrt(0.045 ** 2 + 0.09 ** 2)          # measurement + measured intrinsic scatter
ks_fit = np.linspace(0.75, 1.25, 6) * kstar
chi2_fit = []
for k in ks_fit:
    rr = ratios(a0=k * KAPPA2A0, imf=IMF_HEAD)[1]
    chi2_fit.append(float(np.sum((np.log10(rr) / s_tot_dex) ** 2)))
chi2_fit = np.array(chi2_fit)
cf = np.polyfit(ks_fit, chi2_fit, 2)
kmin = -cf[1] / (2 * cf[0])
sig_k_quad = math.sqrt(1.0 / cf[0])                     # Delta chi2 = 1
P("\n  fixed-Salpeter chi2(kappa) from the full per-lens likelihood: minimum %.4f ; Delta-chi2=1 width %.4f"
  % (kmin, sig_k_quad))
P("  mean-based width sigma_kappa = 0.5*sem/(dlnR/dlnkappa) = %.4f ; (kappa*-0.371)/sigma = %.2f"
  % (sig_k_mean, (kstar - 0.371) / sig_k_mean))
ck("K16", "the fixed-Salpeter kappa error from two independent routes (chi2 curvature, mean/SEM)",
   "full-likelihood %.4f at kappa %.3f vs mean-based %.4f ; tension (kappa*-0.371)/sigma = %.2f"
   % (sig_k_quad, kmin, sig_k_mean, (kstar - 0.371) / sig_k_mean),
   abs(sig_k_quad - sig_k_mean) < 0.04 and abs(kmin - kstar) < 0.25 and (kstar - 0.371) / sig_k_mean > 4.0)
RES["kappa_error_salpeter"] = dict(full_likelihood=float(sig_k_quad), mean_based=float(sig_k_mean),
                                   kmin=float(kmin), tension_sigma=float((kstar - 0.371) / sig_k_mean))

# free IMF: is kappa constrained at all?
K3v = [0.35, 0.50, 0.65]; B3v = [1.00, 1.12, 1.24]
grid = {}
for k in K3v:
    for b in B3v:
        grid[(k, b)] = np.log(ratios(a0=k * KAPPA2A0, imf=IMF_HEAD, boost=b)[1])
def design(x, y): return np.array([np.ones_like(x), x, y, x * x, y * y, x * y]).T
coefs = []
for i in range(len(nm)):
    xs, ys, zs = [], [], []
    for k in K3v:
        for b in B3v:
            xs.append(math.log(k / 0.5)); ys.append(math.log(b)); zs.append(grid[(k, b)][i])
    coefs.append(np.linalg.lstsq(design(np.array(xs), np.array(ys)), np.array(zs), rcond=None)[0])
coefs = np.array(coefs)
def lr_grid(k, b):
    x = math.log(k / 0.5); y = math.log(b)
    return coefs @ np.array([1, x, y, x * x, y * y, x * y])
val = []
for k, b in [(0.42, 1.06), (0.58, 1.18)]:
    true = np.log(ratios(a0=k * KAPPA2A0, imf=IMF_HEAD, boost=b)[1])
    val.append(float(np.max(np.abs(true - lr_grid(k, b)))))
P("\n  2D (kappa, B) surface: quadratic interpolation validated off-grid, max |dlnR| = %.2e / %.2e" % tuple(val))
def chi2_free(k, b, intr=0.09):
    x = lr_grid(k, b) / math.log(10.0)
    s = math.sqrt(0.045 ** 2 + intr ** 2)
    return float(np.sum((x / s) ** 2))
def prof(k):
    r = minimize_scalar(lambda y: chi2_free(k, math.exp(y)), bounds=(math.log(0.9), math.log(1.6)), method="bounded")
    return r.fun, math.exp(r.x)
kscan = np.arange(0.20, 0.81, 0.05)
prof_res = [(k,) + prof(k) for k in kscan]
base = min(p[1] for p in prof_res)
P("  free-IMF profile chi2(kappa) (B marginalised, flat prior):")
for k, c, b in prof_res:
    P("    kappa %.2f  chi2 %.2f  dchi2 %.2f  best B %.3f" % (k, c, c - base, b))
dmax = max(p[1] for p in prof_res) - base
ck("K17", "with the IMF normalisation free, kappa is UNCONSTRAINED: max Delta-chi2 over kappa in [0.2,0.8]",
   "Delta-chi2_max = %.2f over a factor 4 in kappa ; best B range %.3f-%.3f"
   % (dmax, min(p[2] for p in prof_res), max(p[2] for p in prof_res)), dmax < 1.0)
RES["kappa_free_imf"] = dict(dchi2_max=float(dmax), profile=[dict(kappa=float(p[0]), chi2=float(p[1]), B=float(p[2])) for p in prof_res],
                             interp_max_err=float(max(val)))

# =====================================================================================
P("\n" + "-" * 118)
P("TASK 2 -- THE IMF QUESTION")
P("-" * 118)

_, treu = load_table(DATA_TREU)
if MUT == "treu":
    for x in treu: x["log_alpha"] += 0.10
la = np.array([x["log_alpha"] for x in treu])
ep = np.array([x["ep"] for x in treu]); em = np.array([x["em"] for x in treu])
w = 1.0 / ((ep + em) / 2.0) ** 2
wmean = float((w * la).sum() / w.sum())
P("\n  Treu+2010 SLACS (N=%d): <log alpha_Salp> = %.4f +- %.4f (sem), scatter %.4f dex, weighted %.4f +- %.4f"
  % (len(la), la.mean(), la.std(ddof=1) / math.sqrt(len(la)), la.std(ddof=1),
     (w * la).sum() / w.sum(), 1.0 / math.sqrt(w.sum())))
P("  16-84: %+.3f to %+.3f ; 2.5-97.5: %+.3f to %+.3f ; alpha 95%% range %.2f-%.2f x Salpeter"
  % (np.percentile(la, 16), np.percentile(la, 84), np.percentile(la, 2.5), np.percentile(la, 97.5),
     10 ** np.percentile(la, 2.5), 10 ** np.percentile(la, 97.5)))
P("  weighted mean %.4f vs unweighted %.4f (two independent estimators of the same table)" % (wmean, la.mean()))
P("  abstract (Treu+2010): <log alpha> = 0.00 +- 0.03 +- 0.02 for a Salpeter IMF")
sd_tot = math.sqrt(0.03 ** 2 + 0.02 ** 2)
P("  measured mean vs abstract: %.2f sigma ; 95%% CL on the mean: %.3f-%.3f x Salpeter"
  % (abs(la.mean()) / sd_tot, 10 ** (-1.96 * sd_tot), 10 ** (1.96 * sd_tot)))
ck("K18", "Treu+2010 per-lens table reproduces its abstract (0.00 +- 0.03 +- 0.02) and gives the 95% mean range",
   "mean %+.4f (%.2f sigma from 0) ; scatter %.4f ; 95%% %.3f-%.3f"
   % (la.mean(), abs(la.mean()) / sd_tot, la.std(ddof=1), 10 ** (-1.96 * sd_tot), 10 ** (1.96 * sd_tot)),
   abs(la.mean()) < 0.02 and abs(wmean - la.mean()) < 0.03)
RES["treu"] = dict(N=int(len(la)), mean=float(la.mean()), sem=float(la.std(ddof=1) / math.sqrt(len(la))),
                   scatter=float(la.std(ddof=1)), p2_5=float(np.percentile(la, 2.5)),
                   p97_5=float(np.percentile(la, 97.5)), sd_tot=float(sd_tot),
                   hi95=float(10 ** (1.96 * sd_tot)), lo95=float(10 ** (-1.96 * sd_tot)))
pct = float(np.mean(la <= math.log10(B_req)))
P("  required %.3f x Salpeter = %+.4f dex: percentile in Treu's per-lens distribution %.1f%% ; %.2f sigma from the mean"
  % (B_req, math.log10(B_req), 100 * pct, math.log10(B_req) / sd_tot))
for s_imf in (0.03, 0.04, 0.10):
    P("  a %.2f dex IMF measurement separates 1.000 from %.3f at %.1f sigma ; 3 sigma needs %.3f dex"
      % (s_imf, B_req, math.log10(B_req) / s_imf, math.log10(B_req) / 3.0))
P("  A55's 1.283 would be %.2f sigma from the same mean and %s the 95%% interval; the margin for 1.174 is %.2f%%"
  % (math.log10(B_a55) / sd_tot, "INSIDE" if B_a55 <= 10 ** (1.96 * sd_tot) else "OUTSIDE",
     100 * (10 ** (1.96 * sd_tot) / B_req - 1)))
tension_comb = math.log10(B_req) / math.sqrt(sd_tot ** 2 + sig_logB ** 2)
P("  including the lensing error on B (%.4f dex): %.2f sigma from Treu's mean" % (sig_logB, tension_comb))
ck("K19", "where 1.17x Salpeter sits in the direct SLACS dynamical calibration",
   "percentile %.1f%% ; %.2f sigma (%.2f with the lensing error) ; 95%% upper bound %.3f (required %.3f)"
   % (100 * pct, math.log10(B_req) / sd_tot, tension_comb, 10 ** (1.96 * sd_tot), B_req),
   tension_comb < 2.0 and B_req < 10 ** (1.96 * sd_tot))
RES["imf_position_treu"] = dict(percentile=float(pct), sigma=float(math.log10(B_req) / sd_tot),
                                sigma_combined=float(tension_comb),
                                inside95=bool(B_req < 10 ** (1.96 * sd_tot)))

# CvD12b
_, cv = load_table(DATA_CVD)
al = np.array([x["ML_K"] / x["ML_K_MW"] for x in cv])       # alpha_MW = (M/L_K)/(M/L_K)_MW
sg = np.array([x["sigma"] for x in cv])
X = np.vstack([np.ones_like(sg), np.log10(sg / 200.0)]).T
coef, _, _, _ = np.linalg.lstsq(X, np.log10(al), rcond=None)
resid = np.log10(al) - X @ coef
rms = resid.std(ddof=2)
SAL_K = 1.55
a241 = 10 ** (coef[0] + coef[1] * math.log10(241.0 / 200.0)) / SAL_K
P("  Salpeter normalisation: 1.55 (MASSIVE, SNELLS) vs ~1.6 (CvD text) -> %.3f dex ambiguity" % abs(math.log10(1.6 / 1.55)))
P("\n  Conroy & van Dokkum 2012b (N=%d, sigma %.0f-%.0f): alpha_MW = M/L_K/(M/L_K)_MW, mean %.3f, range %.2f-%.2f"
  % (len(al), sg.min(), sg.max(), al.mean(), al.min(), al.max()))
P("  fit log10 alpha_MW = %.4f + %.4f log10(sigma/200), rms %.4f dex (XR33 reports 0.111 + 0.628, rms 0.12)"
  % (coef[0], coef[1], rms))
P("  at sigma=241: alpha_MW %.3f -> alpha_Salp %.3f (Salpeter = %.2f in these units)" % (a241 * SAL_K, a241, SAL_K))
P("  required %.3f is %.2f sigma (of the rms) above the relation, percentile %.0f%% of the sample"
  % (B_req, (math.log10(B_req) - math.log10(a241)) / rms, 100 * np.mean(al / SAL_K < B_req)))
ck("K20", "CvD12b spectroscopic relation: slope and rms vs XR33's fit, and where 1.17x sits",
   "slope %.4f (XR33 0.628), rms %.4f (0.12), alpha_Salp(241) %.3f, required %.1f sigma"
   % (coef[1], rms, a241, (math.log10(B_req) - math.log10(a241)) / rms),
   abs(coef[1] - 0.628) < 0.03 and abs(rms - 0.12) < 0.02 and 0.3 < (math.log10(B_req) - math.log10(a241)) / rms < 1.2)
RES["cvd"] = dict(N=int(len(al)), slope=float(coef[1]), intercept=float(coef[0]), rms=float(rms),
                  a_salp_241=float(a241), sigma_above=float((math.log10(B_req) - math.log10(a241)) / rms),
                  percentile=float(np.mean(al / SAL_K < B_req)))

# random-effects 95% CL across methods
studies = [("Treu+2010 SLACS dyn+lens", 1.000, sd_tot),
           ("CvD12b relation at sigma=241", a241, 0.030),
           ("MASSIVE XXI, R_e/4-R_e/2", 1.74 / SAL_K, 0.42 / SAL_K / math.sqrt(37)),
           ("MASSIVE XVI, R_e/8", 1.84 / SAL_K, 0.50 / SAL_K / math.sqrt(41))]
y = np.array([s[1] for s in studies]); s = np.array([s[2] for s in studies])
wi = 1.0 / s ** 2; ybar = (wi * y).sum() / wi.sum()
Q = float((wi * (y - ybar) ** 2).sum()); df = len(y) - 1
Cq = float(wi.sum() - (wi ** 2).sum() / wi.sum())
tau2 = max(0.0, (Q - df) / Cq)
wr = 1.0 / (s ** 2 + tau2)
mu = float((wr * y).sum() / wr.sum()); sd = float(1.0 / math.sqrt(wr.sum()))
P("\n  literature inputs (alpha in Salpeter units; Kroupa -> Salpeter = 1.55):")
P("    MASSIVE XVI (sigma>250, R_e/8): alpha_Kroupa mean 1.84, range 1.12-3.05 -> %.3f x Salpeter" % (1.84 / SAL_K))
P("    MASSIVE XXI: alpha_Kroupa 2.16 at R_e/8 -> %.3f ; 1.74 at R_e/4-R_e/2 -> %.3f" % (2.16 / SAL_K, 1.74 / SAL_K))
P("    Leier+2016 (18 SLACS ETGs): mu <= 2.2 at 20-30%% dark matter; very bottom-heavy excluded (qualitative)")
P("    Smith, Lucey & Collier 2018: upper-limit lensing excludes >Salpeter in one sigma=314 system (counter-claim)")
P("\n  random-effects (DerSimonian-Laird) over four independent IMF calibrations:")
for nmx, yy, ss in studies:
    P("    %-32s %.3f +- %.3f" % (nmx, yy, ss))
P("    fixed mean %.3f ; Q %.2f for %d dof ; tau %.3f dex ; random mean %.3f +- %.3f ; 95%% %.3f-%.3f"
  % (ybar, Q, df, math.sqrt(tau2), mu, sd, mu - 1.96 * sd, mu + 1.96 * sd))
P("    required %.3f is %+.3f dex from the random mean = %.1f sigma ; inside 95%%: %s"
  % (B_req, math.log10(B_req) - math.log10(mu), abs(math.log10(B_req) - math.log10(mu)) / (sd / mu / math.log(10)),
     mu - 1.96 * sd <= B_req <= mu + 1.96 * sd))
d_re = abs(math.log10(B_req) - math.log10(mu)) / math.sqrt((sd / (mu * math.log(10.0))) ** 2 + sig_logB ** 2)
ck("K21", "the two 95% intervals disagree about 1.17: outside the cross-method one, inside the direct SLACS one",
   "RE 95%% %.3f-%.3f (1.17 at %.2f sigma) ; direct SLACS 95%% %.3f-%.3f (1.17 at %.2f sigma)"
   % (mu - 1.96 * sd, mu + 1.96 * sd, d_re, 10 ** (-1.96 * sd_tot), 10 ** (1.96 * sd_tot),
      math.log10(B_req) / sd_tot),
   B_req > mu + 1.96 * sd and B_req <= 10 ** (1.96 * sd_tot))
RES["imf_random_effects"] = dict(studies=[dict(name=a, value=float(b), sigma=float(c)) for a, b, c in studies],
                                 fixed_mean=float(ybar), Q=Q, tau=float(math.sqrt(tau2)), mean=float(mu),
                                 sd=float(sd), lo95=float(mu - 1.96 * sd), hi95=float(mu + 1.96 * sd),
                                 inside=bool(mu - 1.96 * sd <= B_req <= mu + 1.96 * sd))

# Auger+2010 dynamics: f_DM inside R_e/2, and the theory's mass budget there
_, au = load_table(DATA_AUG10)
fds = np.array([x["fDM_salp"] for x in au]); fdc = np.array([x["fDM_chab"] for x in au])
P("\n  Auger+2010 (N=%d): f_DM(<R_e/2) Salpeter mean %.3f median %.3f (16-84 %.3f-%.3f, %d negative)"
  % (len(au), fds.mean(), np.median(fds), np.percentile(fds, 16), np.percentile(fds, 84), int(np.sum(fds < 0))))
P("                   Chabrier mean %.3f median %.3f (16-84 %.3f-%.3f)"
  % (fdc.mean(), np.median(fdc), np.percentile(fdc, 16), np.percentile(fdc, 84)))
by = {d["name"]: d for d in L}
mb = []
for x in au:
    if x["outlier"] != 0 or x["name"] not in by: continue
    Re = x["re_V_kpc"] * KPC; Ms = 10 ** x["logMs_salp"] * MSUN; Mt = 10 ** x["logM_e2"] * MSUN
    Mst = Ms * M2D_star(0.5 * Re, Re, 4.0)
    yy = G * (Ms * M3D_star(0.5 * Re, Re, 4.0)) / (A0_EFF * (0.5 * Re) ** 2)
    mb.append(Mst * (1.0 + F_ph(yy)) / Mt)
mb = np.array(mb)
P("  theory (Salpeter stars + phantom) at R_e/2: M_theory/M_dyn median %.3f -> implied f_DM %.3f vs measured %.3f"
  % (np.median(mb), 1 - np.median(mb), np.median(fds)))
ck("K22", "independent dynamics at R_e/2: the theory+Salpeter leaves the same dark fraction Auger measures",
   "M_th/M_dyn %.3f (f_DM %.3f) vs f_DM_Salp %.3f (diff %.3f)"
   % (np.median(mb), 1 - np.median(mb), np.median(fds), (1 - np.median(mb)) - np.median(fds)),
   abs((1 - np.median(mb)) - np.median(fds)) < 0.06)
mb_boost = []
for x in au:
    if x["outlier"] != 0 or x["name"] not in by: continue
    Re = x["re_V_kpc"] * KPC; Ms = 10 ** x["logMs_salp"] * MSUN; Mt = 10 ** x["logM_e2"] * MSUN
    Mst = B_req * Ms * M2D_star(0.5 * Re, Re, 4.0)
    yy = G * (B_req * Ms * M3D_star(0.5 * Re, Re, 4.0)) / (A0_EFF * (0.5 * Re) ** 2)
    mb_boost.append(Mst * (1.0 + F_ph(yy)) / Mt)
P("  with the required %.3f x Salpeter: M_theory/M_dyn %.3f -> implied f_DM %.3f (still non-negative)"
  % (B_req, np.median(mb_boost), 1 - np.median(mb_boost)))
RES["auger2010"] = dict(N=int(len(au)), fdm_salp_median=float(np.median(fds)), fdm_chab_median=float(np.median(fdc)),
                        theory_fdm=float(1 - np.median(mb)), theory_fdm_boost=float(1 - np.median(mb_boost)),
                        n_negative_salp=int(np.sum(fds < 0)))

# =====================================================================================
P("\n" + "-" * 118)
P("TASK 4 -- AMPLITUDE OR SHAPE?")
P("-" * 118)

sd_thE = 0.02
sigs = []
for d, r in zip([byall[x] for x in nm], r_sal):
    eF = d["eFs"] if np.isfinite(d["eFs"]) and d["eFs"] > 0 else 0.10
    s_m = 0.5 * math.log(1.0 + eF / max(d["Fs"], 1e-3))
    sigs.append(math.sqrt(sd_thE ** 2 + s_m ** 2 + 0.05 ** 2))
sigs = np.array(sigs)
chi2_55 = float(np.sum((np.log(r_sal) / sigs) ** 2))
P("\n  chi2 with A55's per-lens errors (2%% theta_E + propagated M* + 5%% shape): %.1f / %d dof = %.2f (A55 6.21)"
  % (chi2_55, len(r_sal) - 1, chi2_55 / (len(r_sal) - 1)))
P("  propagated sigma median %.4f dex vs observed scatter %.4f dex (ratio %.1f)"
  % (np.median(sigs) / math.log(10), st_sal["scatter_dex"], st_sal["scatter_dex"] / (np.median(sigs) / math.log(10))))
ck("K23", "A55's chi2/dof and the excess scatter are reproduced, and the 2% R_E error is not what drives either",
   "chi2/dof %.2f vs 6.21 ; propagated %.4f vs observed %.4f dex"
   % (chi2_55 / (len(r_sal) - 1), np.median(sigs) / math.log(10), st_sal["scatter_dex"]),
   abs(chi2_55 / (len(r_sal) - 1) - 6.21) < 0.05 and st_sal["scatter_dex"] > 2.0 * np.median(sigs) / math.log(10))
RES["chi2"] = dict(chi2=chi2_55, dof=len(r_sal) - 1, chi2_dof=chi2_55 / (len(r_sal) - 1),
                   sigma_prop_dex=float(np.median(sigs) / math.log(10)))

# residual trends
def ols(yv, xv):
    xv = np.asarray(xv); yv = np.asarray(yv); A = np.vstack([np.ones_like(xv), xv]).T
    c, _, _, _ = np.linalg.lstsq(A, yv, rcond=None)
    s2 = ((yv - A @ c) ** 2).sum() / (len(yv) - 2)
    se = math.sqrt(s2 * np.linalg.inv(A.T @ A)[1, 1])
    return float(c[1]), float(se)

res_lr = np.log(r_sal)
sv = np.array([byall[x]["sig"] for x in nm])
rev = np.array([byall[x]["RE"] / Re_kpc(byall[x]) for x in nm])
mE = np.array([byall[x]["lME"] for x in nm])
b_sig, e_sig = ols(res_lr, np.log(sv))
b_re, e_re = ols(res_lr, np.log(rev))
b_th, e_th = ols(res_lr, np.log([byall[x]["RE"] * KPC / DA(byall[x]["zl"]) / ARCSEC for x in nm]))
P("\n  residual ln(R_pred/R_obs) trends: vs ln sigma %+.3f +- %.3f (%.1f sigma) ; vs ln(R_E/R_e) %+.3f +- %.3f (%.1f sigma)"
  % (b_sig, e_sig, abs(b_sig / e_sig), b_re, e_re, abs(b_re / e_re)))
P("  vs ln theta_E %+.3f +- %.3f (%.1f sigma) ; vs log M_E %+.3f +- %.3f"
  % (b_th, e_th, abs(b_th / e_th), *ols(res_lr, mE)))
for lo, hi in [(150, 220), (220, 260), (260, 300), (300, 500)]:
    m = (sv >= lo) & (sv < hi)
    P("    sigma [%d,%d): N=%2d  median ratio %.3f" % (lo, hi, int(m.sum()), float(np.exp(np.median(res_lr[m])))))
RES["trends"] = dict(vs_lsigma=dict(slope=b_sig, se=e_sig), vs_lRE_Re=dict(slope=b_re, se=e_re),
                     vs_lthetaE=dict(slope=b_th, se=e_th))

# applying the independently measured IMF(sigma) trend
def alpha_cvd(s): return 10 ** (coef[0] + coef[1] * math.log10(s / 200.0)) / SAL_K
a241_ = alpha_cvd(241.0)
res_corr = []
for x in nm:
    d = byall[x]
    B = alpha_cvd(d["sig"]) / a241_
    res_corr.append(math.log(predict(d, boost=B) / d["RE"]))
res_corr = np.array(res_corr)
b_corr, e_corr = ols(res_corr, np.log(sv))
P("\n  after multiplying by the CvD12b IMF(sigma) trend (normalised at sigma=241):")
P("    mean ln %+.4f (was %+.4f) ; slope vs ln sigma %+.3f +- %.3f (was %+.3f +- %.3f)"
  % (res_corr.mean(), res_lr.mean(), b_corr, e_corr, b_sig, e_sig))
ck("K24", "the mass-dependent residual is the independently measured IMF-sigma trend: the slope flattens to zero",
   "slope %+.3f (%.1f sigma) -> %+.3f (%.1f sigma)" % (b_sig, abs(b_sig / e_sig), b_corr, abs(b_corr / e_corr)),
   abs(b_sig / e_sig) > 2.0 and abs(b_corr / e_corr) < 1.5)
RES["imf_trend_test"] = dict(slope_before=float(b_sig), se_before=float(e_sig),
                             slope_after=float(b_corr), se_after=float(e_corr),
                             mean_before=float(res_lr.mean()), mean_after=float(res_corr.mean()))

# independent shape check: imaging-only total-density slope at theta_E
shape_rows = []
for d in match:
    v = eth[d["name"]]
    REo = v["thE"] * ARCSEC * DA(d["zl"])
    sc = SICR(d["zl"], d["zs"]); Re = Re_kpc(d) * KPC; REaug = d["RE"] * KPC
    def resid(lb):
        B = math.exp(lb)
        A = B * d[IMF_HEAD] * 10 ** d["lME"] / M2D_star(REaug, Re)
        return M2D_from_g(REo, lambda r, A=A: A * M3D_star(r, Re) * MSUN, A0_EFF) - math.pi * REo ** 2 * sc
    try:
        lb = brentq(resid, math.log(0.2), math.log(5.0), xtol=1e-4)
    except Exception:
        continue
    B = math.exp(lb); A = B * d[IMF_HEAD] * 10 ** d["lME"] / M2D_star(REaug, Re)
    kap = lambda R: M2D_from_g(R, lambda r, A=A: A * M3D_star(r, Re) * MSUN, A0_EFF) / (math.pi * R * R * sc)
    hh = 2e-3
    gam = 1.0 - (math.log(kap(REo * (1 + hh))) - math.log(kap(REo * (1 - hh)))) / (2 * hh)
    shape_rows.append((d["name"], gam, v["gam"], B))
sa = np.array([[x[1], x[2], x[3]] for x in shape_rows])
dsh = sa[:, 0] - sa[:, 1]
P("\n  imaging-only shape test, %d lenses (Etherington+2022 power-law gamma vs my A55 model normalised to its theta_E):"
  % len(shape_rows))
P("    gamma_pred median %.3f ; gamma_obs median %.3f ; delta mean %+.3f +- %.3f (median %+.3f), scatter %.3f"
  % (np.median(sa[:, 0]), np.median(sa[:, 1]), dsh.mean(), dsh.std(ddof=1) / math.sqrt(len(dsh)),
     np.median(dsh), dsh.std(ddof=1)))
P("    per-lens M/L boost needed at Etherington's theta_E: median %.3f (16-84 %.2f-%.2f)"
  % (np.median(sa[:, 2]), np.percentile(sa[:, 2], 16), np.percentile(sa[:, 2], 84)))
ck("K25", "shape at fixed amplitude: the model's total-density slope at theta_E vs the imaging-only measurement",
   "gamma_pred %.3f vs gamma_obs %.3f ; delta %+.3f +- %.3f"
   % (np.median(sa[:, 0]), np.median(sa[:, 1]), dsh.mean(), dsh.std(ddof=1) / math.sqrt(len(dsh))),
   abs(dsh.mean()) < 0.06)
sigs_real = np.sqrt(sigs ** 2 + (0.0694 ** 2 - 0.02 ** 2))   # per-lens mass term kept; 2% -> 6.9%
chi2_real = float(np.sum((np.log(r_sal) / sigs_real) ** 2))
P("  control: with the measured inter-pipeline 6.9%% theta_E scatter replacing the assumed 2%%,"
  " chi2/dof = %.2f (vs %.2f) -- the excess scatter survives" % (chi2_real / (len(r_sal) - 1), chi2_55 / (len(r_sal) - 1)))
# partial: does the R_E/R_e trend survive the IMF-sigma correction?
b_re2, e_re2 = ols(res_corr, np.log(rev))
P("  after the IMF-sigma correction the R_E/R_e slope is %+.3f +- %.3f (%.1f sigma; was %+.3f)"
  % (b_re2, e_re2, abs(b_re2 / e_re2), b_re))
RES["k25_controls"] = dict(chi2_dof_real_error=float(chi2_real / (len(r_sal) - 1)),
                           re_re_slope_after_imf=float(b_re2), re_re_se_after_imf=float(e_re2))
RES["shape"] = dict(N=int(len(shape_rows)), gamma_pred_median=float(np.median(sa[:, 0])),
                    gamma_obs_median=float(np.median(sa[:, 1])), delta_mean=float(dsh.mean()),
                    delta_sem=float(dsh.std(ddof=1) / math.sqrt(len(dsh))), delta_scatter=float(dsh.std(ddof=1)),
                    B_median=float(np.median(sa[:, 2])))

# =====================================================================================
P("\n" + "-" * 118)
P("VERDICT")
P("-" * 118)
verdict = dict(
    headline_sigma=float(st_sal["sigma"]),
    B_req=float(B_req),
    B_a55=float(B_a55),
    kappa_star_salpeter=float(kstar),
    kappa_star_free_dchi2=float(dmax),
    imf_95_direct=[float(10 ** (-1.96 * sd_tot)), float(10 ** (1.96 * sd_tot))],
    imf_95_random=[float(mu - 1.96 * sd), float(mu + 1.96 * sd)],
    imf_sigma_from_direct=float(math.log10(B_req) / sd_tot),
    shape_delta=float(dsh.mean()),
)
P("  R_E failure at Salpeter, a0=1.132e-10 : %.2f sigma (A55 4.9)" % st_sal["sigma"])
P("  M/L that zeroes it                   : %.3f x Salpeter (A55 quoted 1.283)" % B_req)
P("  same, in the direct SLACS IMF units  : %.2f sigma from the measured mean" % (math.log10(B_req) / sd_tot))
P("  kappa* with Salpeter fixed           : %.3f (A51 band 0.252-0.490)" % kstar)
P("  kappa* with the IMF free             : unconstrained, Delta-chi2 < %.1f over 0.2-0.8" % dmax)
P("  shape at fixed amplitude             : gamma_pred - gamma_obs = %+.3f +- %.3f" % (dsh.mean(), dsh.std(ddof=1) / math.sqrt(len(dsh))))
RES["verdict"] = verdict

npass = sum(1 for c in CK if c["pass_"]); ntot = len(CK)
P("\n" + "=" * 118)
P("A70: %d/%d checks PASS   (%.1f s)" % (npass, ntot, time.time() - T0))
P("=" * 118)
RES["checks"] = CK; RES["n_pass"] = npass; RES["n_total"] = ntot; RES["runtime_s"] = float(time.time() - T0)

stem = "a70" if not MUT else "a70_MUTATE_%s" % MUT
with open(os.path.join(HERE, stem + ".out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, stem + "_results.json"), "w") as fh: json.dump(RES, fh, indent=1)
sys.exit(0 if npass == ntot else 1)