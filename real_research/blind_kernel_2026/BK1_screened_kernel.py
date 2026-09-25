#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BK1 -- A KERNEL BLIND TO THE LARGE-SCALE FIELD: the screened-argument C-H/K kernel, and its window.

WHY (real_research/switch_audit_2026/BS2, BS3)
  C-H/K + L342's switch is excluded by KiDS-1000 isolated lensing through its own external-field effect.  The switch
  keeps the web Newtonian and LCDM-like; the web's field (~0.015 a0 rms, unchanged by isolation) enters the kernel's
  argument and ends every lens's phantom at ~0.1 Mpc.  The door BS3 left: a kernel blind to the large-scale field,
  which must still hand the Sun the Galaxy's field (L340 S1's Solar-System floor is built on it).

THE CONSTRUCTION (one new length, lambda)
  The kernel's argument is the Yukawa-screened Newtonian field instead of the Newtonian one:
      (nabla^2 - 1/lambda^2) Phi_b = 4 pi G rho,   phantom = div[(nu(|grad Phi_b|/a0) - 1) grad Phi_b],
  everything else as in C-H/K + switch (L340, L342).  A point mass: |g_b| = s(r) G M/r^2, s = (1 + r/lambda) e^(-r/lambda).
  Sources inside lambda act in full; a uniform (long-mode) external field is screened as (k lambda)^2, so the web's
  field -- dominated by k ~ 0.01-0.1 /Mpc -- is suppressed; the Galaxy's field on the Sun (sources within ~20 kpc) is
  kept for lambda >> 20 kpc.  Relativistically: a massive auxiliary scalar, m = hbar/(lambda c) ~ 1e-29 eV (lambda ~ Mpc).
  Stacked-lens flux law (exact in this QUMOND form): M_dyn(<r) = M_b [1 + s (N(s y_N, e_b) - 1)], N as in BS2.

CHECKS (gates set before the run)
  C1 (documentary) lambda_min: the Galaxy's field at 20 kpc kept to >= 99.9% and SPARC point-mass g_obs at 100 kpc
     changed by <= 1% (masses 1e9-10^11.5).
  C2 (documentary) the screened large-scale field on an isolated lens: linear LCDM (BS3's P(k), z = 0.25), matter
     outside the 3 Mpc isolation sphere, exact screened window k int_R^inf j1(kr)(1 + r/lambda)e^(-r/lambda) dr.
  C3 THE WINDOW: some lambda >= lambda_min fits KiDS-1000 (BS3's full-covariance fit: M_b per bin, x_c profiled,
     two-halo b <= 2 per bin) within Delta chi^2 <= 4 of the no-EFE switch fit, all points AND inside 0.3 Mpc, both
     footings, with the lens feeling its own screened external field (Maxwell-stacked).
  C4 (documentary) whether screening alone (x_c = 0) does the switch's lensing job.
  C5 INJECTION: at the best-fitting lambda, synthetic data from the screened construction pass C3's test in >= 80%.
  (lambda grid 0.2-5 Mpc and infinity; 0.6/0.8/0.9/1.2 were added after the first run showed the minimum near 0.7 --
   a finer profile of the same parameter, gates unchanged.)
  MUTATE=1 removes the screening (lambda = infinity only): the kernel reverts to BS3's and C3 must FAIL (rc = 1).
  SCOPE: static, QUMOND-form, point-mass baryons, lens z = 0.25, linear-theory screened field (the near field of faint
  matter inside the isolation sphere is not included -- see C2's 1 Mpc column); growth is still the switch's job.
  NOT done: lambda's origin (a free length); the massive auxiliary's health, tracking (L330/L340) and 1PN.

Run from the repository root:  python3 real_research/blind_kernel_2026/BK1_screened_kernel.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious BLAS warning (no result changes)
from scipy.optimize import brentq, lsq_linear
from scipy.spatial import cKDTree
from scipy.special import spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "BK1_screened_kernel"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "BK1", "mutate": MUTATE, "checks": {}, "numbers": {}}
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


# ------------------------------------------------------------------ L342 / BS2 constants, kernel, data, ESD model
Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200
H0 = 100 * h * 1e3 / Mpc
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOTS = ("canonical", "alt")
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def nu_mono_arr(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM) / y

B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
MS, PCm = 1.98892e30, 3.0857e16; MPCm = PCm * 1e6
Rd, Ed = [], []
for b in (1, 2, 3, 4):
    d = np.genfromtxt(os.path.join(B, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#")
    Rd.append(d[:, 0]); Ed.append(d[:, 1] / d[:, 4])
cv = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
vv = cv[:, 4] / cv[:, 6]; npb = len(Rd[0]); Cf = vv.reshape(4, 4, npb, npb).transpose(0, 2, 1, 3).reshape(4 * npb, 4 * npb)
Cf = (Cf + Cf.T) / 2; Ci = np.linalg.inv(Cf)
rr = np.geomspace(1e-3, 30, 4000) * MPCm; Rp = np.geomspace(0.02, 4, 240) * MPCm
ZL = 0.25; Hlens = H0 * math.sqrt(Om * (1 + ZL) ** 3 + OL)
W = np.zeros((len(Rp), len(rr)))
for i, Rv in enumerate(Rp):
    m = np.where(rr > Rv * 1.0000001)[0]; r_ = rr[m]; dr = np.diff(r_)
    wt = np.zeros_like(r_); wt[:-1] += 0.5 * dr; wt[1:] += 0.5 * dr
    W[i, m] = 2 * r_ / np.sqrt(r_ ** 2 - Rv ** 2) * wt


def esd_from_M(M, Mb, xc):
    if xc:
        rho_dyn = np.gradient(M, rr) / (4 * math.pi * rr ** 2); on = 4 * math.pi * G * rho_dyn / Hlens ** 2 >= xc
        it = int(np.where(on)[0].max()) if on.any() else 0
        M = np.where(np.arange(len(rr)) > it, M[it], M)
    Sig = W @ (np.gradient(M - Mb, rr) / (4 * math.pi * rr ** 2))
    Mc = np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * Rp[1:] + Sig[:-1] * Rp[:-1]) * np.diff(Rp))]) * 2 * math.pi \
        + math.pi * Rp[0] ** 2 * Sig[0]
    return Rp / MPCm, (Mc / (math.pi * Rp ** 2) - Sig + Mb / (math.pi * Rp ** 2)) * PCm ** 2 / MS



LYT = np.linspace(-9.5, 6.5, 1601); YT = 10 ** LYT; MU = np.linspace(-1.0, 1.0, 4001)
def N_of(y, e):
    y = np.atleast_1d(np.asarray(y, float))
    if e == 0: return nu_mono_arr(y)
    out = np.empty_like(y)
    for s in range(0, len(y), 64):
        yy = y[s:s + 64, None]
        w = np.sqrt(np.maximum(yy ** 2 + e ** 2 - 2 * yy * e * MU[None, :], 0.0))
        out[s:s + 64] = 0.5 * _trap(nu_mono_arr(w) * (yy - e * MU[None, :]), MU, axis=1) / yy[:, 0]
    return out

# ------------------------------------------------------------------ linear LCDM: P(k), growth, field normalisation
TH27 = 2.7255 / 2.7; NS, S8 = 0.9649, 0.8111
def T_eh(k):
    omh2 = Om * h * h; fb = Ob / Om
    s_ = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * (Ob * h * h) ** 0.75)
    aG = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    Gm = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s_) ** 4)); q = k * TH27 ** 2 / (Gm * h)
    L_ = np.log(2 * np.e + 1.8 * q); C_ = 14.2 + 731 / (1 + 62.5 * q); return L_ / (L_ + C_ * q * q)
def W_th(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
KK = np.geomspace(1e-5, 50, 40000); PK0 = KK ** NS * T_eh(KK) ** 2
PK0 *= S8 ** 2 / _trap(PK0 * W_th(KK * 8 / h) ** 2 * KK ** 2 / (2 * math.pi ** 2), KK)
def Pk0(k): return np.interp(np.log(np.maximum(k, 1e-5)), np.log(KK), PK0, left=0.0, right=0.0)
def growth(z):
    a_ = np.linspace(1e-4, 1, 20001)
    def D_(a1):
        aa = a_[a_ <= a1]; E = np.sqrt(Om / aa ** 3 + OL); return math.sqrt(Om / a1 ** 3 + OL) * _trap(1 / (aa * E) ** 3, aa)
    return D_(1 / (1 + z)) / D_(1.0)
DZ = growth(ZL)
CG = 1.5 * Om * H0 ** 2 * (1 + ZL) ** 2 * DZ * Mpc          # m/s^2 per (comoving Mpc of grad^-1 delta_0)
SIG2_TOT = CG ** 2 * _trap(PK0, KK) / (2 * math.pi ** 2)     # 3-D variance of g at a random point, no window
# ============================================================================================ B: two-halo template
rgrid = np.geomspace(0.05, 300, 3000)                              # comoving Mpc
kq = np.geomspace(1e-5, 30, 60000)
XI0 = np.array([_trap(kq ** 2 * Pk0(kq) * np.sinc(kq * r / math.pi) * np.exp(-(kq / 20) ** 2), kq) / (2 * math.pi ** 2)
                for r in rgrid])
RHO_M0 = Om * 3 * H0 ** 2 / (8 * math.pi * G) * Mpc ** 3 / MS      # Msun / Mpc^3 comoving
def w_proj(Rc):
    pi_ = np.geomspace(1e-3, 150, 1500)
    return 2 * _trap(np.interp(np.sqrt(Rc ** 2 + pi_ ** 2), rgrid, XI0), pi_)
Rc_g = np.geomspace(0.01, 5, 400) * (1 + ZL)
wv = np.array([w_proj(x) for x in Rc_g])
inner = wv[0] * Rc_g[0] ** 2 / 2                                   # int_0^R0 w R dR with w ~ const inside R0
wbar = np.array([2 * (inner + (_trap(wv[:i + 1] * Rc_g[:i + 1], Rc_g[:i + 1]) if i > 0 else 0.0)) / Rc_g[i] ** 2
                 for i in range(len(Rc_g))])
DS2H = RHO_M0 * DZ ** 2 * (wbar - wv) * (1 + ZL) ** 2 / 1e12     # Msun/pc^2 physical, for b = 1
T2H = [np.interp(Rd[b], Rc_g / (1 + ZL), DS2H) for b in range(4)]
P(f"\n    two-halo template (b = 1, z = {ZL}): Delta Sigma_2h at 0.1 / 0.3 / 1 / 2.6 Mpc = "
  + ", ".join(f"{np.interp(x, Rc_g / (1 + ZL), DS2H):.3f}" for x in (0.1, 0.3, 1.0, 2.6)) + " Msun/pc^2")
OUT["numbers"]["B_template"] = {str(x): float(np.interp(x, Rc_g / (1 + ZL), DS2H)) for x in (0.1, 0.3, 1.0, 2.6)}
TM = np.zeros((4 * npb, 4))
for b in range(4): TM[b * npb:(b + 1) * npb, b] = T2H[b]


def fit_2h(blk, data, bmax, sel=None):
    """chi^2 of model block blk[im, bin, R] + b_bin * T2H, M_b per bin by coordinate descent, b in [0, bmax] per bin
    by bounded least squares under the full (or selected) covariance."""
    D = np.concatenate(data); idx = np.arange(4 * npb) if sel is None else np.array(sel)
    Cs = Cf[np.ix_(idx, idx)]; Csi = np.linalg.inv(Cs); U = np.linalg.cholesky(Csi)
    A = U.T @ TM[idx]; Apinv = np.linalg.pinv(A)
    def solve_batch(R_):                                           # R_: (ncand, 4*npb) residual vectors
        Y = (U.T @ R_[:, idx].T).T
        if bmax == 0: return np.zeros((len(Y), 4)), np.sum(Y ** 2, 1)
        Bu = (Apinv @ Y.T).T; out_b = Bu.copy(); c2 = np.sum((Bu @ A.T - Y) ** 2, 1)
        bad = np.where(np.any(Bu < 0, 1) | np.any(Bu > bmax, 1))[0]
        for i in bad:
            r_ = lsq_linear(A, Y[i], bounds=(0, bmax), method="bvls"); out_b[i] = r_.x
            c2[i] = float(np.sum((A @ r_.x - Y[i]) ** 2))
        return out_b, c2
    im = [len(LM) // 2] * 4; best = None; bb = np.zeros(4)
    for _ in range(8):
        moved = False
        for b in range(4):
            base = np.concatenate([blk[im[q], q] for q in range(4)])
            V = np.repeat(base[None, :], len(LM), axis=0); V[:, b * npb:(b + 1) * npb] = blk[:, b]
            bs, c2 = solve_batch(D[None, :] - V)
            j = int(np.argmin(c2))
            if j != im[b]: im[b], moved = j, True
            best, bb = float(c2[j]), bs[j]
        if not moved: break
    return best, im, bb


# ------------------------------------------------------------------ screened-argument model
LAMS = [0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, float("inf")]
if MUTATE:
    LAMS = [float("inf")]; P("*** MUTATE=1: screening removed (lambda = infinity only) -- the kernel reverts to BS3's ***")
XCS = [0.0, 3.0, 5.0, 7.0, 10.0]
LM = np.round(np.arange(9.8, 11.8001, 0.02), 4)
ENODES = [0.0] + [float(v) for v in np.geomspace(1e-7, 0.05, 40)]
LOGE = np.log10(np.array(ENODES[1:]))
NTAB = {}
def Ntab(ie):
    if ie not in NTAB: NTAB[ie] = N_of(YT, ENODES[ie])
    return NTAB[ie]
def s_scr(r_m, lam):
    if not np.isfinite(lam): return np.ones_like(r_m)
    x = r_m / (lam * MPCm); return (1 + x) * np.exp(-x)
def model_M(Mb, a0, ie, lam):
    s = s_scr(rr, lam); yb = np.maximum(s * G * Mb / rr ** 2 / a0, 1e-12)
    Nv = nu_mono_arr(yb) if ie == 0 else np.interp(np.log10(yb), LYT, Ntab(ie), left=np.nan)
    Nv = np.where(np.isnan(Nv), (Ntab(ie)[0] if ie else 1.0), Nv)       # y below table: N saturates (Newtonian-like)
    return Mb * (1 + s * (Nv - 1))


def stack_weights(e_samples):
    w = np.zeros(len(ENODES)); le = np.log10(np.maximum(e_samples, 1e-14))
    below = le < LOGE[0] - 0.5 * (LOGE[1] - LOGE[0]); w[0] += below.sum()
    idx = np.clip(np.rint((le[~below] - LOGE[0]) / (LOGE[1] - LOGE[0])).astype(int), 0, len(LOGE) - 1) + 1
    np.add.at(w, idx, 1.0); return w / w.sum()


# ------------------------------------------------------------------ the SCREENED external field on an isolated lens
def K_out(k, R, lam):
    """window for the screened field at a sphere's centre from linear matter outside radius R:
    k int_R^inf j1(kr) (1 + r/lam) e^(-r/lam) dr  (-> j0(kR) for lam -> inf)."""
    if not np.isfinite(lam): return np.sinc(k * R / math.pi)
    r = np.geomspace(R, R + 60 * lam, 3000)
    j1 = lambda x: np.where(x > 1e-6, (np.sin(x) / x ** 2 - np.cos(x) / x), x / 3)
    f = (1 + r / lam) * np.exp(-r / lam)
    return np.array([kk * _trap(j1(kk * r) * f, r) for kk in k])
kq = np.geomspace(1e-4, 30, 1500)
SIGE = {}
for lam in LAMS:
    row = {}
    for Ri in (3.0, 1.0):
        Kk = K_out(kq, Ri, lam)
        row[Ri] = math.sqrt(CG ** 2 * _trap(Pk0(kq) * Kk ** 2, kq) / (2 * math.pi ** 2))
    SIGE[lam] = row
GS = np.random.default_rng(3).standard_normal((200000, 3))

# ============================================================================================ C1 (Solar System and SPARC)
banner("C1  WHAT THE SCREENING MUST LEAVE ALONE: the Galaxy's field on the Sun; SPARC rotation curves to 100 kpc")
def gobs(Mb, r_m, a0, lam):
    s = s_scr(np.array([r_m]), lam)[0]; gN = G * Mb / r_m ** 2
    return gN + s * gN * (float(nu_mono_arr(s * gN / a0)) - 1)       # QUMOND point mass, e = 0
c1 = {}
for lam in LAMS:
    if not np.isfinite(lam): continue
    sun = float(s_scr(np.array([20e3 * PCm]), lam)[0])                # Galactic sources within ~20 kpc of the Sun
    sp = max(abs(gobs(10 ** lm * MS, 100e3 * PCm, A0["canonical"], lam) / gobs(10 ** lm * MS, 100e3 * PCm, A0["canonical"], float("inf")) - 1)
             for lm in (9.0, 10.0, 11.0, 11.5))
    c1[lam] = {"galactic_field_factor_20kpc": sun, "sparc_max_frac_change_100kpc": sp}
    P(f"    lambda = {lam:>4} Mpc: Galaxy's field on the Sun kept to {sun:.6f};  largest SPARC change at 100 kpc {100 * sp:.2f}%")
LAM_MIN = min([l for l, v in c1.items() if v["sparc_max_frac_change_100kpc"] <= 0.01 and v["galactic_field_factor_20kpc"] >= 0.999],
              default=float("inf"))
OUT["numbers"]["C1"] = {str(k): v for k, v in c1.items()}; OUT["numbers"]["lambda_min"] = LAM_MIN
check("C1 (documentary) the smallest screening length that keeps the Galaxy's field on the Sun (>= 99.9%) and SPARC to 100 kpc (<= 1%)",
      f"lambda >= {LAM_MIN} Mpc (grid)", True, "", load_bearing=False)

# ============================================================================================ C2 (screened LSS field)
banner("C2  THE SCREENED LARGE-SCALE FIELD ON AN ISOLATED LENS (linear LCDM, matter outside the isolation sphere)")
for lam in LAMS:
    P(f"    lambda = {lam:>4} Mpc: rms |g_ext,screened| = {SIGE[lam][3.0] / A0['canonical']:.2e} a0 (outside 3 Mpc), "
      f"{SIGE[lam][1.0] / A0['canonical']:.2e} a0 (outside 1 Mpc)")
OUT["numbers"]["C2"] = {str(l): {str(k): v / A0["canonical"] for k, v in r.items()} for l, r in SIGE.items()}
check("C2 (documentary) screened external field vs lambda (KiDS single-field bound from BS2: e <= 7.2e-5 / 5.2e-5)",
      {str(l): f"{SIGE[l][3.0] / A0['canonical']:.1e}" for l in LAMS}, True, "", load_bearing=False)

# ============================================================================================ tables
TAB = {}
for jf, foot in enumerate(FOOTS):
    for lam in LAMS:
        w = stack_weights(np.linalg.norm(GS, axis=1) * SIGE[lam][3.0] / math.sqrt(3) / A0[foot])
        nz = [i for i in range(len(ENODES)) if w[i] > 1e-4]; w = w[nz] / w[nz].sum()
        arr = np.zeros((len(XCS), len(LM), 4, npb))
        for im, lm in enumerate(LM):
            Mb = 10 ** lm * MS
            Ms = [model_M(Mb, A0[foot], ie, lam) for ie in nz]
            for ix, xc in enumerate(XCS):
                acc = 0
                for wi, M in zip(w, Ms):
                    Rq, dS = esd_from_M(M, Mb, xc); acc = acc + wi * dS
                arr[ix, im] = [np.interp(Rd[b], Rq, acc) for b in range(4)]
        TAB[(foot, lam)] = arr
    # comparator: BS3's no-EFE switch (lambda = inf, e = 0)
    arr = np.zeros((len(XCS), len(LM), 4, npb))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MS; M = model_M(Mb, A0[foot], 0, float("inf"))
        for ix, xc in enumerate(XCS):
            Rq, dS = esd_from_M(M, Mb, xc); arr[ix, im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
    TAB[(foot, "comparator")] = arr
P(f"\nESD tables built ({time.time() - T0:.0f} s)")
DATA = [np.array(e) for e in Ed]
SEL = [b * npb + i for b in range(4) for i in range(npb) if Rd[b][i] <= 0.3]
def best_over_xc(arr, data, bmax, sel=None):
    best = None
    for ix in range(len(XCS)):
        c_, im, bb = fit_2h(arr[ix], data, bmax, sel)
        if best is None or c_ < best[0]: best = (c_, ix, im, bb)
    return best

# ============================================================================================ C3
banner("C3  KiDS-1000 WITH THE SCREENED KERNEL (its own screened external field, two-halo b <= 2, switch x_c profiled)")
R3 = {}
for foot in FOOTS:
    ref = best_over_xc(TAB[(foot, "comparator")], DATA, 2.0); ref_in = best_over_xc(TAB[(foot, "comparator")], DATA, 2.0, SEL)
    rows = {}
    for lam in LAMS:
        r_ = best_over_xc(TAB[(foot, lam)], DATA, 2.0); r0 = fit_2h(TAB[(foot, lam)][0], DATA, 2.0)
        ri = best_over_xc(TAB[(foot, lam)], DATA, 2.0, SEL)
        rows[lam] = {"dchi2": r_[0] - ref[0], "xc": XCS[r_[1]], "b": [round(x, 2) for x in r_[3]],
                     "dchi2_no_switch": r0[0] - ref[0], "dchi2_inside_0.3": ri[0] - ref_in[0],
                     "logM": [float(LM[i]) for i in r_[2]]}
        P(f"    {foot:9s} lambda = {lam:>4}: Delta chi^2 {rows[lam]['dchi2']:+8.1f} (x_c {rows[lam]['xc']}, b {rows[lam]['b']});  "
          f"no switch {rows[lam]['dchi2_no_switch']:+8.1f};  inside 0.3 Mpc {rows[lam]['dchi2_inside_0.3']:+7.1f}")
    R3[foot] = {"comparator_chi2": ref[0], "rows": rows}
OUT["numbers"]["C3"] = {f_: {"comparator_chi2": R3[f_]["comparator_chi2"], "rows": {str(k): v for k, v in R3[f_]["rows"].items()}} for f_ in FOOTS}
ok_l = [l for l in LAMS if l >= LAM_MIN and all(R3[f_]["rows"][l]["dchi2"] <= 4 and R3[f_]["rows"][l]["dchi2_inside_0.3"] <= 4 for f_ in FOOTS)]
check("C3 THE WINDOW: some screening length lambda >= lambda_min (Sun + SPARC) fits KiDS-1000 within Delta chi^2 <= 4 of "
      "the no-EFE switch (all points and inside 0.3 Mpc), with its own screened external field, both footings",
      f"passing lambda: {ok_l}", len(ok_l) > 0,
      "a non-empty window means the blind kernel survives what excluded C-H/K + switch")
ok_ns = [l for l in LAMS if l >= LAM_MIN and all(R3[f_]["rows"][l]["dchi2_no_switch"] <= 4 for f_ in FOOTS)]
check("C4 (documentary) does the screening alone do the switch's lensing job? lambda passing with x_c = 0 (no switch)",
      f"{ok_ns}", True, "the switch is still needed for growth (L341/L342); this asks only about KiDS", load_bearing=False)

# ============================================================================================ C5 injection
banner("C5  INJECTION at the best-fitting lambda: does the gate pass when the screened construction is true? (canonical)")
lam_inj = min(LAMS, key=lambda l: R3["canonical"]["rows"][l]["dchi2"])                # the best lambda on the data
rngi = np.random.default_rng(20260925); Lch = np.linalg.cholesky(Cf); IMS = [int(np.argmin(np.abs(LM - l))) for l in (10.2, 10.6, 10.9, 11.2)]
arr = TAB[("canonical", lam_inj)]; ixt = XCS.index(5.0)
mean_t = np.concatenate([arr[ixt, IMS[b], b] + T2H[b] for b in range(4)])
dd = []
for t in range(10):
    dv = mean_t + Lch @ rngi.standard_normal(4 * npb); dat = [dv[b * npb:(b + 1) * npb] for b in range(4)]
    dd.append(best_over_xc(arr, dat, 2.0)[0] - best_over_xc(TAB[("canonical", "comparator")], dat, 2.0)[0])
fr = float(np.mean(np.array(dd) <= 4))
P(f"    lambda = {lam_inj}: Delta chi^2 per draw {np.round(dd, 1).tolist()}; pass fraction {fr:.2f}")
OUT["numbers"]["C5"] = {"lambda": lam_inj, "dchi2": dd, "pass_fraction": fr}
check("C5 when the screened construction is true the gate passes in >= 80% of 10 draws", f"{fr:.2f}", fr >= 0.8, "")

# ============================================================================================ verdict
banner("VERDICT")
rc = R3["canonical"]["rows"]; ra = R3["alt"]["rows"]
P("  lambda (Mpc) | screened field (a0) | Delta chi^2 all pts (can/alt) | inside 0.3 Mpc | no switch")
for l in LAMS:
    P(f"  {l:>12} | {SIGE[l][3.0] / A0['canonical']:.1e}             | {rc[l]['dchi2']:+7.1f} / {ra[l]['dchi2']:+7.1f}           | "
      f"{rc[l]['dchi2_inside_0.3']:+6.1f} / {ra[l]['dchi2_inside_0.3']:+6.1f} | {rc[l]['dchi2_no_switch']:+7.1f} / {ra[l]['dchi2_no_switch']:+7.1f}")
lb = min(LAMS, key=lambda l: rc[l]["dchi2"])
pm_ref = {"canonical": 16.9, "alt": 15.6}                           # BS3 G2: pure MOND at its own field, b <= 2, vs the same comparator
P(f"""  Best lambda = {lb} Mpc: Delta chi^2 {rc[lb]['dchi2']:+.1f} / {ra[lb]['dchi2']:+.1f} vs the (EFE-free, hence unphysical) switch comparator;
  for scale, pure MOND at its own field sits at +{pm_ref['canonical']} / +{pm_ref['alt']} and C-H/K + switch unscreened at {rc[float('inf')]['dchi2']:+.0f} / {ra[float('inf')]['dchi2']:+.0f}.
  Sun + SPARC need lambda >= {LAM_MIN} Mpc.  Window (KiDS within 4, both footings, both radius ranges): {ok_l}.
  The blind kernel is one new length, lambda: the kernel's argument is the Yukawa-screened Newtonian field,
  (nabla^2 - 1/lambda^2) Phi_b = 4 pi G rho.  Sources inside lambda (the Galaxy for the Sun; a galaxy for itself) act in
  full; the large-scale web's field -- dominated by long modes -- is screened as (k lambda)^2.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
