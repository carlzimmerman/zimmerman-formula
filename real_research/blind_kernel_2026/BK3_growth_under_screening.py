#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BK3 -- DOES THE SCREENED KERNEL KEEP LINEAR GROWTH LCDM-LIKE ON ITS OWN, OR IS THE SWITCH STILL NEEDED?

BK1/BK2: the C-H/K kernel acting on the Yukawa-screened field (lambda ~ 0.6-0.8 Mpc) is blind to the web's field and
fits KiDS best with NO switch (x_c = 0).  But the switch's job was growth (L341: without it sigma_8 = 18-27).

THE LINEAR RESPONSE (exact within the QUMOND form).  On the web the kernel's argument g_b = g_s + g_L is dominated by
the small-scale screened field g_s (modes k >~ 1/lambda survive; the long modes are screened as (k lambda)^2).  The
long mode's phantom is the isotropic average of d[(nu - 1) g]/dg over g_s:
      phantom_L = C_eff g_b,L,   C_eff = <nu(w) - 1> + <w nu'(w)>/3   (Maxwellian g_s, rms sigma_s),
so the long mode feels G_eff(k, a) = 1 + C_eff(a) k^2/(k^2 + (a/lambda)^2)  (k comoving, lambda physical).
sigma_s from linear LCDM (all modes, screened window); nonlinear small-scale power is larger, so x3 is also run
(a larger sigma_s lowers C_eff -- the linear value is the conservative, larger boost).

CHECKS (gates set before the run)
  G1 with the screening alone (no switch, lambda = 0.7 Mpc) |sigma_8 - 0.811| <= 0.03, both footings, sigma_s x1 and x3.
     (0.5 and 1.0 Mpc reported.)
  G2 (documentary) if the switch must stay: KiDS with screening (lambda = 0.7) and the switch at x_c = 4/5/7.
  MUTATE=1 removes the screening: the kernel sees the full web field; G1 must FAIL (rc = 1).
  SCOPE: linear growth from a = 0.02 with LCDM initial conditions and background; C_eff from a Maxwellian small-scale
  field (the web's small-scale field is non-Gaussian); no switch in G1.

Run from the repository root:  python3 real_research/blind_kernel_2026/BK3_growth_under_screening.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious BLAS warning (no result changes)
from scipy.optimize import brentq, lsq_linear
from scipy.spatial import cKDTree
from scipy.special import spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "BK3_growth_under_screening"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "BK3", "mutate": MUTATE, "checks": {}, "numbers": {}}
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


from scipy.integrate import solve_ivp
# ------------------------------------------------------------------ the kernel's linear response on a noisy web
WG = np.geomspace(1e-9, 1e4, 4001)
NU = nu_mono_arr(WG); DNU = np.gradient(NU, WG)
def C_eff(sig3_over_a0):
    """<(nu - 1)> + <w nu'(w)>/3 over an isotropic Maxwellian small-scale field of 3-D rms sig (units of a0)."""
    if sig3_over_a0 <= 0: return 0.0
    s1 = sig3_over_a0 / math.sqrt(3)
    p = math.sqrt(2 / math.pi) * WG ** 2 / s1 ** 3 * np.exp(-WG ** 2 / (2 * s1 ** 2))
    return float(_trap(p * ((NU - 1) + WG * DNU / 3), WG))
def sig_small(a, lam_phys_mpc, boost=1.0):
    """3-D rms of the SCREENED Newtonian field at a random point (all modes), linear LCDM, physical, units m/s^2."""
    z = 1 / a - 1; m_c = a / lam_phys_mpc                        # comoving screening wavenumber
    D = growth(z) if z > 0 else 1.0
    I = _trap(Pk0(KK) * (KK ** 2 / (KK ** 2 + m_c ** 2)) ** 2, KK) / (2 * math.pi ** 2)
    return boost * 1.5 * Om * H0 ** 2 / a ** 2 * D * math.sqrt(I) * Mpc
def sigma8_modified(lam, foot, boost=1.0, a_start=0.02):
    ks = np.geomspace(1e-3, 5, 60); A = np.geomspace(a_start, 1, 60)
    Cs = np.array([C_eff(sig_small(a, lam, boost) / A0[foot]) if np.isfinite(lam) else 0.0 for a in A])
    ratio = []
    for k in ks:
        def rhs(lna, y):
            a = math.exp(lna); E2 = Om / a ** 3 + OL; Om_a = Om / a ** 3 / E2
            dlnH = -1.5 * Om / a ** 3 / E2
            C = np.interp(lna, np.log(A), Cs); m_c = a / lam
            Geff = 1 + C * k ** 2 / (k ** 2 + m_c ** 2)
            return [y[1], -(2 + dlnH) * y[1] + 1.5 * Om_a * Geff * y[0]]
        def rhs0(lna, y):
            a = math.exp(lna); E2 = Om / a ** 3 + OL; Om_a = Om / a ** 3 / E2
            return [y[1], -(2 - 1.5 * Om / a ** 3 / E2) * y[1] + 1.5 * Om_a * y[0]]
        y0 = [a_start, a_start]
        s1 = solve_ivp(rhs, (math.log(a_start), 0), y0, rtol=1e-6).y[0, -1]
        s0 = solve_ivp(rhs0, (math.log(a_start), 0), y0, rtol=1e-6).y[0, -1]
        ratio.append(s1 / s0)
    ratio = np.array(ratio); T2 = np.interp(np.log(KK), np.log(ks), ratio ** 2, left=ratio[0] ** 2, right=ratio[-1] ** 2)
    s8 = math.sqrt(_trap(PK0 * T2 * W_th(KK * 8 / h) ** 2 * KK ** 2, KK) / (2 * math.pi ** 2))
    return s8, dict(zip(np.round(ks[::10], 4).tolist(), np.round(ratio[::10], 3).tolist())), Cs

# ============================================================================================ G1 growth
banner("G1  LINEAR GROWTH WITH THE SCREENED KERNEL AND NO SWITCH: G_eff(k) = 1 + C_eff k^2/(k^2 + m^2), sigma_8")
LAMS_G = [0.5, 0.7, 1.0] if not MUTATE else [float("inf")]
if MUTATE: P("*** MUTATE=1: screening removed (lambda = infinity): the kernel sees the unscreened web -> growth must blow up ***")
GR = {}
for foot in FOOTS:
    for lam in LAMS_G:
        for boost in (1.0, 3.0):
            if MUTATE:
                # unscreened: argument = full Newtonian web field
                s8 = None
                A = np.geomspace(0.02, 1, 30)
                Cs = [C_eff(sig_small(a, 1e9, boost) / A0[foot]) for a in A]
                GR[(foot, lam, boost)] = {"sigma8": float("nan"), "C_eff_today": Cs[-1]}
                P(f"    {foot:9s} lambda = inf, field x{boost}: C_eff today = {Cs[-1]:.1f} (the linear web's force boosted {1 + Cs[-1]:.0f}x)")
                continue
            s8, rat, Cs = sigma8_modified(lam, foot, boost)
            GR[(foot, lam, boost)] = {"sigma8": s8, "D_ratio_by_k": rat, "C_eff_today": float(Cs[-1]),
                                      "sigma_small_today_over_a0": sig_small(1.0, lam, boost) / A0[foot]}
            P(f"    {foot:9s} lambda = {lam} Mpc, small-scale field x{boost}: rms {sig_small(1.0, lam, boost) / A0[foot]:.2e} a0, "
              f"C_eff today {Cs[-1]:.1f};  sigma_8 = {s8:.3f} (LCDM {S8});  D/D_LCDM by k: {rat}")
OUT["numbers"]["G1"] = {"|".join(map(str, k)): v for k, v in GR.items()}
if MUTATE:
    ok_g = False
else:
    ok_g = all(abs(GR[(f_, 0.7, b_)]["sigma8"] - S8) <= 0.03 for f_ in FOOTS for b_ in (1.0, 3.0))
check("G1 with the screening alone (no switch, lambda = 0.7 Mpc) the linear web grows as in LCDM: |sigma_8 - 0.811| <= 0.03, "
      "both footings, small-scale field x1 and x3", {"|".join(map(str, k)): round(v["sigma8"], 3) for k, v in GR.items() if k[1] == 0.7}
      if not MUTATE else "unscreened", ok_g, "if it passes, the screening does the switch's growth job too and the switch can go")

# ============================================================================================ G2 KiDS with switch + screening
banner("G2  IF THE SWITCH STAYS: KiDS with screening (lambda = 0.7) AND the switch at L342's x_c (4-7)")
XCS2 = [0.0, 4.0, 5.0, 7.0]
LM = np.round(np.arange(9.8, 11.8001, 0.02), 4)
ENODES = [0.0] + [float(v) for v in np.geomspace(1e-7, 0.05, 40)]; LOGE = np.log10(np.array(ENODES[1:]))
NT = {}
def Nt(ie):
    if ie not in NT: NT[ie] = N_of(YT, ENODES[ie])
    return NT[ie]
def s_scr(r_m, lam): x = r_m / (lam * MPCm); return (1 + x) * np.exp(-x)
def model_M(Mb, a0, ie, lam):
    s = s_scr(rr, lam); yb = np.maximum(s * G * Mb / rr ** 2 / a0, 1e-12)
    Nv = nu_mono_arr(yb) if ie == 0 else np.interp(np.log10(yb), LYT, Nt(ie), left=np.nan)
    Nv = np.where(np.isnan(Nv), (Nt(ie)[0] if ie else 1.0), Nv); return Mb * (1 + s * (Nv - 1))
def stack_w(e):
    w = np.zeros(len(ENODES)); le = np.log10(np.maximum(e, 1e-14)); below = le < LOGE[0] - 0.5 * (LOGE[1] - LOGE[0]); w[0] += below.sum()
    idx = np.clip(np.rint((le[~below] - LOGE[0]) / (LOGE[1] - LOGE[0])).astype(int), 0, len(LOGE) - 1) + 1
    np.add.at(w, idx, 1.0); return w / w.sum()
SIG07 = 4.55e-05                                                       # BK1 C2: screened web field outside 3 Mpc at lambda = 0.7, units a0 (canonical)
GN_ = np.linalg.norm(np.random.default_rng(3).standard_normal((100000, 3)), axis=1) / math.sqrt(3)
K2 = {}
for foot in FOOTS:
    w = stack_w(GN_ * SIG07 * A0["canonical"] / A0[foot]); nz = [i for i in range(len(ENODES)) if w[i] > 1e-4]; w = w[nz] / w[nz].sum()
    arr = np.zeros((len(XCS2), len(LM), 4, npb)); cmp_ = np.zeros((5, len(LM), 4, npb))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MS; Ms = [model_M(Mb, A0[foot], ie, 0.7) for ie in nz]
        for ix, xc in enumerate(XCS2):
            acc = 0
            for wi, M in zip(w, Ms):
                Rq, dS = esd_from_M(M, Mb, xc); acc = acc + wi * dS
            arr[ix, im] = [np.interp(Rd[b], Rq, acc) for b in range(4)]
        M0 = Mb * nu_mono_arr(G * Mb / rr ** 2 / A0[foot])
        for ix, xc in enumerate([0.0, 3.0, 5.0, 7.0, 10.0]):
            Rq, dS = esd_from_M(M0, Mb, xc); cmp_[ix, im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
    DATA = [np.array(e) for e in Ed]
    ref = min(fit_2h(cmp_[i], DATA, 2.0)[0] for i in range(5))
    K2[foot] = {str(xc): fit_2h(arr[ix], DATA, 2.0)[0] - ref for ix, xc in enumerate(XCS2)}
    P(f"    {foot:9s}: Delta chi^2 vs the EFE-free switch comparator at x_c = " + ", ".join(f"{k}: {v:+.1f}" for k, v in K2[foot].items()))
OUT["numbers"]["G2"] = K2
check("G2 (documentary) screening + switch at L342's thresholds on KiDS", K2, True,
      "the price of keeping the switch for growth", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
if not MUTATE:
    P(f"""  sigma_8 with the screening alone (lambda = 0.7 Mpc): {', '.join(f"{f_} x{b_:.0f}: {GR[(f_, 0.7, b_)]['sigma8']:.3f}" for f_ in FOOTS for b_ in (1.0, 3.0))}
  (LCDM {S8}).  Screening + switch on KiDS (x_c 4/5/7): canonical {K2['canonical']['4.0']:+.1f}/{K2['canonical']['5.0']:+.1f}/{K2['canonical']['7.0']:+.1f}, alt {K2['alt']['4.0']:+.1f}/{K2['alt']['5.0']:+.1f}/{K2['alt']['7.0']:+.1f}.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
