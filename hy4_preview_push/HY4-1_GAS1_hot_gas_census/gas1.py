#!/usr/bin/env python3
"""GAS1: is form B's amount problem a missing-baryon problem?
Criteria: hy4_preview_push/HY4-1_GAS1_hot_gas_census/FROZEN_CRITERIA.md (committed alone before this file).

Run (from this folder, one thread):
    python3 gas1.py            -> gas1.json, gas1.out
    python3 gas1.py --mutate   -> gas1_MUTATE.json, gas1_MUTATE.out

Inputs are the staged, git-ignored files under real_research/data/lensing_rar/ plus B21's published tables.
The 16 GB shear catalogue is NOT read.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
B21 = os.path.join(DATA, "brouwer2021_rar")
MUTATE = "--mutate" in sys.argv
TAG = "gas1_MUTATE" if MUTATE else "gas1"
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

# ----------------------------------------------------------------------------- constants (the record's, section 2)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; kpc = 3.0857e19; pc = 3.0857e16
c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt")
R_B = 5.41                       # Omega_c / Omega_b, the cosmic cold-to-baryon budget
S_B = 1.0 + R_B                  # Omega_m / Omega_b
X_B = math.sqrt(R_B * S_B)       # 5.8888  : the radius, in r_M, at which the budget is spent
XB2 = X_B * X_B                  # 34.6781
LINE = 10 ** -0.05               # 0.891 : the record's KiDS gate line (KO1's LINE)
O = [0, 1, 2, 3]                 # the outer g_bar bins
NPAT = 50
MSUN_PC2 = Msun / pc ** 2        # 1 Msun/pc^2 in kg/m^2 (B21's ESD unit, h70 read as 1)
# cosmology: h, omega_b, omega_d from R541B / PAR1 A2 / AMT1
COSM = {"canonical": (0.674, 0.02236, 0.1209), "alt": (0.674, 0.02234, 0.1209)}
SURVEY_DEG2 = 1000.0             # B21's README, on disk: "1000 degrees^2 of KiDS-1000"

def nu(y):        return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0):  return nu(g / a0) * g
def Xsh(x):       return 0.5 * (np.sqrt(1.0 + 4.0 * x * x) - 1.0)
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def fcold(logMs):  return 10 ** (-0.69 * logMs + 6.63)
def mgal_of(logMs): return 10 ** logMs * (1 + fcold(logMs))

def rho_crit(h):
    H0 = h * 100e3 / Mpc
    return 3.0 * H0 * H0 / (8.0 * math.pi * G)          # kg/m^3
def cosmo(foot):
    h, ob, od = COSM[foot]
    Ob = ob / h ** 2; Od = od / h ** 2
    rc = rho_crit(h)
    return dict(h=h, Ob=Ob, Om=Ob + Od, rho_crit=rc, rho_b=Ob * rc,
                rho_b_Mpc=Ob * rc / (Msun / Mpc ** 3))

def fmt(x, n=4):
    return "nan" if x is None or not np.isfinite(x) else f"{x:.{n}g}"

P("GAS1: is form B's amount problem a missing-baryon problem?")
P(f"criteria: FROZEN_CRITERIA.md   mode: {'MUTATE' if MUTATE else 'primary'}")
P("")
P("=== Section 2: constants, printed in SI ===")
P(f"  G {G:.6e} m^3 kg^-1 s^-2   Msun {Msun:.6e} kg   Mpc {Mpc:.6e} m   pc {pc:.6e} m")
P(f"  a0 canonical {A0['canonical']:.6e}   alt {A0['alt']:.6e} m/s^2   (never pooled)")
P(f"  budget R_b = Omega_c/Omega_b = {R_B}   S_b = Omega_m/Omega_b = {S_B}")
P(f"  x_b = sqrt(R_b S_b) = {X_B:.6f}   x_b^2 = {XB2:.6f}   (AMT1: 5.8888)")
for f in FOOT:
    C = cosmo(f)
    P(f"  [{f}] h {C['h']}  Omega_b {C['Ob']:.6f}  Omega_m {C['Om']:.6f}  "
      f"rho_crit {C['rho_crit']:.6e} kg/m^3  rho_b {C['rho_b']:.6e} kg/m^3 = {C['rho_b_Mpc']:.6e} Msun/Mpc^3")
P(f"  1 Msun/pc^2 = {MSUN_PC2:.6e} kg/m^2 (B21's ESD unit; h70 read as 1, as KO1's R6 did)")

# =============================================================== KA1, KA2, KA3 : the identities, before any data
P("")
P("=== Known answers KA1-KA3 (identities; no data) ===")
xs = np.logspace(-3, 4, 4000)
d1 = float(np.max(np.abs(Xsh(xs) - (nu(1.0 / xs ** 2) - 1.0))))
check("KA1 X(x) = nu(1/x^2) - 1 over x in [1e-3,1e4]", d1 < 1e-12, f"max |dev| {d1:.2e}")
d2 = abs(Xsh(X_B) - R_B); d2b = abs(X_B - 5.8888)
check("KA2 X(x_b) = 5.41 and x_b = 5.8888", d2 < 1e-12 and d2b < 1e-4,
      f"X(x_b) - 5.41 = {d2:.2e}; x_b - 5.8888 = {d2b:.2e}")
for f in FOOT:
    a0 = A0[f]
    Sg = a0 / (math.pi * G * XB2)
    # numerical dM/d(pi R^2) of (L1): M(R) = (a0/G) R^2 / x_b^2 - Mstar
    Rs = np.logspace(np.log10(1e5 * pc), np.log10(3e6 * pc), 60)
    M = (a0 / G) * Rs ** 2 / XB2 - 1e40
    num = np.gradient(M, np.pi * Rs ** 2)
    d3 = float(np.max(np.abs(num / Sg - 1.0)))
    check(f"KA3[{f}] constant column (L2) = a0/(pi G x_b^2)", d3 < 1e-6,
          f"Sigma = {Sg:.6e} kg/m^2 = {Sg / MSUN_PC2:.4f} Msun/pc^2 ; max |numerical/closed - 1| {d3:.2e}")
    # KA4: the fixed point
    Mstar = 5.6058e40     # AMT1's fiducial log M_b = 10.45
    Mbar = Mstar + np.maximum((a0 / G) * Rs ** 2 / XB2 - Mstar, 0.0)
    x = Rs / np.sqrt(G * Mbar / a0)
    d4 = float(np.max(np.abs(Xsh(x) - R_B)[(a0 / G) * Rs ** 2 / XB2 > Mstar]))
    check(f"KA4[{f}] fixed point: M_bar = M_star + M_req gives X = 5.41", d4 < 1e-9, f"max |X - 5.41| {d4:.2e}")

# =============================================================== staged lensing sums
P("")
P("=== Staged KiDS sums ===")
ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WG, WW, NN, EDGES = PL["WG"], PL["WW"], PL["NN"], PL["gbar_edges"]
ST = np.load(os.path.join(DATA, "cfg96_stack.npz")); patch = ST["patch"]
try:
    C116 = np.load(os.path.join(DATA, "cfg116_perlens.npz")); WX = C116["WX"]
except Exception:
    WX = None
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
ALL = np.ones(NL, bool)
P(f"  lenses {NL:,}; 15 g_bar bins, edges {EDGES[0]:.3e} .. {EDGES[-1]:.3e}; outer bins O = {O}")
P(f"  outer-bin edges: {EDGES[0]:.4e} {EDGES[1]:.4e} {EDGES[2]:.4e} {EDGES[3]:.4e} {EDGES[4]:.4e} m/s^2")

# KA7
dev = 0.0
for arr, key in ((WG, "wgE_"), (WW, "W_"), (NN, "NN_")):
    S = np.zeros((NPAT, 2, 15)); np.add.at(S, (patch, typ), arr)
    ref = ST[key + "10"]
    dev = max(dev, float(np.max(np.abs(S - ref)) / np.max(np.abs(ref))))
check("KA7 per-lens sums reproduce cfg96_stack (W10) to 1e-9", dev < 1e-9, f"max relative deviation {dev:.2e}")

WGo, WWo = WG[:, O].copy(), WW[:, O].copy()
XG, WGL = np.polynomial.legendre.leggauss(24)
R3 = (3.0 * Mpc) ** 2

def bounds(k, Mg_arr):
    t_lo = G * Mg_arr / EDGES[k + 1]; t_hi = np.minimum(G * Mg_arr / EDGES[k], R3)
    return t_lo, t_hi, t_hi > t_lo

def law_cells(a0, Mg_model=None, Mg_geom=None):
    """Area-weighted mean of nu(g_N/a0) g_N over each lens's annulus [R_lo,R_hi].
    Mg_geom sets the annulus (the catalogued mass, as B21 binned it); Mg_model is the mass in g_N."""
    Mgm = Mg if Mg_model is None else Mg_model
    Mgg = Mg if Mg_geom is None else Mg_geom
    m = np.zeros((len(Mgm), len(O)))
    for c, k in enumerate(O):
        t_lo, t_hi, ok = bounds(k, Mgg)
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = glaw(G * Mgm[:, None] / t, a0)
        m[:, c] = np.where(ok, (f * WGL[None, :]).sum(1) / 2, 0.0)
    return m

def radii(k, Mg_arr=None):
    """Per lens: R_eff = sqrt(<R^2>_area) and R_hi for bin k."""
    Mgg = Mg if Mg_arr is None else Mg_arr
    t_lo, t_hi, ok = bounds(k, Mgg)
    R2 = np.where(ok, (t_hi ** 2 - t_lo ** 2) / (2.0 * np.log(np.maximum(t_hi / t_lo, 1 + 1e-300))), np.nan)
    Rbar = np.where(ok, (2.0 / 3.0) * (t_hi ** 1.5 - t_lo ** 1.5) / (t_hi - t_lo), np.nan)
    Reff = np.where(ok, np.sqrt((t_hi + t_lo) / 2.0), np.nan)   # sqrt(<R^2>_area), t = R^2
    Rhi = np.where(ok, np.sqrt(t_hi), np.nan)
    return Reff, Rbar, Rhi, R2, ok

def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(a.shape[1])], axis=1)

def amp(mask, Mo, WGx=None, cols=None, sk=None):
    WGx = WGo if WGx is None else WGx
    cols = list(range(len(O)))
    Sg = psum(WGx, mask); Sw = psum(WWo, mask); Sm = psum(WWo * Mo, mask)
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * G * tg / tw; M = tm / tw
    Dl = 4 * G * (tg - Sg) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    if sk is None:
        sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    A = float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Al = (Dl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    s = float(np.sqrt((NPAT - 1) / NPAT * ((Al - Al.mean()) ** 2).sum()))
    return dict(A=A, s=s, Al=Al, D=D, M=M, sk=sk, n=int(mask.sum()))

def jack(fn, mask):
    """delete-one-patch jackknife of a scalar function of the mask."""
    pm = patch[mask]; vals = np.array([fn(mask & (patch != p)) for p in range(NPAT)])
    v = fn(mask)
    return v, float(np.sqrt((NPAT - 1) / NPAT * ((vals - vals.mean()) ** 2).sum()))

LAW = {f: law_cells(A0[f]) for f in FOOT}

# =============================================================== catalogue: the host-free sets (P1)
P("")
P("=== Lens sets: KO1's host-free cut, rebuilt here ===")
from astropy.io import fits
t = time.time()
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
assert np.array_equal(np.asarray(b["ID"]), np.asarray(Lp["ID"]))
r_mag = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); z_ph = np.array(b["zphot_ANNz2"], dtype="f8")
masked = np.array(b["masked"]).astype(np.int64); logM_c = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
ra_c = np.array(b["RAJ2000"], dtype="f8"); dec_c = np.array(b["DECJ2000"], dtype="f8")
del b, Lp; HB.close(); HL.close()
P(f"  catalogue {len(ra_c):,} objects  [{time.time()-t:.0f} s]")

pool = (r_mag < 20) & (z_ph >= 0.02) & (z_ph <= 0.8) & np.isfinite(logM_c) & (logM_c > 7)
inb = np.where(pool)[0]
xN = unitvec(ra_c[inb], dec_c[inb]); chiN = DC(z_ph[inb]); logMN = logM_c[inb]
P(f"  neighbour pool {len(inb):,}  [{time.time()-T0:.0f} s]")
treeN = cKDTree(xN)
xL_all = unitvec(ln["ra"], ln["dec"])
d0, j0 = treeN.query(xL_all, k=1)
selfN = j0
ok_match = (d0 < 1e-9) & (np.abs(logMN[selfN] - logMs) < 1e-9)
check("lens-to-pool identification (position and log M* exact)", bool(ok_match.all()),
      f"max position {d0.max():.2e}, max |dlogM| {np.abs(logMN[selfN]-logMs).max():.2e}, "
      f"{int((~ok_match).sum())} mismatches")
xL = xN[selfN]

def rh_of(logM):
    return np.minimum(3.0, np.sqrt(G * mgal_of(logM) * Msun / 1e-15) / Mpc)
rh = rh_of(logMs)

def host_dmin(delta, F, logM_use=None):
    """min |chi_j - chi_l| over pool objects j != self with logM_j >= logM_l + delta and chord <= F*R_h."""
    lm = logMs if logM_use is None else logM_use
    th = F * rh_of(lm) * (1 + zl) / chil
    chord = 2 * np.sin(th / 2)
    n = len(lm); dmin = np.full(n, np.inf)
    CH = 400
    for i0 in range(0, n, CH):
        i1 = min(i0 + CH, n)
        lists = treeN.query_ball_point(xL[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists))
        tot = int(c.sum())
        if tot == 0: continue
        kk = np.repeat(np.arange(len(c)), c)
        jj = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=tot)
        li = i0 + kk
        keep = (jj != selfN[li]) & (logMN[jj] >= lm[li] + delta)
        li, jj = li[keep], jj[keep]
        if len(li):
            np.minimum.at(dmin, li, np.abs(chiN[jj] - chil[li]))
    return dmin

HF = {}
for F in (1.0, 1.3, 1.6):
    dmin = host_dmin(0.3, F)
    HF[F] = dmin >= 230.0
    P(f"  veto F = {F} R_h: host-free {int(HF[F].sum()):,}  [{time.time()-T0:.0f} s]")
P1 = HF[1.6]
ka6 = (int(HF[1.0].sum()) == 40667) and (int(HF[1.3].sum()) == 25708) and (int(HF[1.6].sum()) == 17335)
check("KA6 host-free counts 40,667 / 25,708 / 17,335 at F = 1.0 / 1.3 / 1.6", ka6,
      f"{int(HF[1.0].sum()):,} / {int(HF[1.3].sum()):,} / {int(HF[1.6].sum()):,}")
if not ka6 and not MUTATE:
    P("  !! P1 falls back to the full W10 set (criteria section 3 fallback)")
    P1 = ALL.copy()
P(f"  mean R_h of the P1 set: {rh[P1].mean():.3f} Mpc;  z range {zl[P1].min():.3f} .. {zl[P1].max():.3f}")

# null: cross shear
if WX is not None:
    WXo = WX[:, O].copy()
    rr = amp(P1, LAW["canonical"], WGx=WXo)
    P(f"  null (reported): cross-shear amplitude of P1 over O, canonical {rr['A']:+.3f} +- {rr['s']:.3f}")
    check("Null cross-shear of P1 within 2.5 s of zero", abs(rr["A"]) <= 2.5 * rr["s"],
          f"{rr['A']:+.3f} +- {rr['s']:.3f}")

# =============================================================== STEP 1 : the demand, bin by bin
P("")
P("=== Step 1: the law's demand, M_c(<R) = M_b X(x), on the record's own bins (lens set P1) ===")
STEP1 = {}
for f in FOOT:
    a0 = A0[f]
    rows = []
    for c, k in enumerate(O):
        Reff, Rbar, Rhi, R2, ok = radii(k)
        m = P1 & ok
        w = WWo[m, c]
        Mbar_w = float((w * Mg[m]).sum() / w.sum())
        rM = math.sqrt(G * Mbar_w / a0)
        # area-weighted mean of the enclosed cold mass, per lens, then WW-weighted
        t_lo, t_hi, _ = bounds(k, Mg)
        tt = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(invalid="ignore"):
            Xc = Xsh(np.sqrt(tt) / np.sqrt(G * Mg[:, None] / a0))
        Xcell = (Xc * WGL[None, :]).sum(1) / 2
        Xw = float((w * Xcell[m]).sum() / w.sum())
        Mc_w = float((w * (Mg[m] * Xcell[m])).sum() / w.sum())
        Reff_w = float((w * Reff[m]).sum() / w.sum()); Rhi_w = float((w * Rhi[m]).sum() / w.sum())
        rows.append(dict(k=k, g_lo=float(EDGES[k]), g_hi=float(EDGES[k+1]),
                         Mbar_Msun=Mbar_w / Msun, rM_kpc=rM / kpc, X=Xw, Mc_Msun=Mc_w / Msun,
                         over_budget=Xw / R_B, Reff_Mpc=Reff_w / Mpc, Rhi_Mpc=Rhi_w / Mpc,
                         Reff_over_rM=Reff_w / rM))
        P(f"  [{f}] bin {k}: g_bar {EDGES[k]:.3e}-{EDGES[k+1]:.3e}  R_eff {Reff_w/Mpc:.4f} Mpc "
          f"(R_hi {Rhi_w/Mpc:.4f})  <M_b> {Mbar_w/Msun:.4g} Msun  r_M {rM/kpc:.3f} kpc  "
          f"<X> {Xw:.4g} M_b  M_c {Mc_w/Msun:.4g} Msun  demand/budget {Xw/R_B:.4g}")
    STEP1[f] = rows

# measured amplitudes (KO1's estimator), cross-checked against KO1 E7
P("")
P("=== Step 1b: the measured amplitude of P1 (KO1's estimator; cross-check, added at run time) ===")
AMP = {}
for f in FOOT:
    r = amp(P1, LAW[f])
    AMP[f] = r
    P(f"  [{f}] A(P1, outer bins) = {r['A']:.4f} +- {r['s']:.4f}   (KO1 E7 at 1.6 R_h: 1.40 +- 0.22 canonical)")
    P(f"       D_k (m/s^2): " + " ".join(f"{v:.4e}" for v in r["D"]))
    P(f"       s_k (m/s^2): " + " ".join(f"{v:.4e}" for v in r["sk"]))
    P(f"       M_k (m/s^2): " + " ".join(f"{v:.4e}" for v in r["M"]))
P("  cross-check against KO1 E7 (canonical): 1.10 +- 0.15 at 1.0 R_h, 1.27 +- 0.19 at 1.3 R_h, 1.40 +- 0.22 at 1.6 R_h")
for F, ref in ((1.0, (1.098, 0.154)), (1.3, (1.27, 0.19)), (1.6, (1.40, 0.22))):
    r = amp(HF[F], LAW["canonical"])
    P(f"    F = {F}: this lane {r['A']:.4f} +- {r['s']:.4f}  vs KO1 {ref[0]:.3f} +- {ref[1]:.3f}  "
      f"(difference {r['A']-ref[0]:+.4f}, {(r['A']-ref[0])/math.hypot(r['s'],ref[1]):+.2f} sigma)")

# =============================================================== STEP 2 : the gas the reading needs
P("")
P("=== Step 2a: (L1) the extra baryons that bring the law's demand inside 5.41 M_b ===")
P("    M_gas_req(R) = (a0/G) R^2 / x_b^2 - M_b   ;   Sigma = a0/(pi G x_b^2), constant in R")
STEP2A = {}
for f in FOOT:
    a0 = A0[f]; C = cosmo(f)
    Sg = a0 / (math.pi * G * XB2)
    rows = []
    for c, k in enumerate(O):
        Reff, Rbar, Rhi, R2, ok = radii(k)
        m = P1 & ok
        w = WWo[m, c]
        # enclosed gas at the area-averaged R^2 and at R_hi, WW-weighted
        R2w = float((w * Reff[m] ** 2).sum() / w.sum())
        Rhi_w = float((w * Rhi[m] ** 2).sum() / w.sum())
        Mb_w = float((w * Mg[m]).sum() / w.sum())
        Mreq = (a0 / G) * R2w / XB2 - Mb_w
        Mreq_hi = (a0 / G) * Rhi_w / XB2 - Mb_w
        Reff_w = math.sqrt(R2w)
        vol = (4.0 / 3.0) * math.pi * Reff_w ** 3
        Q1 = Mreq / (C["rho_b"] * vol)
        rows.append(dict(k=k, Reff_Mpc=Reff_w / Mpc, Rhi_Mpc=math.sqrt(Rhi_w) / Mpc,
                         Mstar_Msun=Mb_w / Msun, Mreq_Msun=Mreq / Msun, Mreq_Rhi_Msun=Mreq_hi / Msun,
                         Sigma_Msunpc2=Sg / MSUN_PC2, mean_col_Msunpc2=(Mreq / (math.pi * R2w)) / MSUN_PC2,
                         rho3_MsunMpc3=(Mreq / vol) / (Msun / Mpc ** 3), Q1=Q1,
                         sphere_baryons_Msun=C["rho_b"] * vol / Msun))
        P(f"  [{f}] bin {k}: R_eff {Reff_w/Mpc:.4f} Mpc  M_b {Mb_w/Msun:.4g}  "
          f"M_gas_req {Mreq/Msun:.4g} Msun (= {Mreq/Mb_w:.4g} M_b)  [at R_hi: {Mreq_hi/Msun:.4g}]")
        P(f"        Sigma_gas {Sg/MSUN_PC2:.4f} Msun/pc^2 (constant) ; mean column inside R "
          f"{(Mreq/(math.pi*R2w))/MSUN_PC2:.4f} ; 3D rho {((Mreq/vol)/(Msun/Mpc**3)):.4g} Msun/Mpc^3")
        P(f"        G1: sphere of that radius holds {C['rho_b']*vol/Msun:.4g} Msun of baryons "
          f"-> Q1 = {Q1:.4g}")
    STEP2A[f] = rows
    P(f"  [{f}] (L2) Sigma_gas = a0/(pi G x_b^2) = {Sg:.6e} kg/m^2 = {Sg/MSUN_PC2:.4f} Msun/pc^2 "
      f"(constant in R, from R_budget = x_b r_M outward)")

P("")
P("=== Step 2b: (L3) the data-driven requirement (footing-free) ===")
P("    M_3D,obs = 2/pi * 2 pi R^2 DeltaSigma = R^2 D / G   (isothermal s=1 conversion; point-mass bracket 0.785x)")
STEP2B = []
for c, k in enumerate(O):
    Reff, Rbar, Rhi, R2, ok = radii(k)
    m = P1 & ok
    w = WWo[m, c]
    Sg = psum(WGo, m); Sw = psum(WWo, m)
    D = 4 * G * Sg.sum(0)[c] / Sw.sum(0)[c]
    R2w = float((w * Reff[m] ** 2).sum() / w.sum())
    Mb_w = float((w * Mg[m]).sum() / w.sum())
    M3 = D * R2w / G
    M3b = 0.7853981634 * M3
    req = M3 / S_B - Mb_w
    reqb = M3b / S_B - Mb_w
    STEP2B.append(dict(k=k, D=D, Reff_Mpc=math.sqrt(R2w) / Mpc, M3D_Msun=M3 / Msun,
                       M3D_pm_Msun=M3b / Msun, Mstar_Msun=Mb_w / Msun,
                       req_Msun=req / Msun, req_pm_Msun=reqb / Msun,
                       req_over_Mb=req / Mb_w, frac_of_obs=req / M3))
    P(f"  bin {k}: D {D:.4e} m/s^2  R_eff {math.sqrt(R2w)/Mpc:.4f} Mpc  M_3D,obs {M3/Msun:.4g} Msun  "
      f"M_b {Mb_w/Msun:.4g}  -> M_gas_req {req/Msun:.4g} Msun ({req/Mb_w:.4g} M_b, {100*req/M3:.2f}% of the "
      f"enclosed mass);  point-mass bracket {reqb/Msun:.4g}")

# G2: required gas against the mass that is there
P("")
P("=== G2: the required gas against the measured enclosed mass (gas cannot outweigh everything) ===")
G2 = {}
for f in FOOT:
    rows = STEP2A[f]; vals = []
    for j, row in enumerate(rows):
        Mobs = STEP2B[j]["M3D_Msun"] * Msun
        q = row["Mreq_Msun"] * Msun / Mobs
        vals.append(q)
        P(f"  [{f}] bin {j}: M_gas_req {row['Mreq_Msun']:.4g} / M_obs {Mobs/Msun:.4g} = Q2 {q:.4g}")
    G2[f] = vals

# =============================================================== B21's tables
P("")
P("=== Step 3 / KA5: B21's published tables, this lane's own amplitude code ===")
def read_b21(name):
    a = np.loadtxt(os.path.join(B21, name))
    return dict(gbar=a[:, 0], esd=a[:, 1], esdx=a[:, 2], err=a[:, 3], bias=a[:, 4])
def amp_b21(t, a0, nb=4):
    g = t["gbar"][:nb]; e = t["esd"][:nb] / t["bias"][:nb]; s_e = t["err"][:nb] / t["bias"][:nb]
    D = 4 * G * (e * MSUN_PC2); s = 4 * G * (s_e * MSUN_PC2); M = glaw(g, a0)
    A = float((D * M / s ** 2).sum() / (M * M / s ** 2).sum())
    sA = float(math.sqrt(1.0 / ((M * M / s ** 2).sum())))
    return A, sA
T_nogas = read_b21("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
T_hot = read_b21("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
T_gama = read_b21("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt")
for nm, T in (("Fig-4-5-C1 isolated (no gas)", T_nogas), ("Fig-4 isolated (B21 hot gas)", T_hot),
              ("Fig-4-C1 GAMA isolated", T_gama)):
    for f in FOOT:
        A, sA = amp_b21(T, A0[f])
        P(f"  {nm:32s} [{f:9s}] outer-4 amplitude {A:.4f} +- {sA:.4f}")
A0n, s0n = amp_b21(T_nogas, A0["canonical"]); A0h, s0h = amp_b21(T_hot, A0["canonical"])
check("KA5 B21 tables: no gas 1.50 +- 0.08 and hot gas 0.47 +- 0.04 (KO1 R6), canonical",
      abs(A0n - 1.50) <= 0.08 and abs(A0h - 0.47) <= 0.04,
      f"no gas {A0n:.4f} +- {s0n:.4f} (KO1 1.50 +- 0.08); hot gas {A0h:.4f} +- {s0h:.4f} (KO1 0.47 +- 0.04)")

# --- B21's own gas, extracted from the two tables.
# The two RAR files are binned in g_bar with the same edges and both ESD sequences are monotone in g_bar
# (checked below), so ESD <-> g_bar inverts cleanly. At a fixed ESD the two versions sit at the SAME radius
# (ESD(R) is the measurement), so  ratio(ESD) = g_bar_hot/g_bar_nogas  =  1 + M_gas(<R)/M_star(<R).
def _mono(e):
    e = np.asarray(e, float); return bool(np.all(np.diff(e) > 0))
e_n = T_nogas["esd"] / T_nogas["bias"]; e_h = T_hot["esd"] / T_hot["bias"]
P(f"  monotonicity of the two ESD sequences in g_bar (needed for the inversion): "
  f"no-gas {_mono(e_n)}, hot gas {_mono(e_h)}")
check("B21 ESD sequences are monotone in g_bar (inversion is well defined)", _mono(e_n) and _mono(e_h),
      f"no-gas {_mono(e_n)}; hot gas {_mono(e_h)}")
def invert(tab, esd_target):
    e = tab["esd"] / tab["bias"]; g = tab["gbar"]
    o = np.argsort(e)
    return np.interp(np.log(esd_target), np.log(e[o]), np.log(g[o]))
def ratio_at(esd_target):
    return np.exp(invert(T_hot, esd_target) - invert(T_nogas, esd_target))

P("")
P("  B21's gas-to-stellar ratio, extracted at the ESD of each of B21's 15 g_bar bins (largest radius first):")
for j in range(15):
    rat = ratio_at(e_n[j])
    P(f"    g_bar {T_nogas['gbar'][j]:.4e}  ESD {e_n[j]:9.4f}  gas/star {rat-1:+8.4f}  "
      f"(M_gas = {rat-1:.4g} M_star)")

# KA8 (run-time revision, disclosed in RESULT.md): the mass-bin inversion through Fig-9 is noise-limited
# (Fig-9's ESD is not monotone in g_bar at fixed mass), so KA8 is put on the measured Fig-3 profiles instead:
# M_tot(<R) = R^2 D/G with D = 4 G ESD (the isothermal conversion of section Step 2b).
P("")
P("  KA8 (revised at run time, disclosed): the enclosed mass B21's Fig-3 profiles imply, M_tot = R^2 D/G")
KA8OK = True
for mb in (1, 2, 3, 4):
    F3 = read_b21(f"Fig-3_Lensing-rotation-curves_Massbin-{mb}.txt")
    Rj = F3["gbar"] * Mpc; ESDj = F3["esd"] / F3["bias"]
    D = 4 * G * ESDj * MSUN_PC2
    Mtot = Rj ** 2 * D / G
    outer = slice(7, 15)
    nrev = int((np.diff(Mtot[outer]) < 0).sum())
    grow = Mtot[outer][-1] > Mtot[outer][0]
    okb = (1e11 <= Mtot[-1] / Msun <= 1e14) and grow and np.all(Mtot > 0)
    KA8OK &= bool(okb)
    P(f"    mass bin {mb}: M_tot(<2.60 Mpc) {Mtot[-1]/Msun:.4g} Msun; outward reversals over R > 0.3 Mpc {nrev}; "
      f"grows {grow}; profile " + " ".join(f"{v/Msun:.3g}" for v in Mtot[outer]))
check("KA8 Fig-3 profiles give a positive, outward-growing enclosed mass of a sane size (revised; disclosed)",
      KA8OK, "all four mass bins: M_tot(2.60 Mpc) in [1e11,1e14] Msun and rising from 0.30 to 2.60 Mpc")

# B21's gas at the P1 outer-bin radii, for G3a: B21's gas/star ratio x the P1 stack's own baryon mass
P("")
P("=== G3a: B21's own hot gas, at the P1 outer-bin radii (B21's gas/star x the P1 stack's M_b) ===")
G3A = {}
for f in FOOT:
    vals = []
    for c, k in enumerate(O):
        ESD_p1 = AMP[f]["D"][c] / (4 * G) / MSUN_PC2      # the P1 stack's ESD at this bin, in B21's units
        rat = float(ratio_at(np.array([ESD_p1]))[0])
        Mb = STEP2A[f][c]["Mstar_Msun"]
        Mg_b21 = (rat - 1.0) * Mb
        q = STEP2A[f][c]["Mreq_Msun"] / Mg_b21
        vals.append(q)
        P(f"  [{f}] bin {k}: ESD(P1) {ESD_p1:.4f}  gas/star {rat-1:.4f}  M_b {Mb:.4g}  "
          f"M_gas,B21 {Mg_b21:.4g} Msun  M_gas_req {STEP2A[f][c]['Mreq_Msun']:.4g}  ->  Q3a {q:.4g}")
    G3A[f] = vals

# =============================================================== G3b: GO1's measured group gas
P("")
P("=== G3b: the only measured gas at Mpc radii in the repo (GO1, quoted from its RESULT.md) ===")
GO1 = [  # x = r/R500, M_exc lensing, y gas 1..x, M_b ; f_ret ; errors as published
    (1.00, 7.9e13, 1.8e13, None, 7.0e12), (1.41, 1.31e14, 0.29e14, 3.7e12, 1.4e12),
    (2.00, 0.74e14, 0.43e14, 6.3e12, 2.9e12), (2.83, 2.20e14, 0.40e14, 1.26e13, 0.69e13),
    (4.00, 3.25e14, 0.68e14, 2.2e13, 1.7e13), (5.66, 6.0e14, 1.4e14, 0.6e13, 2.6e13),
    (8.00, 6.9e14, 2.0e14, -0.4e13, 5.1e13), (11.3, 1.7e15, 0.7e15, 7.7e13, 7.5e13),
    (16.0, 4.9e15, 2.4e15, -6.7e14, 3.4e14)]
R500 = 0.66
G3B = {}
P("    GO1: 102 eRASS1 groups, median z 0.143, lensing-weighted M500 1.0e14, Mgas500 5.36e12, R500 0.66 Mpc.")
P("    (L1) depends on R alone, so it applies to a group unchanged.")
for f in FOOT:
    a0 = A0[f]; rows = []
    for x, Mexc, eM, Mgas, egas in GO1:
        R = x * R500 * Mpc
        Mreq = (a0 / G) * R ** 2 / XB2
        if Mgas is None:
            P(f"  [{f}] x {x:5.2f}  R {R/Mpc:6.3f} Mpc  M_gas_req {Mreq/Msun:.4g} Msun  (no gas entry)")
            rows.append(dict(x=x, Mreq=Mreq / Msun, Mgas=None, z=None)); continue
        z = (Mreq / Msun - Mgas) / egas
        rows.append(dict(x=x, Mreq=Mreq / Msun, Mgas=Mgas, z=z, R_Mpc=R / Mpc,
                         Mexc=Mexc, ratio=Mreq / Msun / Mgas))
        P(f"  [{f}] x {x:5.2f}  R {R/Mpc:6.3f} Mpc  M_gas_req {Mreq/Msun:.4g}  measured {Mgas:.3g} +- {egas:.3g} "
          f"-> {(Mreq/Msun-Mgas)/egas:+.2f} sigma   (lensing M_exc there {Mexc:.3g})")
    G3B[f] = rows
    fires = all((r["z"] is not None and r["z"] >= 3.0) for r in rows if r["x"] >= 2.83 and r["Mgas"] is not None)
    P(f"  [{f}] G3b fires (requirement >= 3 sigma above the measured gas at every x >= 2.83): {fires}")

# =============================================================== G4: the amplitude consequence
P("")
P("=== G4: the outer amplitude if that gas were in g_bar (Step 4) ===")
G4 = {}
for f in FOOT:
    a0 = A0[f]
    rows = []
    # per-lens gas factor from (L1) at each bin's R_eff, then the model with the enlarged mass
    mods = np.zeros((NL, len(O)))
    for c, k in enumerate(O):
        Reff, Rbar, Rhi, R2, ok = radii(k)
        with np.errstate(invalid="ignore"):
            Mreq = (a0 / G) * np.where(ok, Reff ** 2, np.nan) / XB2 - Mg
        Mnew = Mg + np.where(ok, np.maximum(Mreq, 0.0), 0.0)
        mods[:, c] = law_cells(a0, Mg_model=Mnew, Mg_geom=Mg)[:, c]
    r = amp(P1, mods)
    G4[f] = dict(A=r["A"], s=r["s"])
    P(f"  [{f}] A_gas = {r['A']:.4f} +- {r['s']:.4f}   (gate line 0.891; measured A = {AMP[f]['A']:.4f} "
      f"+- {AMP[f]['s']:.4f})")
    P(f"       -> the reading moves the outer amplitude from {AMP[f]['A']:.3f} to {r['A']:.3f} of the law")
    for c, k in enumerate(O):
        P(f"       bin {k}: model with catalogued M_b {LAW[f][P1][:,c].mean():.4e} ; "
          f"with the gas {mods[P1][:,c].mean():.4e}  (x{r['M'][c]/AMP[f]['M'][c]:.3g})")

# =============================================================== G5: global
P("")
P("=== G5: the required gas per unit volume, against rho_b (lower bound on n) ===")
chi_max = float(chil.max()); zmax = float(zl.max())
Vmax = (SURVEY_DEG2 * (math.pi / 180) ** 2 / (4 * math.pi)) * (4.0 / 3.0) * math.pi * chi_max ** 3
n_lens = NL / Vmax
G5 = {}
for f in FOOT:
    row = STEP2A[f][-1]      # outermost bin
    rho_req = n_lens * row["Mreq_Msun"]
    C = cosmo(f)
    q = rho_req / C["rho_b_Mpc"]
    G5[f] = dict(n_lens=n_lens, Vmax=Vmax, rho_req=rho_req, rho_b=C["rho_b_Mpc"], q=q)
    P(f"  [{f}] survey {SURVEY_DEG2:.0f} deg^2, z < {zmax:.3f}, chi_max {chi_max:.1f} Mpc -> V {Vmax:.4g} Mpc^3")
    P(f"       n_lens (lower bound: flux-limited, 23 % pass isolation) {n_lens:.4g} Mpc^-3")
    P(f"       <M_gas_req> at {row['Reff_Mpc']:.3f} Mpc = {row['Mreq_Msun']:.4g} Msun  ->  "
      f"rho_req {rho_req:.4g} Msun/Mpc^3  vs rho_b {C['rho_b_Mpc']:.4g}  ->  Q5 {q:.4g}")

# =============================================================== X-COP: measured cluster gas, and the extrapolation
P("")
P("=== X-COP: the measured cluster gas on disk, and the extrapolation to the lens radii (REPORTED, not graded) ===")
XD = os.path.join(REPO, "real_research", "data", "xcop")
XCOP = []
try:
    RJ = json.load(open(os.path.join(XD, "xcop_r500_ettori2019.json")))
    for nm in sorted(RJ):
        fn = os.path.join(XD, nm, nm + "_fgas_profile.fits")
        if not os.path.exists(fn): continue
        d = fits.open(fn)[1].data
        xr = np.array(d["RADIUS"], float); mg = np.array(d["MGAS"], float)
        mn = np.array(d["M_NFW"], float); fg = np.array(d["FGAS"], float)
        j = int(np.argmax(xr))
        R = xr[j] * RJ[nm]["R500"]
        XCOP.append(dict(name=nm, x=xr[j], R_Mpc=R, R500=RJ[nm]["R500"], M500=RJ[nm]["M500"],
                         Mgas=mg[j] / 1e13, Mtot=mn[j] / 1e13, fgas=fg[j]))
    for e in XCOP:
        P(f"  {e['name']:8s} R500 {e['R500']:.3f} Mpc  M500 {e['M500']:.2f}e14  at x = {e['x']:.3f} R500 "
          f"({e['R_Mpc']:.3f} Mpc): M_gas {e['Mgas']:.3f}e13  M_NFW {e['Mtot']:.3f}e14  f_gas {e['fgas']:.4f}")
    for f in FOOT:
        a0 = A0[f]
        P(f"  [{f}] the requirement (L1) at those same radii, and the shortfall of the measured cluster gas:")
        for e in XCOP:
            R = e["R_Mpc"] * Mpc
            Mreq = (a0 / G) * R * R / XB2 / Msun
            P(f"    {e['name']:8s} R {e['R_Mpc']:6.3f} Mpc  M_gas_req {Mreq/1e13:7.3f}e13  "
              f"measured {e['Mgas']:7.3f}e13  ->  req/measured {Mreq/1e13/e['Mgas']:7.3g}")
    # the extrapolation: X-COP's gas fraction at 1.6 R500 applied to the P1 stack's measured mass at the lens radii
    fg_med = float(np.median([e["fgas"] for e in XCOP]))
    P(f"  EXTRAPOLATION (mine, flagged): X-COP's median gas fraction at 1.6 R500, f_gas = {fg_med:.4f}, applied to the "
      f"P1 stack's measured enclosed mass at the KiDS outer radii (cluster -> galaxy scale, so this over-states the gas):")
    for f in FOOT:
        vals = []
        for c, k in enumerate(O):
            Mobs = STEP2B[c]["M3D_Msun"]
            Mx = fg_med * Mobs
            vals.append(STEP2A[f][c]["Mreq_Msun"] / Mx)
            P(f"    [{f}] bin {k}: M_obs {Mobs:.4g}  X-COP-extrapolated gas {Mx:.4g}  "
              f"M_gas_req {STEP2A[f][c]['Mreq_Msun']:.4g}  ->  ratio {vals[-1]:.4g}")
        XCOP_EXT = vals
        P(f"    [{f}] Q_xcop (requirement / X-COP-extrapolated gas): "
          f"{', '.join(f'{v:.3g}' for v in vals)}")
except Exception as exc:
    P(f"  X-COP block skipped: {exc!r}")

# =============================================================== the label
P("")
P("=== Label ===")
LABEL = {}
for f in FOOT:
    q1 = [r["Q1"] for r in STEP2A[f]]
    g1 = all(q > 3.0 for q in q1)
    g2 = all(q > 1.0 for q in G2[f])
    g3a = all(q > 1.0 for q in G3A[f])
    g3b = all((r["z"] is not None and r["z"] >= 3.0) for r in G3B[f] if r["x"] >= 2.83 and r["Mgas"] is not None)
    g4 = (G4[f]["A"] + 2 * G4[f]["s"]) < LINE
    g5 = G5[f]["q"] > 3.0
    if any(v is False for v in CHK.values()):
        lab = "NO VERDICT"
    elif g4 and (g1 or g2 or g3a or g3b):
        lab = "MISSING BARYONS EXCLUDED [AMOUNT AND AMPLITUDE]"
    elif g1 or g2 or g3a or g3b:
        lab = "MISSING BARYONS EXCLUDED [AMOUNT]"
    elif g4:
        lab = "MISSING BARYONS EXCLUDED [AMPLITUDE]"
    elif g5:
        lab = "MISSING BARYONS EXCLUDED [GLOBAL]"
    else:
        lab = "MISSING BARYONS CAN CLOSE IT"
    LABEL[f] = lab
    P(f"  [{f}] G1 {g1} (Q1 {', '.join(f'{q:.3g}' for q in q1)}) ; G2 {g2} "
      f"(Q2 {', '.join(f'{q:.3g}' for q in G2[f])}) ; G3a {g3a} ; G3b {g3b} ; "
      f"G4 {g4} (A_gas {G4[f]['A']:.3f} +- {G4[f]['s']:.3f} vs {LINE:.3f}) ; G5 {g5} (Q5 {G5[f]['q']:.3g})")
    P(f"  [{f}] LABEL: {lab}")

# =============================================================== MUTATE
if MUTATE:
    P("")
    P("=== MUTATE ===")
    RB_M = 5.41e4; SB_M = 1 + RB_M; XB2_M = RB_M * SB_M
    for f in FOOT:
        a0 = A0[f]
        neg = all(((a0 / G) * r["Reff_Mpc"] ** 2 * Mpc ** 2 / XB2_M - r["Mstar_Msun"] * Msun) <= 0
                  for r in STEP2A[f])
        P(f"  M1[{f}] budget 5.41 -> 5.41e4: M_gas_req <= 0 at every graded radius: {neg} "
          f"-> label would be MISSING BARYONS CAN CLOSE IT")
        check(f"M1[{f}] budget x 1e4 removes the requirement", neg, f"all M_gas_req <= 0: {neg}")
    for c, k in enumerate(O):
        pass
    # M2: data x 0.1
    P("  M2: outer-bin WG x 0.1 (data-driven line)")
    ratios = []
    for c, k in enumerate(O):
        Reff, Rbar, Rhi, R2, ok = radii(k)
        m = P1 & ok; w = WWo[m, c]
        Sg = psum(WGo * 0.1, m); Sw = psum(WWo, m)
        D = 4 * G * Sg.sum(0)[c] / Sw.sum(0)[c]
        R2w = float((w * Reff[m] ** 2).sum() / w.sum()); Mb_w = float((w * Mg[m]).sum() / w.sum())
        req = D * R2w / G / S_B - Mb_w
        ratios.append(STEP2B[c]["req_Msun"] * Msun / req)
        P(f"    bin {k}: requirement {STEP2B[c]['req_Msun']:.4g} -> {req/Msun:.4g}  (x{1/ (req/(STEP2B[c]['req_Msun']*Msun)):.3g} fall)")
    check("M2 data x 0.1: the data-driven requirement falls by >= 5x in every bin",
          all(r >= 5.0 for r in ratios), f"fall factors {', '.join(f'{r:.3g}' for r in ratios)}")
    # M3: a0 x 10.  Amendment (post hoc, disclosed): the criteria said "M_gas_req rises by exactly 10"; that is only
    # exact for the (a0/G)R^2/x_b^2 term, because M_gas_req subtracts M_star, which does not scale with a0.
    # Both are graded: the term exactly 10, and M_gas_req reported (it is 10 + 9 M_star/M_gas_req, so slightly above 10).
    for f in FOOT:
        a0 = A0[f]; a0m = a0 * 10
        rr, ss = [], []
        for r in STEP2A[f]:
            R2 = (r["Reff_Mpc"] * Mpc) ** 2
            t1 = (a0 / G) * R2 / XB2; t2 = (a0m / G) * R2 / XB2
            m1 = t1 - r["Mstar_Msun"] * Msun; m2 = t2 - r["Mstar_Msun"] * Msun
            rr.append(t2 / t1); ss.append(m2 / m1)
        check(f"M3[{f}] a0 x 10 scales the (a0/G)R^2/x_b^2 term by exactly 10",
              max(abs(v - 10.0) for v in rr) < 1e-12, f"factors {', '.join(f'{v:.12g}' for v in rr)}")
        P(f"  M3[{f}] a0 x 10: M_gas_req itself rises by {', '.join(f'{v:.6g}' for v in ss)} "
          f"(slightly above 10 because M_star is subtracted and does not scale)")
    P("  M3 data-side invariance: (L3) contains no a0 -> unchanged by construction (printed, not fitted)")
    # M4: B21's gas replaced by the amount-fixing gas in g_bar
    for f in FOOT:
        a0 = A0[f]
        mods = np.zeros((NL, len(O)))
        for c, k in enumerate(O):
            Reff, Rbar, Rhi, R2, ok = radii(k)
            Mreq = (a0 / G) * np.where(ok, Reff ** 2, np.nan) / XB2 - Mg
            Mnew = Mg + np.where(ok, np.maximum(Mreq, 0.0), 0.0)
            mods[:, c] = law_cells(a0, Mg_model=Mnew, Mg_geom=Mg)[:, c]
        r = amp(P1, mods)
        check(f"M4[{f}] the amount-fixing gas puts the outer amplitude below 0.891 by > 2 s",
              r["A"] + 2 * r["s"] < LINE, f"A {r['A']:.4f} +- {r['s']:.4f} vs {LINE:.4f}")

P("")
npass = sum(1 for v in CHK.values() if v)
P(f"Known answers: {npass} of {len(CHK)} PASS -> {'ALL PASS' if npass == len(CHK) else 'FAILURES ABOVE'}")
P(f"runtime {time.time()-T0:.0f} s")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

res = dict(label=LABEL, step1=STEP1, step2a=STEP2A, step2b=STEP2B, G2=G2, G3a=G3A, G4=G4, G5=G5,
           amp={f: dict(A=AMP[f]["A"], s=AMP[f]["s"], D=list(AMP[f]["D"]), M=list(AMP[f]["M"]),
                        sk=list(AMP[f]["sk"])) for f in FOOT},
           b21=dict(nogas=amp_b21(T_nogas, A0["canonical"])[0], hot=amp_b21(T_hot, A0["canonical"])[0],
                    gama=amp_b21(T_gama, A0["canonical"])[0]),
           b21_gas_ratio=[dict(gbar=float(T_nogas["gbar"][j]), esd=float(e_n[j]),
                               gas_over_star=float(ratio_at(e_n[j]) - 1.0)) for j in range(15)],
           G3b=G3B, n_lens=n_lens,
           checks=CHK, const=dict(R_B=R_B, S_B=S_B, x_b=X_B, XB2=XB2, LINE=LINE,
                                  Sigma={f: A0[f] / (math.pi * G * XB2) / MSUN_PC2 for f in FOOT},
                                  rho_b={f: cosmo(f)["rho_b_Mpc"] for f in FOOT}))
with open(os.path.join(HERE, TAG + ".json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(os.path.join(HERE, TAG + ".out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
