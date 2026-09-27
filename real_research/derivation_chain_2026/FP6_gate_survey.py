#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP6 -- THE LINCHPIN FROM A SURVEY ANGLE: which action-level mechanism can switch the C-H/K core's MOND sector off on its
own FRW and in the linear web while leaving galaxies and the Solar System alone?  Nonlocal scale gates (b) and kernel
regularisations (e), each tested against FP3's lemma, and their combination.

WHY.  FP1/FP2/FP5 (committed) all point at one link.  Around the core's own FRW (zero field) the QUMOND tangent C = nu - 1 is
infinite: FP5 finds U pinned and alpha_eff = 2 + alpha_c (Hadamard ill-posed, w^2/k^2 = -alpha_c c_2/((2+alpha_c)(2+3c_2))),
and L341 finds sigma_8 = 18-27 in the linear web.  FP3 (committed 9b265b331) proved a lemma for LOCAL gates that multiply the
MOND energy: exactly zero on FRW and one in galaxies means convex somewhere, and convex is an anti-pressure; stable local
gates are concave and chord-bounded.  This lane surveys the classes FP3 does not cover and asks, for each, whether it
escapes that lemma and why:
  (b) a NONLOCAL scale gate: the kernel reads a band-passed field, built from C-H's own heat branch read out at two
      diffusion times;
  (e) a KERNEL REGULARISATION: a finite (or zero) zero-field tangent that keeps the galaxy law at y = 0.01-100;
  (b)+(e) their combination (the class (f) outcome);
  (a), (c), (d) are local multiplier gates: FP3's lemma, CV4 and one derived symbol (S7) close them; they are not re-run.

THE CORE (as FP1/FP2/FP5 vary it; alpha = a0/c^2, b = xi^2/2, q'(Z) = nu(sqrt Z) - 1 with nu = P2, nu_mono the alternative):
  I = c^3/(16 pi G) Int sqrt(-g) { R - 2 Lambda + 2 h^{mn}(D_m U - a_m)(D_n U - a_n) + 2 alpha^2 q(h^{mn} D_m W_b D_n W_b/alpha^2)
        + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - U) + alpha_c a_m a^m - c_2 (K - <K>_h)^2 } + GHY + S_m[g]
THE CLASSES (the action terms tested; everything else in the core unchanged):
  (b)  band-pass:  2 alpha^2 q(h^{mn} D_m(W_b - W_B) D_n(W_b - W_B)/alpha^2) + Int_0^B dz L (d_z W - Delta_h W) + lambda_0 (W_0 - U),
       B = L(<K>_h)^2/2 > b,  L(<K>_h) = L_Lambda Omega_L(<K>_h)^(n/2),  Omega_L(K) = 3 Lambda/K^2 (the vacuum share, a leaf average).
       One heat branch, read out at two diffusion times: the kernel sees (S_xi - S_L) U.
  (e1) shifted kernel:  q_r'(Z) = sqrt(1 + 1/(sqrt Z + y_r)) - 1   (finite zero-field tangent C_0 = sqrt(1 + 1/y_r) - 1).
  (e2) cut-off tangent:  q_c'(Z) = (nu(sqrt Z) - 1) c(sqrt Z/y_th),  c(x) = x^m/(1 + x^m)   (zero zero-field tangent).
  (e3) running cut-off:  (e2) with y_th(<K>_h) = y_Lambda Omega_L(<K>_h)^(-p') (a leaf average; the floor rises into the past).
  (H)  the combination (b) + (e3): the kernel q_c(|D(W_b - W_B)|^2/alpha^2; <K>_h).
The footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt), FP0.

CHECKS
  K  CONTROLS: K1 the growth yardstick reproduces L341 (LCDM 0.8101; ungated nu_mono 23.314 rms / 17.713 per-mode);
     K2 the KiDS lead-grade machinery reproduces L341 F7 (118.0 untruncated, 106.8 cut at 1 Mpc); K3 the LG shell model
     reproduces FP1 E1 / XR4 (nu_RAR isolated 1.929 / 2.021 Mpc); K4 the smoothed-shell mass formula against quadrature and
     the band-passed phantom's L -> oo limit (isolated P2); K5 FP2's committed quadratic block (read from its .out) gives
     FP2's det, FP5's khronon dispersion w^2 = c_2 (2 - E) k^2/(E (2 + 3 c_2)), E = alpha_c + 2C/(1+C), and the static gain.
  S  THE SECOND VARIATION, symbolically (sympy): S1 the heat branch with two readouts eliminated exactly: C_eff = C (e^{-bk^2}
     - e^{-Bk^2})^2; S1b the nonlinear static field equation from the discrete action (the variation band-passes the phantom's
     output too); S2 the discrete heat block: Schur complement C (sigma_n - sigma_N)^2, determinant kernel-free (no mode
     added); S3 the band-pass has no W''(dX)^2 term (the lemma's anti-pressure is absent); S4 the kernel families: closed
     forms, zero-field tangents, and C_T, C_L >= 0 for EVERY cut-off shape when the cut-off multiplies the tangent (the
     energy-multiplied control carries c''); S5 the FRW linearisation of every class from K5's block: E(C_eff) < 2 or not,
     G_eff, slip; S6 order counting of the MOND energy around FRW; S7 class (d): a tidal-invariant gate's (Phi, u) symbol
     has a zero wherever W' > 0.
  E  CLASS (e) ALONE: E1 the galaxy price of each regularisation; E2 the linear web's field y_web(z) against the range where
     galaxies need P2; E3 THE OVERLAP: even the most generous local-in-y kernel fails sigma_8 (load-bearing FAIL of (e));
     E4 the (e) FRW numbers over the alpha_c window.
  B  CLASS (b): B1 statics (SPARC range, Solar-System gain, Gauss compensation); B2 sigma_8 over (L_Lambda, n);
     B3 the flagship floor on L(2.5); B4 forest vs flagship (FAIL); B5 KiDS vs L(0.25); B6 the KiDS-LG pincer, transformed
     (FAIL); B7 (reported) the web field left in nu's argument.
  H  THE COMBINATION (b) + (e3): H1 the window scan (KiDS scored with the floor); H2 the headline cell, every gate, both
     footings, both yardstick modes, nu_mono, the forest filter scale, the k-grid and the ODE tolerance; H2b E < 2 at every field
     and epoch (FP5's band gone, not only the FRW point); H2c (reported) how far in z the flagship survives; H3 the Local Group at
     every KiDS-passing cell (FAIL); H4 the constants.
  T  the class table.   W  the ledger.   G1 (reported) whether any class passes G-1 whole.
MUTATE=1 removes the band-pass (the kernel reads the plain filtered field, L -> oo) in classes (b) and (H): the combination's
sigma_8 check must FAIL (rc = 1).

SCOPE.  Frozen-coefficient linear theory and the record's growth yardstick (L341/L142: EH98, growing-mode ICs, rms and
per-mode field arguments); the forest is a LINEAR-THEORY PROXY (the 1D projection of the linear matter power with a Gaussian
IGM filter, not the flux P1D of L347's pipeline); KiDS is scored at lead grade (L341 F7: isolated lenses, M_b free per bin,
no 2-halo); the LG is XR4's point-mass + Lambda shell model.  No particle-mesh or N-body run.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP6_gate_survey.py
"""
import os, re, sys, json, math, time, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")      # spurious macOS-Accelerate BLAS flags (L341)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP6_gate_survey" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP6", "gate": "G-1 (survey)", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()
BANDPASS = not MUTATE                                        # MUTATE: the kernel reads the plain field in (b) and (H)


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 114 + "\n" + t + "\n" + "=" * 114)


def check(name, measured, ok, load_bearing=True, reading=None):
    CH.append((name, bool(ok), load_bearing))
    OUT["checks"][name] = {"ok": bool(ok), "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")


def el():
    return f"[{time.time() - T0:.0f} s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the band-pass is removed (L -> oo) in classes (b) and (H) -- H2's sigma_8 check must FAIL ***")

# ================================================================================================= constants
c = 2.99792458e8; Mpc = 3.0856775814913673e22; kpc = Mpc / 1e3; G = 6.67430e-11; MSUN = 1.98847e30
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}           # FP0's footings
A0_L341 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}      # L341's inputs (controls only)
FOOTS = ("canonical", "alt")
MODES = ("rms", "permode")
C2W = 7.3e-3                                                # c_2 in the tracking weight (L341/FP3 convention)
ALPHA_C = (9.62e-14, 3.2e-9)                                # FP5 E: the alpha_c window
Y_R = 1e-6                                                  # the (e1) regularisation used with class (b) alone
SIG8_BAND = (0.922, 1.05)                                   # record floor (S_8 strict) and L341 F4's 5% ceiling
SIG8_TIGHT = 1.02                                           # FP3's ceiling, reported alongside
FOREST_TOL = 0.10                                           # the record's 10% (here on the LINEAR PROXY)
FLAG_TOL = 0.05                                             # FP3 C4b: flagship zero-point shift <= 0.05 dex
SPARC_TOL = 0.01                                            # galaxy law intact at y = 0.01-100 to 0.01 dex
KIDS_TOL = 9.0                                              # FP1 E: d chi^2 <= +9
LG_R0, LG_SIG, LG_EDGE = 0.96, 0.03, 0.96 * 10 ** 0.10      # XR4/FP1: 0.96 +- 0.03 Mpc; +0.10 dex band edge 1.21 Mpc
Z_KIDS, Z_FLAG = 0.25, 2.5

# ================================================================================================= growth yardstick (L341)
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100 * h * 1e3 / Mpc; rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB ** 4 / c ** 3) / rho_crit0; Or = Og * (1 + N_eff * (7 / 8) * (4 / 11) ** (4 / 3))
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om - Or
SIG8 = 0.811


def T_EH98(k):
    th = T_CMB / 2.7; s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b ** 0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om) ** 2
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s / h) ** 4)); q = k * th * th / ge
    L = math.log(2 * math.e + 1.8 * q); Cc = 14.2 + 731.0 / (1 + 62.5 * q); return L / (L + Cc * q * q)


def P_un(kh): return (kh * h) ** ns * T_EH98(kh * h) ** 2
def Wth(x): return 3 * (math.sin(x) - x * math.cos(x)) / x ** 3


PN = (SIG8 / math.sqrt(quad(lambda kh: kh ** 2 * P_un(kh) * Wth(8 * kh) ** 2 / (2 * math.pi ** 2), 1e-4, 60, limit=600)[0])) ** 2
def Delta_lin0(kh): return math.sqrt(kh ** 3 * PN * P_un(kh) / (2 * math.pi ** 2))


KH = np.logspace(math.log10(0.02), math.log10(20.0), 48)             # L341's grid (sigma_8)
KHF = np.logspace(math.log10(0.02), math.log10(100.0), 96)           # extended grid (forest proxy)
W8 = np.array([Wth(8 * k) ** 2 for k in KH])
def sigma8_of(D0): return math.sqrt(np.trapz(D0 ** 2 * W8, np.log(KH)))
Ez = lambda a: math.sqrt(Or / a ** 4 + Om / a ** 3 + OL)
dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / Ez(a) ** 2
OmL_a = lambda a: OL / (Or / a ** 4 + Om / a ** 3 + OL)                 # Omega_L(<K>) = 3 Lambda/K^2 on FRW
OmL_z = lambda z: OmL_a(1.0 / (1.0 + z))
A_I = 1 / 1001.0
_r0 = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om / math.exp(3 * N_) / Ez(math.exp(N_)) ** 2) * Y[0] - (2 + dlnH(math.exp(N_))) * Y[1]],
                (math.log(A_I), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]
DI = np.array([Delta_lin0(k) for k in KH]) / _r0
DIF = np.array([Delta_lin0(k) for k in KHF]) / _r0
DREF = np.array([Delta_lin0(k) for k in KH])


# ---- kernels
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM) / y
def nu_p2(y, yr=0.0): return np.sqrt(1.0 + 1.0 / (np.maximum(np.asarray(y, float), 1e-300) + yr))
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (-np.expm1(-np.sqrt(y)))
def cutfac(y, yth, m):
    if yth is None or yth <= 0:
        return np.ones_like(np.asarray(y, float))
    x = np.maximum(np.asarray(y, float), 0.0) / yth
    return x ** m / (1.0 + x ** m)


def gfield(D, a, KHg):
    rho = Om * rho_crit0 / a ** 3
    return 4 * math.pi * G * rho * np.abs(D) / (KHg * h / (a * Mpc))


def growth(model, a0v, mode="rms", KHg=None, Dig=None, zs_out=(), c2=C2W, kernel="p2", rtol=1e-6):
    """L341's integrator, generalised: delta_k'' + (2 + dlnH) delta_k' = 1.5 Om(a) [1 + C_eff,k w_k] delta_k with
    C_eff,k = (nu(y) - 1) c(y/y_th) h_k^2, y the kernel's argument (the rms or the mode's own band-passed field), w the
    tracking weight 1/(1 + (H/(c_s k))^2), c_s^2 = c_2 c^2/(C_eff (2 + 3 c_2)); rms mode evaluates w at 1 h/Mpc (L341)."""
    KHg = KH if KHg is None else KHg; Dig = DI if Dig is None else Dig
    nk = len(KHg); m341 = KHg <= 20.0 * 1.0001
    kk341 = KHg[m341]; norm341 = np.trapz(1 / kk341, kk341)
    def rhs(N_, Y):
        a = math.exp(N_); D = Y[:nk]; Dp = Y[nk:]
        gk = gfield(D, a, KHg)
        hk = model["hfac"](a, KHg)
        gb = gk * hk
        if mode == "rms":
            y = np.full(nk, math.sqrt(np.trapz(gb[m341] ** 2 / kk341, kk341) / norm341) / a0v)
        else:
            y = gb / a0v
        nu = nu_mono(y) if kernel == "mono" else nu_p2(y, model.get("yr", 0.0))
        Ce = (nu - 1.0) * model["cut"](y, a) * hk ** 2
        Ce = np.maximum(Ce, 0.0)
        cs = c * np.sqrt(c2 / (np.maximum(Ce, 1e-300) * (2 + 3 * c2)))
        kk = (1.0 * h / (a * Mpc)) if mode == "rms" else KHg * h / (a * Mpc)
        wt = 1.0 / (1.0 + (H0 * Ez(a) / (cs * kk)) ** 2)
        return np.concatenate([Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * (1.0 + Ce * wt) * D - (2 + dlnH(a)) * Dp])
    Nout = sorted({math.log(1 / (1 + z)) for z in zs_out if z > 0}) + [0.0]
    sol = solve_ivp(rhs, (math.log(A_I), 0.0), np.concatenate([Dig, Dig]), method="LSODA", rtol=rtol, atol=1e-24, t_eval=Nout)
    return {round(1 / math.exp(N_) - 1, 6): sol.y[:nk, i] for i, N_ in enumerate(sol.t)}


def lcdm_model():
    return {"hfac": lambda a, k: np.ones_like(k), "cut": lambda y, a: np.zeros_like(np.asarray(y, float))}


def core_model(yr=0.0):
    return {"hfac": lambda a, k: np.ones_like(k), "cut": lambda y, a: np.ones_like(np.asarray(y, float)), "yr": yr}


def L_phys(LL, n, a):                                       # the band-pass length on the leaf [Mpc, physical]
    return LL * OmL_a(a) ** (n / 2.0)


def bandpass_model(LL, n, yr=Y_R, floor=None, bandpass=None):
    """(b) [+ (e3)]: h_k = 1 - exp(-(k L_com)^2/2) (xi -> 0); floor = (y_th(0.25), p', m) or None."""
    bp = BANDPASS if bandpass is None else bandpass
    def hfac(a, k):
        if not bp:
            return np.ones_like(k)
        Lc = L_phys(LL, n, a) / a
        return 1.0 - np.exp(-0.5 * (k * h * Lc) ** 2)
    if floor is None:
        cut = lambda y, a: np.ones_like(np.asarray(y, float))
    else:
        y25, pp, mm = floor
        yL = y25 * OmL_z(Z_KIDS) ** pp
        cut = lambda y, a: cutfac(y, yL * OmL_a(a) ** (-pp), mm)
    return {"hfac": hfac, "cut": cut, "yr": (yr if floor is None else 0.0)}


def y_th_z(floor, z):
    y25, pp, mm = floor
    return y25 * (OmL_z(Z_KIDS) / OmL_z(z)) ** pp


REF_F = growth(lcdm_model(), A0["canonical"], KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))


def forest_proxy(res, kF=15.0, zs=(2.0, 3.0), kpars=(0.2, 0.5, 1.0, 2.0), KHg=None, REFg=None):
    """LINEAR-THEORY PROXY for the forest: P1D(k_par) = (1/2pi) Int_{k_par} P3D(k) exp(-k^2/k_F^2) k dk, model / LCDM - 1."""
    KHg = KHF if KHg is None else KHg; REFg = REF_F if REFg is None else REFg
    worst = 0.0; rows = {}
    for z in zs:
        P3m = res[z] ** 2 / KHg ** 3; P3r = REFg[z] ** 2 / KHg ** 3
        for kp in kpars:
            m = KHg >= kp
            fm = np.trapz(P3m[m] * KHg[m] * np.exp(-(KHg[m] / kF) ** 2), KHg[m])
            fr = np.trapz(P3r[m] * KHg[m] * np.exp(-(KHg[m] / kF) ** 2), KHg[m])
            rows[(z, kp)] = fm / fr - 1.0; worst = max(worst, abs(fm / fr - 1.0))
    return worst, rows


S8_LCDM = sigma8_of(growth(lcdm_model(), A0["canonical"])[0.0])


def s8ratio(model, foot, mode, kernel="p2"):
    return sigma8_of(growth(model, A0[foot], mode=mode, kernel=kernel)[0.0]) / S8_LCDM


# ================================================================================================= static machinery
G6, MS6, PCm = 6.6743e-11, 1.98892e30, 3.0857e16; MPCm = PCm * 1e6
RG = np.geomspace(1e-5, 80.0, 1000) * MPCm                                   # the phantom grid [m]
RGM = np.sqrt(RG[1:] * RG[:-1])                                               # shell midpoints
_FCACHE = {}


def gfrac_smooth(x):                                                         # enclosed fraction of a 3D Gaussian (sigma = L)
    return erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2)


def shell_frac(r, rp, L):                                                     # a unit shell at rp, Gaussian-smoothed, inside r
    s = math.sqrt(2) * L; rp = np.maximum(rp, 1e-300)
    return 0.5 * (erf((r + rp) / s) + erf((r - rp) / s)) - (L / (rp * math.sqrt(2 * math.pi))) * (
        np.exp(-(r - rp) ** 2 / (2 * L * L)) - np.exp(-(r + rp) ** 2 / (2 * L * L)))


def Fmat(L_m):
    key = round(math.log(L_m), 9)
    if key not in _FCACHE:
        if len(_FCACHE) > 40:
            _FCACHE.clear()
        _FCACHE[key] = shell_frac(RG[:, None], RGM[None, :], L_m)
    return _FCACHE[key]


def phantom(Mb_kg, a0, L_m=None, yth=None, m=4, kernel="p2", out_filter=True):
    """Enclosed phantom mass of a point mass under the (band-passed) kernel, xi -> 0:
    g_bp = (1 - S_L) g_N (Gaussian-smoothed point mass, sigma = L per axis); raw phantom M_raw = (nu_eff - 1) g_bp r^2/G;
    the variation's output filter (1 - S_L) subtracts the Gaussian-smoothed raw phantom (shell by shell)."""
    if not BANDPASS:
        L_m = None                                                            # MUTATE: the kernel reads the plain field
    gN = G6 * Mb_kg / RG ** 2
    gbp = gN if L_m is None else gN * (1.0 - gfrac_smooth(RG / L_m))
    y = gbp / a0
    nu = nu_mono(y) if kernel == "mono" else (nu_rar(y) if kernel == "rar" else nu_p2(y))
    Mraw = (nu - 1.0) * cutfac(y, yth, m) * gbp * RG ** 2 / G6
    if L_m is None or not out_filter:
        return Mraw
    dM = np.diff(Mraw)
    Ms = Fmat(L_m) @ dM + Mraw[0] * gfrac_smooth(RG / L_m)
    return Mraw - Ms


def law_dev_dex(Mb_msun, a0, y, L_mpc=None, yth=None, m=4):
    """log10 of (the class's spherical law / P2) at the radius where g_N = y a0."""
    Mb = Mb_msun * MSUN
    r = math.sqrt(G6 * Mb / (y * a0))
    Mph = phantom(Mb, a0, None if L_mpc is None else L_mpc * MPCm, yth, m)
    g = G6 * (Mb + np.interp(r, RG, Mph)) / r ** 2
    return math.log10(g / (float(nu_p2(y)) * G6 * Mb / r ** 2))


# ---- KiDS lead grade (L341 F7's machinery, with the Abel projection as a matrix)
_B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
_Rd, _Ed, _Sd = [], [], []
for _b in (1, 2, 3, 4):
    _d = np.genfromtxt(os.path.join(_B, f"Fig-3_Lensing-rotation-curves_Massbin-{_b}.txt"), comments="#")
    _Rd.append(_d[:, 0]); _Ed.append(_d[:, 1] / _d[:, 4]); _Sd.append(_d[:, 3] / _d[:, 4])
_cv = np.genfromtxt(os.path.join(_B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
_vv = _cv[:, 4] / _cv[:, 6]; _npb = len(_Rd[0])
_Cf = _vv.reshape(4, 4, _npb, _npb).transpose(0, 2, 1, 3).reshape(4 * _npb, 4 * _npb)
_Ci = np.linalg.inv((_Cf + _Cf.T) / 2)
RR = np.geomspace(1e-3, 30, 4000) * MPCm; RP = np.geomspace(0.02, 4, 240) * MPCm
_WP = np.zeros((len(RP), len(RR)))
for _i, _Rv in enumerate(RP):                                                 # L341's trapz on r > R (1 + 1e-7), as a matrix
    _m = np.where(RR > _Rv * 1.0000001)[0]; _r = RR[_m]
    _w = np.zeros(len(_r)); _dr = np.diff(_r); _w[:-1] += 0.5 * _dr; _w[1:] += 0.5 * _dr
    _WP[_i, _m] = 2 * _w * _r / np.sqrt(_r ** 2 - _Rv ** 2)
LM = np.linspace(9.8, 11.8, 21)


def esd_of_M(M, Mb):
    rho = np.gradient(M - Mb, RR) / (4 * math.pi * RR ** 2)
    Sig = _WP @ rho
    Mc = np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * RP[1:] + Sig[:-1] * RP[:-1]) * np.diff(RP))]) * 2 * math.pi + math.pi * RP[0] ** 2 * Sig[0]
    return RP / MPCm, (Mc / (math.pi * RP ** 2) - Sig + Mb / (math.pi * RP ** 2)) * PCm ** 2 / MS6


def kids_chi2(Mfun):
    """Mfun(Mb_kg) -> enclosed total mass on RR; M_b free per bin on L341's grid; full covariance."""
    cache = {lm: esd_of_M(Mfun(10 ** lm * MS6), 10 ** lm * MS6) for lm in LM}
    mods = []
    for b in range(4):
        best = None
        for lm in LM:
            Rq, dS = cache[lm]; mk = np.interp(_Rd[b], Rq, dS); c_ = float(np.sum(((_Ed[b] - mk) / _Sd[b]) ** 2))
            if best is None or c_ < best[0]:
                best = (c_, mk)
        mods.append(best[1])
    dv = np.concatenate(_Ed) - np.concatenate(mods)
    return float(dv @ _Ci @ dv)


def kids_class(a0, L_mpc=None, yth=None, m=4):
    def Mf(Mb):
        Mph = phantom(Mb, a0, None if L_mpc is None else L_mpc * MPCm, yth, m)
        return Mb + np.interp(RR, RG, Mph)
    return kids_chi2(Mf)


# ---- LG: XR4's point-mass + Lambda shell model (as FP1 E1 copies it: XR4_lg_zero_velocity_construction.py:60-127)
LG_G, LG_Mpc, LG_Msun = 6.674e-11, 3.0857e22, 1.989e30
LG_h = 0.674; LG_H0 = 100 * LG_h * 1e3 / LG_Mpc
LG_OM = 0.02237 / LG_h ** 2 + 0.1200 / LG_h ** 2; LG_OL = 1 - LG_OM
LG_A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LG_MB = 1.145e11
LG_OmL = lambda a: LG_OL / (LG_OM / a ** 3 + LG_OL)
LNA_T = np.linspace(math.log(0.02), 0.0, 41)


def lg_R0(Menc, n_steps=2000, K=24, iters=6):
    """Menc(r_array [m], a) -> enclosed mass [kg].  Returns R0 [Mpc] (zero velocity today)."""
    def integrate(ri, a_start=0.02):
        r = ri.copy(); uu = LG_H0 * math.sqrt(LG_OM / a_start ** 3 + LG_OL) * r
        dead = np.zeros_like(r, dtype=bool); lna = np.linspace(math.log(a_start), 0.0, n_steps + 1); h_ = lna[1] - lna[0]
        def accf(l, rr):
            a = math.exp(l); H = LG_H0 * math.sqrt(LG_OM / a ** 3 + LG_OL); rr = np.maximum(rr, 1e-6 * LG_Mpc)
            return -LG_G * Menc(rr, a) / rr ** 2 + LG_OL * LG_H0 ** 2 * rr, H
        for i in range(n_steps):
            l = lna[i]
            a1, H1 = accf(l, r); k1r, k1u = uu / H1, a1 / H1
            a2, H2 = accf(l + h_ / 2, r + h_ * k1r / 2); k2r, k2u = (uu + h_ * k1u / 2) / H2, a2 / H2
            a3, H3 = accf(l + h_ / 2, r + h_ * k2r / 2); k3r, k3u = (uu + h_ * k2u / 2) / H3, a3 / H3
            a4, H4 = accf(l + h_, r + h_ * k3r); k4r, k4u = (uu + h_ * k3u) / H4, a4 / H4
            r = r + h_ * (k1r + 2 * k2r + 2 * k3r + k4r) / 6; uu = uu + h_ * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
            dead |= r <= 1e-5 * LG_Mpc; r = np.where(dead, 1e-5 * LG_Mpc, r); uu = np.where(dead, -1.0, uu)
        return r, uu
    lo, hi = math.log(0.001 * LG_Mpc), math.log(30.0 * LG_Mpc)
    for _ in range(iters):
        xg = lo + (hi - lo) * np.linspace(0, 1, K); r, uu = integrate(np.exp(xg))
        s_ = np.sign(uu); idx = np.where((s_[:-1] < 0) & (s_[1:] > 0))[0]
        if len(idx) == 0:
            return float("nan")
        j = idx[-1]; lo, hi = xg[j], xg[j + 1]
    r, uu = integrate(np.exp(np.array([lo, hi]))); fr = -uu[0] / (uu[1] - uu[0])
    return float((r[0] + fr * (r[1] - r[0])) / LG_Mpc)


def lg_isolated(a0, kernel="p2"):
    Mb = LG_MB * LG_Msun
    def Menc(r, a):
        gN = LG_G * Mb / r ** 2
        return Mb * (nu_rar(gN / a0) if kernel == "rar" else nu_p2(gN / a0))
    return lg_R0(Menc)


def lg_both(LL=None, n=None, floor=None):
    """The LG under the class, both footings: band-pass L(a) = L_Lambda Omega_L(a)^(n/2) [Mpc] and floor y_th(a), the enclosed
    mass tabulated in ln a (one smoothing matrix per epoch, shared by the footings)."""
    Mb = LG_MB * LG_Msun
    tabs = {f: [] for f in FOOTS}
    for la in LNA_T:
        a = math.exp(la)
        Lm = None if LL is None else LL * LG_OmL(a) ** (n / 2.0) * MPCm
        yth = None
        if floor is not None:
            y25, pp, mm = floor
            yth = y25 * (LG_OmL(1 / 1.25) / LG_OmL(a)) ** pp
        for f in FOOTS:
            tabs[f].append(Mb + phantom(Mb, A0[f], Lm, yth, floor[2] if floor else 4))
    lnR = np.log(RG); out = {}
    for f in FOOTS:
        tab = np.array(tabs[f])
        def Menc(r, a, tab=tab):
            x = math.log(a); j = min(max(np.searchsorted(LNA_T, x) - 1, 0), len(LNA_T) - 2)
            fr_ = (x - LNA_T[j]) / (LNA_T[j + 1] - LNA_T[j]); row = (1 - fr_) * tab[j] + fr_ * tab[j + 1]
            return np.interp(np.log(np.maximum(r, RG[0])), lnR, row)
        out[f] = lg_R0(Menc)
    return out


# ================================================================================================= K  CONTROLS
banner("K  CONTROLS: the reused machinery reproduces the record")
m_core = core_model()
k1 = {"lcdm": S8_LCDM,
      "rms": sigma8_of(growth(m_core, A0_L341["canonical"], mode="rms", kernel="mono")[0.0]),
      "permode": sigma8_of(growth(m_core, A0_L341["canonical"], mode="permode", kernel="mono")[0.0])}
check("K1 CONTROL: the generalised yardstick reproduces L341's committed sigma_8 -- LCDM 0.8101, the ungated core (nu_mono, "
      "canonical, c_2 = 0.0073) 23.314 rms / 17.713 per-mode",
      f"LCDM {k1['lcdm']:.4f}; ungated rms {k1['rms']:.3f}, per-mode {k1['permode']:.3f}",
      abs(k1["lcdm"] - 0.8101) < 1e-3 and abs(k1["rms"] - 23.314) < 0.01 and abs(k1["permode"] - 17.713) < 0.01)
OUT["numbers"]["K1"] = k1

# K2: L341 F7 (nu_mono at L341's a0, hard truncation)
def _M_mono_trunc(rt):
    def Mf(Mb):
        M = Mb * nu_mono(G6 * Mb / RR ** 2 / A0_L341["canonical"])
        if rt is not None:
            M = np.where(RR > rt * MPCm, M[np.searchsorted(RR, rt * MPCm)], M)
        return M
    return Mf
k2 = {"none": kids_chi2(_M_mono_trunc(None)), "1.0": kids_chi2(_M_mono_trunc(1.0)), "0.5": kids_chi2(_M_mono_trunc(0.5))}
check("K2 CONTROL: the KiDS lead-grade machinery (Abel projection as a matrix) reproduces L341 F7's committed chi^2: 118.0 "
      "untruncated, 106.8 cut at 1 Mpc, 223.0 cut at 0.5 Mpc (nu_mono, M_b free per bin, full covariance)",
      f"{k2['none']:.1f} / {k2['1.0']:.1f} / {k2['0.5']:.1f}",
      abs(k2["none"] - 118.0) < 0.15 and abs(k2["1.0"] - 106.8) < 0.15 and abs(k2["0.5"] - 223.0) < 0.15)
OUT["numbers"]["K2"] = k2
P(f"    {el()}")

k3 = [lg_isolated(LG_A0[f], kernel="rar") for f in FOOTS]
check("K3 CONTROL: the LG shell model reproduces FP1 E1 / XR4's isolated-MOND zero-velocity radius (nu_RAR, M_b = 1.145e11 "
      "Msun, no external field): 1.929 / 2.021 Mpc", f"{k3[0]:.4f} / {k3[1]:.4f} Mpc",
      abs(k3[0] - 1.9290) < 2e-3 and abs(k3[1] - 2.0214) < 2e-3)
OUT["numbers"]["K3"] = k3

# K4: the smoothed-shell formula and the L -> oo limit
def _shell_density_quad(r, rp, L):
    f = lambda t: t * (math.exp(-(t - rp) ** 2 / (2 * L * L)) - math.exp(-(t + rp) ** 2 / (2 * L * L)))
    return quad(f, 0, r, limit=200)[0] / (rp * math.sqrt(2 * math.pi) * L)
k4a = max(abs(_shell_density_quad(r, rp, 1.0) - float(shell_frac(r, rp, 1.0))) for r in (0.1, 0.5, 1.0, 2.0, 4.0) for rp in (0.05, 0.7, 2.5))
Mb_t = 1e11 * MSUN
k4b = float(np.max(np.abs(phantom(Mb_t, A0["canonical"], 1e3 * MPCm) - phantom(Mb_t, A0["canonical"], None))[RG < 10 * MPCm]
                   / np.maximum(phantom(Mb_t, A0["canonical"], None)[RG < 10 * MPCm], 1e-300)))
k4c = float(np.max(np.abs(np.log10((1e11 * MSUN + phantom(Mb_t, A0["canonical"], None)) / (1e11 * MSUN * nu_p2(G6 * Mb_t / RG ** 2 / A0["canonical"]))))))
check("K4 CONTROL: the Gaussian-smoothed shell's enclosed mass equals the direct quadrature of its density; the band-passed "
      "phantom tends to the isolated one as L -> oo (the core's P2 law, FP1 B1)",
      f"max |formula - quadrature| = {k4a:.1e}; max relative phantom change at L = 1e3 Mpc (r < 10 Mpc) = {k4b:.1e}; "
      f"unfiltered phantom vs P2 law {k4c:.1e} dex", k4a < 1e-10 and k4b < 1e-4 and k4c < 1e-12)

# K5: FP2's committed quadratic block
_fp2 = open(os.path.join(HERE, "FP2_relativistic_consistency.out")).read()
def _grab(tag):
    mm = re.search(r"^\s*dL/d" + tag + r"\s*:\s*(.+)$", _fp2, re.M); return mm.group(1).strip() if mm else None
syms = {s: sp.Symbol(s) for s in ("A_U", "A_n", "A_psi", "A_B", "A_S", "k", "omega", "alpha_c", "c_2", "C_eff")}
syms["I"] = sp.I
blk = {t: sp.sympify(_grab(t), locals=syms) for t in ("n", "psi", "B", "U")}
An, Apsi, AB, AU = syms["A_n"], syms["A_psi"], syms["A_B"], syms["A_U"]
kS, wS, acS, c2S, CeS = syms["k"], syms["omega"], syms["alpha_c"], syms["c_2"], syms["C_eff"]
MB = sp.Matrix([[sp.diff(blk[t], v) for v in (An, Apsi, AB, AU)] for t in ("n", "psi", "B", "U")])
detM = sp.factor(sp.expand(MB.det()))
_detline = re.search(r"det M = (-64\*k\*\*8\*\(.+?\))\s*$", _fp2, re.M)
det_fp2 = sp.sympify(_detline.group(1), locals=syms) if _detline else None
w2 = None
for cand in sp.solve(detM, wS):
    w2 = sp.simplify(cand ** 2); break
E_of = lambda C: acS + 2 * C / (1 + C)
w2_fp5 = c2S * (2 - E_of(CeS)) * kS ** 2 / (E_of(CeS) * (2 + 3 * c2S))
k5_w = sp.simplify(w2 - w2_fp5) == 0 if w2 is not None else False
# static gain with a matter source on the lapse equation
src = sp.Symbol("s")
stat = sp.solve([blk["n"].subs(wS, 0) + src, blk["psi"].subs(wS, 0), blk["B"].subs(wS, 0), blk["U"].subs(wS, 0)], [An, Apsi, AB, AU], dict=True)[0]
stat0 = {v: sp.simplify(stat[v].subs({CeS: 0, acS: 0})) for v in (An, Apsi)}
gain = sp.simplify(stat[An] / stat0[An]); slip = sp.simplify(stat[Apsi] / stat[An])
k5 = (det_fp2 is not None and sp.simplify(detM - det_fp2) == 0 and k5_w
      and sp.simplify(gain - (1 + CeS) / (1 - acS * (1 + CeS) / 2)) == 0 and slip == 1)
check("K5 CONTROL: FP2's committed quadratic block (read from FP2_relativistic_consistency.out) gives FP2's det M, FP5's khronon "
      "dispersion w^2 = c_2 (2 - E) k^2/(E (2 + 3 c_2)) with E = alpha_c + 2C/(1+C), the static gain (1+C)/(1 - alpha_c(1+C)/2) "
      "and no slip (psi/n = 1) -- for any C_eff: every class below enters the scalar block only through C_eff",
      f"det == FP2's: {det_fp2 is not None and sp.simplify(detM - det_fp2) == 0}; w^2 == FP5's: {k5_w}; gain = {gain}; slip = {slip}", k5)
P(f"    {el()}")

# ================================================================================================= S  SECOND VARIATION
banner("S  THE SECOND VARIATION OF EACH CLASS (sympy)")
# S1: one heat branch read out at two diffusion times, eliminated exactly (Fourier mode k)
z_, kk_, Cc_, U_, bb_, BB_ = sp.symbols("z k C U b B", positive=True)
Wz = U_ * sp.exp(-kk_ ** 2 * z_)                                             # W solves d_z W = -k^2 W, W(0) = U
dW = Wz.subs(z_, bb_) - Wz.subs(z_, BB_)
S_red = 2 * Cc_ * kk_ ** 2 * dW ** 2
# multiplier Lambda(z): -Lambda' + k^2 Lambda = 0 in the bulk; Lambda(B) = 4Ck^2 dW; jump Lambda(b-) - Lambda(b+) = -4Ck^2 dW
A2_ = 4 * Cc_ * kk_ ** 2 * dW * sp.exp(-kk_ ** 2 * BB_)
Lam_hi = A2_ * sp.exp(kk_ ** 2 * z_)
Lam_lo = (Lam_hi.subs(z_, bb_) - 4 * Cc_ * kk_ ** 2 * dW) * sp.exp(-kk_ ** 2 * bb_) * sp.exp(kk_ ** 2 * z_)
bulk_ok = all(sp.simplify(-sp.diff(L_, z_) + kk_ ** 2 * L_) == 0 for L_ in (Lam_hi, Lam_lo))
lam0 = sp.simplify(Lam_lo.subs(z_, 0))
force_ok = sp.simplify(-lam0 - sp.diff(S_red, U_)) == 0
Ceff_s1 = sp.simplify(sp.diff(S_red, U_, 2) / (4 * kk_ ** 2))
xi_, Lb_ = sp.symbols("xi L", positive=True)
s1_form = sp.simplify(Ceff_s1.subs({bb_: xi_ ** 2 / 2, BB_: Lb_ ** 2 / 2}) - Cc_ * (sp.exp(-xi_ ** 2 * kk_ ** 2 / 2) - sp.exp(-Lb_ ** 2 * kk_ ** 2 / 2)) ** 2) == 0
check("S1 the band-pass as an action: C-H's heat branch W(z) extended to z = B = L^2/2 and read out at z = b and z = B is "
      "eliminated exactly -- the multiplier solves its adjoint equation with the kernel's jump at z = b, lambda_0 = -dS_red/dU "
      "-- and the reduced action is 2 C k^2 U^2 (e^{-bk^2} - e^{-Bk^2})^2, i.e. C_eff = C (e^{-xi^2 k^2/2} - e^{-L^2 k^2/2})^2",
      f"bulk equations {bulk_ok}; force identity {force_ok}; C_eff == C (e^-xi^2k^2/2 - e^-L^2k^2/2)^2: {s1_form}",
      bulk_ok and force_ok and s1_form,
      reading="the band-pass is a linear, leafwise operation on U: in linear theory it only multiplies the tangent by h(k)^2")

# S1b: the static field equation with the full nonlinear kernel, from the discrete action (FP1 A3's test, band-passed)
from scipy.linalg import expm
Ng = 10; Id = np.eye(Ng); Dm = np.roll(Id, 1, axis=1) - Id                     # periodic forward difference
Dx = np.kron(Dm, Id); Dy = np.kron(Id, Dm); Lap = -(Dx.T @ Dx + Dy.T @ Dy)
Sbp = expm(0.02 * Lap) - expm(0.9 * Lap)                                      # b = 0.02, B = 0.9 (grid units)
rng_ = np.random.default_rng(6)
u0 = sum(rng_.normal() * np.cos(2 * np.pi * (i * np.arange(Ng)[:, None] + j * np.arange(Ng)[None, :]) / Ng + rng_.uniform(0, 6.28))
         for i in range(3) for j in range(3)).ravel() * 0.4
qP2n = lambda Z: ((2 * np.sqrt(Z) + 1) / 2) * np.sqrt(Z + np.sqrt(Z)) - 0.25 * np.log(2 * np.sqrt(Z) + 1 + 2 * np.sqrt(Z + np.sqrt(Z))) - Z
def _act(u):
    V = Sbp @ u; Z = (Dx @ V) ** 2 + (Dy @ V) ** 2; return float(np.sum(qP2n(Z)))
def _grad(u, out_filter=True):
    V = Sbp @ u; Z = (Dx @ V) ** 2 + (Dy @ V) ** 2; qp = np.sqrt(1 + 1 / np.sqrt(Z)) - 1            # q'(Z) = nu_P2(sqrt Z) - 1
    inner = Dx.T @ (2 * qp * (Dx @ V)) + Dy.T @ (2 * qp * (Dy @ V))
    return (Sbp.T @ inner) if out_filter else inner
fd = np.array([(_act(u0 + 1e-6 * e_) - _act(u0 - 1e-6 * e_)) / 2e-6 for e_ in np.eye(Ng * Ng)])
e_with = float(np.max(np.abs(fd - _grad(u0))) / np.max(np.abs(fd))); e_without = float(np.max(np.abs(fd - _grad(u0, False))) / np.max(np.abs(fd)))
Zr = (Dx @ (Sbp @ u0)) ** 2 + (Dy @ (Sbp @ u0)) ** 2
check("S1b THE STATIC FIELD EQUATION, NONLINEAR: on a periodic 10x10 leaf with S_bp = e^{bLap} - e^{BLap} and the P2 kernel, the "
      "finite-difference gradient of the discrete action equals S_bp^T div[(nu - 1) grad S_bp u] (and fails without the output "
      "filter): the variation band-passes the phantom's output too (FP1 A3's double filter, now a band-pass on both sides)",
      f"relative |FD - equation with S_bp^T| = {e_with:.1e}; without the output filter {e_without:.1e}; field range y = "
      f"{np.sqrt(Zr.min()):.2e}-{np.sqrt(Zr.max()):.2e}", e_with < 1e-6 and e_without > 1e-2)

# S2: discrete heat block (implicit Euler), n steps to b and m more to B
s2 = {}
dz_ = sp.Symbol("dz", positive=True)
for (nn, mm_) in ((1, 1), (2, 1), (1, 2), (2, 2)):
    N_ = nn + mm_
    Wv = sp.symbols(f"W0:{N_ + 1}"); Lv = sp.symbols(f"L1:{N_ + 1}"); l0 = sp.Symbol("l0")
    Lag = 2 * Cc_ * kk_ ** 2 * (Wv[nn] - Wv[N_]) ** 2 + sum(Lv[j - 1] * ((1 + dz_ * kk_ ** 2) * Wv[j] - Wv[j - 1]) for j in range(1, N_ + 1)) + l0 * (Wv[0] - U_)
    xs = list(Wv) + list(Lv) + [l0]
    Hxx = sp.hessian(Lag, xs); HxU = sp.Matrix([sp.diff(Lag, x, U_) for x in xs])
    Schur = sp.simplify(-(HxU.T * Hxx.LUsolve(HxU))[0])
    sig = lambda j: (1 + dz_ * kk_ ** 2) ** (-j)
    s2[(nn, mm_)] = (sp.simplify(Schur - 4 * Cc_ * kk_ ** 2 * (sig(nn) - sig(N_)) ** 2) == 0, not sp.simplify(Hxx.det()).has(Cc_))
check("S2 the discrete heat block (implicit Euler, n steps to b and m more to B): the Schur complement onto U is "
      "4 C k^2 (sigma_n - sigma_{n+m})^2 with sigma_j = (1 + dz k^2)^(-j), and the auxiliary block's determinant does not contain "
      "the kernel: the extended branch is second class and adds no mode (FP5 B2's count, N = 3, unchanged)",
      "; ".join(f"(n,m)={k_}: Schur ok {v[0]}, det kernel-free {v[1]}" for k_, v in s2.items()),
      all(v[0] and v[1] for v in s2.values()))

# S3: the band-pass has no W'' term; a multiplier gate does (frozen background gradient g0; Q, W, B as local polynomials,
# which span every value of Q', Q'', W', W'', B, B', B'' at the background)
eps = sp.Symbol("epsilon"); xS = sp.Symbol("x", real=True); g0 = sp.Symbol("g0", positive=True); hk = sp.Symbol("h_k", positive=True)
Zs = sp.Symbol("Z", positive=True)
a1, a2, a3 = sp.symbols("a1 a2 a3")
Qpoly = lambda Z: a1 * (Z - g0 ** 2) + a2 * (Z - g0 ** 2) ** 2 / 2 + a3 * (Z - g0 ** 2) ** 3 / 6    # Q'(g0^2) = a1, Q'' = a2
dV = hk * sp.cos(kk_ * xS)                                                     # band-passed perturbation: h_k x (dU = cos kx)
Zbp = (g0 + eps * sp.diff(dV, xS)) ** 2
d2_bp = sp.expand(sp.diff(Qpoly(Zbp), eps, 2).subs(eps, 0))
avg_bp = sp.simplify(sp.integrate(d2_bp, (xS, 0, 2 * sp.pi / kk_)) * kk_ / (2 * sp.pi))
target_bp = (2 * a1 + 4 * g0 ** 2 * a2) * hk ** 2 * kk_ ** 2 / 2
s3a = sp.simplify(avg_bp - target_bp) == 0
# multiplier gate reading X = C_g U'' (the density reading), times the MOND energy B(Z)
Cg = sp.Symbol("C_g", positive=True); X0 = sp.Symbol("X0", positive=True)
w0s, w1s, w2s, b0s, b1s, b2s = sp.symbols("w0 w1 w2 b0 b1 b2")
Wpoly = lambda X: w0s + w1s * (X - X0) + w2s * (X - X0) ** 2 / 2
Bpoly = lambda Z: b0s + b1s * (Z - g0 ** 2) + b2s * (Z - g0 ** 2) ** 2 / 2
dU_ = sp.cos(kk_ * xS)
Xg = X0 + eps * Cg * sp.diff(dU_, xS, 2)
Zg = (g0 + eps * sp.diff(dU_, xS)) ** 2
d2_g2 = sp.expand(sp.diff(Wpoly(Xg) * Bpoly(Zg), eps, 2).subs(eps, 0))
avg_g2 = sp.simplify(sp.integrate(d2_g2, (xS, 0, 2 * sp.pi / kk_)) * kk_ / (2 * sp.pi))
w2coef = sp.simplify(sp.diff(avg_g2, w2s))
s3b = sp.simplify(w2coef - b0s * Cg ** 2 * kk_ ** 4 / 2) == 0
check("S3 WHY THE BAND-PASS ESCAPES FP3's LEMMA: its argument is linear in U, so the second variation of 2 alpha^2 q(|grad V|^2) "
      "is [2Q' + 4 g^2 Q''] h_k^2 k^2/2 per unit amplitude -- the constitutive block C_L times h_k^2, k^2-order, no W''(dX)^2 term; a "
      "multiplier gate W(C_g U'') B carries B W'' C_g^2 k^4/2 (FP3 C1's anti-pressure, k^4 order) -- absent here by construction",
      f"band-pass second variation == (2Q' + 4g^2Q'') h^2 k^2/2: {s3a}; multiplier gate's W'' coefficient == B C_g^2 k^4/2: {s3b}",
      s3a and s3b,
      reading="health of (b) is the kernel's own (C_T, C_L >= 0) times h^2 >= 0; the epoch factor L(<K>_h) is a leaf average "
              "(FP3 C1 lemma: no local second variation)")

# S4: kernel families
t_, yr_, s_ = sp.symbols("t y_r s", positive=True)
nuP2 = lambda v: sp.sqrt(1 + 1 / v)
qP2 = ((2 * s_ + 1) / 2) * sp.sqrt(s_ ** 2 + s_) - sp.Rational(1, 4) * sp.log(2 * s_ + 1 + 2 * sp.sqrt(s_ ** 2 + s_)) - s_ ** 2
F1_ = lambda u: qP2.subs(s_, u)                                                # Int 2u (sqrt(1+1/u) - 1) du  (FP1 B2)
G1_ = lambda u: sp.sqrt(u ** 2 + u) + sp.log(2 * u + 1 + 2 * sp.sqrt(u ** 2 + u)) / 2 - u   # Int (sqrt(1+1/u) - 1) du
qr_closed = F1_(s_ + yr_) - F1_(yr_) - 2 * yr_ * (G1_(s_ + yr_) - G1_(yr_))    # q_r(s^2) = Int_0^s 2t (nu_P2(t + y_r) - 1) dt
# check dq_r/d(s^2) = nu_P2(s + y_r) - 1 at points (the closed form differentiated)
dq = sp.diff(qr_closed, s_) / (2 * s_)
s4a = max(abs(float((dq - (nuP2(s_ + yr_) - 1)).subs({s_: sv, yr_: rv}))) for sv in (1e-3, 0.3, 2.0, 50.0) for rv in (1e-4, 0.01, 1.0))
s4a0 = abs(float(qr_closed.subs({s_: 0, yr_: 0.3})))
C0r = sp.limit(nuP2(s_ + yr_) - 1, s_, 0)
yv = sp.Symbol("y", positive=True)
nur = nuP2(yv + yr_)
CLr = sp.simplify(nur - 1 + yv * sp.diff(nur, yv))
CLp2_s = (nuP2(yv) - 1 + yv * sp.diff(nuP2(yv), yv)).subs(yv, yv + yr_)
s4b = sp.simplify(CLr - CLp2_s + yr_ * sp.diff(nuP2(yv), yv).subs(yv, yv + yr_)) == 0
# cut-off on the tangent: C_L = c C_L,P2 + y (nu-1) c'/y_th  (>= 0, no c'')
yth_, m_ = sp.symbols("y_th m", positive=True)
cS = lambda xx: xx ** m_ / (1 + xx ** m_)
Ctan = (nuP2(yv) - 1) * cS(yv / yth_)
CL_tan = sp.diff(yv * Ctan, yv)
CL_sum = cS(yv / yth_) * (nuP2(yv) - 1 + yv * sp.diff(nuP2(yv), yv)) + yv * (nuP2(yv) - 1) * sp.diff(cS(yv / yth_), yv)
s4c = sp.simplify(CL_tan - CL_sum) == 0
c_prime_pos = sp.simplify(sp.diff(cS(xS), xS) - m_ * xS ** (m_ - 1) / (1 + xS ** m_) ** 2) == 0
zero_tan = sp.limit(Ctan.subs({m_: 4, yth_: sp.Rational(1, 100)}), yv, 0)
# control: the energy-multiplied cut-off Q_E = c(y/y_th) q_P2(y^2): C_L = d/dy[(1/2) dQ_E/dy] contains c''
QE = cS(yv / yth_) * qP2.subs(s_, yv)
CL_E = sp.diff(sp.diff(QE, yv) / 2, yv)                                       # C_L = d/dy [y Q_E'(Z)], Q_E' = (1/2y) dQ_E/dy
fE = sp.lambdify((yv, yth_, m_), CL_E, "mpmath")
negE = []
for mv in (4, 8, 16):
    for yvv in np.geomspace(0.05, 20, 400):
        val = float(fE(float(yvv) * 1e-3, 1e-3, mv))
        if val < 0:
            negE.append((mv, round(float(yvv), 3))); break
fT = sp.lambdify((yv, yth_, m_), CL_tan, "mpmath")
minT = min(float(fT(float(yvv) * yth, yth, mv)) for mv in (1, 4, 8, 16, 32) for yth in (1e-5, 1e-3, 0.03) for yvv in np.geomspace(1e-3, 1e3, 120))
check("S4 THE KERNEL FAMILIES (class e) escape FP3's lemma: (e1) q_r has a closed form with q_r' = nu_P2(s + y_r) - 1, q_r(0) = 0, "
      "a FINITE zero-field tangent C_0 = sqrt(1 + 1/y_r) - 1, and C_L = C_L,P2(y + y_r) - y_r nu_P2' > 0; (e2/e3) the cut-off ON THE "
      "TANGENT has C_L = c C_L,P2 + y (nu - 1) c'/y_th -- a sum of non-negative terms with c' only (no c''), so C_T, C_L >= 0 for "
      "EVERY m and y_th, and a ZERO zero-field tangent (m > 1/2); CONTROL: the same cut-off multiplying the ENERGY puts c'' into C_L "
      "and turns it negative for sharp cut-offs",
      f"(e1) max |q_r' - (nu(s+y_r) - 1)| = {s4a:.1e}, q_r(0) = {s4a0:.0e}, C_0 = {C0r}, C_L identity {s4b}; (e2) C_L identity {s4c}, "
      f"c' = m x^(m-1)/(1+x^m)^2: {c_prime_pos}, zero-field tangent (m = 4) = {zero_tan}, min C_L (tangent cut-off, m = 1-32, 3 y_th) = "
      f"{minT:.2e}; energy cut-off: first C_L < 0 at (m, y/y_th) = {negE}",
      s4a < 1e-9 and s4a0 < 1e-12 and s4b and s4c and c_prime_pos and zero_tan == 0 and minT >= 0 and len(negE) > 0,
      reading="reshaping the PHANTOM LAW (the tangent) monotonically is healthy by FP2 C3's criterion whatever its switch shape; "
              "FP3's anti-pressure comes from gating the ENERGY on a density-type variable, which (e) never does")

# S5: FRW linearisation of each class from K5's block
Einf = sp.limit(E_of(CeS), CeS, sp.oo)
w2_frw = lambda Cval: sp.simplify(w2_fp5.subs(CeS, Cval) / kS ** 2)
rows_s5 = {}
for ac in ALPHA_C:
    C0_bound = (2 - ac) / ac                                           # E < 2  <=>  C < (2 - alpha_c)/alpha_c
    yr_min = 1.0 / ((C0_bound + 1) ** 2 - 1)
    rows_s5[ac] = dict(C0_bound=C0_bound, yr_min=yr_min)
w2_zero = sp.simplify(w2_fp5.subs(CeS, 0) / kS ** 2)
Gz = sp.simplify(gain.subs(CeS, 0))
s5_ok = (sp.simplify(Einf - (acS + 2)) == 0 and sp.simplify(w2_zero - c2S * (2 - acS) / (acS * (2 + 3 * c2S))) == 0
         and sp.simplify(Gz - 1 / (1 - acS / 2)) == 0 and slip == 1)
P("    FRW (zero field) per class -- the tangent C_eff at k with the band-pass factor h(k)^2 = (e^{-xi^2k^2/2} - e^{-L^2k^2/2})^2:")
P("      ungated core             C_eff = oo            -> E = alpha_c + 2 > 2: Hadamard ill-posed (FP5 C3)")
P("      (b) band-pass alone      C_eff = oo * h(k)^2    -> E = alpha_c + 2 at every k with h > 0: ill-posed (the band-pass does not cure FRW)")
for ac, r_ in rows_s5.items():
    P(f"      (e1) shifted kernel      C_eff = C_0 finite     -> well-posed iff C_0 < (2 - alpha_c)/alpha_c = {r_['C0_bound']:.3e}, i.e. y_r > {r_['yr_min']:.2e} (alpha_c = {ac:.2e})")
P(f"      (e2), (e3), (H) cut-off  C_eff = 0 exactly      -> E = alpha_c, w^2/k^2 = {w2_zero} > 0: GR + BPS khronon (FP5 C5's cone)")
P(f"      G_eff/G on FRW = (1 + C_eff)/(1 - alpha_c (1 + C_eff)/2) -> {Gz} at C_eff = 0 (FP2 D3); slip psi/n = {slip} for every C_eff (K5)")
check("S5 THE FRW LINEARISATION OF EACH CLASS (from FP2's committed block): E(C) runs from alpha_c to alpha_c + 2, so the ungated core "
      "and the band-pass ALONE (C_eff = oo x h^2) are Hadamard ill-posed on FRW; the shifted kernel (e1) is well-posed iff "
      "y_r > y_r,min(alpha_c) (<= 2.6e-18 over the window); every cut-off class (e2, e3, H) has C_eff = 0 identically on FRW: E = "
      "alpha_c, w^2 > 0, G_eff = G/(1 - alpha_c/2), no slip -- FP5's strict form",
      f"E(oo) = {Einf}; y_r,min = {rows_s5[ALPHA_C[0]]['yr_min']:.2e} / {rows_s5[ALPHA_C[1]]['yr_min']:.2e} (alpha_c ends); "
      f"w^2/k^2 at C = 0: {w2_zero}; G_eff(C=0)/G = {Gz}; slip {slip}", s5_ok)
OUT["numbers"]["S5"] = {str(k_): v for k_, v in rows_s5.items()}

# S6: order counting of the MOND energy around FRW (Z = O(eps^2))
Zv = sp.Symbol("Z", positive=True)
import mpmath as _mp
_mp.mp.dps = 50
q_core_lead = sp.limit(qP2.subs(s_, sp.sqrt(Zv)) / Zv ** sp.Rational(3, 4), Zv, 0)
_fqr = sp.lambdify((s_, yr_), qr_closed, "mpmath")
q_r_lead = float(_fqr(_mp.sqrt(_mp.mpf("1e-28")), _mp.mpf("1e-4")) / _mp.mpf("1e-28"))
C0_1e4 = float(_mp.sqrt(1 + _mp.mpf(10) ** 4) - 1)
lead_int = sp.limit(((nuP2(sp.sqrt(Zv)) - 1) * (sp.sqrt(Zv) / yth_) ** 4 / (1 + (sp.sqrt(Zv) / yth_) ** 4)) / Zv ** sp.Rational(7, 4), Zv, 0)
check("S6 ORDER COUNTING around FRW (Z = O(eps^2)): the core's MOND energy q_P2 ~ (4/3) Z^(3/4) is O(eps^(3/2)) with an infinite "
      "tangent (FP3 B1); the shifted kernel is q_r ~ C_0 Z, O(eps^2) with a finite tangent; the cut-off kernel's tangent (m = 4) "
      "starts at Z^(7/4)/y_th^4, so its energy starts at Z^(11/4), O(eps^(11/2)): it drops out of the quadratic action and the "
      "linear theory on FRW is exactly GR + BPS khronon",
      f"q_P2/Z^(3/4) -> {q_core_lead}; q_r/Z at Z = 1e-28 = {q_r_lead:.6f} vs C_0(y_r = 1e-4) = {C0_1e4:.6f}; cut-off tangent/Z^(7/4) -> {lead_int}",
      q_core_lead == sp.Rational(4, 3) and abs(q_r_lead / C0_1e4 - 1) < 1e-6 and sp.simplify(lead_int - yth_ ** -4) == 0)

# S7: class (d) -- a tidal-invariant gate W(E:E/X_c), E the traceless Hessian of the lapse
kx, ky, kz3 = sp.symbols("k_x k_y k_z", real=True); e0 = sp.Symbol("e0", positive=True); Xc = sp.Symbol("X_c", positive=True)
Bg, W1, W2 = sp.symbols("B_g W1 W2")
kv = sp.Matrix([kx, ky, kz3])
Ebar = e0 * sp.diag(2, -1, -1) / sp.sqrt(6)                                    # axisymmetric traceless background, |E| = e0
dE = -(kv * kv.T - sp.eye(3) * (kv.dot(kv)) / 3)                               # per unit dPhi, Fourier
X1 = 2 * sum(Ebar[i, j] * dE[i, j] for i in range(3) for j in range(3)) / Xc
X2 = sum(dE[i, j] ** 2 for i in range(3) for j in range(3)) / Xc
HPP = sp.simplify(Bg * (W2 * X1 ** 2 + 2 * W1 * X2))                           # d^2/d eps^2 of B W(X0 + eps X1 + eps^2 X2)
Hmag = sp.Symbol("G_N", positive=True); Cc7 = sp.Symbol("C", positive=True)
k2s = kv.dot(kv)
# C-H chassis, static, Fourier: H_Phi,u = -k^2/(4 pi G), H_uu = (1 + C) k^2/(4 pi G), H_PhiPhi = the gate's (FP3 C1's structure)
det7 = sp.simplify(HPP * (1 + Cc7) * k2s / (4 * sp.pi * Hmag) - k2s ** 2 / (16 * sp.pi ** 2 * Hmag ** 2))
magic = {kx: sp.sqrt(sp.Rational(1, 3)), ky: sp.sqrt(sp.Rational(1, 3)), kz3: sp.sqrt(sp.Rational(1, 3))}   # E:kk = 0 here
X1_magic = sp.simplify(X1.subs(magic))
HPP_magic = sp.simplify(HPP.subs(magic))
kst = sp.Symbol("kappa", positive=True)
det_scaled = sp.simplify(det7.subs({kx: kst / sp.sqrt(3), ky: kst / sp.sqrt(3), kz3: kst / sp.sqrt(3)}))
root = [r_ for r_ in sp.solve(sp.Eq(det_scaled, 0), kst ** 2) if r_ != 0]
root_ok = len(root) == 1 and sp.simplify(root[0] - 3 * Xc / (16 * sp.pi * Hmag * Bg * W1 * (1 + Cc7))) == 0
s7_ok = X1_magic == 0 and sp.simplify(HPP_magic - Bg * W1 * sp.Rational(4, 3) / Xc) == 0 and root_ok
check("S7 CLASS (d), a gate on the lapse's TIDAL invariant X = E:E/X_c (every Hessian invariant but the trace is non-linear, so "
      "d^2 X != 0): its second variation B[W'' (dX)^2 + 2 W' d^2X] has, in the directions with E:kk = 0 (they always exist for "
      "a traceless E), only the W' part, +B W' (4/3) k^4/X_c > 0 wherever W' > 0; in the C-H chassis' (Phi, u) block that makes "
      "det = H_PhiPhi (1+C) k^2/(4 pi G) - k^4/(16 pi^2 G^2) vanish at a real k -- singular throughout every transition, "
      "whatever the sign of W'' (strictly worse than FP3's density reading, singular only where W'' > 0)",
      f"E:kk at the magic direction = {X1_magic}; H_PhiPhi there = {HPP_magic} (per |k|^4); det zero at k^2 = {root} "
      f"(real iff B W' > 0)", s7_ok)
P(f"    {el()}")

# ================================================================================================= E  CLASS (e) ALONE
banner("E  CLASS (e): KERNEL REGULARISATIONS ALONE")
ygal = np.logspace(-2, 2, 400)
e1_rows = {}
for yr in (1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 0.1, 1.0):
    dev = float(np.max(np.abs(np.log10(nu_p2(ygal, yr) / nu_p2(ygal)))))
    s_ = {(f, m): s8ratio(core_model(yr), f, m) for f in FOOTS for m in MODES}
    e1_rows[yr] = dict(C0=math.sqrt(1 + 1 / yr) - 1, galaxy_dev=dev, s8=min(s_.values()), s8max=max(s_.values()))
    P(f"    (e1) y_r = {yr:<7g}: C_0 = {e1_rows[yr]['C0']:9.3g}; galaxy law at y = 0.01-100 off by <= {dev:.4f} dex; "
      f"sigma_8/LCDM {e1_rows[yr]['s8']:.3f}-{e1_rows[yr]['s8max']:.3f} (both footings, rms/per-mode)")
e1_ok = any(v["galaxy_dev"] <= SPARC_TOL and v["s8max"] <= SIG8_BAND[1] for v in e1_rows.values())
check("E1 (e1) THE TRADE: every shifted kernel that keeps the galaxy law at y = 0.01-100 within 0.01 dex (y_r <~ 5e-4) leaves "
      "sigma_8 ~ 17-27 x LCDM, and the ones that tame growth move the galaxy law by ~1 dex: no member passes both",
      "; ".join(f"y_r={k_:g}: {v['galaxy_dev']:.3f} dex, s8 {v['s8']:.2f}-{v['s8max']:.2f}" for k_, v in e1_rows.items()),
      not e1_ok)
OUT["numbers"]["E1"] = {str(k_): v for k_, v in e1_rows.items()}

# E2: the linear web's field
zw = [0.0, 0.25, 0.5, 1.0, 2.5, 10.0, 100.0, 999.0]
resw = growth(lcdm_model(), A0["canonical"], zs_out=zw[1:])
yweb = {}
for z in sorted(resw):
    a = 1 / (1 + z); gk = gfield(resw[z], a, KH)
    y341 = math.sqrt(np.trapz(gk ** 2 / KH, KH) / np.trapz(1 / KH, KH)) / A0["canonical"]
    yvar = math.sqrt(np.trapz(gk ** 2 / KH, KH)) / A0["canonical"]
    ypm = [float(np.interp(math.log(k_), np.log(KH), gk)) / A0["canonical"] for k_ in (0.05, 0.2, 1.0)]
    yweb[z] = dict(rms341=y341, rms_var=yvar, permode=ypm)
    P(f"    z = {z:6.2f}: linear web field y = {y341:.2e} (L341 rms) / {yvar:.2e} (variance rms); per-mode at k = 0.05/0.2/1 h/Mpc: "
      + " / ".join(f"{v:.1e}" for v in ypm))
kids_range = (5e-5, 1e-2)                                                    # y where KiDS isolated lenses need P2 (0.03-1 Mpc)
ov = kids_range[0] <= yweb[0.25]["rms341"] <= 100 and kids_range[0] <= min(yweb[0.25]["permode"])
check("E2 THE OVERLAP IN FIELD: at the KiDS epoch (z = 0.25) the linear web's field (L341 rms 4.8e-3, per-mode 3-8e-3, variance "
      "rms 1.3e-2 a0) lies INSIDE the range where KiDS's isolated lenses (y ~ 5e-5-1e-2 between 0.03 and 1 Mpc) and SPARC "
      "(0.01-100) need the P2 law at the same epoch; over cosmic time the web runs y ~ 4e-3 -> 5 (z = 0 -> 1000)",
      f"z = 0.25: {yweb[0.25]['rms341']:.2e} / per-mode {min(yweb[0.25]['permode']):.1e}-{max(yweb[0.25]['permode']):.1e}; "
      f"z = 999: {yweb[999.0]['rms341']:.2f}", ov,
      reading="a kernel that is a function of the local field (and of the epoch) cannot tell the web from a lens's outskirts")
OUT["numbers"]["E2"] = {str(k_): v for k_, v in yweb.items()}

# E3: the most generous local-in-y kernel
def generous(ylo, zmax):
    return {"hfac": lambda a, k: np.ones_like(k),
            "cut": lambda y, a, ylo=ylo, zmax=zmax: (((np.asarray(y) >= ylo) & (np.asarray(y) <= 100.0)) & ((1 / a - 1) <= zmax)).astype(float)}
e3 = {}
for (ylo, zmax) in ((5e-5, 0.25), (5e-5, 0.3), (1e-3, 0.25), (5e-5, 0.1)):
    e3[(ylo, zmax)] = {(f, m): s8ratio(generous(ylo, zmax), f, m) for f in FOOTS for m in MODES}
    P(f"    generous kernel: P2 on [{ylo:g}, 100], Newtonian elsewhere and at every z > {zmax}: sigma_8/LCDM = "
      + ", ".join(f"{f[:3]}/{m}: {v:.3f}" for (f, m), v in e3[(ylo, zmax)].items()))
e3min = min(e3[(5e-5, 0.25)].values())
check("E3 CLASS (e) FAILS G-1 (THE OVERLAP): even the MOST GENEROUS local-in-y kernel -- P2 only on the range KiDS and SPARC "
      "need, [5e-5, 100], and only at z <= 0.25 (KiDS's median lens epoch; SPARC at z ~ 0), exactly Newtonian at every other field "
      "and every earlier epoch, i.e. the smallest boost any kernel of (y, <K>) keeping KiDS and SPARC can have at each (y, z) -- gives "
      "sigma_8/LCDM >= 1.15 on both footings and both yardstick modes, above the 1.05 ceiling (1.03 only if MOND waits until "
      "z = 0.1, which KiDS's lenses at z ~ 0.25 forbid)",
      f"min over footings/modes at [5e-5, 100], z <= 0.25: {e3min:.3f}; z <= 0.3: {min(e3[(5e-5, 0.3)].values()):.3f}; "
      f"z <= 0.1: {min(e3[(5e-5, 0.1)].values()):.3f}", e3min > SIG8_BAND[1],
      reading="no regularisation of the kernel in the field alone -- finite tangent, zero tangent, epoch-dependent floor -- can pass "
              "linear growth while keeping KiDS and SPARC: the discriminator has to be something other than the local field")
OUT["numbers"]["E3"] = {f"{k_[0]}_{k_[1]}": {f"{kk[0]}_{kk[1]}": v for kk, v in d_.items()} for k_, d_ in e3.items()}
check("E4 (e) ON FRW: the finite tangent needs only y_r > 2.6e-18 (E < 2 across the alpha_c window) and the cut-off makes it zero "
      "(S5): regularisation alone cures FP5's Hadamard band -- the failure of (e) is growth (E3), not well-posedness",
      f"y_r,min {rows_s5[ALPHA_C[0]]['yr_min']:.1e} (alpha_c = 9.6e-14) .. {rows_s5[ALPHA_C[1]]['yr_min']:.1e} (3.2e-9)",
      rows_s5[ALPHA_C[1]]["yr_min"] < 1e-17)
P(f"    {el()}")

# ================================================================================================= B  CLASS (b)
banner("B  CLASS (b): THE BAND-PASS SCALE GATE, L = L_Lambda Omega_L(<K>_h)^(n/2)")
# B1 statics
def sparc_dev(L0_mpc, foot, masses=(1e9, 1e10, 1e11, 1e12)):
    return max(abs(law_dev_dex(M, A0[foot], y, L0_mpc)) for M in masses for y in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
L_sparc = {}
for foot in FOOTS:
    for lab, ms_ in (("1e12", (1e9, 1e10, 1e11, 1e12)), ("1e11", (1e9, 1e10, 1e11))):
        try:
            L_sparc[(foot, lab)] = brentq(lambda L_: sparc_dev(L_, foot, ms_) - SPARC_TOL, 0.05, 6.0, xtol=1e-3)
        except ValueError:
            L_sparc[(foot, lab)] = float("nan")
dev_at = {(foot, L0): sparc_dev(L0, foot) for foot in FOOTS for L0 in (0.69, 1.44, 1.78)}
Lsun = 1.44 * MPCm
gain_sun = float(gfrac_smooth(np.array([8.2 * kpc / Lsun]))[0])
Mtot_far = {M: float(phantom(M * MSUN, A0["canonical"], 1.44 * MPCm)[-1] / (M * MSUN)) for M in (1e10, 1e11, 1e12)}
Mpk = {M: float(np.max(phantom(M * MSUN, A0["canonical"], 1.44 * MPCm)) / (M * MSUN)) for M in (1e10, 1e11, 1e12)}
P("    the SPARC-range law (y = 0.01-100) at z = 0, max |dev| vs P2: " + ", ".join(f"{k_[0][:3]} L(0) = {k_[1]}: {v:.1e} dex" for k_, v in dev_at.items()))
P("    L(0) needed for <= 0.01 dex: " + ", ".join(f"{k_[0][:3]} (M_b <= {k_[1]}): {v:.2f} Mpc" for k_, v in L_sparc.items()))
b1_ok = (BANDPASS and all(np.isfinite(v) for v in L_sparc.values()) and max(L_sparc[(f, "1e12")] for f in FOOTS) < 1.44
         and gain_sun < 1e-5 and max(abs(v) for v in Mtot_far.values()) < 1e-3)
check("B1 (b) STATICS: the band-passed law keeps the SPARC range (y = 0.01-100, M_b = 1e9-1e12) within 0.01 dex once L(0) exceeds a "
      "floor (set by the 1e12 outskirts at y = 0.01, r ~ 0.4 Mpc) that sits below the KiDS-allowed L(0) = 1.44 Mpc (n = 2); the "
      "Galaxy's field at the Sun passes with gain 1 - O((8 kpc/L)^3) (FP1's Solar-System floors unchanged); and every isolated system "
      "is GAUSS-COMPENSATED: the phantom is the divergence of (nu - 1) grad V with V band-passed (so it vanishes beyond ~L) and the "
      "output filter (1 - S_L) keeps its monopole zero, so beyond ~2L the system weighs its baryons -- the record's L352 edge, now "
      "produced by the action",
      "L_SPARC " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.2f}" for k_, v in L_sparc.items())
      + f" Mpc; smoothed fraction of the Galactic field at the Sun {gain_sun:.1e}; phantom/M_b peak "
      + ", ".join(f"{M:.0e}: {Mpk[M]:.0f}" for M in Mpk) + "; total at 80 Mpc " + ", ".join(f"{v:.1e}" for v in Mtot_far.values()), b1_ok)
OUT["numbers"]["B1"] = {"L_sparc": {f"{k_[0]}_{k_[1]}": v for k_, v in L_sparc.items()}, "dev": {f"{k_[0]}_{k_[1]}": v for k_, v in dev_at.items()},
                        "gain_sun": gain_sun, "phantom_total_far": Mtot_far, "phantom_peak": Mpk}

# B2 sigma_8 map
b2 = {}
for n in (0, 1, 2, 3):
    for LL in (0.5, 1.0, 2.0, 3.0, 5.0):
        b2[(n, LL)] = {m: s8ratio(bandpass_model(LL, n), "canonical", m) for m in MODES}
P("    sigma_8/LCDM (canonical; rms / per-mode) for the band-pass + (e1, y_r = 1e-6):")
for n in (0, 1, 2, 3):
    P(f"      n = {n}: " + "; ".join(f"L_Lambda = {LL}: {b2[(n, LL)]['rms']:.3f}/{b2[(n, LL)]['permode']:.3f}" for LL in (0.5, 1.0, 2.0, 3.0, 5.0)))
b2_ok = (min(b2[(0, LL)]["rms"] for LL in (0.5, 1.0, 2.0, 3.0, 5.0)) > 3
         and all(max(b2[(2, LL)].values()) <= SIG8_BAND[1] for LL in (0.5, 1.0, 2.0, 3.0)))
check("B2 (b) FIXES LATE-TIME GROWTH ONLY IF IT SHRINKS INTO THE PAST: a fixed scale (n = 0) boosts every sub-L mode at every epoch "
      "(sigma_8 3.5-19 x LCDM); with the vacuum share, L = L_Lambda Omega_L^(n/2), n >= 2 keeps sigma_8 <= 1.05 for L_Lambda <= 3 Mpc",
      f"n = 0 min {min(b2[(0, LL)]['rms'] for LL in (0.5, 1.0, 2.0, 3.0, 5.0)):.2f}; n = 2, L_Lambda <= 3: max "
      f"{max(max(b2[(2, LL)].values()) for LL in (0.5, 1.0, 2.0, 3.0)):.4f}; n = 3, L_Lambda = 5: {max(b2[(3, 5.0)].values()):.4f}", b2_ok)
OUT["numbers"]["B2"] = {f"{k_[0]}_{k_[1]}": v for k_, v in b2.items()}
P(f"    {el()}")

# B3 the flagship floor on L(2.5)
def flag_dev(Lkpc, foot, M=1e11, yth=None):
    return law_dev_dex(M, A0[foot], 0.1, Lkpc / 1e3, yth)
Lflag = {}
for foot in FOOTS:
    try:
        Lflag[foot] = brentq(lambda Lk: flag_dev(Lk, foot) + FLAG_TOL, 5.0, 400.0)
    except ValueError:                                                        # MUTATE: no band-pass, no floor on L
        Lflag[foot] = float("nan")
rF = {M: math.sqrt(G6 * M * MSUN / (0.1 * A0["canonical"])) / kpc for M in (1e10, 1e11)}
LF = max(Lflag.values()) if all(np.isfinite(list(Lflag.values()))) else 50.0
check("B3 THE FLAGSHIP FLOOR: at z = 2.5 the 1e11 Msun flagship (g_bar = 0.1 a0 at r_F) stays within 0.05 dex of P2 only if "
      "L(2.5) >= ~50 kpc (both footings); the band-pass's edge then sits beyond ~1.3 r_F",
      f"L_flag = {Lflag['canonical']:.1f} / {Lflag['alt']:.1f} kpc; r_F = {rF[1e11]:.1f} kpc (1e11), {rF[1e10]:.1f} kpc (1e10)",
      all(np.isfinite(list(Lflag.values()))) and 30 < LF < 90)
OUT["numbers"]["B3"] = dict(L_flag_kpc=Lflag, r_F_kpc=rF)

# B4 forest vs flagship
kF_phys = 1.0 / (15.0 * h) / (1 + Z_FLAG) * 1e3                              # 1/k_F in physical kpc at z = 2.5
b4 = {}
for n in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
    for fac in (1.0, 1.5):
        LL = fac * LF / 1e3 / OmL_z(Z_FLAG) ** (n / 2)
        rows_ = {}
        for foot in FOOTS:
            for m in MODES:
                rr_ = growth(bandpass_model(LL, n), A0[foot], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))
                rows_[(foot, m)] = forest_proxy(rr_)[0]
        b4[(n, fac)] = rows_
        P(f"    n = {n}, L(2.5) = {fac:.1f} x L_flag = {fac * LF:.0f} kpc (L_Lambda {LL:.2f} Mpc): forest proxy worst |dP1D| "
          + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.3g}" for k_, v in rows_.items()))
b4_min = min(min(v.values()) for v in b4.values())
check("B4 (b) FAILS THE FOREST WHEREVER IT KEEPS THE FLAGSHIP: at z ~ 2.5 the IGM's filtering length (1/k_F = 28 kpc physical "
      "at k_F = 15 h/Mpc) is shorter than the flagship floor L_flag ~ 50 kpc, so every IGM mode between them is MOND-boosted at "
      "full strength; for every epoch law tested (n = 1-4) with L(2.5) >= L_flag the linear forest proxy is off by > 10% on both "
      "footings and both yardstick modes -- a scale overlap no monotone L(z) removes (and the forest's data bracket z = 2.5)",
      f"1/k_F = {kF_phys:.0f} kpc vs L_flag = {LF:.0f} kpc; smallest worst-deviation over the scan {b4_min:.3g}", b4_min > FOREST_TOL)
OUT["numbers"]["B4"] = {f"{k_[0]}_{k_[1]}": {f"{kk[0]}_{kk[1]}": v for kk, v in d_.items()} for k_, d_ in b4.items()}
P(f"    {el()}")

# B5 KiDS vs L(0.25)
b5 = {}
for foot in FOOTS:
    base = kids_class(A0[foot])
    b5[(foot, None)] = base
    for L25 in ((0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6, 2.0) if BANDPASS else (1.3,)):
        b5[(foot, L25)] = kids_class(A0[foot], L25 if BANDPASS else None) - base
    P(f"    KiDS lead grade, {foot}: isolated P2 chi^2 {base:.1f}; d chi^2 at L(0.25) = "
      + ", ".join(f"{L25}: {b5[(foot, L25)]:+.1f}" for L25 in ((0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6, 2.0) if BANDPASS else (1.3,))))
L_kids = {}
if BANDPASS:
    for foot in FOOTS:
        xs_ = [0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6, 2.0]; ys_ = [b5[(foot, x)] for x in xs_]
        j = next(i for i in range(len(xs_) - 1) if ys_[i] > KIDS_TOL >= ys_[i + 1])
        L_kids[foot] = xs_[j] + (KIDS_TOL - ys_[j]) * (xs_[j + 1] - xs_[j]) / (ys_[j + 1] - ys_[j])
check("B5 (b) AND KiDS: with no external field in nu's argument (a harmonic field passes the band-pass with gain 0), isolated "
      "lenses tolerate the Gauss-compensated edge only if L(0.25) >~ 1.1-1.2 Mpc (d chi^2 <= +9; lead grade, L341 F7 machinery)",
      ("L_KiDS = " + ", ".join(f"{f_}: {v:.2f} Mpc" for f_, v in L_kids.items())) if L_kids else "band-pass removed (MUTATE)",
      (not BANDPASS) or (0.8 < min(L_kids.values()) and max(L_kids.values()) < 1.6),
      reading="assumes the isolated lenses' band-passed external field is negligible: the band-pass removes the > L bulk flow (97% of "
              "the linear variance, B7), leaving sub-Mpc structure that the 3-Mpc isolation cut selects against -- an estimate, not "
              "computed; the 2.4e-3 a0 sub-Mpc linear rms at a random point is its upper bound")
OUT["numbers"]["B5"] = {f"{k_[0]}_{k_[1]}": v for k_, v in b5.items()}
P(f"    {el()}")

# B6 the pincer, transformed
b6 = {}
L25G = (0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6)
R0_iso = {f: lg_isolated(A0[f]) for f in FOOTS}
P(f"    LG isolated (P2, no band-pass): R0 = {R0_iso['canonical']:.3f} / {R0_iso['alt']:.3f} Mpc")
for n in (1, 2, 3, 4):
    for L25 in L25G:
        b6[(n, L25)] = lg_both(L25 / OmL_z(Z_KIDS) ** (n / 2), n)
    P(f"    n = {n}: LG R0 at L(0.25) = " + ", ".join(f"{L25}: {b6[(n, L25)]['canonical']:.3f}/{b6[(n, L25)]['alt']:.3f}" for L25 in L25G) + " Mpc (can/alt)")
b6x = {}
for n in (1, 2, 3, 4):
    for f in FOOTS:
        R_ = np.array([b6[(n, L25)][f] for L25 in L25G]); X_ = np.array(L25G)
        L_lg = float(np.interp(LG_R0, R_, X_)) if (R_[0] <= LG_R0 <= R_[-1] and np.all(np.diff(R_) > 0)) else (float("-inf") if R_[0] > LG_R0 else float("inf"))
        R_at_k = float(np.interp(L_kids[f], X_, R_)) if BANDPASS else float("nan")
        kd_at_lg = float(np.interp(L_lg, [0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6, 2.0], [b5[(f, x)] for x in (0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.3, 1.6, 2.0)])) if (BANDPASS and np.isfinite(L_lg)) else float("nan")
        b6x[(n, f)] = dict(L_LG=L_lg, R0_at_LKiDS=R_at_k, KiDS_at_LLG=kd_at_lg)
for (n, f), v in b6x.items():
    P(f"      n = {n} {f:9s}: R0 = 0.96 at L(0.25) = {v['L_LG']:.2f} Mpc (KiDS d chi^2 there {v['KiDS_at_LLG']:+.0f}); at KiDS's floor "
      f"L_KiDS = {L_kids.get(f, float('nan')):.2f} Mpc, R0 = {v['R0_at_LKiDS']:.3f} Mpc")
b6_ok = BANDPASS and all(v["L_LG"] < L_kids[f] and v["R0_at_LKiDS"] > LG_EDGE for (n, f), v in b6x.items())
check("B6 (b) DOES NOT RESOLVE THE KiDS-LG PINCER, IT TRANSFORMS IT: the band-pass removes the external field for the Local Group "
      "as for the lenses, so the LG's R0 is set by the truncation alone; for every epoch law (n = 1-4) and both footings R0 = 0.96 "
      "needs L(0.25) BELOW the floor KiDS sets (where KiDS's d chi^2 is >> +9), and at KiDS's floor R0 exceeds even the +0.10 dex "
      "band edge (1.21 Mpc)",
      "; ".join(f"n={n}/{f[:3]}: L_LG {v['L_LG']:.2f} vs L_KiDS {L_kids.get(f, float('nan')):.2f}, R0(L_KiDS) {v['R0_at_LKiDS']:.2f}"
                for (n, f), v in b6x.items()), b6_ok)
OUT["numbers"]["B6"] = {"R0_isolated": R0_iso, "cells": {f"{k_[0]}_{k_[1]}": v for k_, v in b6.items()},
                        "pincer": {f"{k_[0]}_{k_[1]}": v for k_, v in b6x.items()}}

# B7 (reported) the linear web field left in nu's argument
kw = np.logspace(-4, 2, 1200)
Dw = np.array([Delta_lin0(k) for k in kw])
aK = 1 / (1 + Z_KIDS); DgK = growth(lcdm_model(), A0["canonical"], zs_out=(Z_KIDS,))[Z_KIDS][0] / DREF[0]
gw = gfield(Dw * DgK, aK, kw)
hw = 1 - np.exp(-0.5 * (kw * h * 1.3 / aK) ** 2)
var_all = np.trapz(gw ** 2 / kw, kw); var_bp = np.trapz((gw * hw) ** 2 / kw, kw)
check("B7 (reported) the linear web field in nu's argument at z = 0.25: all matter 3D rms y = 1.3e-2 without the band-pass; with "
      "L(0.25) = 1.3 Mpc what survives is the sub-Mpc linear power (an upper bound: for a lens isolated within 3 Mpc its "
      "neighbours' fields are harmonic there and pass with gain ~0)",
      f"all {math.sqrt(var_all) / A0['canonical']:.2e} a0 -> band-passed {math.sqrt(var_bp) / A0['canonical']:.2e} a0 "
      f"({100 * var_bp / var_all:.1f}% of the variance)", True, load_bearing=False)
P(f"    {el()}")

# ================================================================================================= H  THE COMBINATION
banner("H  THE COMBINATION (b) + (e3): band-pass for the late web, a running field floor for the early web")
P("    the kernel's tangent: (nu_P2(y) - 1) c(y/y_th), c = x^m/(1+x^m), y = |grad (S_xi - S_L) U|/a0,")
P("    L = L_Lambda Omega_L(<K>_h)^(n/2),  y_th = y_Lambda Omega_L(<K>_h)^(-p')  (cells labelled by L(0.25), y_th(0.25))")
h1 = {}
H1_L25, H1_Y25, H1_PP = (1.3, 1.6, 2.0), (3e-7, 1e-6, 3e-6), (3.5, 4.0, 4.5)
kids_h1 = {(L25, y25): (kids_class(A0["canonical"], L25 if BANDPASS else None, y25, 4) - b5[("canonical", None)])
           for L25 in H1_L25 for y25 in H1_Y25}
P("    KiDS (lead grade, canonical) with the floor at z = 0.25: " + ", ".join(f"L={k_[0]}/y_th={k_[1]:g}: {v:+.1f}" for k_, v in kids_h1.items()))
for n in (1.5, 2.0, 2.5):
    for L25 in H1_L25:
        for pp in H1_PP:
            for y25 in H1_Y25:
                LL = L25 / OmL_z(Z_KIDS) ** (n / 2); fl = (y25, pp, 4)
                mod = bandpass_model(LL, n, floor=fl)
                s8 = {m: s8ratio(mod, "canonical", m) for m in MODES}
                fr = {m: forest_proxy(growth(mod, A0["canonical"], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0)))[0] for m in MODES}
                Lz = L_phys(LL, n, 1 / (1 + Z_FLAG)) * 1e3
                fd = flag_dev(Lz, "canonical", yth=y_th_z(fl, Z_FLAG))
                h1[(n, L25, pp, y25)] = dict(s8=s8, forest=fr, flag=fd, kids=kids_h1[(L25, y25)], Lflag_kpc=Lz,
                                             yth2=y_th_z(fl, 2.0), yth25=y_th_z(fl, Z_FLAG), yth3=y_th_z(fl, 3.0))
def _inwin(v):
    return (max(v["s8"].values()) <= SIG8_BAND[1] and min(v["s8"].values()) >= SIG8_BAND[0] and max(v["forest"].values()) <= FOREST_TOL
            and abs(v["flag"]) <= FLAG_TOL and v["kids"] <= KIDS_TOL)
win = [k_ for k_, v in h1.items() if BANDPASS and _inwin(v)]
fail_by = {g_: sum(1 for v in h1.values() if not ok_(v)) for g_, ok_ in (
    ("sigma_8", lambda v: SIG8_BAND[0] <= min(v["s8"].values()) and max(v["s8"].values()) <= SIG8_BAND[1]),
    ("forest", lambda v: max(v["forest"].values()) <= FOREST_TOL), ("flagship", lambda v: abs(v["flag"]) <= FLAG_TOL),
    ("KiDS", lambda v: v["kids"] <= KIDS_TOL))}
P(f"    {len(h1)} cells (canonical): in the window (sigma_8 [0.922, 1.05], forest proxy <= 10%, flagship <= 0.05 dex, KiDS <= +9): "
  f"{len(win)}; cells failing each gate: {fail_by}")
for k_, v in sorted(h1.items()):
    if k_[0] == 2.0 and k_[3] == 1e-6:
        P(f"      n={k_[0]} L(0.25)={k_[1]} p'={k_[2]} y_th(0.25)={k_[3]:g} (y_th = {v['yth2']:.1e}/{v['yth25']:.3f}/{v['yth3']:.3f} at z = 2/2.5/3): "
          f"s8 {v['s8']['rms']:.4f}/{v['s8']['permode']:.4f}, forest {v['forest']['rms']:.2g}/{v['forest']['permode']:.2g}, flagship "
          f"{v['flag']:+.4f} dex, KiDS {v['kids']:+.1f}{'  <- window' if k_ in win else ''}")
check("H1 THE COMBINATION HAS A WINDOW on the linchpin's gates (canonical scan of 81 cells): sigma_8 in [0.922, 1.05], the linear "
      "forest proxy within 10% at z = 2 and 3, the 1e11 flagship within 0.05 dex at z = 2.5, and KiDS (lead grade, band-pass and floor "
      "together) within +9 -- the band-pass removes the late web, the floor the early web and the IGM; KiDS caps the floor at "
      "y_th(0.25) ~ 1e-6, the forest then needs p' ~ 4",
      f"{len(win)} of {len(h1)} cells in the window; e.g. {win[:4]}", len(win) >= 3)
OUT["numbers"]["H1"] = {f"{k_[0]}_{k_[1]}_{k_[2]}_{k_[3]}": v for k_, v in h1.items()}
P(f"    {el()}")

# H2 the headline cell, every gate
HEAD = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6, m=4)
LLh = HEAD["L25"] / OmL_z(Z_KIDS) ** (HEAD["n"] / 2); FLh = (HEAD["y25"], HEAD["pp"], HEAD["m"])
modh = bandpass_model(LLh, HEAD["n"], floor=FLh)
h2 = {"s8": {}, "forest": {}, "flag": {}, "sparc": {}, "kids": {}, "Geff": {}}
for foot in FOOTS:
    for m in MODES:
        h2["s8"][(foot, m)] = s8ratio(modh, foot, m)
        res_ = growth(modh, A0[foot], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0))
        for kF in (10.0, 15.0, 20.0):
            h2["forest"][(foot, m, kF)] = forest_proxy(res_, kF=kF)[0]
    h2["s8"][(foot, "mono_rms")] = s8ratio(modh, foot, "rms", kernel="mono")
    for M in (1e10, 1e11):
        h2["flag"][(foot, M)] = law_dev_dex(M, A0[foot], 0.1, L_phys(LLh, HEAD["n"], 1 / (1 + Z_FLAG)), y_th_z(FLh, Z_FLAG))
    L0h = L_phys(LLh, HEAD["n"], 1.0); y0h = y_th_z(FLh, 0.0)
    h2["sparc"][foot] = max(abs(law_dev_dex(M, A0[foot], y, L0h, y0h)) for M in (1e9, 1e10, 1e11, 1e12) for y in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
    h2["kids"][foot] = (kids_class(A0[foot], HEAD["L25"] if BANDPASS else None, y_th_z(FLh, Z_KIDS)) - b5[(foot, None)])
h2["s8_rtol"] = (sigma8_of(growth(modh, A0["canonical"], mode="rms")[0.0]) / S8_LCDM,
                 sigma8_of(growth(modh, A0["canonical"], mode="rms", rtol=1e-8)[0.0]) / S8_LCDM)
# grid convergence of the forest proxy (canonical, both modes): 96 -> 144 k-points
KHF2 = np.logspace(math.log10(0.02), math.log10(100.0), 144); DIF2 = np.array([Delta_lin0(k) for k in KHF2]) / _r0
REF_F2 = growth(lcdm_model(), A0["canonical"], KHg=KHF2, Dig=DIF2, zs_out=(2.0, 3.0))
h2["forest_conv"] = {m: (forest_proxy(growth(modh, A0["canonical"], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0)))[0],
                         forest_proxy(growth(modh, A0["canonical"], mode=m, KHg=KHF2, Dig=DIF2, zs_out=(2.0, 3.0)), KHg=KHF2, REFg=REF_F2)[0])
                     for m in MODES}
# G_eff in the linear web today (max over the sigma_8 modes), both modes
aa = 1.0; resh = growth(modh, A0["canonical"], mode="permode")[0.0]
gk_ = gfield(resh, aa, KH); hk_ = modh["hfac"](aa, KH); y_ = gk_ * hk_ / A0["canonical"]
Ce_ = (nu_p2(y_) - 1) * modh["cut"](y_, aa) * hk_ ** 2
sel = (KH >= 0.05) & (KH <= 0.5)
h2["Geff"] = dict(max_sigma8_modes=float(np.max(Ce_[sel])), max_all=float(np.max(Ce_)))
P(f"    headline cell: n = {HEAD['n']}, L(0.25) = {HEAD['L25']} Mpc (L_Lambda = {LLh:.2f} Mpc; L(0) = {L_phys(LLh, HEAD['n'], 1.0):.2f} Mpc, "
  f"L(2.5) = {1e3 * L_phys(LLh, HEAD['n'], 1 / 3.5):.0f} kpc), y_th(0.25) = {HEAD['y25']:g}, p' = {HEAD['pp']}, m = {HEAD['m']} "
  f"(y_th = {y_th_z(FLh, 0):.2e} / {y_th_z(FLh, 1.0):.2e} / {y_th_z(FLh, 2.0):.2e} / {y_th_z(FLh, 2.5):.3f} / {y_th_z(FLh, 3.0):.3f} at z = 0/1/2/2.5/3)")
P("      sigma_8/LCDM: " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.4f}" for k_, v in h2["s8"].items()))
P("      forest proxy worst |dP1D| (z = 2, 3; k_F = 10/15/20 h/Mpc): " + ", ".join(f"{k_[0][:3]}/{k_[1]}/{k_[2]:.0f}: {v:.3g}" for k_, v in h2["forest"].items()))
P("      flagship (g_bar = 0.1 a0, z = 2.5): " + ", ".join(f"{k_[0][:3]} {k_[1]:.0e}: {v:+.4f} dex" for k_, v in h2["flag"].items()))
P("      SPARC range (z = 0, M_b = 1e9-1e12, y = 0.01-100): max |dev| " + ", ".join(f"{k_[:3]}: {v:.1e} dex" for k_, v in h2["sparc"].items()))
P("      KiDS lead grade d chi^2 (band-pass + floor at z = 0.25): " + ", ".join(f"{k_[:3]}: {v:+.1f}" for k_, v in h2["kids"].items()))
P(f"      sigma_8 (canonical, rms) at ODE rtol 1e-6 / 1e-8: {h2['s8_rtol'][0]:.5f} / {h2['s8_rtol'][1]:.5f}")
P("      forest proxy, 96 vs 144 k-points (canonical): " + ", ".join(f"{m}: {v[0]:.2e} / {v[1]:.2e}" for m, v in h2["forest_conv"].items()))
P(f"      linear web today: C_eff <= {h2['Geff']['max_sigma8_modes']:.2e} on the sigma_8 modes (0.05-0.5 h/Mpc), <= {h2['Geff']['max_all']:.2f} on "
  f"any mode to 20 h/Mpc (G_eff = G (1 + C_eff)/(1 - alpha_c(1 + C_eff)/2), no slip)")
h2_ok = (all(SIG8_BAND[0] <= v <= SIG8_BAND[1] for v in h2["s8"].values())
         and all(v <= FOREST_TOL for v in h2["forest"].values())
         and all(abs(v) <= FLAG_TOL for v in h2["flag"].values())
         and all(v <= SPARC_TOL for v in h2["sparc"].values())
         and all(v <= KIDS_TOL for v in h2["kids"].values())
         and all(max(v) <= FOREST_TOL for v in h2["forest_conv"].values())
         and abs(h2["s8_rtol"][0] - h2["s8_rtol"][1]) < 1e-3)
check("H2 THE HEADLINE CELL passes every linchpin gate on both footings: sigma_8 in [0.922, 1.05] (rms, per-mode, and nu_mono), the "
      "forest proxy within 10% at k_F = 10, 15, 20 h/Mpc, the 1e10 and 1e11 flagships within 0.05 dex, the SPARC-range law within "
      "0.01 dex, KiDS (lead grade) within +9 -- with the MOND tangent exactly zero on FRW (S5) and a non-negative second variation "
      "(S3, S4)",
      f"sigma_8 {min(h2['s8'].values()):.4f}-{max(h2['s8'].values()):.4f}; forest <= {max(h2['forest'].values()):.3g}; flagship "
      f"{min(h2['flag'].values()):+.3f}..{max(h2['flag'].values()):+.3f} dex; SPARC {max(h2['sparc'].values()):.1e} dex; KiDS "
      f"{min(h2['kids'].values()):+.1f}..{max(h2['kids'].values()):+.1f}", h2_ok,
      reading="the LINCHPIN as posed (MOND tangent zero on FRW, small and finite in the linear web, galaxies and the Solar System "
              "untouched) is met by one action term -- at five DECLARED constants (H4), with the forest and KiDS at proxy/lead grade")
OUT["numbers"]["H2"] = {k_: {str(kk): v for kk, v in d_.items()} if isinstance(d_, dict) else d_ for k_, d_ in h2.items()}
P(f"    {el()}")

# H2b: E < 2 at EVERY field and epoch, not only on exact FRW (FP5's ill-posed band y < y* is gone)
yL_h = HEAD["y25"] * OmL_z(Z_KIDS) ** HEAD["pp"]                         # the de Sitter-limit floor (the smallest y_th ever)
ysc = np.logspace(-14, 4, 4000)
def _CTL(yv_):                                                                # C_T and C_L = d[y (nu - 1) c]/dy on a log grid
    CT = (nu_p2(ysc) - 1) * cutfac(ysc, yv_, HEAD["m"]); CL = np.gradient(ysc * CT, ysc)
    return float(max(np.max(CT), np.max(CL)))
Cmax = {lab: _CTL(yv_) for lab, yv_ in (("z=0", y_th_z(FLh, 0.0)), ("de Sitter", yL_h))}
Emax = {(lab, ac): ac + 2 * Cv / (1 + Cv) for lab, Cv in Cmax.items() for ac in ALPHA_C}
check("H2b THE WHOLE ILL-POSED BAND IS GONE: with the floor, C_eff <= max_y max(C_T, C_L) ~ y_th^(-1/2) at every field "
      "value, largest in the de Sitter limit (y_th -> y_Lambda); that stays far below (2 - alpha_c)/alpha_c, so E < 2 (the khronon "
      "healthy, FP5 C1) at every field and epoch -- the ungated core's band y < y* (FP5 C4) has no counterpart",
      "max C_eff: " + ", ".join(f"{k_}: {v:.3g}" for k_, v in Cmax.items()) + "; E_max: "
      + ", ".join(f"{k_[0]}/alpha_c={k_[1]:.1e}: 2 - {2 - v:.2e}" for k_, v in Emax.items()),
      all(v < 2 for v in Emax.values()) and max(Cmax.values()) < 0.01 * (2 - ALPHA_C[1]) / ALPHA_C[1])
OUT["numbers"]["H2b"] = {"Cmax": Cmax, "Emax": {f"{k_[0]}_{k_[1]}": v for k_, v in Emax.items()}}
# (reported) how far in z the 1e11 flagship survives in the headline cell
def _flag_z(z, foot="canonical"):
    return law_dev_dex(1e11, A0[foot], 0.1, L_phys(LLh, HEAD["n"], 1 / (1 + z)), y_th_z(FLh, z)) + FLAG_TOL
try:
    zfl = {f: brentq(lambda z: _flag_z(z, f), 2.0, 6.0, xtol=1e-3) for f in FOOTS}
except ValueError:
    zfl = {f: float("nan") for f in FOOTS}
check("H2c (reported) the headline cell's 1e11 flagship (g_bar = 0.1 a0) stays within 0.05 dex of P2 up to z_max; beyond it the "
      "running floor switches MOND off (a prediction, like the vacuum gate's z_on; FP3's D1 reached 4.1, DE2's p = 1 gate 4.2-5.0)",
      f"z_max = {zfl['canonical']:.2f} (canonical) / {zfl['alt']:.2f} (alt)", True, load_bearing=False)
OUT["numbers"]["H2c"] = zfl

# H3 the Local Group
h3 = {}
for (n, L25) in ((2.0, 1.3), (2.0, 1.6), (2.5, 1.3), (1.5, 1.3), (2.0, 1.0), (2.0, 0.6)):
    LL = L25 / OmL_z(Z_KIDS) ** (n / 2)
    h3[(n, L25)] = lg_both(LL, n, floor=FLh)
    P(f"    n = {n}, L(0.25) = {L25} Mpc + floor: LG R0 = {h3[(n, L25)]['canonical']:.3f} / {h3[(n, L25)]['alt']:.3f} Mpc")
kids_ok_cells = [k_ for k_ in h3 if BANDPASS and k_[1] >= max(L_kids.values())]
h3_fail = all(min(h3[k_].values()) > LG_EDGE for k_ in kids_ok_cells) and len(kids_ok_cells) > 0
check("H3 THE COMBINATION FAILS THE LOCAL GROUP (the pincer, verified at every KiDS-passing cell tested, both footings): with the "
      "EFE removed by the band-pass and the floor below 3e-4 at z < 1, the LG keeps its phantom to ~L and R0 = 1.3-1.5 Mpc against "
      "0.96 +- 0.03 (and the +0.10 dex edge 1.21); R0 = 0.96 returns only at L(0.25) ~ 0.6 Mpc, which KiDS excludes",
      "; ".join(f"n={k_[0]} L25={k_[1]}: {v['canonical']:.2f}/{v['alt']:.2f}" for k_, v in h3.items()), h3_fail)
OUT["numbers"]["H3"] = {f"{k_[0]}_{k_[1]}": v for k_, v in h3.items()}

# H4 the constants
consts = [
    ("L_Lambda", f"{LLh:.2f} Mpc (headline)", "DECLARED", "band-pass length in the de Sitter limit; window from KiDS (L(0.25) >= ~1.2 Mpc) and the flagship (L(2.5) >= ~50 kpc)"),
    ("n", f"{HEAD['n']}", "DECLARED", "the vacuum-share power of L; growth needs n >= ~2 (B2); the vacuum gate's analogue is 1 + p"),
    ("y_Lambda", f"{HEAD['y25'] * OmL_z(Z_KIDS) ** HEAD['pp']:.2e} (y_th(0.25) = {HEAD['y25']:g})", "DECLARED", "the field floor in the de Sitter limit; KiDS caps y_th(0.25) <~ 1e-6-3e-6 (H1)"),
    ("p'", f"{HEAD['pp']}", "DECLARED", "the floor's vacuum-share power; with y_th(0.25) ~ 1e-6 the forest needs p' >~ 3.75, the flagship p' <~ 4.5 (H1)"),
    ("m", f"{HEAD['m']}", "DECLARED", "the cut-off's sharpness; health holds for every m (S4); m > 1/2 zeroes the FRW tangent"),
    ("xi, alpha_c, c_2, kappa", "unchanged", "as FP0/FP1/FP5", "the core's own constants"),
]
for k_, v, s_, w_ in consts:
    P(f"    {k_:22s} {v:34s} {s_:10s} {w_}")
check("H4 (reported) THE PRICE: the combination adds five constants, every one DECLARED (none derived): L_Lambda, n (the band-pass), "
      "y_Lambda, p', m (the floor); the epoch enters only through Omega_L(<K>_h), a leaf average (no local second variation)",
      f"{len(consts) - 1} new constants, 0 derived", True, load_bearing=False)
OUT["numbers"]["H4"] = consts
P(f"    {el()}")

# ================================================================================================= T  THE TABLE
banner("T  THE CLASS TABLE")
tab = [
    ("(a) local monotone gate", "W(rho_dyn) x 2 alpha^2 q", "iff W(FRW) = 0", "concave 1.014-1.020 (FP3)", "concave: L* outskirts/KiDS cut",
     "rho_* (+ p)", "FAILS (FP3 lemma: convex = anti-pressure; concave = chord-bounded, FP5 band survives)"),
    ("(b) band-pass (+e1)", "q(|D(W_b - W_B)|^2/alpha^2), B = L(<K>)^2/2", "alone NO (oo x h^2); with e1 yes", f"n>=2: <= {max(max(b2[(2, LL)].values()) for LL in (0.5, 1.0, 2.0, 3.0)):.3f}",
     "yes (SPARC, Sun); Gauss edge", "L_Lambda, n (+y_r)", "FAILS forest vs flagship (B4) and KiDS-LG (B6); escapes the lemma (S3)"),
    ("(c) khronon-variable gate", "W(K) or W(K - <K>_h)", "-", "-", "K = 3H in galaxies (CV4)", "-", "FAILS: blind (CV4), backreaction too weak (FP3 C7)"),
    ("(d) tidal-invariant gate", "W(E:E/X_c) x 2 alpha^2 q", "-", "-", "-", "X_c", "FAILS: (Phi,u) symbol zero wherever W' > 0 (S7)"),
    ("(e1) shifted kernel", "q' = nu(y + y_r) - 1", "yes, y_r > 2.6e-18", f"y_r<=1e-4: {e1_rows[1e-4]['s8']:.0f}-{e1_rows[1e-4]['s8max']:.0f}", "yes at y_r <~ 5e-4",
     "y_r", "FAILS growth (E1, E3); escapes the lemma (S4)"),
    ("(e2/e3) cut-off tangent", "q' = (nu - 1) c(y/y_th(<K>))", "yes, zero tangent", f">= {e3min:.2f} (E3 bound)", "only if y_th below KiDS",
     "y_Lambda, p', m", "FAILS growth alone (E3); escapes the lemma (S4)"),
    ("(H) = (b) + (e3)", "q_c(|D(W_b - W_B)|^2/alpha^2; <K>_h)", "yes, zero tangent", f"{min(h2['s8'].values()):.3f}-{max(h2['s8'].values()):.3f}",
     f"yes (SPARC, Sun, KiDS lead; flagship to z ~ {min(zfl.values()):.1f})", "L_Lambda, n, y_Lambda, p', m", "linchpin MET; FAILS the LG (H3); forest/KiDS proxy/lead grade"),
]
P(f"    {'class':26s} | {'FRW well-posed?':30s} | {'sigma_8 / LCDM':24s} | {'galaxies intact?':32s} | {'new constants':26s} | status")
for row in tab:
    P(f"    {row[0]:26s} | {row[2]:30s} | {row[3]:24s} | {row[4]:32s} | {row[5]:26s} | {row[6]}")
    P(f"    {'':26s}   action: {row[1]}")
OUT["numbers"]["table"] = tab

# ================================================================================================= W  LEDGER
banner("W  THE LEDGER")
LEDGER = [
    ("G6a", "the band-pass as an action: C-H's heat branch read at two diffusion times; linear theory C_eff = C (e^{-xi^2k^2/2} - e^{-L^2k^2/2})^2; no mode added", "DERIVED", "S1 (exact elimination), S2 (Schur, kernel-free det)"),
    ("G6b", "(b) and (e) escape FP3's lemma: no multiplier on the MOND energy, no W''(dX)^2 term; health = monotone phantom (C_T, C_L >= 0) x h^2", "DERIVED", "S3, S4; the energy-multiplied cut-off control carries c''"),
    ("G6c", "FRW linearisation per class: ungated and band-pass-alone ill-posed; (e1) well-posed iff y_r > 2.6e-18; cut-off classes exactly GR + BPS on FRW (G_eff = G/(1 - alpha_c/2), no slip)", "DERIVED", "S5 on FP2's committed block; S6 order counting"),
    ("G6d", "class (e) alone (any kernel of the local field and the epoch): linear growth", "FAILS", "E2-E3: the web's field at z = 0.25 lies in KiDS/SPARC's range; the most generous kernel gives sigma_8 >= 1.15"),
    ("G6e", "(b) Gauss compensation: every isolated system weighs its baryons beyond ~2L", "DERIVED", "B1 (the record's L352 edge: the band-passed input vanishes beyond ~L, the output filter keeps the monopole zero)"),
    ("G6f", "(b) late-time growth: sigma_8 <= 1.05 needs L shrinking as Omega_L^(n/2), n >= 2", "DERIVED", "B2"),
    ("G6g", "(b) alone: the forest (z = 2-3) against the 1e11 flagship (z = 2.5)", "FAILS", "B3-B4: 1/k_F ~ 28 kpc < L_flag ~ 50 kpc -- a scale overlap no L(z) removes"),
    ("G6h", "(b): the KiDS-LG pincer", "FAILS", "B5-B6: transformed from the EFE into the truncation scale (the LG needs L(0.25) ~ 0.5 Mpc, KiDS >= ~1.2 Mpc); not resolved"),
    ("G6i", "the combination (H): band-passed argument + running field floor, both through Omega_L(<K>_h)", "POSTULATED", "chosen after the survey; five declared constants (H4)"),
    ("G6j", f"(H) meets the linchpin: MOND tangent zero on FRW and E < 2 at every field, sigma_8 within 2%, forest proxy <= 10%, flagship <= 0.05 dex (to z ~ {min(zfl.values()):.1f}), SPARC and the Sun untouched, KiDS lead grade", "DERIVED", "H1-H2c, given G6i and its constants (forest a linear proxy, KiDS lead grade)"),
    ("G6k", "(H): the Local Group's zero-velocity radius (the pincer)", "FAILS", "H3: R0 = 1.3-1.5 Mpc at every KiDS-passing cell"),
    ("G6l", "(H)'s constants L_Lambda, n, y_Lambda, p', m", "POSTULATED", "declared; windows set by KiDS, the flagship, the forest and sigma_8 (H1)"),
    ("G6m", "classes (a), (c), (d): local multiplier gates", "FAILS", "FP3's lemma (C1, C3, C5, C7, T), CV4; (d) S7: symbol zero wherever W' > 0"),
    ("G6n", "(H) beyond linear order: the sub-L web keeps C_eff ~ 0.6 at k <= 0.5 h/Mpc and ~12 at 20 h/Mpc today (cosmic shear, halo masses); the flux P1D (PM); full KiDS (2-halo, and the isolated lenses' band-passed external field, estimated <~ 2e-4 a0 but not computed); the carrier in galaxies; nonlinear well-posedness of a Mpc-range leafwise filter", "OPEN", "not computed here (no PM run in this lane)"),
]
for k_, what, status, why in LEDGER:
    P(f"    {k_:5s} {status:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w, status=s_, basis=b) for k_, w, s_, b in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
gpass = False
check("G1 (reported) G-1 passed WHOLE by a class in this survey (linchpin gates AND the Local Group)",
      "no: (H) meets the linchpin's gates but fails the LG; (b) and (e) alone fail growth or the forest", gpass, load_bearing=False)

# ================================================================================================= VERDICT
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"""  (e) Kernel regularisations escape FP3's lemma -- reshaping the phantom law monotonically is healthy for every switch shape
      (C_L = c C_L,P2 + y (nu - 1) c'/y_th >= 0) -- and they cure FP5's Hadamard band (finite or zero tangent on FRW).  Alone they
      FAIL growth: the linear web's field at z = 0.25 sits inside the range KiDS and SPARC need, so even the most generous local
      kernel gives sigma_8 >= {e3min:.2f} x LCDM.
  (b) A band-pass built from C-H's own heat branch (read at two diffusion times) also escapes the lemma (it is linear in U), and
      the variation makes every isolated system Gauss-compensated.  Shrinking with the vacuum share (n >= 2) it fixes late growth.
      Alone it is ill-posed on FRW, and it FAILS the forest against the flagship (IGM filtering length ~28 kpc < flagship floor
      ~{LF:.0f} kpc at z ~ 2.5) and does not resolve the KiDS-LG pincer: it transforms it into a truncation scale.
  (H) The combination -- band-pass for the late web, a running field floor y_th = y_Lambda Omega_L^(-p') for the early web -- meets
      the linchpin as posed: MOND tangent zero on FRW, sigma_8 {min(h2['s8'].values()):.3f}-{max(h2['s8'].values()):.3f}, forest proxy <= {max(h2['forest'].values()):.2g}, flagship within {max(abs(v) for v in h2['flag'].values()):.3f} dex,
      SPARC and the Sun untouched, KiDS (lead grade) within +9.  It FAILS the Local Group (R0 = 1.3-1.5 Mpc): the pincer survives.
      Five DECLARED constants; nothing here is derived from the framework's first principles.  Not 'closed'.  Time {time.time() - T0:.0f} s.""")
json.dump(OUT, open(os.path.join(HERE, f"FP6_gate_survey_results{'_MUTATE' if MUTATE else ''}.json"), "w"), indent=1, default=str)
P(f"\n  {len(CH) - sum(1 for _, ok, _ in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"FP6_gate_survey_results{'_MUTATE' if MUTATE else ''}.json")
sys.exit(0 if n_fail == 0 else 1)
