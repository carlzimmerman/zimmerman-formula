#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BK2 -- DERIVING BK1's SCREENING LENGTH lambda (or showing it cannot be derived).

BK1 (real_research/blind_kernel_2026/BK1_screened_kernel.py): the C-H/K kernel acting on the Yukawa-screened field,
(nabla^2 - 1/lambda^2) Phi_b = 4 pi G rho, is blind to the web's field and fits KiDS-1000 best at a CONSTANT
lambda ~ 0.7 Mpc (Delta chi^2 +7.7 / +8.0 vs the EFE-free switch comparator; window <= 4 empty).  lambda was free.

THE ARGUMENT
  (1) A constant length cannot come from the framework's constants: c/H0 ~ 4400 Mpc, a0/H0^2 ~ 760 Mpc, c^2/a0 ~ 3e4
      Mpc; reaching 0.7 Mpc needs a dimensionless factor ~1e-3, i.e. a new number.  D0 counts how many small-exponent
      combinations c/H0 x Z^n Omega_L^m Omega_m^q (2 pi)^r land near 0.7 Mpc (the price of any 'hit').
  (2) The construction DOES supply a length near 1 Mpc, but it is mass-dependent: in a bound (deep-MOND, flat)
      region v^2 = |a|^2/(4 pi G rho_dyn) with |a| the aether acceleration and 4 pi G rho_dyn = x H^2 (L342's switch
      scalar, x = 9 R3/(4 K^2)), all C-H/K clock scalars.  A screening mass built from them,
          m^2 = X H^4/|a|^2 * x  ->  lambda = v_flat/(sqrt(X) H),
      is L342's switch radius r_t with X in the role of x_c: NO new number if X falls in the switch's range.
      It predicts lambda ~ M_b^(1/4); a constant lambda (BK1) and lambda ~ M_b^(1/2) are the alternatives.

CHECKS (gates set before the run)
  D0 (documentary) the dimensional audit and the look-elsewhere count.
  D1 KiDS prefers lambda ~ M^(1/4) over a constant length (chi^2 lower, both footings); M^(1/2) reported.
  D2 the derived form's fitted X lies in 2-7 (L342 4-7, BS1 per-bin 2-6).
  D3 the derived form fits KiDS within Delta chi^2 <= 4 of the EFE-free switch comparator, both footings (BK1's gate).
  D4 with the derived lambda, SPARC is changed <= 1% at R_last and the Sun keeps >= 99.9% of the Galaxy's field.
  Every fit: BS3/BK1 machinery (full covariance, M_b per bin, two-halo b <= 2 per bin), each lens feeling its own
  screened web field (linear LCDM outside 3 Mpc, exact screened window, Maxwell-stacked).
  MUTATE=1 replaces the data with a synthetic draw from the CONSTANT-lambda model (0.7 Mpc): D1 must then FAIL (rc = 1).
  SCOPE: static; the local screening mass is identified in a flat deep-MOND region (the relation v^2 = |a|^2/4 pi G rho
  holds there, not in the baryon-dominated core, where lambda >> r and screening is irrelevant anyway); the field
  equation for a position-dependent mass, its health and tracking are NOT done.

Run from the repository root:  python3 real_research/blind_kernel_2026/BK2_derive_lambda.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious BLAS warning (no result changes)
from scipy.optimize import brentq, lsq_linear
from scipy.spatial import cKDTree
from scipy.special import spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "BK2_derive_lambda"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "BK2", "mutate": MUTATE, "checks": {}, "numbers": {}}
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


# ------------------------------------------------------------------ screened-argument model (BK1), with a mass-dependent length
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
    Nv = np.where(np.isnan(Nv), (Ntab(ie)[0] if ie else 1.0), Nv)
    return Mb * (1 + s * (Nv - 1))
def stack_weights(e_samples):
    w = np.zeros(len(ENODES)); le = np.log10(np.maximum(e_samples, 1e-14))
    below = le < LOGE[0] - 0.5 * (LOGE[1] - LOGE[0]); w[0] += below.sum()
    idx = np.clip(np.rint((le[~below] - LOGE[0]) / (LOGE[1] - LOGE[0])).astype(int), 0, len(LOGE) - 1) + 1
    np.add.at(w, idx, 1.0); return w / w.sum()
def K_out(k, R, lam):
    r = np.geomspace(R, R + 60 * lam, 3000)
    j1 = lambda x: np.where(x > 1e-6, (np.sin(x) / x ** 2 - np.cos(x) / x), x / 3)
    f = (1 + r / lam) * np.exp(-r / lam)
    return np.array([kk * _trap(j1(kk * r) * f, r) for kk in k])
kq = np.geomspace(1e-4, 30, 1500)
LAMG = np.geomspace(0.05, 20, 40)
SIG_L = np.array([math.sqrt(CG ** 2 * _trap(Pk0(kq) * K_out(kq, 3.0, l) ** 2, kq) / (2 * math.pi ** 2)) for l in LAMG])
def sig_e(lam): return float(np.exp(np.interp(np.log(lam), np.log(LAMG), np.log(SIG_L))))
GS = np.random.default_rng(3).standard_normal((100000, 3)); GN = np.linalg.norm(GS, axis=1) / math.sqrt(3)
def esd_screened(Mb, foot, lam):
    w = stack_weights(GN * sig_e(lam) / A0[foot]); nz = [i for i in range(len(ENODES)) if w[i] > 1e-4]
    w = w[nz] / w[nz].sum(); acc = 0
    for wi, ie in zip(w, nz):
        Rq, dS = esd_from_M(model_M(Mb, A0[foot], ie, lam), Mb, 0.0); acc = acc + wi * dS
    return [np.interp(Rd[b], Rq, acc) for b in range(4)]
def vflat(Mb, foot): return (G * Mb * A0[foot]) ** 0.25                     # m/s
HZ = Hlens                                                                   # 1/s at z = 0.25
MPIV = 10 ** 10.6 * MS

# ------------------------------------------------------------------ families
XS = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.5, 10.0, 15.0, 20.0, 30.0]      # lambda = v_flat/(sqrt(X) H)
L0S = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0]                  # lambda = L0 (M/M_piv)^p
FAM = {}
def lam_of(fam, par, Mb, foot):
    if fam == "v/(sqrt(X) H)": return vflat(Mb, foot) / (math.sqrt(par) * HZ) / MPCm
    p = {"const": 0.0, "M^1/4": 0.25, "M^1/2": 0.5}[fam]
    return par * (Mb / MPIV) ** p
for foot in FOOTS:
    for fam, pars in (("v/(sqrt(X) H)", XS), ("const", L0S), ("M^1/4", L0S), ("M^1/2", L0S)):
        arr = np.zeros((len(pars), len(LM), 4, npb))
        for ip, par in enumerate(pars):
            for im, lm in enumerate(LM):
                Mb = 10 ** lm * MS; arr[ip, im] = esd_screened(Mb, foot, lam_of(fam, par, Mb, foot))
        FAM[(foot, fam)] = arr
    arr = np.zeros((1, len(LM), 4, npb))                                     # comparator: EFE-free switch (BS3)
    cmp_ = {}
    for ix, xc in enumerate([0.0, 3.0, 5.0, 7.0, 10.0]):
        a_ = np.zeros((len(LM), 4, npb))
        for im, lm in enumerate(LM):
            Mb = 10 ** lm * MS; Rq, dS = esd_from_M(model_M(Mb, A0[foot], 0, float("inf")), Mb, xc)
            a_[im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
        cmp_[xc] = a_
    FAM[(foot, "comparator")] = cmp_
P(f"model tables built ({time.time() - T0:.0f} s)")
DATA = [np.array(e) for e in Ed]
if MUTATE:
    Lch_ = np.linalg.cholesky(Cf); rgm = np.random.default_rng(777)
    IMS_ = [int(np.argmin(np.abs(LM - l))) for l in (10.2, 10.6, 10.9, 11.2)]
    arr = FAM[("canonical", "const")]; ip = L0S.index(0.7)
    mv = np.concatenate([arr[ip, IMS_[b], b] + T2H[b] for b in range(4)]) + Lch_ @ rgm.standard_normal(4 * npb)
    DATA = [mv[b * npb:(b + 1) * npb] for b in range(4)]
    P("*** MUTATE=1: data replaced by a synthetic draw from the CONSTANT-lambda model (0.7 Mpc, b = 1): D1 must FAIL ***")

def best_family(foot, fam, data, bmax=2.0):
    arr = FAM[(foot, fam)]; best = None
    for ip in range(arr.shape[0]):
        c_, im, bb = fit_2h(arr[ip], data, bmax)
        if best is None or c_ < best[0]: best = (c_, ip, im, bb)
    return best
def comparator(foot, data, bmax=2.0):
    return min(fit_2h(a_, data, bmax)[0] for a_ in FAM[(foot, "comparator")].values())

# ============================================================================================ D0 dimensional audit
banner("D0  CAN A CONSTANT lambda ~ 0.7 Mpc BE DERIVED FROM THE FRAMEWORK'S CONSTANTS? (and what numerology costs)")
c_ = 2.99792458e8; H0s = H0; LH = c_ / H0s / MPCm
Z = math.sqrt(32 * math.pi / 3)
base = {"c/H0": LH, "a0/H0^2 (canonical)": A0["canonical"] / H0s ** 2 / MPCm, "c^2/a0 (canonical)": c_ ** 2 / A0["canonical"] / MPCm}
for k, v in base.items(): P(f"    {k:22s} = {v:.4g} Mpc")
# look-elsewhere: c/H0 x Z^n x Omega_L^m x Omega_m^q x (2 pi)^r, small integer exponents
hits, tot = [], 0
for n in range(-8, 9):
    for m in range(-3, 4):
        for q in range(-3, 4):
            for r_ in range(-3, 4):
                tot += 1; v = LH * Z ** n * OL ** m * Om ** q * (2 * math.pi) ** r_
                if 0.6 <= v <= 0.8: hits.append((n, m, q, r_, round(v, 3)))
P(f"    combinations c/H0 x Z^n Omega_L^m Omega_m^q (2pi)^r with |n|<=8, |m|,|q|,|r|<=3: {tot}; landing in 0.6-0.8 Mpc: {len(hits)}")
P(f"    e.g. {hits[:6]}")
OUT["numbers"]["D0"] = {"base_lengths_Mpc": base, "n_combinations": tot, "n_hits_0.6_0.8": len(hits), "examples": hits[:20]}
check("D0 (documentary) no constant length near 0.7 Mpc follows from (c, H0, a0, G rho): the natural ones are "
      f"{LH:.0f} / {base['a0/H0^2 (canonical)']:.0f} / {base['c^2/a0 (canonical)']:.3g} Mpc; {len(hits)} of {tot} small-exponent "
      "combinations land in 0.6-0.8 Mpc, so any single 'hit' is numerology", len(hits), True, "", load_bearing=False)

# ============================================================================================ D1 mass scaling
banner("D1  WHICH MASS SCALING DOES KiDS WANT FOR lambda?  (two-halo b <= 2, M_b per bin, full covariance)")
R = {}
for foot in FOOTS:
    ref = comparator(foot, DATA); row = {"comparator": ref}
    for fam, pars in (("const", L0S), ("M^1/4", L0S), ("M^1/2", L0S), ("v/(sqrt(X) H)", XS)):
        c2, ip, im, bb = best_family(foot, fam, DATA)
        row[fam] = {"dchi2": c2 - ref, "par": pars[ip], "b": [round(x, 2) for x in bb], "logM": [float(LM[i]) for i in im]}
        P(f"    {foot:9s} {fam:14s}: best {'X' if fam.startswith('v/') else 'L0'} = {pars[ip]:>5}  Delta chi^2 vs comparator {c2 - ref:+7.2f}")
    R[foot] = row
OUT["numbers"]["D1"] = R
d14 = {f_: round(R[f_]["M^1/4"]["dchi2"] - R[f_]["const"]["dchi2"], 2) for f_ in FOOTS}
check("D1 KiDS prefers lambda ~ M^(1/4) (the clock-built v/H scaling) over a constant length: chi^2(M^1/4) < chi^2(const), both footings",
      d14, all(v < 0 for v in d14.values()), "negative = M^(1/4) better")

# ============================================================================================ D2 the derived form
banner("D2  THE DERIVED FORM lambda = v_flat/(sqrt(X) H): v^2 = |a|^2/(4 pi G rho_dyn) and 4 pi G rho_dyn = x H^2 are C-H/K clock scalars")
dX = {f_: R[f_]["v/(sqrt(X) H)"] for f_ in FOOTS}
inrange = all(2.0 <= dX[f_]["par"] <= 7.0 for f_ in FOOTS)
check("D2 the fitted X lies in L342/BS1's switch-threshold range 2-7 (so lambda is the switch's own r_t, no new number)",
      {f_: dX[f_]["par"] for f_ in FOOTS}, inrange, "")
check("D3 the derived form fits KiDS within Delta chi^2 <= 4 of the EFE-free switch comparator, both footings",
      {f_: round(dX[f_]["dchi2"], 2) for f_ in FOOTS}, all(dX[f_]["dchi2"] <= 4 for f_ in FOOTS),
      "BK1's gate, now with lambda derived rather than free")

# ============================================================================================ D4 Sun / SPARC for the derived form
banner("D4  THE DERIVED lambda LEAVES THE SUN AND SPARC ALONE?")
d4 = {}
for foot in FOOTS:
    X = dX[foot]["par"]; worst = 0.0
    for lm, Rlast_kpc in ((8.0, 8.0), (9.0, 15.0), (10.0, 30.0), (10.5, 50.0), (11.0, 80.0), (11.5, 100.0)):
        Mb = 10 ** lm * MS; lam = lam_of("v/(sqrt(X) H)", X, Mb, foot)
        r_m = Rlast_kpc * 1e3 * PCm; s = float(s_scr(np.array([r_m]), lam)[0]); gN = G * Mb / r_m ** 2
        g1 = gN + s * gN * (float(nu_mono_arr(s * gN / A0[foot])) - 1); g0 = gN * float(nu_mono_arr(gN / A0[foot]))
        worst = max(worst, abs(g1 / g0 - 1))
    lam_mw = lam_of("v/(sqrt(X) H)", X, 6e10 * MS, foot) * H0s / HZ                # today, H0
    sun = float(s_scr(np.array([20e3 * PCm]), lam_mw)[0])
    d4[foot] = {"X": X, "worst_sparc_change": worst, "lambda_MW_today_Mpc": lam_mw, "galactic_field_kept": sun}
    P(f"    {foot:9s}: X = {X}: worst SPARC change at R_last {100 * worst:.2f}%;  lambda(MW, z=0) = {lam_mw:.2f} Mpc, Galaxy's field on the Sun kept to {sun:.6f}")
OUT["numbers"]["D4"] = d4
check("D4 with the derived lambda, SPARC changes <= 1% at R_last (1e8-10^11.5 Msun) and the Sun keeps >= 99.9% of the Galaxy's field",
      {f_: f"{100 * v['worst_sparc_change']:.2f}%, {v['galactic_field_kept']:.5f}" for f_, v in d4.items()},
      all(v["worst_sparc_change"] <= 0.01 and v["galactic_field_kept"] >= 0.999 for v in d4.values()), "")

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  A constant lambda cannot be derived: the framework's lengths are {LH:.0f}, {base['a0/H0^2 (canonical)']:.0f} and {base['c^2/a0 (canonical)']:.2g} Mpc, and {len(hits)} of
  {tot} small-exponent combinations of them land at 0.6-0.8 Mpc (numerology, not derivation).  The one length near 1 Mpc
  the construction supplies is mass-dependent: lambda = v_flat/(sqrt(X) H), from C-H/K's own clock scalars.
  KiDS: M^(1/4) vs constant {d14['canonical']:+.2f} / {d14['alt']:+.2f};  derived form best X = {dX['canonical']['par']} / {dX['alt']['par']} at Delta chi^2
  {dX['canonical']['dchi2']:+.2f} / {dX['alt']['dchi2']:+.2f};  constant {R['canonical']['const']['dchi2']:+.2f} / {R['alt']['const']['dchi2']:+.2f};  M^(1/2) {R['canonical']['M^1/2']['dchi2']:+.2f} / {R['alt']['M^1/2']['dchi2']:+.2f}.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
