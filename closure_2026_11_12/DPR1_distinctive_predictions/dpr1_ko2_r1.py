#!/usr/bin/env python3
"""DPR1: rival R1 (the record's cold reference halo) planted through KO2's own-field machinery.  TEST lane; adopts nothing.

Copied from closure_2026_11_09/KO2_kids_own_field_by_type/ko2_formB.py (KO2 amendment A3, ece364d804), with ONE change: form B's
per-halo profile (PD1's law phantom truncated at R_trunc) is replaced by the record's cold reference halo, FRZ1's rule as
re-written in closure_2026_11_10/SRH1R_blind_lensing_regrade/srh1r_model.py (ref_halo, layout case "ref"): the same total cold
mass as form B (PD1's share X M_b), laid out as an NFW profile with the record's concentration relation, truncated at the
turnaround radius, at the median lens redshift.  Every lens and every pool neighbour follows the rule; the planted sums are
fitted with KO2's primary, secondary and untied designs exactly as form B's were.  KO2's data, designs and weights unchanged.

Run (after ko2.py, same cache):  KO2_CACHE=<dir> KO2_JSON=<ko2.json> python3 dpr1_ko2_r1.py -> dpr1_ko2_r1[_tag].json / .out
Brackets: DPR1_CFAC (concentration factor, default 1), DPR1_ZREF (default median lens z), DPR1_TAG (output suffix).
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
if sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    os.environ["MallocMediumZone"] = "0"; os.environ["MallocLargeCache"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)
import json, math, time, resource
import numpy as np
from scipy.spatial import cKDTree
from scipy import sparse
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
PD1DIR = os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust")
CACHE = os.environ.get("KO2_CACHE", "")
if not CACHE: sys.exit("set KO2_CACHE (the cache ko2.py wrote)")
T0 = time.time(); OUT = []
def mem(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20 if sys.platform == "darwin" else resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 10
def P(s=""):
    print(s, flush=True); OUT.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

# ================================================================== PD1's rule, copied verbatim from pd1.py (lines 24-111)
G_, MS, PC = 6.6743e-11, 1.98892e30, 3.0857e16; MPC = 1e6 * PC; KPC = 1e3 * PC
A0_PD1 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
def glaw_pd1(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
def Mph(r, Mb, a0):
    if r <= 0: return 0.0
    y = G_ * Mb / r ** 2 / a0; return Mb * (math.sqrt(0.25 + 1.0 / y) - 0.5)
class BG:
    def __init__(s, OB, OD, h, OR_h2=4.15e-5):
        s.OB, s.OD, s.h = OB, OD, h; s.R = OD / OB; s.Om = (OB + OD) / h ** 2; s.Orr = OR_h2 / h ** 2; s.OL = 1 - s.Om - s.Orr
        s.H0s = 100 * h * 1e3 / MPC; s.RHOC = 3 * s.H0s ** 2 / (8 * math.pi * G_); s.RHO_M0 = s.Om * s.RHOC; s.RHO_D0 = OD / h ** 2 * s.RHOC
    def Hs(s, a): return s.H0s * math.sqrt(s.Orr / a ** 4 + s.Om / a ** 3 + s.OL)
    def shell(s, xL, dM, a0, a_end=1.0):
        AI = 1 / 1001.0
        def rhs(t, y):
            a, r, v = y; acc = -(4 * math.pi * G_ / 3) * (s.RHO_M0 / a ** 3 + 2 * s.Orr * s.RHOC / a ** 4 - 2 * s.OL * s.RHOC) * r; gN = G_ * dM / r ** 2
            acc -= (float(glaw_pd1(gN, a0)) if a0 > 0 else gN); return [a * s.Hs(a), v, acc]
        def turn(t, y): return y[2]
        turn.terminal, turn.direction = True, -1
        def end(t, y): return y[0] - a_end
        end.terminal = True
        r0 = xL * AI; so = solve_ivp(rhs, (0, 3e18), [AI, r0, s.Hs(AI) * r0], events=(turn, end), rtol=1e-9, atol=[1e-12, r0 * 1e-12, 1e-6], method="DOP853")
        if so.t_events[0].size: return "early", so.y_events[0][0]
        return "late", so.y_events[1][0] if so.t_events[1].size else so.y[:, -1]
    def r_ta(s, dM, a0, a_end=1.0):
        lo, hi = math.log(1e-6 * MPC), math.log(1e3 * MPC)
        for _ in range(60):
            mid = 0.5 * (lo + hi); kind, st = s.shell(math.exp(mid), dM, a0, a_end)
            if kind == "early": lo = mid
            else: hi = mid
            if hi - lo < 1e-7: break
        kind, st = s.shell(math.exp(hi), dM, a0, a_end); return float(st[1]), math.exp(hi)
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
def footing_bg(f): th = Q15["footings"][f]["main"]["theta"]; return BG(th["omega_b"], th["omega_d"], float(Q15["footings"][f]["main"]["h"]))
LM = np.arange(7.0, 15.001, 0.25)
def share_table(B, a0, z, share_mult=1.0, rule="ta"):
    aE = 1 / (1 + z); rows = []
    for m in LM:
        Mb = 10 ** m * MS; rms, xL = B.r_ta(Mb * (1 + B.R), 0.0, aE)
        sh = B.RHO_D0 * 4 * math.pi / 3 * xL ** 3 + B.R * Mb; am_ok = None
        sh *= share_mult; mp = Mph(rms, Mb, a0)
        rt = brentq(lambda r: Mph(r, Mb, a0) - sh, 1e-6 * KPC, rms) if mp > sh else rms; left = max(0.0, sh - mp)
        rows.append(dict(AM_in_range=am_ok, logMb=float(m), R_ms_Mpc=rms / MPC, x_ta_Mpc=xL / MPC, share_over_Mb=sh / Mb, Mph_Rms_over_share=mp / sh, R_trunc_kpc=rt / KPC, leftover_over_Mb=left / Mb))
    return rows
def interp(tab, key, m): return float(10 ** np.interp(m, [r["logMb"] for r in tab], np.log10(np.maximum([r[key] for r in tab], 1e-300))))
def halo_of(tab, Mb_sun, trunc=True):
    m = math.log10(Mb_sun); rms = interp(tab, "R_ms_Mpc", m) * MPC
    if not trunc: return math.inf, rms, 0.0
    rt = interp(tab, "R_trunc_kpc", m) * KPC; lm = np.array([r["logMb"] for r in tab]); lv = np.array([r["leftover_over_Mb"] for r in tab])
    j = int(np.clip(np.searchsorted(lm, m), 1, len(lm) - 1)); left = (interp(tab, "leftover_over_Mb", m) * Mb_sun * MS) if (lv[j - 1] > 0 and lv[j] > 0) else 0.0
    return rt, rms, left
# ================================================================== end of the copy

FOOT = ("canonical", "alt"); NF = 2
P("DPR1 R1 plant through KO2.  PD1's z = 0 share tables, transcribed (they set the total cold mass)")
TABS = {}
PD1J = json.load(open(os.path.join(PD1DIR, "pd1.json")))
ka_b1 = 0.0
for f in FOOT:
    TABS[f] = share_table(footing_bg(f), A0_PD1[f], 0.0)
    ref = PD1J[f]["share_tables"]["z0.0"]
    for a, b in zip(TABS[f], ref):
        for k in ("share_over_Mb", "R_ms_Mpc", "R_trunc_kpc", "leftover_over_Mb"):
            if b[k] != 0 or a[k] != 0:
                ka_b1 = max(ka_b1, abs(a[k] - b[k]) / max(abs(b[k]), 1e-300))
    P(f"  {f}: share {TABS[f][0]['share_over_Mb']:.3f} M_b; first node with a leftover log M_b {min(r['logMb'] for r in TABS[f] if r['leftover_over_Mb'] > 0):.2f}  [{time.time() - T0:.0f} s]")
check("KA-B1 transcribed share tables equal pd1.json's z = 0 tables (share, R_ms, R_trunc, leftover) to 1e-6", ka_b1 < 1e-6, f"max relative deviation {ka_b1:.1e}")
def halo_vec(tab, Mb_sun):
    """vectorised halo_of: R_trunc (m), R_ms (m), leftover / M_b."""
    m = np.log10(Mb_sun); lm = np.array([r["logMb"] for r in tab])
    li = lambda key: 10 ** np.interp(m, lm, np.log10(np.maximum([r[key] for r in tab], 1e-300)))
    rms = li("R_ms_Mpc") * MPC; rt = li("R_trunc_kpc") * KPC; lv = np.array([r["leftover_over_Mb"] for r in tab])
    j = np.clip(np.searchsorted(lm, m), 1, len(lm) - 1); has = (lv[j - 1] > 0) & (lv[j] > 0)
    lam = np.where(has, li("leftover_over_Mb"), 0.0)
    return rt, rms, lam
rng = np.random.default_rng(52); mt = 10 ** rng.uniform(7.5, 13.5, 1000); kv = 0.0
for f in FOOT:
    rt, rms, lam = halo_vec(TABS[f], mt)
    for i in range(1000):
        a, b, c = halo_of(TABS[f], mt[i])
        kv = max(kv, abs(rt[i] / a - 1), abs(rms[i] / b - 1), abs(lam[i] * mt[i] * MS - c) / max(c, 1e-300) if c > 0 else lam[i])
check("KA-B1b vectorised halo_of equals PD1's halo_of at 1,000 masses", kv < 1e-12, f"max deviation {kv:.1e}")

# ================================================================== KO2's machinery (copied from ko2.py)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
NPAT = 50; NB = 13; W_PRI = 230.0; REACH = 2.0; DMIN = 0.005; NSHUF = 5
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0): return nu(g / a0) * g
def Qf(g, a0): return g / 2 + np.sqrt(g) / 2 * np.sqrt(g + 4 * a0) + 2 * a0 * np.arcsinh(np.sqrt(g / (4 * a0)))
def Sf(g, a0): return Qf(g, a0) - glaw(g, a0)
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def mgal_of(logMs): return 10 ** logMs * (1 + 10 ** (-0.69 * logMs + 6.63))
from astropy.io import fits
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); bcat = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
r_ = np.array(bcat["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(bcat["zphot_ANNz2"], dtype="f8")
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
ra_ = np.array(bcat["RAJ2000"], dtype="f8"); dec_ = np.array(bcat["DECJ2000"], dtype="f8")
del bcat, Lp; HB.close(); HL.close(); del HB, HL
ln = np.load(os.path.join(DATA, "lr_lenses.npz")); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WW, WG, EDGES = PL["WW"], PL["WG"], PL["gbar_edges"]; WX = np.load(os.path.join(DATA, "cfg116_perlens.npz"))["WX"]
patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
e0 = EDGES[0]; e13 = EDGES[13]
RH = np.minimum(3.0, np.sqrt(G * Mg / e0) / Mpc); DMAX = RH + REACH; DA = chil / (1 + zl)
RE = np.minimum(np.sqrt(G * Mg[:, None] / EDGES[None, :14]) / Mpc, 3.0)
nb = (r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7); inb = np.where(nb)[0]
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]
MbN = mgal_of(logMN)                                               # M_b of every pool object, Msun
ellN = np.sqrt(G * MbN * Msun / e0) / Mpc
kp = np.ascontiguousarray(np.c_[ra_[inb], dec_[inb]]).view(np.dtype((np.void, 16))).ravel()
kl = np.ascontiguousarray(np.c_[ln["ra"], ln["dec"]]).view(np.dtype((np.void, 16))).ravel()
okp = np.argsort(kp, kind="stable"); pos_ = np.minimum(np.searchsorted(kp[okp], kl), len(kp) - 1)
selfN = np.where(kp[okp][pos_] == kl, okp[pos_], -1); assert np.all(selfN >= 0)
del kp, kl, okp, pos_, r_, z_, logM_, ra_, dec_, nb
treeN = cKDTree(xN); xL = xN[selfN]
P(f"  pool {len(inb):,}; max log M_b of the pool {np.log10(MbN).max():.2f}  [{time.time() - T0:.0f} s, peak {mem():.0f} MB]")

# ------------------------------------------------------------------ R1: the record's cold reference halo (FRZ1's rule as re-written in SRH1R's srh1r_model.py)
# The same total cold mass as form B (PD1's share X M_b from TABS), laid out as an NFW profile truncated at the turnaround radius
# (srh1r_model.ref_halo, copied).  Lensing in the same convention as the law and form B: 4 G DeltaSigma = G M(<R) / R^2, M 3D.
XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
h_r, OMB_r, OMC_r = 0.6736, 0.02237, 0.1200
Om_r = (OMB_r + OMC_r) / h_r ** 2; FB_r = OMB_r / (OMB_r + OMC_r); RHO_M_r = Om_r * 2.77536627e11
CFAC = float(os.environ.get("DPR1_CFAC", "1.0"))                    # concentration bracket (1.0 = the record's relation)
ZREF = os.environ.get("DPR1_ZREF", "median")                        # "median" = median lens redshift; else a number
def m_nfw(x): return np.log1p(x) - x / (1 + x)
def Omz_r(z): return Om_r * (1 + z) ** 3 / (Om_r * (1 + z) ** 3 + 1 - Om_r)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz_r(z)) / (1 - Om_r)
_REF = {}
def ref_halo(Mta, z):
    """srh1r_model.ref_halo (copied; CFAC multiplies c): r_s, r_ta in physical kpc for turnaround mass Mta (Msun) at z."""
    key = (round(float(z), 6), CFAC)
    if key not in _REF:
        lM = np.arange(6.0, 17.0001, 0.01); M = 10 ** lM
        c = CFAC * 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
        r2 = (3 * M / (4 * math.pi * 200 * RHO_M_r)) ** (1 / 3)
        tgt = dta_of(z) / 200.0; xl, xh = np.full(len(M), 1.0), np.full(len(M), 200.0)
        for _ in range(80):
            xm = 0.5 * (xl + xh); big = m_nfw(c * xm) / m_nfw(c) / xm ** 3 > tgt
            xl = np.where(big, xm, xl); xh = np.where(big, xh, xm)
        xta = 0.5 * (xl + xh); MtaG = M * m_nfw(c * xta) / m_nfw(c) / h_r
        f_ = 1e3 / (h_r * (1 + z)); _REF[key] = (np.log10(MtaG), np.log10(r2 / c * f_), np.log10(xta * r2 * f_))
    a, b, d = _REF[key]; l = np.log10(np.asarray(Mta, float))
    return 10 ** np.interp(l, a, b), 10 ** np.interp(l, a, d)
Z_R1 = float(np.median(zl)) if ZREF == "median" else float(ZREF)
def share_vec(f, Mb_sun):
    m = np.log10(Mb_sun); lm = np.array([r["logMb"] for r in TABS[f]])
    return np.interp(m, lm, [r["share_over_Mb"] for r in TABS[f]])
def params(f, Mb_sun):
    """(x_s, x_ta, A) in units l = sqrt(G M_b / e0): cold mass M_c(<r) = A M_b m_nfw(min(r, r_ta) / r_s)."""
    Mb_sun = np.asarray(Mb_sun, float); X = share_vec(f, Mb_sun)
    rs, rta = ref_halo(X * Mb_sun / (1 - FB_r), Z_R1)               # kpc
    ell = np.sqrt(G * Mb_sun * Msun / e0) / (Mpc / 1e3)              # kpc
    return rs / ell, rta / ell, X / m_nfw(rta / rs)
def m_of(x, xs, xta, A): return 1.0 + A * m_nfw(np.minimum(x, xta) / xs)
def Ic_exact(x, xs, xta, A, n=400):
    """cold part of 4 G Sigma_bar / e0 = int_x^inf 2 m_c(x') / x'^3 dx' (direct Gauss-Legendre in ln x'), for checks."""
    x = np.atleast_1d(np.asarray(x, float)); out = A * m_nfw(xta / xs) / np.maximum(x, xta) ** 2
    XQ_, WQ_ = np.polynomial.legendre.leggauss(n)
    for i, xi in enumerate(x):
        if xi >= xta: continue
        a_, b_ = math.log(xi), math.log(xta); u = (a_ + b_) / 2 + (b_ - a_) / 2 * XQ_; xx = np.exp(u)
        out[i] += (b_ - a_) / 2 * float((2 * A * m_nfw(xx / xs) / xx ** 2 * WQ_).sum())
    return out
class Prof:
    """one halo's profile, tabulated on a fine log grid for the cold Sigma_bar integral."""
    def __init__(s, xs, xta, A):
        s.xs, s.xta, s.A = float(xs), float(xta), float(A)
        s.lg = np.linspace(math.log(1e-5), math.log(s.xta), 4001); xx = np.exp(s.lg)
        fx = 2 * s.A * m_nfw(xx / s.xs) / xx ** 2                    # integrand in d ln x
        cum = np.concatenate([[0.0], np.cumsum((fx[1:] + fx[:-1]) / 2 * np.diff(s.lg))])
        s.Itab = (cum[-1] - cum) + s.A * m_nfw(s.xta / s.xs) / s.xta ** 2
    def Ic(s, x):
        x = np.asarray(x, float); xin = np.clip(x, 1e-5, s.xta)
        v = np.interp(np.log(xin), s.lg, s.Itab)
        return np.where(x >= s.xta, s.A * m_nfw(s.xta / s.xs) / np.maximum(x, 1e-300) ** 2, v)
    def sB(s, x):
        """4 G Sigma / e0 (cold part; the baryon point has Sigma = 0 off-centre in this convention)."""
        x = np.asarray(x, float)
        return np.where(x < s.xta, s.Ic(x) - s.A * m_nfw(np.minimum(x, s.xta) / s.xs) / np.maximum(x, 1e-300) ** 2, 0.0)
    def FB_true(s, x):
        """4 M_2D(<x) / M_b = pi m(x) + pi x^2 s(x)."""
        x = np.asarray(x, float); return math.pi * m_of(x, s.xs, s.xta, s.A) + math.pi * x * x * s.sB(x)
X13 = math.sqrt(e0 / e13)
def mc_prof(p): return float(p.FB_true(np.array([X13]))[0])
def FBx(x, p): return p.FB_true(np.maximum(x, X13)) - mc_prof(p)
NR, ND = 801, 561
LNR = np.linspace(math.log(1e-3), math.log(60.0), NR); LND = np.linspace(math.log(1e-3), math.log(60.0), ND); DLR = LNR[1] - LNR[0]; DLD = LND[1] - LND[0]
XQ, WQ = np.polynomial.legendre.leggauss(48); TH = (XQ + 1) * math.pi / 2; WTH = WQ * math.pi / 2
def m_prof(r, delta, p):
    m = np.zeros_like(r)
    full = r > delta
    if full.any(): m[full] = FBx(r[full] - delta, p)
    lo = np.maximum(np.abs(r - delta), X13); hi = np.minimum(r + delta, p.xta); okp = hi > lo
    if okp.any():
        a, b = lo[okp][:, None], hi[okp][:, None]
        x = (a + b) / 2 - (b - a) / 2 * np.cos(TH)[None, :]; jac = (b - a) / 2 * np.sin(TH)[None, :]
        arg = np.clip((x * x + delta * delta - r[okp][:, None] ** 2) / (2 * x * delta), -1.0, 1.0)
        m[okp] += (2 * math.pi * x * p.sB(x) * (np.arccos(arg) / math.pi) * jac * WTH[None, :]).sum(1)
    return m
def build_table(p):
    T = np.zeros((NR, ND)); r = np.exp(LNR)
    for jd, dl in enumerate(np.exp(LND)):
        m = m_prof(r, dl, p)
        T[:, jd] = np.concatenate([[0.0], np.cumsum((m[1:] + m[:-1]) * DLR)]) - m
    return T
def lookup(T, r, j0, h):
    t = np.clip((np.log(np.maximum(r, 1e-300)) - LNR[0]) / DLR, 0.0, NR - 1 - 1e-9); i0 = t.astype(np.int64); f = t - i0
    Tf = T.ravel(); base = i0 * ND + j0
    return Tf[base] * (1 - f) * (1 - h) + Tf[base + ND] * f * (1 - h) + Tf[base + 1] * (1 - f) * h + Tf[base + ND + 1] * f * h
def dindex(delta):
    t = np.clip((np.log(np.maximum(delta, 1e-300)) - LND[0]) / DLD, 0.0, ND - 1 - 1e-9); j0 = t.astype(np.int64); return j0, t - j0
def cell_kernel(T, rlo, rhi, delta):
    j0, h = dindex(delta)
    return (e0 / math.pi) * (lookup(T, rhi, j0, h) - lookup(T, rlo, j0, h)) / (rhi ** 2 - rlo ** 2)
def point_cell(mc, rlo, rhi, delta):
    with np.errstate(divide="ignore", invalid="ignore"):
        Jh = np.where(rhi > delta, 2 * np.log(rhi / delta) - 1, 0.0); Jl = np.where(rlo > delta, 2 * np.log(rlo / delta) - 1, 0.0)
    return (e0 / math.pi) * mc * (Jh - Jl) / (rhi ** 2 - rlo ** 2)

P(f"\nR1 reference: z_ref {Z_R1:.4f}, concentration factor {CFAC:.3f}")
DSTEP = float(os.environ.get("DPR1_DSTEP", "0.1"))
NODES, TBL, MCNODE = {}, {}, {}
lmin = float(min(np.log10(MbN).min(), np.log10(ln["Mgal"]).min())) - 0.01; lmax = float(max(np.log10(MbN).max(), np.log10(ln["Mgal"]).max(), 12.35)) + 0.01   # 12.35 covers KA-R3's draws, as KO2's form-B nodes do
ka_r1 = {}
for fi, f in enumerate(FOOT):
    nodes = np.arange(math.floor(lmin / DSTEP) * DSTEP, lmax + DSTEP, DSTEP)
    NODES[f] = dict(nodes=nodes)
    prof = [Prof(*[float(v[0]) for v in params(f, np.array([10 ** m]))]) for m in nodes]
    MCNODE[f] = np.array([mc_prof(p) for p in prof])
    # KA-R1: the tabulated cold Sigma_bar integral against direct quadrature, every node, 20 radii
    dev = 0.0
    for p in prof[::3]:
        xx = np.exp(np.linspace(math.log(X13), math.log(1.5 * p.xta), 20))
        ex = Ic_exact(xx, p.xs, p.xta, p.A); dev = max(dev, float(np.max(np.abs(p.Ic(xx) - ex) / np.maximum(ex, 1e-300))))
    ka_r1[f] = dev
    TBL[f] = [build_table(p) for p in prof]
    mid = prof[len(prof) // 2]
    P(f"  {f}: {len(nodes)} R1 tables built (log M_b {nodes[0]:.2f} .. {nodes[-1]:.2f}, step {DSTEP}); e.g. log M_b {nodes[len(nodes)//2]:.2f}: "
      f"x_s {mid.xs:.3f}, x_ta {mid.xta:.3f}, A {mid.A:.3f}  [{time.time() - T0:.0f} s, peak {mem():.0f} MB]")
check("KA-R1 tabulated cold Sigma_bar equals direct quadrature to 1e-4 (relative)", all(v < 1e-4 for v in ka_r1.values()), "; ".join(f"{f}: {v:.1e}" for f, v in ka_r1.items()))
def node_weights(f, logm):
    nd = NODES[f]["nodes"]; k = np.clip(np.searchsorted(nd, logm) - 1, 0, len(nd) - 2); w = np.clip((logm - nd[k]) / (nd[k + 1] - nd[k]), 0.0, 1.0)
    return k, k + 1, w
def mc_vec(f, Mb_sun): return np.interp(np.log10(Mb_sun), NODES[f]["nodes"], MCNODE[f])

# ------------------------------------------------------------------ KA-R3: node-interpolated R1 kernels against direct quadrature about the lens
P("\nKA-R3: R1 kernels")
def ref_prof(p, rlo, rhi, delta):
    R = np.concatenate([np.exp(np.linspace(math.log(1e-4 * rhi), math.log(rlo), 1600))[:-1], np.exp(np.linspace(math.log(rlo), math.log(rhi), 401))])
    psi = (np.arange(4096) + 0.5) * 2 * math.pi / 4096; cps = np.cos(psi); C = np.zeros(len(R))
    for i0 in range(0, len(R), 100):
        Rr = R[i0:i0 + 100][:, None]; X = np.sqrt(np.maximum(Rr * Rr + delta * delta - 2 * Rr * delta * cps[None, :], 1e-300))
        C[i0:i0 + 100] = np.where(X >= X13, p.sB(X), 0.0).mean(1)
    lnR = np.log(R); fR = C * 2 * math.pi * R * R
    M = C[0] * math.pi * R[0] ** 2 + np.concatenate([[0.0], np.cumsum((fR[1:] + fR[:-1]) / 2 * np.diff(lnR))]); k0 = 1599
    g2 = 2 * M[k0:]; I = float(((g2[1:] + g2[:-1]) / 2 * np.diff(lnR[k0:])).sum())
    ext = (e0 / math.pi) * (I - (M[-1] - M[k0])) / (rhi ** 2 - rlo ** 2)
    def Jp(r): return 2 * math.log(r / delta) - 1 if r > delta else 0.0
    pt = (e0 / math.pi) * mc_prof(p) * (Jp(rhi) - Jp(rlo)) / (rhi ** 2 - rlo ** 2)
    return ext + pt
rng = np.random.default_rng(53); cfg = []
for i in range(300):
    li = rng.integers(NL); b = int(rng.integers(NB)); lMj = rng.uniform(8.0, 12.3)
    ellj = math.sqrt(G * mgal_of(lMj) * Msun / e0) / Mpc; rhi, rlo = RE[li, b], RE[li, b + 1]
    if rhi <= rlo * 1.0001: rhi, rlo = RE[li, 4], RE[li, 5]
    d = math.exp(rng.uniform(math.log(0.005), math.log(DMAX[li]))); cfg.append((lMj, rlo / ellj, rhi / ellj, d / ellj))
kr3 = {}
for fi, f in enumerate(FOOT):
    v3 = []
    for lMj, rl, rh, dl in cfg:
        logmb = math.log10(mgal_of(lMj)); a_, b_, w_ = node_weights(f, np.array([logmb]))
        kt = float((1 - w_[0]) * cell_kernel(TBL[f][a_[0]], np.array([rl]), np.array([rh]), np.array([dl]))[0] + w_[0] * cell_kernel(TBL[f][b_[0]], np.array([rl]), np.array([rh]), np.array([dl]))[0])
        kt += float(point_cell(float(mc_vec(f, np.array([10 ** logmb]))[0]), np.array([rl]), np.array([rh]), np.array([dl]))[0])
        p = Prof(*[float(v[0]) for v in params(f, np.array([10 ** logmb]))])
        v3.append((kt, ref_prof(p, rl, rh, dl)))
    v3 = np.array(v3); mx = np.max(np.abs(v3[:, 1])); kr3[f] = (int((np.abs(v3[:, 0] - v3[:, 1]) > 0.01 * np.abs(v3[:, 1]) + 0.003 * mx).sum()), float(np.max(np.abs(v3[:, 0] - v3[:, 1])) / mx))
check("KA-R3 R1 kernels (node-interpolated in mass) against direct quadrature about the lens (300 configurations, masses 10^8-10^12.3), KO2's KA-B3 tolerance",
      all(v[0] == 0 for v in kr3.values()), "; ".join(f"{f}: {v[0]} outside, max {v[1]:.1e} of max" for f, v in kr3.items()))
P(f"  [{time.time() - T0:.0f} s, peak {mem():.0f} MB]")
if os.environ.get("KO2B_STAGE") == "kernels":
    sys.exit(0)

# ------------------------------------------------------------------ own R1 cells (3D mass, exact per lens)
def own_B(fi):
    f = FOOT[fi]; out = np.zeros((NL, NB))
    xs, xta, A = params(f, ln["Mgal"]); ell = np.sqrt(G * Mg / e0)       # metres
    rs, rta = xs * ell, xta * ell
    for b in range(NB):
        lo = np.sqrt(G * Mg / EDGES[b + 1]); hi = np.minimum(np.sqrt(G * Mg / EDGES[b]), 3.0 * Mpc); ok = hi > lo
        acc = np.zeros(NL)
        for (p_, q_) in ((lo, np.clip(rta, lo, hi)), (np.clip(rta, lo, hi), hi)):
            t = p_[:, None] ** 2 + (q_ ** 2 - p_ ** 2)[:, None] * (XG[None, :] + 1) / 2; R = np.sqrt(t)
            M = Mg[:, None] * (1 + A[:, None] * m_nfw(np.minimum(R, rta[:, None]) / rs[:, None]))
            acc += (G * M / t * WGL[None, :]).sum(1) / 2 * (q_ ** 2 - p_ ** 2)
        out[:, b] = np.where(ok, acc / np.where(ok, hi ** 2 - lo ** 2, 1.0), 0.0)
    return out
# KA-R2: zero cold mass gives the bare point mass in every own cell (G M_b / R^2 averaged over the cell)
def own_point(fi):
    out = np.zeros((NL, NB))
    for b in range(NB):
        lo2 = G * Mg / EDGES[b + 1]; hi2 = np.minimum(G * Mg / EDGES[b], R3); ok = hi2 > lo2
        out[:, b] = np.where(ok, G * Mg * np.log(hi2 / np.where(ok, lo2, 1.0)) / np.where(ok, hi2 - lo2, 1.0), 0.0)
    return out
OWNB = {f: own_B(fi) for fi, f in enumerate(FOOT)}
_A_save = None
def _own_zero(fi):
    f = FOOT[fi]; out = np.zeros((NL, NB))
    for b in range(NB):
        lo = np.sqrt(G * Mg / EDGES[b + 1]); hi = np.minimum(np.sqrt(G * Mg / EDGES[b]), 3.0 * Mpc); ok = hi > lo
        t = lo[:, None] ** 2 + (hi ** 2 - lo ** 2)[:, None] * (XG[None, :] + 1) / 2
        out[:, b] = np.where(ok, (G * Mg[:, None] / t * WGL[None, :]).sum(1) / 2, 0.0)
    return out
kr2 = max(float(np.max(np.abs(_own_zero(fi) - own_point(fi)) / np.maximum(own_point(fi), 1e-300) * (own_point(fi) > 0))) for fi in range(NF))
check("KA-R2 own-cell quadrature of a bare point mass equals the closed form to 1e-6", kr2 < 1e-6, f"max relative deviation {kr2:.1e}")
# ------------------------------------------------------------------ neighbour form-B sums (real - mean of the five shuffles, as the main columns)
def chunk_B(ids, qx, qself, fi):
    f = FOOT[fi]; n = len(ids); out = np.zeros((n, NB))
    chord = 2 * np.sin(DMAX[ids] * (1 + zl[ids]) / chil[ids] / 2)
    lists = treeN.query_ball_point(qx, r=chord)
    c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=n); tot = int(c.sum())
    if tot == 0: return out
    li = np.repeat(np.arange(n), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot); del lists
    gl = ids[li]; dchi = np.abs(chiN[j] - chil[gl]); keep = (j != qself[li]) & (dchi < W_PRI)
    li, j, gl = li[keep], j[keep], gl[keep]
    d = 2 * np.arcsin(np.minimum(np.linalg.norm(xN[j] - qx[li], axis=1) / 2, 1.0)) * DA[gl]
    keep = (d >= DMIN) & (d < DMAX[gl]); li, j, gl, d = li[keep], j[keep], gl[keep], d[keep]
    if len(li) == 0: return out
    ell = ellN[j]; delta = d / ell; REl = RE[gl]
    ka, kb, w = node_weights(f, np.log10(MbN[j]))
    K = np.zeros((len(li), NB))
    mcj = MCN[f][j]; rp0 = REl[:, 0] / ell
    for b in range(NB):
        rn0 = REl[:, b + 1] / ell; den0 = rp0 ** 2 - rn0 ** 2
        K[:, b] += np.where(den0 > 1e-12 * rp0 ** 2, point_cell(mcj, rn0, rp0, delta), 0.0); rp0 = rn0
    for tix in np.unique(np.concatenate([ka, kb[w > 0]])):
        wt = np.where(ka == tix, 1 - w, 0.0) + np.where((kb == tix) & (w > 0), w, 0.0); s_ = wt > 0
        if not s_.any(): continue
        T = TBL[f][tix]; j0, h = dindex(delta[s_]); el = ell[s_]
        Jp = lookup(T, REl[s_, 0] / el, j0, h); rp = REl[s_, 0] / el
        for b in range(NB):
            rn = REl[s_, b + 1] / el; Jn = lookup(T, rn, j0, h); den = rp ** 2 - rn ** 2
            K[s_, b] += wt[s_] * np.where(den > 1e-12 * rp ** 2, (e0 / math.pi) * (Jp - Jn) / np.where(den > 0, den, 1.0), 0.0)
            Jp, rp = Jn, rn
    for b in range(NB):
        out[:, b] = np.bincount(li, weights=K[:, b], minlength=n)
    return out
perms = [np.random.default_rng(52 + s).permutation(NL) for s in range(NSHUF)]
MCN = {f: mc_vec(f, MbN) for f in FOOT}                                      # each pool object's own centre point
NBB = {f: np.zeros((NL, NB)) for f in FOOT}
P("\nneighbour form-B sums (real positions minus the mean of the five shuffles)")
CH = 1200
for c0 in range(0, NL, CH):
    ids = np.arange(c0, min(c0 + CH, NL))
    for fi, f in enumerate(FOOT):
        real = chunk_B(ids, xL[ids], selfN[ids], fi)
        sh = sum(chunk_B(ids, xL[perms[s][ids]], selfN[perms[s][ids]], fi) for s in range(NSHUF)) / NSHUF
        NBB[f][ids] = real - sh
    if (c0 // CH) % 30 == 0:
        P(f"  lenses {c0 + len(ids):,} / {NL:,}  [{time.time() - T0:.0f} s, peak {mem():.0f} MB]")
del TBL

# ------------------------------------------------------------------ fit the planted sums with KO2's designs (main normal matrix rebuilt from the cache)
OWNF = None
def own_cells_all(fi):
    own = np.zeros((NL, NB, 4)); a0 = A0[FOOT[fi]]
    def bk(g, B):
        if B == 0: return g * Qf(e13, a0) / e13
        g1 = EDGES[{1: 7, 2: 4, 3: 0}[B]]; g2 = EDGES[{1: 13, 2: 7, 3: 4}[B]]
        return np.where(g >= g2, 0.0, np.where(g >= g1, glaw(g, a0) - g * Qf(g2, a0) / g2, g * (Qf(g1, a0) / g1 - Qf(g2, a0) / g2)))
    for c0 in range(0, NL, 20000):
        sl = slice(c0, c0 + 20000); M_ = Mg[sl]
        for b in range(NB):
            t_lo = G * M_ / EDGES[b + 1]; t_hi = np.minimum(G * M_ / EDGES[b], R3); ok = t_hi > t_lo
            t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2; g = G * M_[:, None] / t
            for B in range(4): own[sl, b, B] = np.where(ok, (bk(g, B) * WGL[None, :]).sum(1) / 2, 0.0)
    return own
# classes, exactly as ko2.py (weights only)
urN = None
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HB[1].data
urN = (np.array(Lp["MAG_ABS_u"], dtype="f8") - np.array(Lp["MAG_ABS_r"], dtype="f8"))[inb]; del Lp; HB.close(); del HB
wl = WW[:, :NB].sum(1); THR = {}
for t in (0, 1):
    m = typ == t; o = np.argsort(logMs[m]); lv_ = logMs[m][o]; cw = np.cumsum(wl[m][o]); v = float(lv_[np.searchsorted(cw, 0.5 * cw[-1])])
    THR[t] = 0.5 * (v + float(logMN[logMN > v].min()))
def class_of(logm, ur, giant_ok=True):
    t = (ur > 2.0).astype(np.int64); thr = np.where(t == 1, THR[1], THR[0]); c = 2 * t + (logm >= thr).astype(np.int64)
    return np.where(logm >= 11.0, 4, c) if giant_ok else c
CLS = class_of(logMs, np.where(typ == 1, 3.0, 1.0), giant_ok=False)
NBASE = 41
XFILES = [os.path.join(CACHE, f"ko2_X230_{f}.f32") for f in FOOT]
def read_X(fi, c0, n):
    return np.fromfile(XFILES[fi], dtype=np.float32, count=n * NB * 25, offset=c0 * NB * 25 * 4).reshape(n, NB, 25).astype(np.float64)
def design(kind, closure="continued"):
    cols, names = [], []
    def add(entries, name):
        v = np.zeros(NBASE)
        for e_ in entries: v[e_] += 1.0
        cols.append(v); names.append(name)
    oc = lambda c, B: 4 * c + B; nc = lambda g, B: 16 + 5 * g + B
    if kind == "untied":
        for c in range(4):
            add([oc(c, 0)], (c, "centre")); add([oc(c, 1)], (c, "inner")); add([oc(c, 2), oc(c, 3)], (c, "ext"))
        for g in range(5):
            add([nc(g, 0)], ("nb", g, "centre")); add([nc(g, 1)], ("nb", g, "inner")); add([nc(g, 2), nc(g, 3), nc(g, 4)], ("nb", g, "ext"))
        return np.array(cols).T, names
    for c in range(5):
        o = c < 4
        add(([oc(c, 0)] if o else []) + [nc(c, 0)], (c, "centre")); add(([oc(c, 1)] if o else []) + [nc(c, 1)], (c, "inner"))
        if kind == "primary":
            add(([oc(c, 2), oc(c, 3)] if o else []) + [nc(c, 2), nc(c, 3), nc(c, 4)], (c, "ext"))
        else:
            add(([oc(c, 2)] if o else []) + [nc(c, 2)], (c, "middle")); add(([oc(c, 3)] if o else []) + [nc(c, 3), nc(c, 4)], (c, "outer"))
    return np.array(cols).T, names
def solve(N, v, T):
    Nt, vt = N.sum(0), v.sum(0); M = T.T @ Nt @ T; b = T.T @ vt; sc = 1 / np.sqrt(np.diag(M))
    a = sc * np.linalg.solve(M * sc[:, None] * sc[None, :], b * sc); al = np.zeros((NPAT, T.shape[1]))
    for p in range(NPAT):
        Mp = T.T @ (Nt - N[p]) @ T; bp = T.T @ (vt - v[p]); al[p] = sc * np.linalg.solve(Mp * sc[:, None] * sc[None, :], bp * sc)
    return a, al
def jk(xl): xl = np.asarray(xl); return float(np.sqrt((NPAT - 1) / NPAT * ((xl - xl.mean(0)) ** 2).sum(0)))
RES = dict(lane="DPR1", stage="R1 (cold reference) plant through KO2", source="ko2_formB.py (ece364d804) with the profile replaced", z_ref=Z_R1, cfac=CFAC, checks=CHK, nodes={f: dict((k, (v.tolist() if isinstance(v, np.ndarray) else v)) for k, v in NODES[f].items()) for f in FOOT},
           share_over_Mb={f: TABS[f][0]["share_over_Mb"] for f in FOOT}, foot={})
TYPN = {0: "late", 1: "early"}
for fi, f in enumerate(FOOT):
    own = own_cells_all(fi)
    W = np.array([float((WW[CLS == c, :NB] * own[CLS == c].sum(2) ** 2).sum()) for c in range(4)]); WCL = {0: W[:2] / W[:2].sum(), 1: W[2:] / W[2:].sum()}
    N = np.zeros((NPAT, NBASE, NBASE)); vB = np.zeros((NPAT, NBASE)); vX = np.zeros((NPAT, NBASE)); vD = np.zeros((NPAT, NBASE)); vM3 = np.zeros((NPAT, NBASE))
    WGM3 = WG[:, :NB].copy(); WGM3[np.ix_(typ == 0, np.arange(7))] *= 0.4
    mB = OWNB[f] + NBB[f]
    vL = None
    for c0 in range(0, NL, 5000):
        ids = np.arange(c0, min(c0 + 5000, NL)); n = len(ids); x = np.zeros((n, NB, NBASE))
        for c in range(4):
            m = CLS[ids] == c; x[m, :, 4 * c:4 * c + 4] = own[ids][m]
        x[:, :, 16:] = read_X(fi, c0, n); ww = WW[ids, :NB]
        oh = sparse.csr_matrix((np.ones(n), (patch[ids], np.arange(n))), shape=(NPAT, n))
        N += (oh @ np.einsum("nb,nbk,nbl->nkl", ww, x, x, optimize=True).reshape(n, -1)).reshape(NPAT, NBASE, NBASE)
        vB += oh @ np.einsum("nb,nbk->nk", ww * mB[ids], x)
        vX += oh @ np.einsum("nb,nbk->nk", 4 * G * WX[ids, :NB] * (ww > 0), x)
        vD += oh @ np.einsum("nb,nbk->nk", 4 * G * WG[ids, :NB] * (ww > 0), x)
        vM3 += oh @ np.einsum("nb,nbk->nk", 4 * G * WGM3[ids] * (ww > 0), x)
    vL = N.sum(axis=2)                                              # the law everywhere: every base column at amplitude 1
    F = {}
    for kind, nb_ in (("primary", "ext"), ("secondary", "outer"), ("untied", "ext")):
        T, names = design(kind); F[kind] = {}
        for tag, vv in (("noiseless", vB), ("with WX noise", vB + vX), ("law everywhere, noiseless (KA-B4)", vL), ("data (check against ko2.json)", vD), ("data, M3 (D2)", vM3)):
            a, al = solve(N, vv, T); F[kind][tag] = {}
            for t in (0, 1):
                cs = (2 * t, 2 * t + 1); Wt = WCL[t]
                inum = [names.index((c, nb_)) for c in cs]; iden = [names.index((c, "inner")) for c in cs]
                R = float(Wt @ a[inum]) / float(Wt @ a[iden]); Rl = (al[:, inum] @ Wt) / (al[:, iden] @ Wt)
                per = {f"{['late-low', 'late-high', 'early-low', 'early-high'][c]}": float(a[names.index((c, nb_))] / a[names.index((c, 'inner'))]) for c in cs}
                F[kind][tag][TYPN[t]] = dict(R=R, s=jk(Rl), per_class=per, Rl=Rl)
            P(f"  {f:9s} {kind:9s} {tag:32s}: " + "; ".join(f"{TYPN[t]} R {F[kind][tag][TYPN[t]]['R']:+.3f} +- {F[kind][tag][TYPN[t]]['s']:.3f} "
                                                       f"(classes {', '.join(f'{k} {v:+.2f}' for k, v in F[kind][tag][TYPN[t]]['per_class'].items())})" for t in (0, 1)))
    kb4 = max(abs(F[k]["law everywhere, noiseless (KA-B4)"][t]["R"] - 1) for k in ("primary", "secondary", "untied") for t in ("late", "early"))
    K2 = json.load(open(os.environ.get("KO2_JSON", os.path.join(REPO, "closure_2026_11_09", "KO2_kids_own_field_by_type", "ko2.json"))))["foot"][f]["fits"]
    kb5 = max(abs(F[k]["data (check against ko2.json)"][t]["R"] - K2[{"primary": "primary", "secondary": "secondary", "untied": "B3 untied"}[k]]["R"][t]["R"]) for k in ("primary", "secondary", "untied") for t in ("late", "early"))
    check(f"KA-B5 the rebuilt normal matrix reproduces ko2.json's data readings ({f})", kb5 < 1e-6, f"max |difference| {kb5:.1e}")
    # D1: per-amplitude pulls of the cross-shear fit (primary design)
    Tp, namp = design("primary"); a, al = solve(N, vX, Tp); pulls = a / np.array([jk(al[:, k]) for k in range(len(namp))])
    io = int(np.argmax(np.abs(pulls)))
    D1 = dict(pulls={f"{['late-low', 'late-high', 'early-low', 'early-high', 'giant'][nm[0]]} {nm[1]}": float(pulls[k]) for k, nm in enumerate(namp)},
              max=(f"{['late-low', 'late-high', 'early-low', 'early-high', 'giant'][namp[io][0]]} {namp[io][1]}", float(pulls[io])),
              n_over_2=int((np.abs(pulls) > 2).sum()), n_over_3=int((np.abs(pulls) > 3).sum()))
    P(f"  D1 {f}: cross-shear fit, largest pull {D1['max'][0]} {D1['max'][1]:+.2f}; |pull| > 2: {D1['n_over_2']}, > 3: {D1['n_over_3']} of {len(namp)}")
    # D2: M3 on each design
    D2 = {}
    for k in ("primary", "secondary", "untied"):
        dl = F[k]["data, M3 (D2)"]["late"]["Rl"] - F[k]["data (check against ko2.json)"]["late"]["Rl"]
        d0 = F[k]["data, M3 (D2)"]["late"]["R"] - F[k]["data (check against ko2.json)"]["late"]["R"]; sd = jk(dl)
        D2[k] = dict(change=d0, s=sd, z=d0 / sd, bites=bool(d0 < -2 * sd))
        P(f"  D2 {f} M3 on {k:9s}: R(late) {F[k]['data (check against ko2.json)']['late']['R']:+.3f} -> {F[k]['data, M3 (D2)']['late']['R']:+.3f}; change {d0:+.3f} +- {sd:.3f} ({d0 / sd:+.2f} sigma) -> {'BITES' if d0 < -2 * sd else 'does not bite'}")
    # D3: information shares of each class's ext column in the primary design
    Nt = N.sum(0); D3 = {}
    for c in range(5):
        to = np.zeros(NBASE); tn = np.zeros(NBASE)
        if c < 4: to[[4 * c + 2, 4 * c + 3]] = 1
        tn[[16 + 5 * c + 2, 16 + 5 * c + 3, 16 + 5 * c + 4]] = 1
        Io, In, Ic = float(to @ Nt @ to), float(tn @ Nt @ tn), float(2 * to @ Nt @ tn); It = Io + In + Ic
        D3[['late-low', 'late-high', 'early-low', 'early-high', 'giant'][c]] = dict(own=Io / It, neighbours=In / It, cross=Ic / It)
    P(f"  D3 {f} ext information shares (own / neighbours / cross): " + "; ".join(f"{k} {v['own']:.2f}/{v['neighbours']:.2f}/{v['cross']:+.2f}" for k, v in D3.items()))
    F["D1"], F["D2"], F["D3"] = D1, D2, D3
    check(f"KA-B4 the law planted everywhere is recovered at R = 1 ({f})", kb4 < 1e-6, f"max |R - 1| {kb4:.1e}")
    xs_, xta_, A_ = params(f, ln["Mgal"]); ell_ = np.sqrt(G * Mg / e0) / (Mpc / 1e3)
    F["planted_truth"] = dict(share_over_Mb=TABS[f][0]["share_over_Mb"], z_ref=Z_R1, cfac=CFAC,
                              r_s_kpc_at_class_medians={nm: float(np.median((xs_ * ell_)[CLS == c])) for c, nm in enumerate(["late-low", "late-high", "early-low", "early-high"])},
                              r_ta_kpc_at_class_medians={nm: float(np.median((xta_ * ell_)[CLS == c])) for c, nm in enumerate(["late-low", "late-high", "early-low", "early-high"])})
    RES["foot"][f] = F
    del own
P(f"\nchecks: {sum(CHK.values())} of {len(CHK)} pass;  runtime {time.time() - T0:.0f} s, peak {mem():.0f} MB")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
TAG = os.environ.get("DPR1_TAG", "")
json.dump(clean(RES), open(os.path.join(HERE, f"dpr1_ko2_r1{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"dpr1_ko2_r1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
