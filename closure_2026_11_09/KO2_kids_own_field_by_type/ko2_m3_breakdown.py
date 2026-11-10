#!/usr/bin/env python3
"""KO2 M3 breakdown (POST HOC, beyond AMENDMENT_A4; reported only): why M3 (late WG x 0.4 in bins 0-6) does not move R_ext(late).
Prints, with and without the mutation, the late classes' centre, inner and ext amplitudes and the weighted numerator and denominator
of R_ext in the primary and untied designs (canonical footing; alt scales identically), and the late lenses' model and data in bins 0-6.
Machinery copied from ko2_formB.py (itself copied from ko2.py).  Run: KO2_CACHE=<dir> python3 ko2_m3_breakdown.py -> ko2_m3_breakdown.out
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
P("KO2 M3 breakdown (post hoc, beyond A4)")
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

OWNF = None
XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
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

f = "canonical"; fi = 0
own = own_cells_all(fi)
W = np.array([float((WW[CLS == c, :NB] * own[CLS == c].sum(2) ** 2).sum()) for c in range(4)]); Wl = W[:2] / W[:2].sum()
N = np.zeros((NPAT, NBASE, NBASE)); vD = np.zeros((NPAT, NBASE)); vM3 = np.zeros((NPAT, NBASE))
WGM3 = WG[:, :NB].copy(); WGM3[np.ix_(typ == 0, np.arange(7))] *= 0.4
for c0 in range(0, NL, 5000):
    ids = np.arange(c0, min(c0 + 5000, NL)); n = len(ids); x = np.zeros((n, NB, NBASE))
    for c in range(4):
        m = CLS[ids] == c; x[m, :, 4 * c:4 * c + 4] = own[ids][m]
    x[:, :, 16:] = read_X(fi, c0, n); ww = WW[ids, :NB]
    oh = sparse.csr_matrix((np.ones(n), (patch[ids], np.arange(n))), shape=(NPAT, n))
    N += (oh @ np.einsum("nb,nbk,nbl->nkl", ww, x, x, optimize=True).reshape(n, -1)).reshape(NPAT, NBASE, NBASE)
    vD += oh @ np.einsum("nb,nbk->nk", 4 * G * WG[ids, :NB] * (ww > 0), x)
    vM3 += oh @ np.einsum("nb,nbk->nk", 4 * G * WGM3[ids] * (ww > 0), x)
late_out = (typ == 0)[:, None] & (np.arange(NB) < 7)[None, :]
D06 = float((4 * G * WG[:, :NB] * late_out).sum()); D06m = float((4 * G * WGM3 * late_out).sum())
P(f"late lenses, bins 0-6: sum 4 G WG {D06:.4e} -> {D06m:.4e} under M3 (ratio {D06m / D06:.3f})")
for kind in ("primary", "untied"):
    T, names = design(kind)
    for tag, v in (("data", vD), ("M3", vM3)):
        a, al = solve(N, v, T)
        rows = []
        for c in (0, 1):
            rows.append(" / ".join(f"{a[names.index((c, B))]:+.3f}" for B in ("centre", "inner", "ext")))
        num = float(Wl @ a[[names.index((c, "ext")) for c in (0, 1)]]); den = float(Wl @ a[[names.index((c, "inner")) for c in (0, 1)]])
        # model of the late lenses in bins 0-6 from the late own columns only (centre + inner + ext), relative to the data sum
        P(f"  {kind:8s} {tag:4s}: late-low c/in/ext {rows[0]};  late-high {rows[1]};  weighted ext {num:+.3f}, inner {den:+.3f}, R_ext {num / den:+.3f}")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "ko2_m3_breakdown.out"), "w").write("\n".join(OUT) + "\n")
