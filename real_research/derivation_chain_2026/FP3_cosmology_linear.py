#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP3 -- GATE G-1, LINEAR COSMOLOGY WITH NO PRESCRIBED MASK, on the ungated C-H/K core: what, in the core's own
variables, can keep the MOND sector off in the linear web and on in galaxies -- and what no local mechanism can do.

WHY.  The ungated C-H/K core drives sigma_8 to 18-27 (L341, committed) and has no well-posed linearisation on its own
FRW (FP5, committed a26136bc4: at zero field U is pinned and the khronon's alpha_eff = alpha_c + 2 > 2).  Every repair
on the record is either posited (L359's vacuum gate, a prescribed mask) or, as a varied action term, unstable (a
threshold gate flat at both ends has W'' of both signs: DE7, DE12, DE13, CV3), blind (K-only: CV4) or leaks/slips
(curvature or matter readings: MS1, DE7).  This lane derives, from the core's own action: (i) why the core fails linear
cosmology; (ii) FP5's criterion and C1's stability rule for any local gate on the MOND energy; (iii) the most a stable
local gate can deliver (the chord bound) and one explicit construction at that bound; (iv) the construction proposed in
the G-1 brief (a leaf-average global factor times a convex local ramp), tested; (v) the resulting trilemma.

THE ACTION (the ungated core: astra's C-H, ACTION.md; L340's BPS terms with beta = 0; L350's leaf average; nu_mono):
    I = c^3/(16 pi G) Int d^4x sqrt(-g) { R - 2 Lambda + 2 h^{mn}(D_m U - a_m)(D_n U - a_n)
          + 2 alpha^2 q(h^{mn} D_m W_b D_n W_b / alpha^2) + Int_0^b dz L (d_z W - Delta_h W) + lambda_0 (W_0 - U)
          + alpha_c a_m a^m - c_2 (K - <K>_h)^2 } + GHY + S_m[g] + S_dark[g; declared cold state]
    alpha = a0/c^2;  q'(Z) = nu_mono(sqrt Z) - 1, q(0) = 0;  n_m = -d_m tau/sqrt(X), a_m = D_m ln N, K = nabla_m n^m.
    The dark mass is declared cold initial data at Omega_c (FP4 owns it).
THE GATES TESTED (one factor on the MOND term, 2 alpha^2 q -> 2 alpha^2 W q, varied with everything else):
    concave:  W = w(rho_dyn/rho_*(<K>_h)), w(u) = u/(1+u^4)^(1/4),  rho_dyn = (c^2/8 pi G)(<K>_h^2/3 - Lambda + 2 D_i a^i)
              (the dynamical density read off the clock's own acceleration divergence D_i a^i -- the physical
              potential's Laplacian -- plus the leaf mean); rho_* > 0 a function of the LEAF-AVERAGED expansion only.
    proposal: W = [Omega_L(<K>_h)/Omega_L0]^p ((x - x_c)_+ / (x_N - x_c))^n,  x = 4 pi G (rho_dyn - rho_bar)/H^2
              (proposed in the G-1 brief: a leaf-average global factor times a convex local ramp, flat only at the low end).
    threshold (control): a C^inf step flat at both ends (CV3's transition).
The footings: a0 = 9.3603e-11 (rho_Lambda) and 1.1312e-10 (rho_total), FP0.

CHECKS
  A1 FRW by minisuperspace variation (sympy): with the leaf average the Friedmann equation is GR's (G_cos = G).
  A2 CONTROL: plain -c_2 K^2 gives H^2(1 + 3c_2/2).     A3 a0 absent from the background; a0(z)/a0(0) = 1, both footings.
  B1 ORDER COUNTING (sympy): q(Z) = (4/3) Z^(3/4) + ... is O(eps^(3/2)) around FRW -- below the O(eps^2) action: the
     linear theory is non-analytic; an AQUAL-type J(Y) ~ Y^(3/2) would be O(eps^3).
  B2 CONTROL: L341's growth yardstick, re-implemented, reproduces L341's committed sigma_8.  B3 the ungated core: > 10.
  C0 FP5'S CRITERION FOR GATES (FP5's committed E(C), checked symbolically): with a gate the zero-field tangent is
     C_eff = W C_T; the khronon is healthy iff C_eff < (2 - alpha_c)/alpha_c; the tangent vanishes identically on FRW
     iff W(FRW) = 0 and W = o(sqrt y) there.
  C1 THE STABILITY RULE (sympy static symbol, gate reading the lapse Laplacian): B = 2 alpha^2 q >= 0; the symbol has a
     zero iff B W'' > 0; the gate's local term on matter is a pressure of sign -B W''; psi = phi.  Stable <=> W concave.
     Lemma: a factor built from a leaf average (<K>_h) adds nothing to the local second variation.
  C2 THE SIGMA_8 TOLERANCE f_max (web on-fraction with sigma_8 <= 1.02 x LCDM), both footings, rms and per-mode.
  C3 THE CHORD BOUND: concave W >= 0 obeys W(rho) <= (rho/rho_bar) W(rho_bar): every stable local gate is half off
     beyond ~0.1-0.3 Mpc of an isolated galaxy (the Mpc lensing halo cannot be its MOND phantom).
  C4 THE CONCAVE CONSTRUCTION at the bound, four designs (D1 flagship <= 1e11; D2 <= 1e12; D3/D4 RAR tails):
     (a) sigma_8 within 2%, (b) galaxy interiors on (D1) and the trade across designs (b', reported), (c) non-negative
     second variation (the local-K reading as a failing control), (d) unique self-consistent state, (e) its prices
     (reported: KiDS radius, IGM force boost, z > z_on, the gate's own force), (f) FP5: its tangent does NOT vanish on FRW.
  C5 CONTROL: the threshold gate passes sigma_8, the galaxies and FP5, but W'' takes both signs and it is bistable.
  C8 THE PROPOSAL (leaf-average factor x convex ramp): (a) the global factor has no local second variation; (b) FP5,
     sigma_8 and the z = 2-3 IGM pass; (c) the convex ramp FAILS the second variation (anti-pressure); (d) without an
     upper plateau the RAR fails -- the kernel's saturation does not bound W.
  C6 THE TRACKING CLASS FAILS (sigma_8 vs KM2's moving-source pole).   C7 THE K-FLOOR WITH BACKREACTION FAILS.
  T  THE TRILEMMA: no local gate tested meets FP5, a non-negative second variation and sigma_8 + galaxies together.
  W  the ledger.        G1 (reported, not load-bearing) the gate's status.
MUTATE=1 replaces C4's concave gate by the threshold gate with the same edge: C4(c) and C4(d) must FAIL (rc = 1).

SCOPE.  Frozen-coefficient, local (WKB) stability as in CV3/DE12/FP5; sigma_8 from the record's L341/L142 growth
yardstick (the MOND boost on the linear field at its physical amplitude, rms and per-mode); spherical point-mass
phantoms for galaxies.  Not a Boltzmann run, not a nonlinear or N-body result.

Run from the repository root:  python3 real_research/derivation_chain_2026/FP3_cosmology_linear.py
"""
import os, sys, json, math, time, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP3_cosmology_linear" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP3", "gate": "G-1", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)


def check(name, measured, ok, load_bearing=True):
    CH.append((name, bool(ok), load_bearing))
    OUT["checks"][name] = {"ok": bool(ok), "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: C4's concave gate is replaced by the threshold (flat-flat) gate with the same edge -- "
      "C4(c) and C4(d) must FAIL ***")

# --------------------------------------------------------------------------------------------- constants
c = 2.99792458e8; Mpc = 3.0856775814913673e22; kpc = Mpc / 1e3; G = 6.67430e-11; MSUN = 1.98847e30
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # FP0's footings (H0 = 67.4, Omega_L = 0.6847)
A0_L341 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}       # L341's committed inputs (control reproduction only)
FOOTS = ("canonical", "alt")
MODES = ("rms", "permode")
C2W = 7.3e-3                                                 # c_2 at L340's window floor (leaf average: background-safe)
ALPHA_C = (9.624e-14, 3.2e-9)                                # L340's alpha_c window ends (FP5 C3)
V_MOVE = 600e3                                               # a galaxy's speed relative to the CMB frame (KM2)
V_GAS = 100e3                                                # a generous gas/stellar dispersion at a galaxy's MOND radius

# ============================================================================================= A  FRW background
banner("A  THE CORE ON FRW: minisuperspace variation (sympy), leaf average vs plain c_2")
t = sp.symbols("t", real=True)
Nf = sp.Function("N", positive=True)(t)
af = sp.Function("a", positive=True)(t)
Gs, Lam, c2s, rho0 = sp.symbols("G Lambda c_2 rho_0", positive=True)
Hn = sp.diff(af, t) / (af * Nf)                               # expansion rate per proper time
Kfrw = 3 * Hn                                                 # K = nabla_m n^m of the comoving clock
KijKij_minus_K2 = 3 * Hn ** 2 - Kfrw ** 2                     # flat leaves: R^(3) = 0
# On FRW: N = N(t) so a_m = D_m ln N = 0; U = U(t) so h^{mn} D U D U = 0; W_b = U (the constant mode has gain one),
# L = lambda_0 = 0; q(0) = 0; and (K - <K>_h) = 0 on a homogeneous leaf.  Every C-H/K term but R - 2 Lambda vanishes.
L_core = Nf * af ** 3 / (16 * sp.pi * Gs) * (KijKij_minus_K2 - 2 * Lam) - Nf * rho0            # dust: rho = rho0/a^3
L_ctrl = Nf * af ** 3 / (16 * sp.pi * Gs) * (KijKij_minus_K2 - 2 * Lam - c2s * Kfrw ** 2) - Nf * rho0
Hs = sp.symbols("H", positive=True)


def H2_from(L):
    """the N-equation (Hamiltonian constraint) at N = 1, solved for H^2."""
    e = sp.diff(L, Nf).subs(Nf, 1).subs(sp.diff(af, t), Hs * af)
    sol = sp.solve(sp.Eq(e, 0), Hs)
    return sp.simplify(sol[0] ** 2) if sol else None


H2c = H2_from(L_core)
gr = 8 * sp.pi * Gs * rho0 / (3 * af ** 3) + Lam / 3
okA1 = H2c is not None and sp.simplify(H2c - gr) == 0
ELa = sp.diff(sp.diff(L_core, sp.diff(af, t)), t) - sp.diff(L_core, af)          # the a-equation
ELa1 = sp.simplify(ELa.doit().subs(sp.diff(Nf, t), 0).subs(Nf, 1))
acc = sp.solve(sp.Eq(ELa1, 0), sp.diff(af, t, 2))
acc_q = sp.simplify((acc[0] / af).subs(sp.diff(af, t), sp.sqrt(H2c) * af)) if acc else None
acc_ok = acc_q is not None and sp.simplify(acc_q - (-4 * sp.pi * Gs * rho0 / (3 * af ** 3) + Lam / 3)) == 0
check("A1 on FRW every C-H/K term but R - 2 Lambda vanishes (a_m = 0, U homogeneous, q(0) = 0, K = <K>), and the "
      "minisuperspace variation gives GR's Friedmann and acceleration equations: G_cos = G",
      f"H^2 = {H2c}; a''/a = {acc_q}", okA1 and acc_ok)
H2x = H2_from(L_ctrl)
okA2 = H2x is not None and sp.simplify(H2x * (1 + sp.Rational(3, 2) * c2s) - gr) == 0
check("A2 CONTROL: the plain -c_2 K^2 term (no leaf average) renormalises the Friedmann equation, H^2 (1 + 3 c_2/2) = "
      "8 pi G rho/3 + Lambda/3 (L350's G_cos/G = 1/(1 + 3 c_2/2) at alpha_c = 0)", f"H^2 = {H2x}", okA2)
sS = sp.symbols("s", positive=True)
nu_rar_s = 1 / (1 - sp.exp(-sp.sqrt(sS)))                     # nu_mono = nu_RAR below the phantom peak (L340)
lim_phantom = sp.limit((nu_rar_s - 1) * sS, sS, 0)           # (nu - 1) s -> 0: the phantom flux vanishes with the field
alpha_sym = sp.symbols("alpha", positive=True)
bg_has_a0 = any(alpha_sym in e.free_symbols for e in (H2c, acc_q))
check("A3 a0 is absent from the background: the MOND term 2 alpha^2 q(0) = 0 and its first variation ~ (nu - 1) s -> 0 "
      "on FRW, so Friedmann is a0-blind; in the action a0 is a constant coupling: a0(z)/a0(0) = 1 on both footings",
      f"lim (nu-1)s = {lim_phantom}; a0 in the background equations: {bg_has_a0}; a0 = {A0['canonical']:.4e} / "
      f"{A0['alt']:.4e} m/s^2, a0(z)/a0(0) = 1 (canonical and alt)", lim_phantom == 0 and not bg_has_a0)
OUT["numbers"]["A"] = {"H2_core": str(H2c), "H2_plain_c2": str(H2x), "a0": A0}

# ============================================================================================= B  order counting
banner("B  WHY THE CORE FAILS LINEAR COSMOLOGY: the MOND energy is O(eps^(3/2)) around FRW")
w_ = sp.symbols("w", positive=True)                            # w = Z^(1/4) = sqrt(g_N/a0)
qprime_w = 1 / (1 - sp.exp(-w_)) - 1                           # q'(Z) = nu_RAR(sqrt Z) - 1
dq = sp.series(qprime_w * 4 * w_ ** 3, w_, 0, 7).removeO()     # dq/dw = q'(Z) dZ/dw
qser = sp.expand(sp.integrate(dq, (w_, 0, w_)))
low = min(m[0] for m in sp.Poly(qser, w_).monoms())
lead_exp = sp.Rational(low, 4)                                  # exponent of Z
lead_coef = sp.Poly(qser, w_).coeff_monomial(w_ ** low)
order_core = sp.Rational(low, 2)                               # Z = O(eps^2) => w = O(eps^(1/2))
Ysym, epsA = sp.symbols("Y epsilon", positive=True)
J_aqual = sp.integrate(sp.sqrt(Ysym), (Ysym, 0, Ysym))          # an AQUAL-type J with J' ~ Y^(1/2)
order_aqual = sp.Poly(sp.powsimp(J_aqual.subs(Ysym, epsA ** 2), force=True), epsA).monoms()[0][0]
tan_core = sp.limit(sp.diff(qser, w_) / (4 * w_ ** 3), w_, 0)  # q'(Z) at Z -> 0: the zero-field tangent
tan_aqual = sp.limit(sp.diff(J_aqual, Ysym), Ysym, 0)
check("B1 ORDER COUNTING: q(Z) = (4/3) Z^(3/4) + ... ; with Z = |grad S U|^2/alpha^2 = O(eps^2) around FRW the core's "
      "MOND energy is O(eps^(3/2)), BELOW the O(eps^2) quadratic action, and its zero-field tangent q'(0) is infinite "
      "(FP5's pinned U); an AQUAL-type J(Y) ~ Y^(3/2) is O(eps^3) with zero tangent and drops out of linear order",
      f"q = {qser} (w = Z^(1/4)); leading Z exponent {lead_exp} (coef {lead_coef}); eps order: core {order_core}, "
      f"AQUAL-type {order_aqual}; zero-field tangent: core {tan_core}, AQUAL-type {tan_aqual}",
      lead_exp == sp.Rational(3, 4) and lead_coef == sp.Rational(4, 3) and order_core == sp.Rational(3, 2)
      and order_aqual == 3 and tan_core == sp.oo and tan_aqual == 0)
OUT["numbers"]["B1"] = {"q_series": str(qser), "order_core": str(order_core), "order_aqual": str(order_aqual)}

# ---------------------------------------------------------------------------------------- L341's growth yardstick
h = 0.6736; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965
H0 = 100 * h * 1e3 / Mpc; rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * G)
Og = (4 * 5.670374419e-8 * T_CMB ** 4 / c ** 3) / rho_crit0; Or = Og * (1 + N_eff * (7 / 8) * (4 / 11) ** (4 / 3))
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om - Or; SIG8 = 0.811
RHOM0 = Om * rho_crit0
Ez = lambda a: math.sqrt(Or / a ** 4 + Om / a ** 3 + OL)
dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / Ez(a) ** 2
Hz = lambda z_: H0 * Ez(1 / (1 + z_))


def T_EH98(k):
    th = T_CMB / 2.7; s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b ** 0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om) ** 2
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s / h) ** 4)); qq = k * th * th / ge
    L = math.log(2 * math.e + 1.8 * qq); Cc = 14.2 + 731.0 / (1 + 62.5 * qq); return L / (L + Cc * qq * qq)


def P_un(kh): return (kh * h) ** ns * T_EH98(kh * h) ** 2
def Wth(x): return 3 * (math.sin(x) - x * math.cos(x)) / x ** 3


PN = (SIG8 / math.sqrt(quad(lambda kh: kh ** 2 * P_un(kh) * Wth(8 * kh) ** 2 / (2 * math.pi ** 2), 1e-4, 60, limit=600)[0])) ** 2
KH = np.logspace(math.log10(0.02), math.log10(20.0), 48)
DREF = np.array([math.sqrt(k ** 3 * PN * P_un(k) / (2 * math.pi ** 2)) for k in KH])
W8 = np.array([Wth(8 * k) ** 2 for k in KH])
def sigma8_of(D0): return math.sqrt(np.trapz(D0 ** 2 * W8, np.log(KH)))


# L340's monotone kernel nu_mono (identical construction to L340/L341)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
QM = 2.0 * (float(HM[0]) * YG[0] + np.concatenate([[0.0], np.cumsum(0.5 * (HM[1:] + HM[:-1]) * np.diff(YG))]))


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM) / y
def q_of_y(y):                                                 # q(Z = y^2) = 2 Int_0^y h(y') dy'
    y = np.maximum(np.asarray(y, float), 1e-14); return np.interp(np.log10(y), LYG, QM)
def nu_prime(y, e=1e-5): return (nu_mono(y * (1 + e)) - nu_mono(y * (1 - e))) / (2 * y * e)


def growth(fweb, a0v, mode="rms", c2=C2W, z_i=1000.0):
    """L341's integrator: delta'' + (2 + dlnH) delta' = 1.5 Omega_m(a) G_eff delta, G_eff = 1 + W_web (nu - 1) x tracking."""
    a_i = 1 / (1 + z_i)
    r0 = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om / math.exp(3 * N_) / Ez(math.exp(N_)) ** 2) * Y[0] - (2 + dlnH(math.exp(N_))) * Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]
    Di = DREF / r0

    def boost(y, a, kh):
        fw = fweb(a)
        if fw <= 0:
            return 1.0
        Cc = fw * (float(nu_mono(y)) - 1.0)
        if Cc <= 0:
            return 1.0
        cs = c * math.sqrt(c2 / (Cc * (2 + 3 * c2))); kphys = kh * h / (a * Mpc)
        return 1.0 + Cc / (1.0 + (H0 * Ez(a) / (cs * kphys)) ** 2)
    if mode == "rms":
        def rhs(N_, Y):
            a = math.exp(N_); D, Dp = Y; rho = RHOM0 / a ** 3
            gk = 4 * math.pi * G * rho * np.abs(Di * D) / (KH * h / (a * Mpc))
            grms = math.sqrt(np.trapz(gk ** 2 / KH, KH) / np.trapz(1 / KH, KH))
            return [Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost(grms / a0v, a, 1.0) * D - (2 + dlnH(a)) * Dp]
        return Di * solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12).y[0][-1]
    out = []
    for i, kh in enumerate(KH):
        def rhs(N_, Y, kh=kh):
            a = math.exp(N_); d, dp = Y; gN = 4 * math.pi * G * RHOM0 / a ** 3 * abs(d) / (kh * h / (a * Mpc))
            return [dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost(gN / a0v, a, kh) * d - (2 + dlnH(a)) * dp]
        out.append(solve_ivp(rhs, (math.log(a_i), 0.0), [Di[i], Di[i]], method="LSODA", rtol=1e-7, atol=1e-22).y[0][-1])
    return np.array(out)


S8_LCDM = sigma8_of(growth(lambda a: 0.0, A0["canonical"]))
def s8ratio(fweb, foot, mode, **kw): return sigma8_of(growth(fweb, A0[foot], mode, **kw)) / S8_LCDM


banner("B2-B3  THE YARDSTICK (L341's, re-implemented) AND THE UNGATED CORE")
L341J = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L341_chk_frw_gate_results.json")))
ref_ung = L341J["numbers"]["F2"]["('canonical', 0.0073, 'rms')"][0]
ref_lcdm = L341J["numbers"]["F4"]["rms"]
rep_ung = sigma8_of(growth(lambda a: 1.0, A0_L341["canonical"], "rms"))
yy_ = np.logspace(-6, 0, 400)
mono_rar = float(np.max(np.abs(nu_mono(yy_) / (1.0 / (-np.expm1(-np.sqrt(yy_)))) - 1)))
check("B2 CONTROL: the re-implemented yardstick reproduces L341's committed sigma_8 -- LCDM and the ungated core "
      "(canonical, c_2 = 0.0073, rms) -- to 1e-3; nu_mono = nu_RAR below the phantom peak (the kernel B1 expanded)",
      f"LCDM {S8_LCDM:.5f} vs {ref_lcdm:.5f}; ungated {rep_ung:.4f} vs {ref_ung:.4f}; |nu_mono/nu_RAR - 1| <= {mono_rar:.1e}",
      abs(S8_LCDM / ref_lcdm - 1) < 1e-3 and abs(rep_ung / ref_ung - 1) < 1e-3 and mono_rar < 1e-4)
ung = {(f, m): sigma8_of(growth(lambda a: 1.0, A0[f], m)) for f in FOOTS for m in MODES}
check("B3 THE UNGATED CORE FAILS G-1: at FP0's footings its MOND kernel on the linear web gives sigma_8 > 10 "
      "(both footings, rms and per-mode) -- the record's L341 failure, on this lane's inputs",
      ", ".join(f"{k_[0]}/{k_[1]} {v_:.2f}" for k_, v_ in ung.items()), min(ung.values()) > 10)
OUT["numbers"]["B"] = {"sigma8_LCDM": S8_LCDM, "ungated": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in ung.items()}}

# ============================================================================================= C0 FP5's criterion
banner("C0  FP5'S WELL-POSEDNESS CRITERION, APPLIED TO A GATE (FP5's committed E(C), read and checked)")
FP5J = json.load(open(os.path.join(HERE, "FP5_dof_and_a0_field_results.json")))
Ce, alc, cCH, c2e, kk = sp.symbols("C_e alpha_c c_CH c_2 k", positive=True)
E_expr = sp.sympify(FP5J["numbers"]["B3"]["E"], locals={"C_e": Ce, "alpha_c": alc, "c_CH": cCH})
w2_expr = sp.sympify(FP5J["numbers"]["B3"]["omega2"], locals={"C_e": Ce, "alpha_c": alc, "c_CH": cCH, "c_2": c2e, "k": kk})
w2_expr = w2_expr[0] if isinstance(w2_expr, (list, tuple)) else w2_expr
E2 = sp.simplify(E_expr.subs(cCH, 2))                          # C-H's structural c_CH = 2
E0, Einf = sp.limit(E2, Ce, 0), sp.limit(E2, Ce, sp.oo)
dEdC = sp.simplify(sp.diff(E2, Ce))
C_edge = sp.solve(sp.Eq(E2, 2), Ce)
w2_sign = sp.simplify(w2_expr.subs(cCH, 2) - c2e * (2 - E2) * kk ** 2 / (E2 * (2 + 3 * c2e)))
check("C0 FP5's committed reduced khronon E(C) (c_CH = 2) is E = alpha_c + 2C/(1+C): E(0) = alpha_c, E(inf) = alpha_c + 2, "
      "dE/dC > 0, and w^2 = c_2 (2 - E) k^2/(E (2 + 3 c_2)); with a gate the zero-field tangent is C_eff = W C_T, so the "
      "linearisation on FRW is well-posed iff C_eff < (2 - alpha_c)/alpha_c, and the MOND tangent vanishes IDENTICALLY "
      "on FRW iff W(FRW) = 0 with W = o(sqrt y) (C_T ~ y^(-1/2))",
      f"E = {E2}; E(0) = {E0}; E(inf) = {Einf}; dE/dC = {dEdC}; E = 2 at C = {C_edge}; w^2 form check {w2_sign}",
      sp.simplify(E2 - (alc + 2 * Ce / (1 + Ce))) == 0 and E0 == alc and sp.simplify(Einf - (alc + 2)) == 0
      and sp.simplify(dEdC - 2 / (1 + Ce) ** 2) == 0 and w2_sign == 0
      and len(C_edge) == 1 and sp.simplify(C_edge[0] - (2 - alc) / alc) == 0)
OUT["numbers"]["C0"] = {"E": str(E2), "C_edge": str(C_edge)}


def fp5_band(W_frw, ac):
    """the zero-field band y < y* where E > 2 for a gate that is W_frw on FRW: W_frw C_T(y*) = (2 - ac)/ac, with the
    transverse C_T = nu - 1 of nu_mono = nu_RAR there (closed form: y* = log1p(1/target)^2)."""
    if W_frw <= 0:
        return 0.0
    target = (2 - ac) / (ac * W_frw)
    return math.log1p(1.0 / target) ** 2


# ============================================================================================= C1 stability rule
banner("C1  THE STABILITY RULE: a gate on the dynamical density is stable iff it is concave (sympy symbol)")
k2 = sp.symbols("k2", positive=True)                          # k^2
B_, Wpp, Wb, CT, Cn = sp.symbols("B W2 Wbar C_T C", real=True)
psi_, phi_, U_, drho, Gc = sp.symbols("psi phi U delta_rho G", real=True)
# static C-H bracket, plane waves (grad^2 -> -k^2), frozen coefficients, k transverse to the background field:
#   2|grad psi|^2 - 4 grad phi.grad psi + 2|grad(U - phi)|^2 + 2 alpha^2 [W q]_2 - 16 pi G rho phi
#   [W q]_2 = (1/2) W'' qbar (delta x)^2 + Wbar q' |grad dU|^2/alpha^2,  delta x = C lap(delta phi) = -C k^2 phi,
#   with B = 2 alpha^2 qbar (the MOND energy) and C_T = nu - 1 = q' (the transverse constitutive coefficient)
L2 = (2 * k2 * psi_ ** 2 - 4 * k2 * phi_ * psi_ + 2 * k2 * (U_ - phi_) ** 2
      + (B_ / 2) * Wpp * (Cn * k2 * phi_) ** 2 + 2 * Wb * CT * k2 * U_ ** 2 - 16 * sp.pi * Gc * drho * phi_)
X = [psi_, phi_, U_]
M = sp.Matrix(3, 3, lambda i, j: sp.diff(L2, X[i], X[j]))
detM = sp.factor(M.det())
roots = [r_ for r_ in sp.solve(sp.Eq(detM, 0), k2)]
J = sp.Matrix([-sp.diff(L2, x_).subs({psi_: 0, phi_: 0, U_: 0}) for x_ in X])
solX = M.LUsolve(J)
dphi = sp.simplify(solX[1]); dpsi = sp.simplify(solX[0])
noslip = sp.simplify(dphi - dpsi) == 0
eps_ = sp.symbols("e", positive=True)                          # e = B W'' C^2 (its sign is the question)
dphi_ser = sp.series(sp.simplify(dphi.subs(Wpp, eps_ / (B_ * Cn ** 2))), eps_, 0, 2).removeO()
newton = sp.simplify(dphi_ser.subs(eps_, 0))
local = sp.simplify(dphi_ser - newton)
local_k = sp.simplify(sp.diff(local, k2))
q_nonneg = bool(np.min(HM) >= -1e-15 and np.all(np.diff(QM) >= -1e-18))
# the leaf-average lemma: a factor built from <K>_h (or any leaf average) has no local second variation, because a
# k != 0 mode of K leaves <K>_h unchanged on a periodic leaf
xl, Lx, kn, eK = sp.symbols("x L_x n epsilon", positive=True)
avg_var = sp.simplify(sp.integrate(eK * sp.cos(2 * sp.pi * sp.Symbol("m", integer=True, positive=True) * xl / Lx), (xl, 0, Lx)) / Lx)
Fg = sp.Function("F")
Kb = sp.symbols("Kbar", positive=True)
second_local = sp.simplify(sp.diff(Fg(Kb + avg_var), eK, 2))
sign_rule = (len(roots) == 1 and sp.simplify(roots[0] - 4 / (B_ * Wpp * Cn ** 2 * (1 + Wb * CT))) == 0)
check("C1 THE STABILITY RULE: B = 2 alpha^2 q >= 0 (q' = nu_mono - 1 >= 0, q(0) = 0); for a gate reading the lapse "
      "Laplacian the static symbol det = 16 k^6 [B W'' C^2 k^2 (1 + W C_T) - 4] has a zero at k^2 = 4/(B W'' C^2 (1+W C_T)) "
      "iff B W'' > 0; the gate's local term on matter is delta phi_loc = -pi G B W'' C^2 (1 + W C_T)^2 delta rho (an "
      "anti-pressure iff W'' > 0; CV3 G3/G4 in this reading); psi = phi (no slip).  STABLE <=> W CONCAVE",
      f"q >= 0 on the grid: {q_nonneg}; det = {detM}; zero at k^2 = {roots}; Newtonian part {newton}; local part "
      f"{local} (k-independent: {local_k == 0}); psi = phi: {noslip}; leaf-average lemma: delta<K> of a k != 0 mode = "
      f"{avg_var}, so a factor F(<K>_h) adds {second_local} to the local second variation",
      q_nonneg and sign_rule and noslip and local_k == 0 and avg_var == 0 and second_local == 0
      and sp.simplify(local + sp.pi * Gc * eps_ * (1 + Wb * CT) ** 2 * drho) == 0)
OUT["numbers"]["C1"] = {"det": str(detM), "zero_k2": str(roots), "local_term": str(local), "newtonian": str(newton)}


def c_gate2(q, rho, W_rhorho):
    """the gate's local 'sound speed' squared, from delta phi_loc: c_g^2 = -(a0^2 q/8 pi G) rho W_rho,rho (SI units,
    a0 canonical); negative = an anti-pressure (unstable), positive = a pressure."""
    return -(A0["canonical"] ** 2 * q / (8 * math.pi * G)) * rho * W_rhorho


# ============================================================================================= C2 sigma_8 tolerance
banner("C2  THE SIGMA_8 TOLERANCE: how much MOND the linear web may carry")
def fmax_for(foot, mode, z_on=None, target=1.02):
    fw = (lambda f_: (lambda a: f_)) if z_on is None else (lambda f_: (lambda a: f_ if (1 / a - 1) <= z_on else 0.0))
    return brentq(lambda f_: s8ratio(fw(f_), foot, mode) - target, 1e-6, 0.5, xtol=1e-7, rtol=1e-6)


FMAX = {(f, m): fmax_for(f, m) for f in FOOTS for m in MODES}
FMAX_LOW = {(f, m): fmax_for(f, m, z_on=0.5) for f in FOOTS for m in MODES}
for k_ in FMAX:
    P(f"    {k_[0]:9s} {k_[1]:7s}: uniform f_max = {FMAX[k_]:.3e};  active only at z <= 0.5: {FMAX_LOW[k_]:.3e}")
fmax_all = min(FMAX.values()); fmax_low = max(FMAX_LOW.values())
check("C2 sigma_8 <= 1.02 x LCDM allows a uniform web on-fraction of at most f_max ~ 2e-3 (both footings, rms and "
      "per-mode); a gate active only at z <= 0.5 may carry more (the low-z budget C3 uses)",
      "; ".join(f"{k_[0]}/{k_[1]} {FMAX[k_]:.2e} (z<=0.5: {FMAX_LOW[k_]:.2e})" for k_ in FMAX),
      1e-3 < fmax_all < 3e-3 and all(FMAX_LOW[k_] > FMAX[k_] for k_ in FMAX))
OUT["numbers"]["C2"] = {"fmax": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in FMAX.items()},
                        "fmax_z_le_0.5": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in FMAX_LOW.items()}}

# ============================================================================================= C3 chord bound
banner("C3  THE CHORD BOUND: a concave gate's on/off ratio is capped by the density ratio")
rng = np.random.default_rng(3)
uu = np.logspace(-3, 4, 700)
viol = 0
for _ in range(4000):                                          # random concave, nonnegative, increasing gates with w(0) = 0
    nb = rng.integers(1, 5); bs = 10 ** rng.uniform(-2, 3, nb); cs_ = rng.dirichlet(np.ones(nb))
    ex = rng.uniform(0, 1); be = 10 ** rng.uniform(-2, 3)
    wv = (1 - ex) * (cs_[None, :] * np.minimum(1.0, uu[:, None] / bs[None, :])).sum(1) + ex * (1 - np.exp(-uu / be))
    ratio = wv / uu                                            # the chord from the origin: w(u)/u must be non-increasing
    viol += int(np.any(np.diff(ratio) > 1e-12 * ratio[:-1]))
thr = lambda u: np.clip((u - 0.75) / 0.5, 0, 1) ** 2 * (3 - 2 * np.clip((u - 0.75) / 0.5, 0, 1))
thr_viol = bool(np.any(np.diff(thr(uu) / uu) > 1e-12))
P(f"    4000 random concave gates: {viol} violations of w(u)/u non-increasing; a smooth threshold gate violates: {thr_viol}")


def rho_dyn_point(r, Mb, a0v):
    """dynamical (phantom) density of a point mass with nu_mono at radius r [m]: -(M/2 pi r^3) y nu'(y)."""
    y = G * Mb / (r ** 2 * a0v)
    return float(-(Mb / (2 * math.pi * r ** 3)) * y * nu_prime(y))


def r_at_density(rho_t, Mb, a0v):
    return math.exp(brentq(lambda lr: math.log(max(rho_dyn_point(math.exp(lr), Mb, a0v), 1e-300) / rho_t),
                           math.log(1e-3 * kpc), math.log(1e3 * Mpc)))


RT, RT_LOW = {}, {}
fmax_uni = max(FMAX.values())
for f in FOOTS:
    for Mb in (1e10, 1e11, 1e12):
        # z = 0.25: W <= 1/2 wherever rho_dyn < rho_bar/(2 f); f = the uniform budget, or the budget spent only at z <= 0.5
        RT[(f, Mb)] = r_at_density(RHOM0 * 1.25 ** 3 / (2 * fmax_uni), Mb * MSUN, A0[f]) / Mpc
        RT_LOW[(f, Mb)] = r_at_density(RHOM0 * 1.25 ** 3 / (2 * fmax_low), Mb * MSUN, A0[f]) / Mpc
        P(f"    {f:9s} M_b = {Mb:.0e}: a stable gate is at most half on beyond r = {RT[(f, Mb)]:.3f} Mpc (epoch-independent "
          f"budget) / {RT_LOW[(f, Mb)]:.3f} Mpc (budget spent at z <= 0.5), z = 0.25")
F7 = L341J["numbers"]["F7"]
check("C3 THE CHORD BOUND: a concave W >= 0 with W(0) >= 0 has W(rho)/rho non-increasing, so W(rho) <= (rho/rho_bar) "
      "W(rho_bar) <= (rho/rho_bar) f -- a stable local gate is at most half on where rho_dyn < rho_bar/(2 f).  With an "
      "epoch-independent amplitude (f = f_max) that is beyond ~0.2-0.5 Mpc of an isolated M_b = 1e10-1e12 galaxy at z = 0.25; "
      "only an amplitude that spends the sigma_8 budget at z <= 0.5 (f ~ 3e-2) reaches ~0.5-1.5 Mpc (both footings)",
      f"random concave: {viol}/4000 violations; threshold gate violates: {thr_viol}; half-on radius (Mpc), uniform / low-z: "
      + ", ".join(f"{k_[0][:3]}/{k_[1]:.0e} {RT[k_]:.2f}/{RT_LOW[k_]:.2f}" for k_ in RT),
      viol == 0 and thr_viol and max(RT.values()) < 0.6 and min(RT_LOW.values()) > max(RT.values()))
check("C3b (reported: KiDS at lead grade) L341 F7's committed hard-truncation scores: a phantom cut inside 0.5 Mpc costs "
      "chi^2 >= 223 (0.3 Mpc: 374) against 107-118 uncut or cut at 1 Mpc.  An epoch-independent stable gate is cut there; "
      "reaching the KiDS scale needs the sigma_8 budget spent at z <= 0.5, which C4's KiDS-plus-flagship design tests",
      f"F7 chi^2: none {F7['None']:.1f}, 1 Mpc {F7['1.0']:.1f}, 0.5 Mpc {F7['0.5']:.1f}, 0.3 Mpc {F7['0.3']:.1f}; "
      f"stable-gate half-on radii: uniform <= {max(RT.values()):.2f} Mpc, low-z >= {min(RT_LOW.values()):.2f} Mpc",
      F7["0.5"] - F7["None"] > 50, load_bearing=False)
OUT["numbers"]["C3"] = {"violations": viol, "threshold_violates": thr_viol,
                        "half_on_radius_Mpc_z0.25_uniform": {f"{k_[0]}/{k_[1]:.0e}": v_ for k_, v_ in RT.items()},
                        "half_on_radius_Mpc_z0.25_lowz": {f"{k_[0]}/{k_[1]:.0e}": v_ for k_, v_ in RT_LOW.items()}}

# ============================================================================================= C4 the concave construction
banner("C4  THE CONCAVE CONSTRUCTION at the chord bound: W = w(rho_dyn/rho_*(<K>_h)), w concave")
def w_soft(u):
    u = np.asarray(u, float); return np.where(u > 0, u / (1 + np.abs(u) ** 4) ** 0.25, u)
def w_soft_d(u):                                               # analytic w', w''
    u = np.asarray(u, float); up = np.maximum(u, 0.0)
    return np.where(u > 0, (1 + up ** 4) ** -1.25, 1.0), np.where(u > 0, -5 * up ** 3 * (1 + up ** 4) ** -2.25, 0.0)
def smooth_step(u, lo=0.75, hi=1.25):                          # C^infinity, flat at both ends (CV3's transition)
    g = lambda s_: np.where(s_ > 0, np.exp(-1.0 / np.maximum(s_, 1e-300)), 0.0)
    s_ = (np.asarray(u, float) - lo) / (hi - lo); return g(s_) / (g(s_) + g(1 - s_))
def smooth_step_d(u, lo=0.75, hi=1.25, e=1e-4):                # derivatives in the transition only (exactly 0 outside)
    u = np.asarray(u, float); inside = (u > lo) & (u < hi); ds = e * (hi - lo)
    d1 = (smooth_step(u + ds) - smooth_step(u - ds)) / (2 * ds)
    d2 = (smooth_step(u + ds) - 2 * smooth_step(u) + smooth_step(u - ds)) / ds ** 2
    return np.where(inside, d1, 0.0), np.where(inside, d2, 0.0)


w_gate = smooth_step if MUTATE else w_soft
w_gate_d = smooth_step_d if MUTATE else w_soft_d
GATE_NAME = "threshold (flat-flat) C^inf step at u = 0.75..1.25" if MUTATE else "concave softmin u/(1+u^4)^(1/4)"
P(f"    gate: {GATE_NAME}")


def gated_profile(Mb, a0v, rho_star, zz, r_max, n=400, gate=None):
    """self-consistent pointwise gate: rho = rho_bar(z) + w(rho/rho_*) p(r), p = the full phantom density; returns the
    radii, W(r), the gated and the full phantom mass inside r, and the largest number of self-consistent roots."""
    gate = gate or w_gate
    rbar = RHOM0 * (1 + zz) ** 3
    rr = np.logspace(math.log10(r_max) - 5, math.log10(r_max), n)
    pp = np.maximum(np.array([rho_dyn_point(r, Mb, a0v) for r in rr]), 0.0)
    fr = np.concatenate([[0.0], np.logspace(-9, 0, 600)])
    Wr = np.empty(n); nmax = 0
    for i, p in enumerate(pp):
        grid = rbar + fr * (p + rbar)
        vals = grid - rbar - gate(grid / rho_star) * p
        sc = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
        nmax = max(nmax, len(sc) + int(vals[0] == 0.0))
        if len(sc):
            j = sc[-1]                                           # the collapsed (history-selected) branch if several
            rho = brentq(lambda x_: x_ - rbar - float(gate(x_ / rho_star)) * p, grid[j], grid[j + 1])
        else:
            rho = rbar
        Wr[i] = float(gate(rho / rho_star))
    dM = 4 * math.pi * rr ** 2 * pp
    Mph_full = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(rr))])
    Mph_g = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] * Wr[1:] + dM[:-1] * Wr[:-1]) * np.diff(rr))])
    return rr, Wr, Mph_g, Mph_full, nmax


def on_fraction(Mb, a0v, rho_star, zz, y_at, gate=None):
    """g_gated / g_full at the radius where g_bar = y_at a0 (spherical point mass)."""
    rF = math.sqrt(G * Mb / (y_at * a0v))
    rr, Wr, Mg, Mf, nr = gated_profile(Mb, a0v, rho_star, zz, rF, gate=gate)
    return (Mb + Mg[-1]) / (Mb * float(nu_mono(y_at))), nr


Y_DES, TARGET, P_RISE, W_RISE = 0.1, 0.95, 3.0, 0.05          # design: >= 95% at the flagship radius; the clock rise
DESIGNS = {"D1 (M_b <= 1e11)": (1e11 * MSUN, 0.1), "D2 (M_b <= 1e12)": (1e12 * MSUN, 0.1),
           "D3 (RAR tail, 1e10 at 0.01 a0)": (1e10 * MSUN, 0.01), "D4 (RAR tail, 1e11 at 0.01 a0)": (1e11 * MSUN, 0.01)}
RSTAR0 = {}
for dn, (Md, yd) in DESIGNS.items():
    for f in FOOTS:
        RSTAR0[(dn, f)] = math.exp(brentq(lambda lrs: on_fraction(Md, A0[f], math.exp(lrs), 0.0, yd)[0] - TARGET,
                                          math.log(1e-2 * RHOM0), math.log(1e7 * RHOM0), xtol=1e-6))
        P(f"    {dn} {f:9s}: rho_*0 = {RSTAR0[(dn, f)] / RHOM0:.1f} rho_m0 (the design galaxy at g/g_MOND = {TARGET} at {yd} a0, z = 0)")


def rho_star_of(zz, dn, f, z_on, low=None):
    """rho_*(<K>_h): a function of the LEAF-AVERAGED clock expansion (<K>_h = 3H(z) on every leaf), flat (= rho_*0) until
    z_on, then rising as (1+z)^(3p) (a smooth max in ln(1+z), width W_RISE); an optional low-z value (z <= 0.5) for the
    KiDS-plus-flagship design.  rho_dyn's mean part rho_bar(<K>_h) is likewise a leaf average (C1's lemma)."""
    r = (math.log1p(zz) - math.log1p(z_on)) / W_RISE
    rise = math.exp(3 * P_RISE * W_RISE * (r + math.log1p(math.exp(-r))) if r > 30 else 3 * P_RISE * W_RISE * math.log1p(math.exp(r)))
    base = RSTAR0[(dn, f)] * rise
    if low is not None:
        blend = 0.5 * (1 - math.tanh((zz - 0.5) / 0.05))
        base = math.exp(blend * math.log(low) + (1 - blend) * math.log(base))
    return base


def web_gate(dn, f, z_on, gate=None, low=None):
    gate = gate or w_gate
    return lambda a: float(gate(RHOM0 / a ** 3 / rho_star_of(1 / a - 1, dn, f, z_on, low)))


def zon_max(dn, f, m, low=None):
    g = lambda zo: s8ratio(web_gate(dn, f, zo, low=low), f, m) - 1.02
    if g(12.0) < 0:
        return 12.0
    if g(0.0) > 0:
        return -1.0
    return brentq(g, 0.0, 12.0, xtol=1e-3)


ZON = {(dn, f, m): zon_max(dn, f, m) for dn in DESIGNS for f in FOOTS for m in MODES}
for k_, v_ in ZON.items():
    P(f"    {k_[0]} {k_[1]:9s} {k_[2]:7s}: sigma_8 <= 1.02 keeps the design galaxies on up to z_on = {v_:.2f}")
Z_ONS = {dn: math.floor(min(v_ for k_, v_ in ZON.items() if k_[0] == dn) * 20) / 20.0 for dn in DESIGNS}
HEAD = "D1 (M_b <= 1e11)"
Z_ON = Z_ONS[HEAD]
S8C = {(dn, f, m): s8ratio(web_gate(dn, f, Z_ONS[dn]), f, m) for dn in DESIGNS for f in FOOTS for m in MODES}
for dn in DESIGNS:
    P(f"    {dn}: design z_on = {Z_ONS[dn]:.2f}; sigma_8 ratio "
      + ", ".join(f"{k_[1]}/{k_[2]} {v_:.4f}" for k_, v_ in S8C.items() if k_[0] == dn))
WEB = {(dn, f): {z_: float(w_gate(RHOM0 * (1 + z_) ** 3 / rho_star_of(z_, dn, f, Z_ONS[dn]))) for z_ in (0.0, 1.0, 2.5, 5.0, 10.0)}
       for dn in DESIGNS for f in FOOTS}
for k_, v_ in WEB.items():
    P(f"    {k_[0]} {k_[1]:9s}: web on-fraction W(rho_bar) at z = 0/1/2.5/5/10: " + ", ".join(f"{x_:.1e}" for x_ in v_.values()))
check("C4a sigma_8 WITHIN 2%: the concave gate, designed at the chord bound, keeps sigma_8 <= 1.02 x LCDM on both "
      "footings (rms and per-mode) with the design galaxies on up to z_on >= 2.5 (headline design D1; D2-D4 reported)",
      f"z_on: " + ", ".join(f"{dn} {z_:.2f}" for dn, z_ in Z_ONS.items()) + "; "
      + ", ".join(f"{k_[0][:2]}/{k_[1][:3]}/{k_[2]} {v_:.4f}" for k_, v_ in S8C.items()),
      max(v_ for k_, v_ in S8C.items() if k_[0] == HEAD) <= 1.02 and Z_ON >= 2.5)

GAL = {}
for dn in DESIGNS:
    if dn.startswith("D2") or dn.startswith("D4") or dn.startswith("D3"):
        continue
    for f in FOOTS:
        for Mb in (1e10, 1e11, 1e12):
            for zz, ytag in ((2.5, 0.1), (0.0, 0.1), (0.0, 0.03), (0.0, 0.01)):
                ratio, nr = on_fraction(Mb * MSUN, A0[f], rho_star_of(zz, dn, f, Z_ONS[dn]), zz, ytag)
                GAL[(dn, f, Mb, zz, ytag)] = (ratio, 2 * math.log10(ratio), nr,
                                             math.sqrt(G * Mb * MSUN / (ytag * A0[f])) / kpc)
for k_, v_ in GAL.items():
    P(f"    {k_[0][:2]} {k_[1]:9s} M_b = {k_[2]:.0e} z = {k_[3]:.1f} g_bar = {k_[4]:.2f} a0 (r = {v_[3]:.0f} kpc): "
      f"g/g_MOND = {v_[0]:.4f} ({v_[1]:+.3f} dex)")
DEX_OK = 0.05
flag_ok = all(abs(GAL[(HEAD, f, Mb, zz, 0.1)][1]) <= DEX_OK for f in FOOTS for Mb in (1e10, 1e11) for zz in (0.0, 2.5))
check(f"C4b GALAXY INTERIORS ON (D1): at the flagship radius (g_bar = 0.1 a0) the deep-MOND BTFR zero point moves by <= "
      f"{DEX_OK} dex (flagship precision 0.13) for M_b = 1e10-1e11 at z = 2.5 and z = 0, both footings; the 1e12 rows, "
      f"D2 and the RAR tail are reported",
      "D1 flagship: " + ", ".join(f"{k_[1][:3]}/{k_[2]:.0e}/z{k_[3]:g} {v_[1]:+.3f}" for k_, v_ in GAL.items()
                                    if k_[0] == HEAD and k_[4] == 0.1)
      + " | D1 RAR tail z = 0 (0.03/0.01 a0): " + ", ".join(
          f"{f[:3]}/{Mb:.0e} {GAL[(HEAD, f, Mb, 0.0, 0.03)][1]:+.2f}/{GAL[(HEAD, f, Mb, 0.0, 0.01)][1]:+.2f}"
          for f in FOOTS for Mb in (1e10, 1e11)),
      flag_ok)
# the other designs: what the same sigma_8 budget buys when it is spent on the RAR tail or on 1e12 galaxies
DES_TAB = {}
for dn in DESIGNS:
    for f in FOOTS:
        row = {"z_on": Z_ONS[dn]}
        for Mb, zz, yv in ((1e10, 0.0, 0.01), (1e11, 0.0, 0.01), (1e11, 0.0, 0.03), (1e11, 2.5, 0.1), (1e12, 2.5, 0.1), (1e12, 0.0, 0.1)):
            row[f"{Mb:.0e}/z{zz:g}/y{yv}"] = 2 * math.log10(on_fraction(Mb * MSUN, A0[f], rho_star_of(zz, dn, f, Z_ONS[dn]), zz, yv)[0])
        for dl in (1.0, 10.0):                                     # the z = 2.5 IGM: gate x MOND tangent (a 1 Mpc lump)
            Wi = float(w_gate(RHOM0 * 3.5 ** 3 * (1 + dl) / rho_star_of(2.5, dn, f, Z_ONS[dn])))
            yi = 4 * math.pi * G * RHOM0 * 3.5 ** 3 * dl * (Mpc / 3.5) / 3 / A0[f]
            row[f"IGM boost z2.5 delta{dl:g}"] = Wi * (float(nu_mono(yi)) - 1)
        DES_TAB[(dn, f)] = row
for k_, v_ in DES_TAB.items():
    P(f"    {k_[0][:31]:31s} {k_[1][:3]}: z_on {v_['z_on']:.2f}; dex " + ", ".join(f"{kk_} {vv_:+.2f}" for kk_, vv_ in v_.items() if kk_ != "z_on"))
tail_ok = [dn for dn in DESIGNS if all(abs(DES_TAB[(dn, f)]["1e+10/z0/y0.01"]) <= DEX_OK and abs(DES_TAB[(dn, f)]["1e+11/z2.5/y0.1"]) <= DEX_OK
                                       for f in FOOTS)]
lstar_ok = [dn for dn in DESIGNS if all(abs(DES_TAB[(dn, f)]["1e+11/z0/y0.03"]) <= DEX_OK and abs(DES_TAB[(dn, f)]["1e+11/z2.5/y0.1"]) <= DEX_OK
                                        and abs(DES_TAB[(dn, f)]["1e+12/z2.5/y0.1"]) <= DEX_OK for f in FOOTS)]
check("C4b' (reported) THE TRADE: one 2% sigma_8 budget, spent four ways (D1-D4).  Designs keeping the dwarf RAR tail "
      "(1e10 at 0.01 a0, z = 0) AND the 1e11 flagship (z = 2.5) within 0.05 dex, and designs keeping the L* outskirts "
      "(1e11 at 0.03 a0) with the 1e11 and 1e12 flagships, are listed; the z = 2.5 IGM force boost of each design is printed",
      f"dwarf tail + 1e11 flagship: {tail_ok or 'none'}; L* outskirts + 1e11/1e12 flagships: {lstar_ok or 'none'}; IGM boost "
      "(delta = 1/10): " + ", ".join(f"{k_[0][:2]}/{k_[1][:3]} {v_['IGM boost z2.5 delta1']:.2f}/{v_['IGM boost z2.5 delta10']:.2f}"
                                     for k_, v_ in DES_TAB.items()), True, load_bearing=False)

# second variation: u^2 w'' <= 0 on the domain (analytic); K-block below c_2
ug = np.logspace(-6, 6, 60001)
w2 = w_gate_d(ug)[1]
w2_max = float(np.max(w2 * ug ** 2)); w2_min = float(np.min(w2 * ug ** 2))
alpha = {f: A0[f] / c ** 2 for f in FOOTS}
KB = {}
ZG = np.linspace(0.0, 15.0, 3001)
lnK = np.log(3 * np.array([Hz(z_) for z_ in ZG]) / c)
UG = np.logspace(-4, 6, 161)
wp_g, wpp_g = w_gate_d(UG)
for dn, (Md, yd) in DESIGNS.items():
    for f in FOOTS:
        rgrid = np.logspace(math.log10(1e-3 * kpc), math.log10(1e3 * Mpc), 3000)
        rho_g = np.array([rho_dyn_point(r, Md, A0[f]) for r in rgrid]); y_g = G * Md / (rgrid ** 2 * A0[f])
        ok_ = rho_g > 0
        lrho, ly = np.log(rho_g[ok_])[::-1], np.log(y_g[ok_])[::-1]      # rho_dyn decreases outward: reverse to ascend
        lrs = np.log(np.array([rho_star_of(z_, dn, f, Z_ONS[dn]) for z_ in ZG]))
        g1 = np.gradient(lrs, lnK); g2 = np.gradient(g1, lnK)             # d ln rho_*/d ln K and its derivative
        worst = 0.0
        for iz in range(0, len(ZG), 5):
            rho_u = UG * math.exp(lrs[iz])
            y_u = np.exp(np.interp(np.log(rho_u), lrho, ly))              # the y the design galaxy has at that density
            qv = q_of_y(y_u)
            K2WKK = wpp_g * UG ** 2 * g1[iz] ** 2 + wp_g * UG * (g1[iz] ** 2 + g1[iz] - g2[iz])
            worst = max(worst, float(np.max(alpha[f] ** 2 * qv * np.abs(K2WKK) / math.exp(lnK[iz]) ** 2 / C2W)))
        KB[(dn, f)] = worst
P(f"    u^2 w'' in [{w2_min:.3e}, {w2_max:.3e}]; CONTROL, the same rho_* read off the LOCAL K: max alpha^2 q |W_KK| / c_2 = "
  + ", ".join(f"{k_[0][:2]}/{k_[1][:3]} {v_:.2e}" for k_, v_ in KB.items()))
check("C4c NON-NEGATIVE SECOND VARIATION: u^2 w'' <= 0 everywhere (C1: no symbol zero, the gate adds only pressure), and "
      "the clock enters only through leaf averages (<K>_h in rho_* and rho_bar), which add nothing to the local second "
      "variation (C1's lemma).  CONTROL: read off the LOCAL K instead, the same rho_* would overwhelm the khronon's "
      "stiffness c_2 (its threshold climbs into dense cores where q is huge) -- the leaf average is required",
      f"u^2 w'' in [{w2_min:.2e}, {w2_max:.2e}]; leaf-average second variation {second_local}; local-K control ratio "
      + ", ".join(f"{k_[0][:2]}/{k_[1][:3]} {v_:.1e}" for k_, v_ in KB.items()),
      w2_max <= 0.0 and second_local == 0 and max(KB.values()) > 1.0)

multi = 0; cells = 0
for rm in np.logspace(-3, 3, 25):
    for pv in np.concatenate([np.logspace(-3, 4, 29), -np.logspace(-3, 1, 9)]):
        grid = np.concatenate([[0.0], np.logspace(-8, 5, 3000)])
        vals = grid - rm - w_gate(grid) * pv
        n_ = int(np.sum(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0))
        cells += 1; multi += int(n_ != 1)
P(f"    self-consistent rho = rho_m + w(rho/rho_*) p on {cells} cells (units rho_*): {multi} cells with != 1 solution")
check("C4d A UNIQUE SELF-CONSISTENT STATE: with the gate reading the density it helps create (matter + phantom), a "
      "concave w gives exactly one solution in every cell (no bistability, no history dependence)",
      f"{multi}/{cells} cells not unique", multi == 0)

PR = {}
for f in FOOTS:
    rr, Wr, Mg, Mf, _ = gated_profile(1e11 * MSUN, A0[f], rho_star_of(0.25, HEAD, f, Z_ON), 0.25, 3 * Mpc)
    PR[(f, "r_half_Mpc (1e11, z=0.25)")] = float(rr[np.argmin(np.abs(Wr - 0.5))] / Mpc)
    for zz in (2.5, 3.0):
        for dl in (1.0, 10.0):
            Wi = float(w_gate(RHOM0 * (1 + zz) ** 3 * (1 + dl) / rho_star_of(zz, HEAD, f, Z_ON)))
            yi = 4 * math.pi * G * RHOM0 * (1 + zz) ** 3 * dl * (1 * Mpc / (1 + zz)) / 3 / A0[f]   # field of a 1 Mpc/h-ish IGM lump
            PR[(f, f"W_IGM z={zz} delta={dl:g}")] = Wi
            PR[(f, f"IGM force boost W(nu-1) z={zz} delta={dl:g}")] = Wi * (float(nu_mono(yi)) - 1)
    for zz in (4.0, 6.0):
        PR[(f, f"flagship dex z={zz} 1e11")] = 2 * math.log10(on_fraction(1e11 * MSUN, A0[f], rho_star_of(zz, HEAD, f, Z_ON), zz, 0.1)[0])
    Md = DESIGNS[HEAD][0]; rs0 = rho_star_of(0.0, HEAD, f, Z_ON); vf2 = (G * Md * A0[f]) ** 0.5
    d1e, d2e = w_gate_d(np.array([1.0])); w1e, w2e = float(d1e[0]), float(d2e[0])
    PR[(f, "gate potential / v_f^2 at u = 1 (D1)")] = A0[f] ** 2 * float(q_of_y(0.1)) * w1e / (8 * math.pi * G * rs0) / vf2
    PR[(f, "gate pressure c_g [km/s] at u = 1 (D1)")] = math.sqrt(max(c_gate2(float(q_of_y(0.1)), rs0, w2e / rs0 ** 2), 0)) / 1e3
for k_, v_ in PR.items():
    P(f"    price {k_[0]:9s} {k_[1]}: {v_:.3g}")
# the KiDS-plus-flagship design: the same gate, with a low-z rho_* that puts the 1e11 half-on radius at 1 Mpc (z = 0.25)
KIDS = {}
for f in FOOTS:
    def half_at(lrs, f=f):
        rr, Wr, Mg, Mf, _ = gated_profile(1e11 * MSUN, A0[f], math.exp(lrs), 0.25, 3 * Mpc)
        return float(np.interp(1.0, rr / Mpc, Wr)) - 0.5
    low = math.exp(brentq(half_at, math.log(0.1 * RHOM0), math.log(1e5 * RHOM0), xtol=1e-4))
    KIDS[(f, "rho_low/rho_m0")] = low / RHOM0
    for m in MODES:
        KIDS[(f, m)] = s8ratio(web_gate(HEAD, f, Z_ON, low=low), f, m)
P("    KiDS-plus-flagship design (1e11 half on at 1 Mpc at z = 0.25, D1 above z = 0.5): "
  + ", ".join(f"{k_[0][:3]}/{k_[1]} {v_:.4g}" for k_, v_ in KIDS.items()))
check("C4e (reported) THE PRICES of the concave gate (D1): the 1e11 phantom is half on only to r_half at z = 0.25; the "
      "z = 2.5-3 IGM carries W ~ 1e-3-1e-2 (a forest cost to price); galaxy MOND fades above z_on; the gate's own "
      "potential and (positive) pressure at its edge; and serving KiDS (1 Mpc at z = 0.25) as well costs sigma_8",
      "; ".join(f"{k_[0][:3]} {k_[1]} {v_:.3g}" for k_, v_ in PR.items()) + " | KiDS+flagship sigma_8: "
      + ", ".join(f"{k_[0][:3]}/{k_[1]} {v_:.4f}" for k_, v_ in KIDS.items() if k_[1] in MODES), True, load_bearing=False)

W_FRW = {f: WEB[(HEAD, f)][0.0] for f in FOOTS}
BAND = {(f, ac): fp5_band(W_FRW[f], ac) for f in FOOTS for ac in ALPHA_C}
BAND_UNG = {ac: fp5_band(1.0, ac) for ac in ALPHA_C}
P("    FP5 band (E > 2 below y*): ungated " + ", ".join(f"alpha_c={ac:.1e}: y* = {v_:.2e}" for ac, v_ in BAND_UNG.items())
  + " | concave gate " + ", ".join(f"{k_[0][:3]}/{k_[1]:.1e}: y* = {v_:.2e}" for k_, v_ in BAND.items()))
check("C4f FP5 (the strict form): the concave gate is NOT zero on FRW (W(FRW) = w(rho_bar/rho_*) > 0), so its zero-field "
      "tangent C_eff = W C_T is still infinite: the ill-posed band y < y* survives, shrunk from the ungated core's by "
      "~ W(FRW)^2 -- amplitude-harmless (FP5 C4) but the MOND tangent does not vanish identically on FRW",
      f"W(FRW, z = 0) = {', '.join(f'{f} {v_:.2e}' for f, v_ in W_FRW.items())}; y* (gate) max "
      f"{max(BAND.values()):.1e} vs ungated {max(BAND_UNG.values()):.1e}",
      min(W_FRW.values()) > 0 and all(0 < BAND[(f, ac)] < BAND_UNG[ac] for f in FOOTS for ac in ALPHA_C)
      and abs(BAND_UNG[ALPHA_C[1]] / 2.56e-18 - 1) < 0.01)
OUT["numbers"]["C4"] = {"gate": GATE_NAME, "rho_star0_over_rho_m0": {f"{k_[0]}/{k_[1]}": v_ / RHOM0 for k_, v_ in RSTAR0.items()},
                        "zon_max": {f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in ZON.items()}, "z_on": Z_ONS,
                        "sigma8_ratio": {f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in S8C.items()},
                        "web_gate": {f"{k_[0]}/{k_[1]}": {str(z_): v_ for z_, v_ in d_.items()} for k_, d_ in WEB.items()},
                        "galaxies": {f"{k_[0]}/{k_[1]}/{k_[2]:.0e}/z{k_[3]}/y{k_[4]}": list(v_[:2]) + [v_[3]] for k_, v_ in GAL.items()},
                        "kids_plus_flagship": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in KIDS.items()},
                        "design_table_dex": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in DES_TAB.items()},
                        "u2_wpp_range": [w2_min, w2_max], "Kblock": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in KB.items()},
                        "nonunique_cells": multi,
                        "prices": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in PR.items()},
                        "fp5_band_ystar": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in BAND.items()},
                        "fp5_band_ungated": {str(k_): v_ for k_, v_ in BAND_UNG.items()}}

# ============================================================================================= C5 control: threshold gate
banner("C5  CONTROL (both ways): the threshold gate -- passes the data gates and FP5, fails stability")
st2 = np.gradient(np.gradient(smooth_step(ug), ug), ug)
th_pos, th_neg = float(np.max(st2[5:-5] * ug[5:-5] ** 2)), float(np.min(st2[5:-5] * ug[5:-5] ** 2))
multi_t = 0
for rm in np.logspace(-3, 1, 17):
    for pv in np.logspace(-1, 3, 17):
        grid = np.linspace(0, rm + pv + 1, 20001)
        vals = grid - rm - smooth_step(grid) * pv
        multi_t += int(np.sum(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0) > 1)
s8_thr = {(f, m): s8ratio(web_gate(HEAD, f, Z_ON, gate=smooth_step), f, m) for f in FOOTS for m in MODES}
thr_flag = {f: 2 * math.log10(on_fraction(1e11 * MSUN, A0[f], rho_star_of(2.5, HEAD, f, Z_ON), 2.5, 0.1, gate=smooth_step)[0]) for f in FOOTS}
thr_frw = {f: float(smooth_step(RHOM0 / rho_star_of(0.0, HEAD, f, Z_ON))) for f in FOOTS}
check("C5 CONTROL: a threshold gate flat at both ends (same edge) keeps the web exactly off (sigma_8 = LCDM), keeps the "
      "flagship on and vanishes on FRW (FP5 satisfied), but u^2 W'' takes both signs (an anti-pressure on half of every "
      "layer, a symbol zero there by C1) and the self-consistent state is bistable -- the record's obstruction",
      f"u^2 W'' in [{th_neg:.2f}, {th_pos:.2f}]; bistable cells {multi_t}/289; W(FRW) {thr_frw}; sigma_8 ratio "
      + ", ".join(f"{k_[0][:3]}/{k_[1]} {v_:.5f}" for k_, v_ in s8_thr.items())
      + "; flagship (1e11, z = 2.5) " + ", ".join(f"{f[:3]} {v_:+.3f} dex" for f, v_ in thr_flag.items()),
      th_pos > 0 and th_neg < 0 and multi_t > 0 and max(abs(v_ - 1) for v_ in s8_thr.values()) < 1e-6
      and max(thr_frw.values()) == 0.0 and max(abs(v_) for v_ in thr_flag.values()) <= 2 * DEX_OK)

# ============================================================================================= C8 the proposal
banner("C8  THE PROPOSED CONSTRUCTION: a leaf-average global factor x a convex local ramp (flat only at the low end)")
# (a) the global factor reads <K>_h: C1's leaf-average lemma applies
P_SW, XC, NR = 1.0, 2.5, 2                                     # p (L359's linear cell), x_c (its threshold), n (convex)
def xread(rho_dyn, zz):                                        # x = 4 pi G (rho_dyn - rho_bar)/H^2 = 1.5 Omega_m(z) delta_dyn
    return 4 * math.pi * G * (rho_dyn - RHOM0 * (1 + zz) ** 3) / Hz(zz) ** 2
def glob(zz):                                                  # [Omega_L(<K>)/Omega_L0]^p, Omega_L(<K>) = 3 Lambda c^2/<K>^2
    return (1.0 / Ez(1 / (1 + zz)) ** 2) ** P_SW
rF11 = math.sqrt(G * 1e11 * MSUN / (0.1 * A0["canonical"]))
X_N = xread(rho_dyn_point(rF11, 1e11 * MSUN, A0["canonical"]), 0.0)   # normalise: W = 1 at the 1e11 flagship radius, z = 0
def ramp(x, zz):
    return glob(zz) * (max(x - XC, 0.0) / (X_N - XC)) ** NR
R8 = {}
R8["W(FRW) all z"] = max(ramp(0.0, z_) for z_ in (0, 1, 2.5, 5, 10))
for zz in (2.0, 3.0):
    for dl in (1.0, 10.0):
        R8[f"W_IGM z={zz} delta={dl:g}"] = ramp(1.5 * Om * (1 + zz) ** 3 / Ez(1 / (1 + zz)) ** 2 * dl, zz)
for yv in (0.01, 0.1, 1.0):                                    # the RAR at z = 0 without a plateau (1e11 Msun)
    rr_ = math.sqrt(G * 1e11 * MSUN / (yv * A0["canonical"]))
    Wv = ramp(xread(rho_dyn_point(rr_, 1e11 * MSUN, A0["canonical"]), 0.0), 0.0)
    nuv = float(nu_mono(yv)); R8[f"RAR dex at g_bar={yv} a0 (no plateau)"] = 2 * math.log10((1 + Wv * (nuv - 1)) / nuv)
    R8[f"W at g_bar={yv} a0"] = Wv
# (c) the second variation at the flagship radius, z = 0 and z = 2.5 (1e11): c_g^2 = -(a0^2 q/8 pi G) rho W_rho,rho
for zz in (0.0, 2.5):
    rhoF = rho_dyn_point(rF11, 1e11 * MSUN, A0["canonical"])
    xF = xread(rhoF, zz)
    dxdrho = 4 * math.pi * G / Hz(zz) ** 2
    Wxx = glob(zz) * NR * (NR - 1) * max(xF - XC, 0.0) ** (NR - 2) / (X_N - XC) ** NR if xF > XC else 0.0
    cg2 = c_gate2(float(q_of_y(0.1)), rhoF, Wxx * dxdrho ** 2)
    R8[f"c_g^2 sign at flagship z={zz}"] = float(np.sign(cg2))
    R8[f"|c_g| km/s at flagship z={zz}"] = math.sqrt(abs(cg2)) / 1e3
s8_ramp = {(f, m): s8ratio(lambda a: ramp(0.0, 1 / a - 1), f, m) for f in FOOTS for m in MODES}
W25 = ramp(xread(rho_dyn_point(rF11, 1e11 * MSUN, A0["canonical"]), 2.5), 2.5)      # the flagship radius at z = 2.5
R8["W at the 1e11 flagship radius, z = 2.5"] = W25
R8["flagship dex z = 2.5 (1e11)"] = 2 * math.log10((1 + min(W25, 1.0) * (float(nu_mono(0.1)) - 1)) / float(nu_mono(0.1)))
for k_, v_ in R8.items():
    P(f"    {k_}: {v_:.4g}")
check("C8a the leaf-average global factor [Omega_L(<K>)/Omega_L0]^p has NO local second variation (C1's lemma: a k != 0 "
      "mode of K leaves <K>_h unchanged, so d^2 F(<K>)/d eps^2 = 0) -- that part sidesteps CV3's obstruction",
      f"delta<K> of a k != 0 mode = {avg_var}; d^2F/d eps^2 = {second_local}", avg_var == 0 and second_local == 0)
check("C8b the proposal passes FP5 (W = 0 identically near FRW: the MOND tangent vanishes on the background), sigma_8 "
      "(web exactly off) and the z = 2-3 IGM (W < 1e-3 at delta <= 10) at L359's cell p = 1, x_c = 2.5 (DECLARED, not derived)",
      f"W(FRW) = {R8['W(FRW) all z']}; sigma_8 " + ", ".join(f"{k_[0][:3]}/{k_[1]} {v_:.5f}" for k_, v_ in s8_ramp.items())
      + "; IGM " + ", ".join(f"{k_}={v_:.1e}" for k_, v_ in R8.items() if k_.startswith("W_IGM")),
      R8["W(FRW) all z"] == 0.0 and max(abs(v_ - 1) for v_ in s8_ramp.values()) < 1e-6
      and max(v_ for k_, v_ in R8.items() if k_.startswith("W_IGM")) < 1e-3)
check("C8c THE CONVEX RAMP FAILS THE SECOND VARIATION: W'' > 0 wherever the ramp curves, which by C1 is an anti-pressure "
      "(and a symbol zero) at every galaxy's MOND radius -- the sign CV3/DE12 found for the unstable half of a threshold; "
      "one-signed W'' of the CONVEX sign is not a repair",
      "; ".join(f"{k_} {v_:.3g}" for k_, v_ in R8.items() if "c_g" in k_),
      R8["c_g^2 sign at flagship z=0.0"] < 0 and R8["|c_g| km/s at flagship z=0.0"] > 1.0)
check("C8d WITHOUT AN UPPER PLATEAU THE RAR FAILS: the kernel saturates in the field y, not in the density x, so W grows "
      "~ x^n across a galaxy's MOND region (W = 1 at 0.1 a0 by normalisation) -- a plateau is needed, and a plateau "
      "makes W concave there: W'' of both signs again (C5); normalised at z = 0, the global factor also switches the "
      "z = 2.5 flagship off (reported)",
      "; ".join(f"{k_} {v_:.3g}" for k_, v_ in R8.items() if k_.startswith("RAR") or k_.startswith("W at") or k_.startswith("flagship")),
      max(abs(R8[f"RAR dex at g_bar={yv} a0 (no plateau)"]) for yv in (0.01, 1.0)) > 0.1)
OUT["numbers"]["C8"] = {"p": P_SW, "x_c": XC, "n": NR, "x_N": X_N, "results": R8,
                        "sigma8": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in s8_ramp.items()}}

# ============================================================================================= C6 tracking class
banner("C6  THE TRACKING CLASS: the khronon's finite response speed cannot separate the web from galaxies")
C2MAX = {}
for f in FOOTS:
    for m in MODES:
        g = lambda lc: s8ratio(lambda a: 1.0, f, m, c2=10 ** lc) - 1.02
        C2MAX[(f, m)] = 10 ** brentq(g, -16, -5, xtol=1e-3)
CSMIN = {Cc: 2 * Cc * (V_MOVE / c) ** 2 for Cc in (1.0, 10.0, 100.0)}  # c_s = v at c_2 ~ 2 C v^2/c^2 (KM2's pole)
check("C6 THE TRACKING CLASS FAILS: sigma_8 <= 1.02 needs c_2 <= c_2,max (the phantom must not follow the linear modes), "
      "while a galaxy moving at 600 km/s needs c_s > 600 km/s (KM2's pole), i.e. c_2 >= 2 C (v/c)^2 -- apart by >= 2 "
      "decades for every constitutive C = 1-100",
      "c_2,max: " + ", ".join(f"{k_[0][:3]}/{k_[1]} {v_:.2e}" for k_, v_ in C2MAX.items())
      + "; c_2,min(C = 1/10/100): " + ", ".join(f"{v_:.1e}" for v_ in CSMIN.values()),
      max(C2MAX.values()) * 100 < min(CSMIN.values()))
OUT["numbers"]["C6"] = {"c2max": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in C2MAX.items()},
                        "c2min_moving": {str(k_): v_ for k_, v_ in CSMIN.items()}}

# ============================================================================================= C7 K-floor backreaction
banner("C7  THE K-FLOOR WITH BACKREACTION: can the MOND energy pull the clock's K down inside galaxies?")
xs = sp.symbols("x", real=True)
pif = sp.Function("pi")(xs)
Kbar, c2k = sp.symbols("Kbar c_2", positive=True)
Bf = sp.Function("B")
dK = -sp.diff(pif, xs, 2)                                      # static leaf: delta K = -lap(pi) (CV4 K1)
Lleaf = -c2k * dK ** 2 + Bf(Kbar + dK)
el = euler_equations(Lleaf, [pif], [xs])[0].lhs
flux = sp.diff(Lleaf, sp.diff(pif, xs, 2))                     # dL/d(pi'') = 2 c_2 dK - B'(Kbar + dK)
fl_ok = (sp.simplify(el - sp.diff(flux, xs, 2)) == 0 or sp.simplify(el + sp.diff(flux, xs, 2)) == 0)
flux_form = sp.simplify(sp.diff(flux, c2k) - 2 * dK) == 0 and sp.simplify(sp.diff(flux.subs(c2k, 0), pif)) == 0


def Bfloor_K(K, s, f):
    """quartic K-floor (L341 F4): B = 2 alpha^2 q(sqrt(s^4 + kappa^4)), kappa = K/(3 alpha); returns dB/dK."""
    kap = K / (3 * alpha[f]); Zeff = math.sqrt(s ** 4 + kap ** 4); seff = math.sqrt(Zeff)
    qp = float(nu_mono(seff)) - 1.0
    return 2 * alpha[f] ** 2 * qp * (2 * kap ** 3 / Zeff) / (3 * alpha[f])


C7, C7B = {}, {}
for f in FOOTS:
    K0 = 3 * H0 / c
    web = Bfloor_K(K0, 0.0, f)
    kap0 = K0 / (3 * alpha[f])
    for s in (0.1, 1.0, 2.54):
        C7[(f, s)] = (Bfloor_K(K0, s, f) - web) / (2 * C2W * K0)
        kap = kap0 * (1 + C7[(f, s)]); se = (s ** 4 + kap ** 4) ** 0.25
        C7B[(f, s)] = (float(nu_mono(se)) - 1) * (s / se) ** 2 / (float(nu_mono(s)) - 1)   # floored/free MOND tangent
P("    delta K / K inside a galaxy (s = g_N/a0) relative to the web, z = 0, c_2 = 7.3e-3: "
  + ", ".join(f"{k_[0][:3]}/s={k_[1]} {v_:+.2e}" for k_, v_ in C7.items()))
check("C7 THE K-FLOOR CANNOT UNBLIND ITSELF: the static khronon equation with a K-dependent MOND energy B(K) is "
      "lap^2(2 c_2 dK - B_K) = 0, so delta K = (B_K - <B_K>)/(2 c_2); inside a galaxy the floor dominates (s << kappa = "
      "cH/a0 ~ 6-7), so delta K/K = O((s/kappa)^4): K drops by <= 0.3% for s <= 1 (4-9% at the phantom peak), and the "
      "back-reacted floor leaves < 1% of the free MOND tangent in the MOND region -- galaxies stay Newtonian (L341 F6)",
      f"EL = lap^2(flux): {fl_ok}; flux = 2 c_2 dK - B'(K): {flux_form}; delta K/K "
      + ", ".join(f"{k_[0][:3]}/s={k_[1]} {v_:+.1e}" for k_, v_ in C7.items())
      + "; floored/free tangent " + ", ".join(f"{k_[0][:3]}/s={k_[1]} {v_:.1e}" for k_, v_ in C7B.items()),
      fl_ok and flux_form and max(abs(C7[(f, s_)]) for f in FOOTS for s_ in (0.1, 1.0)) < 0.01
      and max(C7B[(f, s_)] for f in FOOTS for s_ in (0.1, 1.0)) < 0.01)
OUT["numbers"]["C7"] = {"dK_over_K": {f"{k_[0]}/s={k_[1]}": v_ for k_, v_ in C7.items()},
                        "floored_over_free_tangent": {f"{k_[0]}/s={k_[1]}": v_ for k_, v_ in C7B.items()}}

# ============================================================================================= T the trilemma
banner("T  THE TRILEMMA: FP5 (tangent zero on FRW), non-negative second variation, sigma_8 + galaxies")
CLASSES = {
    "ungated core": dict(fp5=bool(tan_core != sp.oo), stable=True, data=bool(min(ung.values()) <= 1.02 * S8_LCDM)),
    "concave gate (C4)": dict(fp5=bool(min(W_FRW.values()) == 0), stable=bool(w2_max <= 0.0 and second_local == 0),
                              data=bool(max(v_ for k_, v_ in S8C.items() if k_[0] == HEAD) <= 1.02 and flag_ok)),
    "threshold gate (C5)": dict(fp5=bool(max(thr_frw.values()) == 0), stable=bool(th_neg >= 0),
                                data=bool(max(abs(v_ - 1) for v_ in s8_thr.values()) < 1e-6)),
    "convex ramp x leaf average (C8)": dict(fp5=bool(R8["W(FRW) all z"] == 0), stable=bool(R8["c_g^2 sign at flagship z=0.0"] >= 0),
                                           data=bool(max(abs(R8[f"RAR dex at g_bar={yv} a0 (no plateau)"]) for yv in (0.01, 1.0)) <= 0.1)),
    "tracking (C6)": dict(fp5=False, stable=True, data=not (max(C2MAX.values()) * 100 < min(CSMIN.values()))),
    "K-floor + backreaction (C7)": dict(fp5=True, stable=True,
                                       data=bool(L341J["numbers"]["F6"]["canonical"]["floor"] < L341J["numbers"]["F6"]["canonical"]["free"] + 10
                                                 or max(C7B.values()) > 0.5)),
}
for k_, v_ in CLASSES.items():
    P(f"    {k_:34s} FP5 {str(v_['fp5']):5s}  stable {str(v_['stable']):5s}  sigma_8+galaxies {v_['data']}")
nall = sum(1 for v_ in CLASSES.values() if all(v_.values()))
check("T THE TRILEMMA: no local mechanism tested meets all three of FP5 (MOND tangent zero on FRW), a non-negative second "
      "variation, and sigma_8 within 2% with galaxy interiors on; the reason is one lemma: a gate that is exactly zero "
      "on FRW and one in galaxies switches on from zero, so it is convex somewhere (DE13's Lean lemma), and convex "
      "where the MOND energy B > 0 is C1's anti-pressure",
      f"classes meeting all three: {nall} of {len(CLASSES)}", nall == 0)
OUT["numbers"]["T"] = CLASSES

# ============================================================================================= W ledger
banner("W  THE LEDGER: FP3 / G-1 on the ungated C-H/K core")
LEDGER = [
    ("G1a", "FRW background of the core (leaf average): Friedmann = GR, G_cos = G", "DERIVED", "A1 sympy minisuperspace; A2 control"),
    ("G1b", "a0 absent from the background; a0(z)/a0(0) = 1 (canonical reading)", "DERIVED", "A3; both footings"),
    ("G1c", "the dark mass on FRW: cold, w = 0, Omega_c", "POSTULATED", "declared field initial data (FP4 owns it)"),
    ("G1d", "the core's MOND energy around FRW: O(eps^(3/2)), infinite zero-field tangent", "DERIVED", "B1 sympy; FP5's pinned U"),
    ("G1e", "ungated core in linear cosmology: sigma_8 18-27", "FAILS", "B2 (L341 reproduced), B3 at FP0's footings"),
    ("G1f", "well-posed on FRW iff the gated tangent W C_T < (2 - alpha_c)/alpha_c", "DERIVED", "C0 on FP5's committed E(C)"),
    ("G1g", "a local gate has a non-negative second variation iff it is concave; leaf averages add none", "DERIVED",
     "C1 static symbol + local pressure + leaf-average lemma"),
    ("G1h", "sigma_8 within 2% caps the web's MOND on-fraction at ~2e-3 (3e-2 if spent at z <= 0.5)", "CONSTRAINT",
     "C2, L341 yardstick, both footings"),
    ("G1i", "chord bound: a stable local gate's on-fraction <= (rho/rho_bar) x its web value", "DERIVED", "C3 theorem"),
    ("G1j", "the concave gate W = w(rho_dyn/rho_*(<K>_h)): the form and rho_*", "POSTULATED",
     "chosen inside the class G1g allows; rho_* bounded by C2-C4"),
    ("G1k", "sigma_8 within 2% with the flagship on (M_b <= 1e11, z <= 2.5) or the dwarf RAR tail; stable, unique", "DERIVED",
     "C4a-C4d (D1, D3), given G1j"),
    ("G1l", "L* outskirts (1e11 beyond ~70 kpc), 1e12 at the flagship radius, KiDS 1 Mpc, galaxies at z >~ 4", "FAILS",
     "C4b/C4b'/C4e: the chord bound spends the sigma_8 budget"),
    ("G1m", "the z = 2.5-3 IGM under the concave gate (force boost 11-28% for D1)", "OPEN", "C4e; a P1D run owed; likely fails"),
    ("G1n", "the concave gate's MOND tangent on FRW (FP5 strict)", "FAILS", "C4f: W(FRW) > 0; the band y < y* shrinks, survives"),
    ("G1o", "leaf-average global factor: no local second variation", "DERIVED", "C1 lemma, C8a"),
    ("G1p", "convex local ramp (the proposal; p = 1, x_c = 2.5 declared)", "FAILS", "C8c anti-pressure; C8d RAR without plateau"),
    ("G1q", "tracking (khronon c_s) as the switch", "FAILS", "C6: sigma_8 vs KM2's moving-source pole"),
    ("G1r", "K-floor with backreaction", "FAILS", "C7: delta K/K = O((s/kappa)^4)"),
    ("G1s", "G-1 by any local gate on the MOND energy", "FAILS", "T: FP5 x second variation x data trilemma"),
    ("G1t", "a MOND term with ZERO zero-field tangent on a field with its own inertia (AQUAL-type, O(eps^3))", "OPEN",
     "B1 + C0: meets FP5 by order counting with no gate; not in the core (its kernel reads the constrained U)"),
]
for k_, what, status, why in LEDGER:
    P(f"    {k_:5s} {status:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w__, status=s_, basis=b_) for k_, w__, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
check("G1 (reported) G-1 passed by a mechanism in the core's own variables (FP5 tangent zero on FRW, sigma_8 within 2%, "
      "galaxies on, non-negative second variation)",
      f"no: the concave gate meets sigma_8 + galaxy interiors (z <= {Z_ON:.2f}) + stability but not FP5's strict form; "
      f"every FP5-exact gate is convex somewhere (T)", False, load_bearing=False)

# ============================================================================================= verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
n_pass = sum(1 for _, ok, _lb in CH if ok)
banner("VERDICT")
P(f"  The ungated core fails linear cosmology because its MOND energy is O(eps^(3/2)) around FRW with an infinite"
  f"\n  zero-field tangent (sigma_8 ~ 20; FP5's pinned U).  A local gate on the MOND energy is stable iff concave (C1),"
  f"\n  and a concave gate's on-fraction is capped by the density ratio (C3).  Spent at that bound, one concave gate built"
  f"\n  from the clock's D_i a^i and leaf average <K>_h keeps sigma_8 within 2% (D1 max {max(v_ for k_, v_ in S8C.items() if k_[0] == HEAD):.4f})"
  f"\n  with the flagship on for M_b <= 1e11 to z_on = {Z_ON:.2f}, stable and unique -- but it cuts the L* outskirts, the"
  f"\n  1e12 flagship and KiDS, pushes 11-28% extra force into the z = 2.5-3 IGM, and is not zero on FRW (FP5's band"
  f"\n  shrinks to y < {max(BAND.values()):.0e} but survives).  Every gate that IS zero on FRW switches on from zero and is"
  f"\n  convex somewhere: the proposed convex ramp and the threshold carry C1's anti-pressure.  No local gate meets all"
  f"\n  three; the door left is a MOND term with a ZERO zero-field tangent on a field with its own inertia -- not in the core.")
P(f"  Time {time.time() - T0:.0f} s.")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")), "w"),
          indent=1, default=str)
P(f"\n  {n_pass}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{SLUG.replace('_MUTATE', '')}_results{'_MUTATE' if MUTATE else ''}.json")
sys.exit(0 if n_fail == 0 else 1)
