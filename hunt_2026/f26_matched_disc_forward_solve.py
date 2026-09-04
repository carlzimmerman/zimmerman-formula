#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f26 -- the matched QUMOND disc forward solve, for every kernel, at the profiled parameters.

WHAT THE LEAD ASKED FOR (two_kernel_orbit_shape_2026/REPORT.md section 6): "a matched AQUAL or QUMOND disk/external-
field forward solve, with a0, distance, inclination and stellar M/L treated consistently", because every kernel
comparison so far (f21, f23, f25, the lead's kernel_comparison.py) applied the SPHERICAL algebraic relation
g = nu(g_bar/a_0) g_bar point by point to DISCS.  For a disc the QUMOND field differs from the algebraic relation by the
curl-field / disc-geometry correction, which is a few to ten per cent in the transition (f16-f18) -- the same size as
the difference between the kernels.  So the algebraic ranking could in principle be an artefact of the geometry.

WHAT THIS FILE DOES.  For each SPARC galaxy and each kernel it
  1. builds the baryonic Newtonian field in the plane from the catalogue components at the kernel's own profiled
     disc M/L (f25: Upsilon_d = 0.50 for nu_RAR, 0.60 for mu_exp and mu_10; bulge 1.4 Upsilon_d),
  2. inverts it to a thick-disc surface density with f18's analytic razor-thin Hankel inversion plus thick-disc polish
     (sech^2, z_0 = 0.1 R_d), and records the inversion residual,
  3. solves QUMOND for that 3-D density with the kernel's nu, on the same Hankel grid (no finite differences), at
     the kernel's profiled a_0 and at +/- 0.15 dex, and forms the disc correction T(R) = log10[g_QUMOND / g_algebraic]
     from the solver's own Newtonian field (so T is the geometry correction and not the inversion error),
  4. applies T to the algebraic prediction on the data, re-profiles a_0 (T interpolated in log a_0), and repeats the
     lead's paired-galaxy resampling on the CORRECTED residuals.
Distance and inclination stay at catalogue values for every kernel -- the same values, which is what a paired
comparison needs; per-galaxy nuisance marginalisation is out of scope and said so.  No external field: SPARC discs
sit at e_N ~ 0.01-0.03 and the data radii have g_bar/a_0 > 0.03 almost everywhere.  Descriptive MSE, no sigma.

Every check can fail.  Cached to f26_forward_cache.npz (delete to recompute).
"""
import os, sys, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning)      # numpy prints absolute paths in its warnings; keep them out of the .out
from scipy.special import j0, j1
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260904)
TWO_PI_G = 2*math.pi*G; PC2 = (3.0857e16)**2
CACHE = os.path.join(HERE, "f26_forward_cache.npz")
t0 = time.time()

# ---------------------------------------------------------------- kernels in QUMOND nu form, y = |g_N|/a_0
YG = np.logspace(-7, 7, 2801); lyg = np.log(YG)
def nu_table(mu):
    out = np.empty_like(YG)
    for i, yy in enumerate(YG):
        out[i] = brentq(lambda x: x*mu(x) - yy, 1e-14, yy + 60.0, xtol=1e-14)/yy if yy < 300 else 1.0
    return out
def mk(tab): return lambda y: np.exp(np.interp(np.log(np.clip(np.asarray(y, float), 1e-7, 1e7)), lyg, tab))
NU = {"nu_rar": lambda y: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-30)))),
      "mu_exp": mk(np.log(nu_table(lambda x: 1.0 - math.exp(-x)))),
      "mu_10": mk(np.log(nu_table(lambda x: x/(1 + x**10)**0.1)))}
PROF = {"nu_rar": (0.50, 8.71e-11), "mu_exp": (0.60, 8.91e-11), "mu_10": (0.60, 1.122e-10)}     # f25 joint optima
DLA = np.array([-0.15, 0.0, 0.15])

# ---------------------------------------------------------------- the Hankel QUMOND solver (f18's class, nu as an argument)
def _trapw(x):
    w = np.empty_like(x); w[1:-1] = 0.5*(x[2:] - x[:-2]); w[0] = 0.5*(x[1]-x[0]); w[-1] = 0.5*(x[-1]-x[-2]); return w
class Grid:
    def __init__(self, Rmax, Rd, NR=1000, Nz=151, z_soft=None):
        dR = Rmax/NR; self.R = np.arange(0.5*dR, Rmax, dR); zmax = Rmax
        z_soft = 0.01*Rd if z_soft is None else z_soft
        u = np.linspace(0.0, math.asinh(zmax/z_soft), Nz); zp = z_soft*np.sinh(u); self.z = np.concatenate([-zp[:0:-1], zp])
        kmin, dk, kmax = 0.5/Rmax, 0.02/Rd, 14.0/Rd
        klo = np.exp(np.linspace(math.log(kmin), math.log(0.999*dk), 25)); self.k = np.concatenate([klo, np.arange(dk, kmax + 0.5*dk, dk)])
        self.wR = _trapw(self.R); self.wR[0] += self.R[0]; self.wz = _trapw(self.z); self.wk = _trapw(self.k); self.wk[0] += self.k[0]
        self.J0 = j0(np.outer(self.k, self.R)); self.J1 = j1(np.outer(self.k, self.R)); self.RwR = self.R*self.wR
        d = self.z[:, None] - self.z[None, :]; self.absd = np.abs(d); self.sgn = np.sign(d)
        self.iz0 = int(np.argmin(np.abs(self.z))); self.taper = (0.6*Rmax, 0.9*Rmax)
    def h0(self, f): return (self.J0*self.RwR) @ f
    def h1(self, f): return (self.J1*self.RwR) @ f
    def _E(self, kk, h):
        Ek = np.exp(-kk*self.absd); hw = h*self.wz; return Ek @ hw, (self.sgn*Ek) @ hw
    def newton(self, rho):
        rh = self.h0(rho); I = np.empty_like(rh); dI = np.empty_like(rh)
        for i, kk in enumerate(self.k):
            e0, e1 = self._E(kk, rh[i]); I[i] = e0; dI[i] = -kk*e1
        return -TWO_PI_G*((self.J1.T*(self.wk*self.k)) @ I), +TWO_PI_G*((self.J0.T*self.wk) @ dI)
    def qumond(self, rho, a0, nufun, gN=None):
        gRn, gzn = self.newton(rho) if gN is None else gN
        fac = nufun(np.hypot(gRn, gzn)/a0) - 1.0
        r = np.hypot(self.R[:, None], self.z[None, :]); t0_, t1_ = self.taper
        w = np.clip((t1_ - r)/(t1_ - t0_), 0.0, 1.0); w = w*w*(3 - 2*w)
        FR1 = self.h1(-fac*gRn*w); Fz0 = self.h0(-fac*gzn*w); Iph = np.empty_like(FR1)
        for i, kk in enumerate(self.k):
            aR0, aR1 = self._E(kk, FR1[i]); az0, az1 = self._E(kk, Fz0[i])
            Iph[i] = kk*(aR0 - az1)
        return gRn - 0.5*((self.J1.T*(self.wk*self.k)) @ Iph), (gRn, gzn)
def rho_of(grid, Sig, z0):
    e = np.exp(-2.0*np.abs(grid.z[None, :])/z0)                       # sech^2 without overflow: 4 e^{-2|z|/z0} / (1 + e^{-2|z|/z0})^2
    return Sig[:, None]*(4.0*e/(1.0 + e)**2)/(2*z0)
def solve_sigma(grid, Rdat, gbar, z0, nit=3, damp=0.5):
    lR = np.log(Rdat); lg = np.log(gbar); lRg = np.log(grid.R)
    sl = np.polyfit(lR[-4:], lg[-4:], 1)[0] if len(lg) >= 4 else -2.0; sl = float(np.clip(sl, -6.0, -1.5))
    tgt = np.interp(lRg, lR, lg)
    tgt[lRg < lR[0]] = lg[0] + 1.0*(lRg[lRg < lR[0]] - lR[0]); tgt[lRg > lR[-1]] = lg[-1] + sl*(lRg[lRg > lR[-1]] - lR[-1])
    g_t = np.exp(tgt)
    S = ((grid.J1*grid.RwR) @ g_t)/(2*math.pi*G); Sig = np.maximum((grid.J0.T*(grid.wk*grid.k)) @ S, 0.0)
    err = float("nan")
    for it in range(nit):
        gRn, _ = grid.newton(rho_of(grid, Sig, z0)); gm = np.abs(gRn[:, grid.iz0])
        err = float(np.abs(np.log(np.interp(Rdat, grid.R, gm)) - lg).max())
        if err < 0.01: break
        Sig = Sig*np.clip(g_t/np.maximum(gm, 1e-30), 0.5, 2.0)**damp
    gRn, gzn = grid.newton(rho_of(grid, Sig, z0)); gm = np.abs(gRn[:, grid.iz0])
    return Sig, float(np.abs(np.log(np.interp(Rdat, grid.R, gm)) - lg).max()), (gRn, gzn)

# ---------------------------------------------------------------- 0. validation on an exact exponential disc
P("=" * 118); P("0.  validation: the per-galaxy machinery on an exact exponential disc, all three kernels"); P("=" * 118)
Rd0 = 3.0*kpc; S0 = 11.5*Msun/PC2; z0 = 0.1*Rd0
gex = Grid(15*Rd0, Rd0); Sig_ex = S0*np.exp(-gex.R/Rd0); rho_ex = rho_of(gex, Sig_ex, z0)
gN_ex = gex.newton(rho_ex); Rdat0 = np.geomspace(0.3*Rd0, 10*Rd0, 30)
gbar_ex = np.interp(Rdat0, gex.R, np.abs(gN_ex[0][:, gex.iz0]))
grid0 = Grid(max(4*Rdat0[-1], 15*Rd0), Rd0); Sig_s, err0, gN_s = solve_sigma(grid0, Rdat0, gbar_ex, z0)
info(f"inversion of the exponential's own field: max |log g_model/g_target| = {err0:.4f}   ({time.time()-t0:.0f} s)")
worst = 0.0
for k, nuf in NU.items():
    a0 = PROF[k][1]
    gq_ex, _ = gex.qumond(rho_ex, a0, nuf, gN_ex); gq_s, _ = grid0.qumond(rho_of(grid0, Sig_s, z0), a0, nuf, gN_s)
    gNp_ex = np.abs(gN_ex[0][:, gex.iz0]); gNp_s = np.abs(gN_s[0][:, grid0.iz0])
    T_ex = np.log10(np.interp(Rdat0, gex.R, np.abs(gq_ex[:, gex.iz0]))/np.interp(Rdat0, gex.R, nuf(gNp_ex/a0)*gNp_ex))
    T_s = np.log10(np.interp(Rdat0, grid0.R, np.abs(gq_s[:, grid0.iz0]))/np.interp(Rdat0, grid0.R, nuf(gNp_s/a0)*gNp_s))
    dT_ = np.abs(T_s - T_ex); interior = Rdat0 < 0.9*Rdat0[-1]
    worst = max(worst, float(dT_[interior].max())); worst_edge = float(dT_.max()); iw = int(np.argmax(dT_))
    info(f"{k:7s}: exact-disc template T(R) range [{T_ex.min():+.3f}, {T_ex.max():+.3f}] dex; solved-from-data template differs by at most {dT_[interior].max():.4f} on interior points and {dT_.max():.4f} at the outermost point (R = {Rdat0[iw]/Rd0:.2f} R_d, where the inversion extrapolates)")
ck("V0 the inversion + solve chain reproduces the exact exponential disc's QUMOND correction to 0.02 dex on interior "
   "points for every kernel (f18's bar) and to 0.05 dex at the outermost point where the inversion extrapolates; the "
   "exponential's correction has f16's size: |T| peaks between 0.01 and 0.3 dex",
   err0 < 0.07 and worst < 0.02 and worst_edge < 0.05 and 0.01 < np.abs(T_ex).max() < 0.3,
   f"inversion {err0:.4f}, interior mismatch {worst:.4f}, edge mismatch {worst_edge:.4f}, |T| peak {np.abs(T_ex).max():.3f}")

# ---------------------------------------------------------------- 1. every galaxy, every kernel, three a_0
P("\n" + "=" * 118); P("1.  SPARC: disc correction T(R) per galaxy per kernel at the profiled (Upsilon_d, a_0) and +/- 0.15 dex"); P("=" * 118)
gals = [g for g in load_sparc() if g["Rdisk"] > 0 and len(g["r"]) >= 6]
info(f"{len(gals)} galaxies (Q <= 2, i >= 30, >= 6 points, R_d known)")
def gbar_ups(g, ups): return (g["vg"]*np.abs(g["vg"]) + ups*g["vd"]**2 + 1.4*ups*g["vb"]**2)/g["r"]*KMS2_KPC
if os.path.exists(CACHE):
    C = np.load(CACHE, allow_pickle=True)["C"].item(); info(f"cache loaded: {len(C)} galaxies")
else:
    C = {}
for n, g in enumerate(gals):
    if g["name"] in C: continue
    Rdat = g["r"]*kpc; Rd = g["Rdisk"]*kpc; z0g = 0.1*Rd
    grid = Grid(max(4.0*Rdat[-1], 15*Rd), Rd)
    rec = {}
    for ups in sorted(set(v[0] for v in PROF.values())):
        gb = gbar_ups(g, ups); okp = gb > 0
        if okp.sum() < 5: continue
        Sig, err, gN = solve_sigma(grid, Rdat[okp], gb[okp], z0g); rho = rho_of(grid, Sig, z0g)
        gNp = np.abs(gN[0][:, grid.iz0])
        for k, (u_k, a_k) in PROF.items():
            if u_k != ups: continue
            T = np.empty((len(DLA), int(okp.sum())))
            for j, dl in enumerate(DLA):
                a0 = a_k*10**dl
                gq, _ = grid.qumond(rho, a0, NU[k], gN)
                T[j] = np.log10(np.interp(Rdat[okp], grid.R, np.abs(gq[:, grid.iz0]))/np.interp(Rdat[okp], grid.R, NU[k](gNp/a0)*gNp))
            rec[k] = dict(err=err, T=T, ok=okp)
    C[g["name"]] = rec
    if (n + 1) % 10 == 0:
        np.savez(CACHE, C=np.array(C, dtype=object)); info(f"   [{n+1}/{len(gals)}] {g['name']:12s} inversion err {rec.get('nu_rar', {}).get('err', float('nan')):.3f}   {time.time()-t0:.0f} s")
np.savez(CACHE, C=np.array(C, dtype=object))
errs = np.array([C[g["name"]]["nu_rar"]["err"] for g in gals if "nu_rar" in C[g["name"]]])
info(f"inversion residual (max |log g_model/g_bar| per galaxy): median {np.median(errs):.3f}, {int((errs < 0.05).sum())} of {len(errs)} under 0.05, {int((errs < 0.1).sum())} under 0.10")
ck("D1 the inversion is usable on the bulk of the sample: at least half the galaxies invert to 0.10 and the median "
   "residual is under 0.10", np.median(errs) < 0.10 and (errs < 0.10).sum() >= 0.5*len(errs), f"median {np.median(errs):.3f}; {int((errs < 0.10).sum())}/{len(errs)} under 0.10")

# ---------------------------------------------------------------- 2. size of the correction, and its kernel dependence
P("\n" + "=" * 118); P("2.  the disc correction: how big, and how kernel-dependent"); P("=" * 118)
allT = {k: np.concatenate([C[g["name"]][k]["T"][1] for g in gals if k in C[g["name"]]]) for k in NU}
ally = np.concatenate([(gbar_ups(g, 0.5)[C[g["name"]]["nu_rar"]["ok"]])/PROF["nu_rar"][1] for g in gals if "nu_rar" in C[g["name"]]])
info("median |T| (dex) per kernel over all data points: " + ", ".join(f"{k} {np.median(np.abs(v)):.4f}" for k, v in allT.items()))
nn = min(len(allT["nu_rar"]), len(allT["mu_exp"]))
dT = allT["mu_exp"][:nn] - allT["nu_rar"][:nn]
info(f"median |T_exp - T_RAR| = {np.median(np.abs(dT)):.4f} dex; the algebraic kernel difference in the transition is up to 0.073 dex (f21)")
for lo, hi in ((0.03, 0.1), (0.1, 0.3), (0.3, 1.0), (1.0, 3.0), (3.0, 30.0)):
    m = (ally >= lo) & (ally < hi)
    if m.sum() > 10: info(f"   g_bar/a_0 in [{lo:.2f}, {hi:.1f}): N = {int(m.sum()):4d}  median T: " + ", ".join(f"{k} {np.median(allT[k][:len(ally)][m]):+.4f}" for k in NU))
ck("D2 the disc correction is small compared with the kernel difference: the median |T_exp - T_RAR| across the data "
   "is under 0.02 dex, so geometry cannot manufacture or erase the algebraic ranking",
   np.median(np.abs(dT)) < 0.02, f"median |dT| = {np.median(np.abs(dT)):.4f} dex")

# ---------------------------------------------------------------- 3. the paired comparison on corrected residuals
P("\n" + "=" * 118); P("3.  the lead's paired-galaxy comparison, repeated on the QUMOND-corrected residuals (a_0 re-profiled)"); P("=" * 118)
LOGA = np.linspace(-10.8, -9.2, 161)
names = [g["name"] for g in gals if all(k in C[g["name"]] for k in NU)]; NG = len(names)
def losses(k, corrected, subset=None):
    u_k, a_k = PROF[k]; L = np.full((NG, len(LOGA)), np.nan)
    for i, g in enumerate([g for g in gals if g["name"] in names]):
        if subset is not None and g["name"] not in subset: L[i] = 0.0; continue
        rec = C[g["name"]][k]; gb = gbar_ups(g, u_k)[rec["ok"]]; go = g["gobs"][rec["ok"]]
        for ia, la in enumerate(LOGA):
            a0 = 10**la; pred = np.log10(NU[k](gb/a0)*gb)
            if corrected:
                Tj = np.array([np.interp(la - math.log10(a_k), DLA, rec["T"][:, p]) for p in range(len(gb))])
                pred = pred + Tj
            L[i, ia] = np.mean((np.log10(go) - pred)**2)
    return L
W0 = np.full((1, NG), 1.0/NG); W = rng.multinomial(NG, np.full(NG, 1.0/NG), size=999)/NG
def prof(L, Wt):
    m = Wt @ L; j = np.argmin(m, axis=1); return m[np.arange(len(Wt)), j], j
OUT = {}
for corrected in (False, True):
    tag = "QUMOND-corrected" if corrected else "algebraic"
    res = {}
    for k in NU:
        L = losses(k, corrected); full, j = prof(L, W0); boot, _ = prof(L, W)
        res[k] = dict(full=float(full[0]), a0=float(10**LOGA[j[0]]), boot=boot)
        info(f"{tag:17s} {k:7s}: best a_0 = {res[k]['a0']:.3e}, equal-galaxy RMS = {math.sqrt(res[k]['full']):.4f} dex")
    for k in ("mu_exp", "mu_10"):
        d = res[k]["boot"] - res["nu_rar"]["boot"]; pc = np.percentile(d, [2.5, 50, 97.5]); res[k]["pc"] = pc; res[k]["frac"] = float(np.mean(d > 0))
        info(f"{tag:17s} paired MSE({k}) - MSE(nu_rar): [{pc[0]:+.5f}, {pc[1]:+.5f}, {pc[2]:+.5f}] dex^2; fraction > 0 = {res[k]['frac']:.3f}")
    OUT[tag] = res
A, Q = OUT["algebraic"], OUT["QUMOND-corrected"]
ck("D3 the algebraic ranking is reproduced on this galaxy set before any correction (mu_10 loses in >= 99% of resamples; "
   "the exp-RAR interval contains zero)", A["mu_10"]["frac"] >= 0.99 and A["mu_exp"]["pc"][0] < 0 < A["mu_exp"]["pc"][2],
   f"mu_10 fraction {A['mu_10']['frac']:.3f}; exp interval [{A['mu_exp']['pc'][0]:+.5f}, {A['mu_exp']['pc'][2]:+.5f}]")
ck("D4 (HYPOTHESIS CHECK -- a FAIL is a result) with the matched QUMOND disc solve, mu_10 STILL loses to nu_RAR in "
   ">= 99% of paired resamples.  If this fails, the disc geometry WEAKENS the mu_10 rejection: mu_10's correction is "
   "~0 above a_0 while the RAR's is negative there, so the forward solve moves mu_10 toward the data at high "
   "acceleration; the verdict on mu_10 then rests on the algebraic comparison (f25, f28) and is 'disfavoured' here",
   Q["mu_10"]["frac"] >= 0.99, f"fraction {Q['mu_10']['frac']:.3f} (algebraic {A['mu_10']['frac']:.3f}); RMS {math.sqrt(Q['mu_10']['full']):.4f} vs {math.sqrt(Q['nu_rar']['full']):.4f}")
ck("D5 (HYPOTHESIS CHECK -- a FAIL is a result) exp vs RAR remains undecided after the forward solve (interval contains zero)",
   Q["mu_exp"]["pc"][0] < 0 < Q["mu_exp"]["pc"][2], f"interval [{Q['mu_exp']['pc'][0]:+.5f}, {Q['mu_exp']['pc'][2]:+.5f}], fraction > 0 = {Q['mu_exp']['frac']:.3f}")
dm = {k: Q[k]["full"] - A[k]["full"] for k in NU}
ck("D6 (HYPOTHESIS CHECK -- a FAIL is a result, and f18 predicts it fails) the QUMOND disc correction IMPROVES the fit "
   "of the framework's kernel (MSE falls).  f18 found SPARC's inner discs sit on the opposite side of the curl "
   "template from modified gravity; if the correction worsens the fit here, that is the same finding on the full sample",
   dm["nu_rar"] < 0, "; ".join(f"{k}: dMSE = {v:+.5f} dex^2 (RMS {math.sqrt(A[k]['full']):.4f} -> {math.sqrt(Q[k]['full']):.4f})" for k, v in dm.items()))
# the well-inverted subset: repeat the corrected comparison on galaxies whose inversion residual is under 0.10
good = set(g["name"] for g in gals if "nu_rar" in C[g["name"]] and C[g["name"]]["nu_rar"]["err"] < 0.10)
info(f"well-inverted subset (residual < 0.10): {len(good)} galaxies -- corrected comparison repeated on it")
gi = np.array([1.0 if n_ in good else 0.0 for n_ in names]); Wg0 = (W0*gi)/np.sum(W0*gi); Wg = (W*gi)/np.sum(W*gi, axis=1, keepdims=True)
S = {}
for k in NU:
    L = losses(k, True, subset=good); full, j = prof(L, Wg0); boot, _ = prof(L, Wg)
    S[k] = dict(full=float(full[0]), boot=boot)
    info(f"subset corrected  {k:7s}: equal-galaxy RMS = {math.sqrt(S[k]['full']):.4f} dex")
for k in ("mu_exp", "mu_10"):
    d = S[k]["boot"] - S["nu_rar"]["boot"]; pc = np.percentile(d, [2.5, 50, 97.5]); S[k]["pc"] = pc; S[k]["frac"] = float(np.mean(d > 0))
    info(f"subset corrected  paired MSE({k}) - MSE(nu_rar): [{pc[0]:+.5f}, {pc[1]:+.5f}, {pc[2]:+.5f}] dex^2; fraction > 0 = {S[k]['frac']:.3f}")
ck("D7 on the well-inverted subset the corrected verdicts are the same in kind as on the full sample: mu_10 disfavoured "
   "(worse in > 80% of resamples) and exp vs RAR undecided",
   S["mu_10"]["frac"] > 0.8 and S["mu_exp"]["pc"][0] < 0 < S["mu_exp"]["pc"][2],
   f"mu_10 fraction {S['mu_10']['frac']:.3f}; exp interval [{S['mu_exp']['pc'][0]:+.5f}, {S['mu_exp']['pc'][2]:+.5f}]")
P(f"\n  total runtime {time.time()-t0:.0f} s")
P("  scope: catalogue distance and inclination for every kernel (paired); Upsilon at each kernel's f25 optimum; no")
P("  external field; QUMOND (the AQUAL disc solve is a different operator; f24 shows AQUAL is the more constraining side")
P("  for the Solar-System quadrupole, but for discs the two agree to the curl-field level).  Descriptive MSE, no sigma.")
sys.exit(ck.done())
