#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR20 -- ONE FIELD FOR a0 AND LAMBDA?  Four ties written into the chain's root action (FP7) and varied: the unimodular
multiplier (Henneaux-Teitelboim), the four-form (Brown-Teitelboim), the khronon's leaf curvature K, and vacuum-energy
sequestering.  For each: the flat law, the degree-of-freedom count, FRW and PPN, and the size of any local a0 variation.

WHY.  The chain's top declares P1, a0 = kappa c sqrt(G rho_Lambda) (FP0; kappa = 1/2 FITTED, equivalently Z = 5.7888).
FP5 (a26136bc4) found that no term of the core ties a0 to Lambda (D1-D5): promoted to a free field, alpha = a0/c^2 obeys
an equation that switches MOND off unless a potential is put in by hand (D3), and the khronon's only background scale is
K = 3H, the rival footing (D4).  The record's four-form (kappa_closure/k04) links the two scales with a free coupling
ratio.  Dimensional analysis already fixes the sqrt(G rho) form (FP0 C1); the only question here is whether a0 becomes a
consequence of the field that sets Lambda, with kappa as the only coupling.  Nothing here derives kappa.

THE ROOT (real_research/derivation_chain_2026/FP7_aqual_type_repair.py; units c = 1, per 1/16 pi G):
  I = Int sqrt(-g) { R - 2 Lambda + alpha_c a^2 - c_2 (K - <K>_h)^2 + (2 - alpha_c) h(2a - Dchi).Dchi
                     - 2 alpha^2 J_P2(Y/alpha^2) + 2 lambda (n.dphi)^2 + heat filter } + S_m,      Y = h^{mn} d_m phi d_n phi,
  J_P2(s) = -(1/4) ln(1 - 2 sqrt s) - sqrt(s)/2 - s/2.  The kernel scale alpha = a0/c^2 enters ONLY through the J term, and
      d/d alpha [-2 alpha^2 J(Y/alpha^2)] = 4 alpha F,   F = s J'(s) - J(s) >= 0
  (F = x^3/3 in deep MOND and F -> y/2 in the Newtonian regime; x = sqrt(s) is the scalar's force in units of a0 and
  y = g_N/a0).  On P2's spherical law F(y) = 2 Int_0^y h - y h(y) with h the MOND boost: the same density as FP5 D3's
  (q - Z q') in the C-H core.

THE FOUR TIES (each replaces the constant alpha; nothing else in the root changes):
  T1 unimodular (Henneaux & Teitelboim 1989): Lambda -> Lambda(x) plus 2 Lambda d_m T^m (T^m a vector density: the
     3-form multiplier), and alpha = alpha(Lambda) = kappa sqrt(Lambda/8 pi).
  T2 four-form (Brown & Teitelboim 1987-88): F = dA with dual amplitude q; sqrt(-g) (Z_q/2) q^2 replaces -2 Lambda, and
     alpha = beta |q|.  Z_q is the four-form's stiffness (the record's name, 738216fbd), NOT the framework's Z = 5.7888.
  T3 khronon: alpha = kappa_K K, K = nabla.n the leaf mean curvature, kappa_K fixed by today's a0.
  T4 sequestering (Kaloper & Padilla 2014): global Lambda and lambda with sigma(Lambda/(lambda^4 mu^4)); alpha a function
     of a global variable.

PRE-DECLARED (written into this docstring before any code of this lane was run; the expectations come from
pencil-and-paper algebra done while planning the lane, not from any script output):
  H1  T1: d Lambda = 0 is an exact field equation, so a0 is exactly constant in space and time; the MOND sector's
      dL/dLambda goes only into d_m T^m (the unimodular clock), where it shifts the rate by (kappa^2/8 pi) F; no local
      mode is added (0 local, 1 global); the metric equations are FP7's at Lambda = Lambda_0, so FRW and PPN are
      unchanged.  EXPECT TRUE.  Status: TIED (a coupling function of one integration constant; kappa still fitted).
  H2a T2: the conserved quantity is the conjugate Pi = dL/dq, not q, so a0_loc/a0 = 1/(1 + (kappa^2/8 pi) F(y_loc));
      the flux amplitude cancels (the one coupling is beta^2/Z_q = kappa^2/32 pi); SPARC's RAR moves by < 0.01 dex.
      EXPECT TRUE.
  H2b T2 health: the slaved kernel stays monotone (C_L,eff > 0) up to the flux's switch-off.  EXPECT FALSE: the algebra
      puts a fold of the four-form's Legendre map at (1 - 2x)^2 ~ kappa^2/(64 pi), i.e. y ~ 7, with the switch-off at
      y = 16 pi/kappa^2 ~ 201.
  H3  T3: a0 follows K = 3H(z), so a0(z)/a0(0) = E(z), +0.576 dex at z = 2.5 (FP5 D4): the flat law FAILS.  EXPECT TRUE.
  H4  T4: alpha of a global variable is exactly constant, but the sequestered Lambda carries -V_vac and the residual
      <tau>/4 is <= 0 for ordinary matter: constant, NOT tied to the observed rho_Lambda.  EXPECT TRUE.
"""
# (the docstring above is the pre-declaration; everything below was written after it and before the first run)
DOC_CHECKS = r"""
CHECKS
  C1 CONTROL FP5 D3 (the 'a0 as a field' check) reproduced from FP5's own nu_mono functions: (q - Z q')/s^1.5 has its
     minimum 9.782e-04 at s = 1e6 and the deep-MOND value 0.3333, and the symbolic identity holds.
  C2 CONTROL FP0 R3 / FP5 D4: E(z) = 1.322, 1.791, 3.769, 8.294 at z = 0.5, 1, 2.5, 5 and log10 E(2.5) = 0.576.
  C3 CONTROL FP5 D5: Lambda/alpha^2 = 100.531 (32 pi, canonical) / 68.834 (alt) and kappa_alt = 0.6043, to 1e-12.
  C4 CONTROL FP7's static law at one point: the Sun's Galactic field (g_ext = 2.32e-10) gives x_e = 0.4501,
     mu_T = 4.507, mu_L = 49.64 (FP7 A4, committed .out).
  C5 CONTROL this lane's four-form solver, run in k04's own convention and kernel, reproduces k04's committed F3 rows
     (a0_loc/a0 and the RAR shift at seven accelerations, K_B = 0 and 0.25) to the printed digits.
  C6 CONTROL SPARC: FP1's C0 RAR statistic (0.1083 dex, 175 galaxies) and FP7's median per-point error (0.0370 dex).
  A  the algebra (sympy): J_P2' = mu_s; d/dalpha[-2 alpha^2 J(Y/alpha^2)] = 4 alpha (s J' - J); along P2's spherical law
     dF/dy = x/(2(1 - x)), F = 2 Int x dy - y x (the QUMOND/AQUAL envelope identity), and x F'(y)/x'(y) = x^3/(1 - 2x)^2
     (the identity that makes the four-form's fold and the kernel's non-monotonicity one condition); the closed form
     matches direct quadrature.
  T1a HT, varied (1+1 toy with a background density sqrt(-g)): the multiplier's equations are d_t Lambda = d_x Lambda = 0;
      Lambda's equation fixes d_m T^m; phi's equation on shell is the root's at alpha(Lambda_0).
  T1b the unimodular clock: d_m T^m = sqrt(-g) [1 - (kappa^2/8 pi) F]; FP5 D3's obstruction (a free alpha-field forces
      F = 0, no MOND) is absorbed by the multiplier.
  T1c the Dirac count on a periodic lattice: the constraints are first class, no secondary constraint with the MOND
      coupling, 2N - 2(N - 1) = 2 phase-space dimensions: one global degree of freedom, none local.
  T1d FRW and PPN: the HT term is metric-free, so the metric equations are the root's at Lambda_0: FP7 B1 (GR + Lambda)
      and D2 (gamma = 1, khronometric alphas) carry over exactly.
  T1e (reported) the vacuum-energy caveat: a matter vacuum energy enters the observed Lambda but not a0.
  T2a BT, varied: the conjugate Pi = dL/dq is constant; Lambda_eff = (q P' - P)/2 = Z_q q^2/4; the flux amplitude
      cancels: alpha_0^2/Lambda_0 = 4 beta^2/Z_q = kappa^2/8 pi; locally a0_loc/a0 = 1/(1 + (kappa^2/8 pi) F(y_loc)).
  T2b the local a0 and the RAR shift in galaxies, both footings.
  T2c = H2a  SPARC: the RAR statistic with the four-form's local a0, both footings; max per-point shift < 0.01 dex.
  T2d the fold, located two independent ways (the family's du/dy = 0, and L_qq|_Y = 0 by 40-digit finite differences of
      the action's own J_P2), agreeing to < 1e-6; C_L,eff = dy/du < 0 on the whole band up to the switch-off y_off = 2/eps.
  T2d2 the fold's consequence in FP7's own reduced quadratic form (T, V of FP7 C1): one omega^2 < 0, ~ k^2, on the band;
      CONTROL: none at fixed alpha.
  T2d3 the same on FP14's zero-knob root (lambda = 0; c_2 finite and -> oo), from FP14 L2's committed one-mode formulas
      (added after FP14 landed during this lane; disclosed).
  T2e (reported, = H2b as it falls) where the band sits: SPARC points, a solar-mass star's shell, wide binaries.
  T2f (reported) the same test on the C-H core's nu_mono and on k04's saturated kernel.
  T2g (reported) power-law four-forms P ~ q^n: the fold for n = 1.5, 2, 3.
  T2h FRW: F = 0 on the homogeneous background, so q = q_0, Lambda_eff constant and a0(z) flat; DOF as T1c.
  T3a the khronon's K on FRW is 3H (sympy); T3b the K tie gives a0(z)/a0(0) = E(z): +0.576 dex at z = 2.5 (FP5 D4) -- the
      candidate FAILS the flat law (L37 S8b: the rival is killed at recombination, committed).
  T3c (reported) the K tie's local structure: the khronon's lambda shifted by 2 kappa_K^2 (x^3/(1-2x)^2 - F), and the
      leaf-harmonic estimate delta K/K = 2 kappa_K^2 F/c_2.
  T4a sequestering, varied (the global equations, sympy): Lambda_s = <T>/4, the vacuum energy cancels from the Einstein
      equation, lambda^4 = sigma'/(mu^4 Vol); the matter-scaling identity d/dlambda[lambda^4 L(lambda^-2 g)] = lambda^3 T~
      verified on a scalar field.
  T4b Lambda_s = -V_vac + <tau>/4: alpha(Lambda_s) inherits the vacuum energy; tau = -rho(1 - 3w) <= 0 for w <= 1/3.
  T4c (record) k02's committed magnitudes for the MOND scalar's own spacetime average.
  HEADLINE-FLAT  the headline tie (T1) on the solutions of its own field equations: a0(z)/a0(0) = 1 at z = 0.5, 1, 2.5,
      5, 1100 and a0_loc/a0 = 1 across a galaxy, to 1e-12.
  W  the ledger of the four ties.
MUTATE=1: the headline tie reads the khronon's K (= 3H on FRW, T3) instead of the conserved HT field: HEADLINE-FLAT must
FAIL (rc = 1).  Every other check is unchanged by the mutation.

SCOPE.  The ties are varied at the level the task sets: the field equations of each tie in the root (sympy, 1+1 toys for
the local structure, minisuperspace for FRW), the spherical static law for the local a0 (P2 is exact there in the root,
FP7 A2), SPARC's RAR through FP1's C0 statistic, and a lattice Dirac count.  Discs are not re-solved with the local a0
(the shifts are <= 0.002 dex, far inside FP7 A3's AQUAL/QUMOND disc difference).  Both a0 footings are carried
(canonical 9.3603e-11, alt 1.1312e-10 m/s^2; on rho_Lambda the alt footing is kappa = 0.6043).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR20_a0_lambda_tie.py   (MUTATE=1 for
the control).  Writes XR20_a0_lambda_tie[_MUTATE].out and XR20_a0_lambda_tie_results[_MUTATE].json next to itself.
"""
import os, re, sys, json, math, time
import numpy as np
import sympy as sp
import mpmath as mp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR20_a0_lambda_tie"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
T_START = time.time()


class _Tee:
    """the script writes its own .out: everything printed goes to the terminal and to the file."""

    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


TEE = _Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "XR20", "part": "the ties T1-T4 in FP7's root", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 114 + "\n" + t + "\n" + "=" * 114)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def rd(rel):
    p = os.path.join(REPO, rel)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


def num_zero(expr, fixed, overrides=None, n=4, seed=20):
    """expr == 0 as a function: every Derivative / applied-function atom is replaced at once (xreplace: exact nodes only,
    so a first derivative never rewrites a mixed second derivative) by the value in `overrides` or a random value in
    (0.05, 0.3), in a deterministic atom order; the fixed couplings keep every J_P2 argument below 1/4; n draws,
    |value| < 1e-12 at each."""
    rng = np.random.default_rng(seed)
    e0 = expr.subs(fixed)
    atoms = set(e0.atoms(sp.Derivative)) | {a_ for a_ in e0.atoms(sp.Function) if isinstance(a_, sp.core.function.AppliedUndef)}
    atoms = sorted(atoms, key=sp.default_sort_key)
    worst = 0.0
    for _ in range(n):
        m_ = {a_: sp.Float((overrides or {}).get(a_, rng.uniform(0.05, 0.3))) for a_ in atoms}
        worst = max(worst, abs(complex(sp.N(e0.xreplace(m_), 30))))
    return worst < 1e-12, worst


P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: the headline tie reads the khronon's K (= 3H on FRW) instead of the conserved HT field; "
      "HEADLINE-FLAT must FAIL ***")

# ================================================================================================ inputs
c_SI, G_SI = 299792458.0, 6.67430e-11
MPC = 3.0856775814913673e22
AU = 1.495978707e11
GM_SUN = 1.32712440018e20
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153                                  # FP0's canonical pair
fp0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))
A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
H0 = H0_KMS * 1e3 / MPC
rho_c = 3 * H0 ** 2 / (8 * math.pi * G_SI)
rho_L = OM_L * rho_c
LAM_SI = 8 * math.pi * G_SI * rho_L / c_SI ** 2                              # 1/m^2
KAP = {f: a / (c_SI * math.sqrt(G_SI * rho_L)) for f, a in A0.items()}       # kappa on rho_Lambda: 1/2 and 0.604
EPS = {f: k ** 2 / (8 * math.pi) for f, k in KAP.items()}                   # alpha^2/Lambda: the one coupling of T1/T2
E_of = lambda z: math.sqrt(OM_M * (1 + z) ** 3 + OM_L)
P(f"\n  inputs (FP0): a0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2; rho_Lambda = {rho_L:.4e} kg/m^3; "
  f"Lambda = {LAM_SI:.4e} 1/m^2;\n  kappa on rho_Lambda = {KAP['canonical']:.4f} / {KAP['alt']:.4f}; eps = kappa^2/8pi = "
  f"{EPS['canonical']:.6f} / {EPS['alt']:.6f}")
OUT["numbers"]["inputs"] = dict(a0=A0, rho_Lambda=rho_L, Lambda=LAM_SI, kappa=KAP, eps=EPS)

# ================================================================================================ kernels
# (1) the root's P2 in AQUAL form: mu_s(x) x = y  ->  x = sqrt(y^2 + y) - y (stable forms); F = s J' - J at s = x^2
xs_ = sp.symbols("x", positive=True)
F_A_SYM = xs_ ** 3 / (1 - 2 * xs_) + sp.log(1 - 2 * xs_) / 4 + xs_ / 2 + xs_ ** 2 / 2
_ser = sp.expand(sp.series(F_A_SYM, xs_, 0, 12).removeO())
F_SER = [(k, float(_ser.coeff(xs_, k))) for k in range(0, 12) if _ser.coeff(xs_, k) != 0]


def x_p2(Y):
    return Y / (math.sqrt(Y * Y + Y) + Y) if Y > 0 else 0.0


def om_p2(Y):                                   # 1 - 2x without cancellation
    return 1.0 / (1.0 + 2.0 * Y + 2.0 * math.sqrt(Y * Y + Y))


def F_p2(Y):
    """F(y) = s J'(s) - J(s) on P2's law (= 2 Int_0^y x - y x): the alpha-conjugate density of the root's MOND term."""
    if Y <= 0:
        return 0.0
    x = x_p2(Y)
    if x < 2e-3:
        return sum(cf * x ** k for k, cf in F_SER)
    om = om_p2(Y)
    return x ** 3 / om + 0.25 * math.log(om) + x / 2 + x * x / 2


def J_P2(s):
    r = mp.sqrt(s)
    return -mp.log(1 - 2 * r) / 4 - r / 2 - s / 2


# (2) the C-H core's nu_mono, verbatim from FP5 (h = the MOND boost in units of a0; H_mono = Int_0^s h)
DELTA_FLOOR = 0.05


def h_rar(y):
    return y / math.expm1(math.sqrt(y)) if y > 0 else 0.0


def dh_rar(y):
    s = math.sqrt(y); e = math.expm1(s)
    return (1.0 / e) * (1.0 - 0.5 * s * (e + 1.0) / e)


Y_P = brentq(dh_rar, 1.0, 5.0); H_P = h_rar(Y_P)
Y_S = brentq(lambda y: dh_rar(y) - DELTA_FLOOR * H_P / (y + Y_P), 1.0, Y_P); H_S = h_rar(Y_S)


def h_mono(y):
    return h_rar(y) if y <= Y_S else H_S + DELTA_FLOOR * H_P * math.log((y + Y_P) / (Y_S + Y_P))


_HS = quad(lambda v: 2 * v ** 3 / math.expm1(v) if v > 0 else 0.0, 0, math.sqrt(Y_S), epsabs=0, epsrel=1e-13)[0]


def H_mono(s):
    if s <= Y_S:
        return quad(lambda v: 2 * v ** 3 / math.expm1(v) if v > 0 else 0.0, 0, math.sqrt(s), epsabs=0, epsrel=1e-13)[0]
    return _HS + H_S * (s - Y_S) + DELTA_FLOOR * H_P * ((s + Y_P) * math.log((s + Y_P) / (Y_S + Y_P)) - (s - Y_S))


def F_mono(Y):                                  # FP5 D3's (q - Z q') at Z = s^2, alpha = 1
    return 2 * H_mono(Y) - Y * h_mono(Y)


# (3) k04's kernel and its own fixed-point iteration, verbatim (kappa_closure/k04_four_form_promotion_consistency.py)
def k04_Delta(s):
    return s / np.expm1(np.sqrt(s)) if s > 0 else 0.0


_opt = minimize_scalar(lambda s: -k04_Delta(s), bounds=(0.5, 6), method='bounded')
K04_SSAT, K04_DSAT = _opt.x, -_opt.fun
K04_JSAT = 2 * (K04_SSAT * K04_DSAT - quad(k04_Delta, 0, K04_SSAT)[0])


def k04_j(s):
    return 2 * (s * k04_Delta(s) - quad(k04_Delta, 0, s)[0]) if s <= K04_SSAT else K04_JSAT


def k04_Dl(s):
    return k04_Delta(s) if s <= K04_SSAT else K04_DSAT


def F_k04(s):
    return s * k04_Dl(s) - k04_j(s)


def k04_ratio_iter(gN, a0, KB, ZoB=8.0):
    r = 1.0
    for _ in range(200):
        s = gN / (a0 * r); r_new = 1.0 / (1.0 + (2 - KB) * (8.0 / ZoB) * (s * k04_Dl(s) - k04_j(s)) / (64 * math.pi))
        if abs(r_new - r) < 1e-12:
            break
        r = r_new
    return r


def bt_family(y, eps, Ffun):
    """T2's static law at fixed conjugate: r = a0_loc/a0 solves r (1 + eps F(y/r)) = 1; 0 beyond the switch-off."""
    if y <= 0:
        return 1.0
    f = lambda r: r * (1.0 + eps * Ffun(y / r)) - 1.0
    lo = 1e-13
    if f(lo) < 0:                                  # one crossing between lo and 1 (f(1) = eps F(y) > 0)
        return brentq(f, lo, 1.0, xtol=1e-16, rtol=1e-15, maxiter=500)
    rg = np.logspace(0, -13, 261)                  # otherwise: the physical root is the first crossing below r = 1
    prev = f(rg[0])
    for i in range(1, len(rg)):
        cur = f(rg[i])
        if cur < 0 <= prev:
            return brentq(f, rg[i], rg[i - 1], xtol=1e-16, rtol=1e-15, maxiter=500)
        prev = cur
    return 0.0                                     # no physical root: the flux is off (q = 0)


# ================================================================================================ C controls
banner("C   CONTROLS: the committed numbers this lane builds on, reproduced")
# C1 FP5 D3
sg, Zs_, zeta = sp.symbols('sigma Z zeta', positive=True)
d3_sym = True
for qtest in (zeta ** sp.Rational(3, 4) + zeta ** 2 / 7, sp.log(1 + zeta) * zeta ** sp.Rational(1, 3)):
    lhs_ = sp.diff(2 * sg ** 2 * qtest.subs(zeta, Zs_ / sg ** 2), sg)
    rhs_ = (4 * sg * (qtest - zeta * sp.diff(qtest, zeta))).subs(zeta, Zs_ / sg ** 2)
    d3_sym = d3_sym and sp.simplify(lhs_ - rhs_) == 0
svals = np.logspace(-10, 6, 161)
gvals = [F_mono(s_) / s_ ** 1.5 for s_ in svals]
c1_str = f"min {min(gvals):.3e} at s = {svals[int(np.argmin(gvals))]:.1e}, deep-MOND value {gvals[0]:.4f}"
fp5 = json.load(open(os.path.join(CHAIN, "FP5_dof_and_a0_field_results.json")))
fp5_d3 = [v for k, v in fp5["checks"].items() if k.startswith("D3")][0]["measured"]
check("C1 CONTROL FP5 D3 reproduced from FP5's own nu_mono: (q - Z q')/s^1.5 minimum and deep value, and the symbolic "
      "identity d_sigma[2 sigma^2 q(Z/sigma^2)] = 4 sigma (q - Z q')",
      f"this lane: {c1_str}; identity {d3_sym}; FP5 committed: '{fp5_d3}'", d3_sym and c1_str in fp5_d3,
      "(q - Z q') is the same alpha-conjugate density F that drives every tie below")
# C2 FP0 R3 / FP5 D4
c2_str = ", ".join(f"{E_of(z):.3f}" for z in (0.5, 1.0, 2.5, 5.0)) + f" (+{math.log10(E_of(2.5)):.3f} dex at z = 2.5)"
fp0_r3 = [v for k, v in fp0["checks"].items() if k.startswith("R3 ")][0]["measured"]
fp5_d4 = [v for k, v in fp5["checks"].items() if k.startswith("D4")][0]["measured"]
check("C2 CONTROL FP0 R3 / FP5 D4: the rival E(z) at z = 0.5, 1, 2.5, 5 and log10 E(2.5) = 0.576",
      f"this lane: {c2_str}; FP0 committed '...{fp0_r3[-60:]}'; FP5 D4 has 'log10 E(2.5) = {math.log10(E_of(2.5)):.3f}': "
      f"{('log10 E(2.5) = %.3f' % math.log10(E_of(2.5))) in fp5_d4}",
      c2_str in fp0_r3 and ("log10 E(2.5) = %.3f" % math.log10(E_of(2.5))) in fp5_d4)
# C3 FP5 D5
lam_a2 = {f: LAM_SI / (a / c_SI ** 2) ** 2 for f, a in A0.items()}
d5 = fp5["numbers"]["D5"]
c3_ok = all(abs(lam_a2[f] / d5["Lambda_over_alpha2"][f] - 1) < 1e-12 for f in A0) and abs(KAP["alt"] / d5["kappa_alt"] - 1) < 1e-12
check("C3 CONTROL FP5 D5: Lambda/alpha^2 = 8 pi/kappa^2 on both footings and kappa_alt, to 1e-12",
      f"{lam_a2['canonical']:.6f} (32 pi = {32 * math.pi:.6f}) / {lam_a2['alt']:.6f}; kappa_alt {KAP['alt']:.10f}; FP5: "
      f"{d5['Lambda_over_alpha2']['canonical']:.6f} / {d5['Lambda_over_alpha2']['alt']:.6f}, {d5['kappa_alt']:.10f}", c3_ok)
# C4 FP7's static law at one point
yN_of = lambda gobs, a0: (-a0 + math.sqrt(a0 ** 2 + 4 * gobs ** 2)) / 2 / a0
YE = {f: yN_of(2.32e-10, a) for f, a in A0.items()}
xe_c = math.sqrt(YE["canonical"] ** 2 + YE["canonical"]) - YE["canonical"]
muT_c, muL_c = xe_c / (1 - 2 * xe_c), 2 * xe_c * (1 - xe_c) / (1 - 2 * xe_c) ** 2
c4_str = f"x_e = {xe_c:.4f}, mu_T = {muT_c:.3f}, mu_L = {muL_c:.2f}"
fp7_out = rd("real_research/derivation_chain_2026/FP7_aqual_type_repair.out") or ""
check("C4 CONTROL FP7's static law at one point (A4): the Sun's Galactic field g_ext = 2.32e-10 m/s^2 on P2's AQUAL law",
      f"this lane: {c4_str} (y_N,ext = {YE['canonical']:.4f}); in FP7's committed .out: {c4_str in fp7_out}", c4_str in fp7_out)
# C5 k04's F3 rows through this lane's solver
k04_out = rd("kappa_closure/k04_four_form_promotion_consistency.out") or ""
c5_ok, c5_rows = True, []
for KB in (0.0, 0.25):
    parts_mine, parts_iter = [], []
    for s0 in (0.01, 0.1, 1.0, 2.54, 10.0, 100.0, 1e3):
        a0k = 9.3619e-11; gN = s0 * a0k
        r_m = bt_family(s0, (2 - KB) / (64 * math.pi), F_k04)
        r_i = k04_ratio_iter(gN, a0k, KB)
        g_p = gN + a0k * r_m * k04_Dl(gN / (a0k * r_m)) if r_m > 0 else gN          # beyond the switch-off the scalar is off
        dl_m = math.log10(g_p / (gN + a0k * k04_Dl(s0)))
        parts_mine.append(f"s={s0:g}: {r_m:.4f} ({dl_m:+.4f} dex)")
        parts_iter.append(abs(r_m - r_i))
    line = f"F3: K_B = {KB:.2f} canonical: a0_loc/a0 (Delta log g_obs): " + ", ".join(parts_mine)
    c5_rows.append(line)
    c5_ok = c5_ok and (line in k04_out) and max(parts_iter) < 1e-9
    P(f"    {line}\n      (k04's own iteration vs this lane's bracketing solver: max |dr| = {max(parts_iter):.1e})")
check("C5 CONTROL this lane's four-form solver in k04's convention and kernel reproduces k04's committed F3 rows to the "
      "printed digits (K_B = 0 and 0.25), and agrees with k04's own fixed-point iteration to < 1e-9",
      f"both rows found verbatim in the committed k04 output: {c5_ok}", c5_ok)
# C6 SPARC
kpc = 3.0857e19
DATA = os.path.join(REPO, "real_research", "data", "sparc_data")
GAL = []
for fn in sorted(os.listdir(DATA)):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        d = np.genfromtxt(os.path.join(DATA, fn), comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    GAL.append(tuple(d[:, i] for i in range(6)))
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)


def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


def gal_sums(nuf, a0):
    """FP1's C0 statistic (rar_framework_a0_mlfit.py's), verbatim: per-galaxy weighted SSR on the Upsilon grid."""
    S = np.zeros((len(GAL), len(UPS)))
    Wt = np.zeros((len(GAL), len(UPS)))
    for ig, (R, Vobs, eV, Vgas, Vdisk, Vbul) in enumerate(GAL):
        Rm = R * kpc
        for iu, U in enumerate(UPS):
            Vbar2 = np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2
            gb = Vbar2 * 1e6 / Rm
            go = (Vobs * 1e3) ** 2 / Rm
            ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
            r_ = np.log10(go[ok]) - np.log10(nuf(gb[ok] / a0) * gb[ok])
            w_ = 1 / (np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)) ** 2
            S[ig, iu] = np.sum(w_ * r_ ** 2)
            Wt[ig, iu] = np.sum(w_)
    return S, Wt


a0_mlfit = (2.998e8 / 2) * math.sqrt(6.674e-11 * 0.685 * 3 * 2.184e-18 ** 2 / (8 * math.pi * 6.674e-11))
S0, W0 = gal_sums(nu_p2, a0_mlfit)
iu70 = int(np.argmin(np.abs(UPS - 0.70)))
rms70 = math.sqrt(S0[:, iu70].sum() / W0[:, iu70].sum())
errs = []
for fn in sorted(os.listdir(DATA)):
    if fn.endswith("_rotmod.dat"):
        d = np.genfromtxt(os.path.join(DATA, fn), comments="#")
        if d.ndim == 2 and d.shape[1] >= 3:
            ok_ = (d[:, 1] > 0) & (d[:, 2] > 0)
            errs += list(2 * d[ok_, 2] / d[ok_, 1] / math.log(10))
SPARC_MED, N_SPARC = float(np.median(errs)), len(errs)
fp1 = json.load(open(os.path.join(CHAIN, "FP1_static_sector_results.json")))
fp1_c0 = [v for k, v in fp1["checks"].items() if k.startswith("C0")][0]["measured"]
fp7j = json.load(open(os.path.join(CHAIN, "FP7_aqual_type_repair_results.json")))
c6_ok = fp1_c0.startswith(f"{rms70:.4f} dex") and f"{len(GAL)} galaxies" in fp1_c0 and \
    abs(SPARC_MED - fp7j["numbers"]["A3"]["sparc_median_err"]) < 1e-12 and N_SPARC == 3391
check("C6 CONTROL SPARC: FP1's C0 RAR statistic and FP7's median per-point error in log g_obs",
      f"rms at Upsilon = 0.70: {rms70:.4f} dex ({len(GAL)} galaxies; FP1: '{fp1_c0}'); median error {SPARC_MED:.4f} dex over "
      f"{N_SPARC} points (FP7: {fp7j['numbers']['A3']['sparc_median_err']:.4f})", c6_ok)
OUT["numbers"]["controls"] = dict(C1=c1_str, C2=c2_str, C3=lam_a2, C4=c4_str, C5=c5_rows, C6=dict(rms70=rms70, sparc_med=SPARC_MED))

# ================================================================================================ A the algebra of F
banner("A   THE ALGEBRA: the alpha-conjugate density F of the root's MOND term, on P2's law (sympy + quadrature)")
s_ = sp.symbols("s", positive=True)
Jsym = -sp.log(1 - 2 * sp.sqrt(s_)) / 4 - sp.sqrt(s_) / 2 - s_ / 2
a1 = sp.simplify(sp.diff(Jsym, s_) - sp.sqrt(s_) / (1 - 2 * sp.sqrt(s_))) == 0 and Jsym.subs(s_, 0) == 0
al_, Y_ = sp.symbols("alpha Y", positive=True)
Jg = sp.Function("J")
lhsA = sp.diff(-2 * al_ ** 2 * Jg(Y_ / al_ ** 2), al_)
rhsA = 4 * al_ * (Y_ * sp.diff(Jg(Y_ / al_ ** 2), Y_) - Jg(Y_ / al_ ** 2))     # s J'(s) = Y d/dY J(Y/alpha^2)
a2 = sp.simplify(lhsA - rhsA) == 0
FA_x = sp.simplify((s_ * sp.diff(Jsym, s_) - Jsym).subs(s_, xs_ ** 2))
a3 = sp.simplify(FA_x - F_A_SYM) == 0
y_of_x = xs_ ** 2 / (1 - 2 * xs_)                                           # P2's spherical law: mu_s(x) x = y
dFdy = sp.simplify(sp.diff(F_A_SYM, xs_) / sp.diff(y_of_x, xs_))
a4 = sp.simplify(dFdy - xs_ / (2 * (1 - xs_))) == 0
# the envelope identity: d/dx[2 Int x dy - y x] = 2 x y'(x) - y'(x) x - y = x y' - y ; compare with dF/dx
env_ok = sp.simplify(sp.diff(F_A_SYM, xs_) - (xs_ * sp.diff(y_of_x, xs_) - y_of_x)) == 0 and F_A_SYM.subs(xs_, 0) == 0
fold_id = sp.simplify(xs_ * (xs_ / (2 * (1 - xs_))) / (1 / sp.diff(y_of_x, xs_)) - xs_ ** 3 / (1 - 2 * xs_) ** 2) == 0
qd = []
for Yv in (1e-6, 1e-3, 0.1, 1.0, 10.0, 1e3):
    Iq = quad(lambda yy: x_p2(yy) / (2 * (1 - x_p2(yy))), 0, Yv, epsabs=0, epsrel=1e-12, limit=400)[0]
    qd.append(abs(F_p2(Yv) / Iq - 1))
a5 = max(qd) < 1e-8
check("A  THE ALGEBRA: J_P2' = mu_s(sqrt s), J(0) = 0; d/dalpha[-2 alpha^2 J(Y/alpha^2)] = 4 alpha (s J' - J) for any J; "
      "F = s J' - J = x^3/(1-2x) + ln(1-2x)/4 + x/2 + x^2/2; along P2's law dF/dy = x/(2(1-x)), F = 2 Int x dy - y x "
      "(envelope), x F'(y)/x'(y) = x^3/(1-2x)^2 (the fold identity); the closed form (+ series below x = 2e-3) equals direct "
      "quadrature",
      f"J' {a1}; alpha-derivative {a2}; F closed form {a3}; dF/dy {a4}; envelope {env_ok}; fold identity {fold_id}; "
      f"max rel |closed - quadrature| over y = 1e-6..1e3: {max(qd):.1e}",
      a1 and a2 and a3 and a4 and env_ok and fold_id and a5,
      "F > 0 for every y > 0 (F >= x^3/3); F -> y/2 at high y: the MOND term's alpha-derivative is Newton-strength there")
OUT["numbers"]["A"] = dict(series=F_SER, quad_rel=max(qd))

# ================================================================================================ T1 unimodular (HT)
banner("T1  HENNEAUX-TEITELBOIM: Lambda(x) with a 3-form multiplier, alpha = kappa sqrt(Lambda/8 pi)")
t_, xx_ = sp.symbols('t x', real=True)
LamF, T0F, T1F, phF = (sp.Function(n_)(t_, xx_) for n_ in ("Lambda", "T0", "T1", "phi"))
gdet = sp.Function('g', positive=True)(t_, xx_)                              # sqrt(-g): a background density in the toy
kap_s, lamI = sp.symbols('kappa lambda_I', positive=True)
Ls, L0 = sp.symbols('L_s Lambda_0', positive=True)
alpha_of = lambda L_: kap_s * sp.sqrt(L_ / (8 * sp.pi))
Jc = lambda s: -sp.log(1 - 2 * sp.sqrt(s)) / 4 - sp.sqrt(s) / 2 - s / 2      # the root's J_P2
phx, pht = sp.diff(phF, xx_), sp.diff(phF, t_)


def L_M(al, J=Jc):
    return -2 * al ** 2 * J(phx ** 2 / al ** 2) + 2 * lamI * pht ** 2


L_HT = gdet * (-2 * LamF + L_M(alpha_of(LamF))) + 2 * LamF * (sp.diff(T0F, t_) + sp.diff(T1F, xx_))
EL = euler_equations(L_HT, [LamF, T0F, T1F, phF], [t_, xx_])
el_T0, el_T1 = sp.simplify(EL[1].lhs), sp.simplify(EL[2].lhs)
m1 = sp.simplify(el_T0 + 2 * sp.diff(LamF, t_)) == 0 and sp.simplify(el_T1 + 2 * sp.diff(LamF, xx_)) == 0
# phi's equation on shell (Lambda = Lambda_0) against the root's with alpha = alpha(Lambda_0)
el_phi_on = sp.simplify(EL[3].lhs.subs(LamF, L0).doit())
al0 = sp.Symbol('alpha_0', positive=True)
EL_root = euler_equations(gdet * (-2 * L0 + L_M(al0)), [phF], [t_, xx_])
m2, m2_w = num_zero(el_phi_on - EL_root[0].lhs.subs(al0, alpha_of(L0)), {L0: 100, kap_s: sp.Rational(1, 2), lamI: sp.Rational(7, 10)})
# Lambda's own equation: sqrt(-g)(-2 + dL_M/dLambda) + 2 d_m T^m = 0, with dL_M/dLambda = (kappa^2/4 pi) F
sx = sp.Symbol('s_x', positive=True)
LM_s = -2 * alpha_of(Ls) ** 2 * Jc(sx / alpha_of(Ls) ** 2)
dLM_dL = sp.diff(LM_s, Ls)
F_s = (sx / alpha_of(Ls) ** 2) * sp.diff(Jc(s_), s_).subs(s_, sx / alpha_of(Ls) ** 2) - Jc(sx / alpha_of(Ls) ** 2)
m3_e = dLM_dL - kap_s ** 2 / (4 * sp.pi) * F_s
m3 = sp.simplify(m3_e) == 0 or max(abs(complex(sp.N(m3_e.subs({Ls: Lv, sx: sv, kap_s: 0.5}), 30)))
                                   for Lv, sv in ((1.3, 0.001), (0.7, 0.001), (2.0, 0.003))) < 1e-13
el_L = sp.expand(EL[0].lhs)
m4 = sp.simplify(el_L.coeff(sp.diff(T0F, t_)) - 2) == 0 and sp.simplify(el_L.coeff(sp.diff(T1F, xx_)) - 2) == 0
check("T1a HT VARIED: the multiplier's equations are -2 d_t Lambda = -2 d_x Lambda = 0 (Lambda uniform in space AND "
      "time, exactly); phi's equation on shell is the root's at alpha(Lambda_0); Lambda's own equation contains "
      "2 d_m T^m and the MOND term's dL/dLambda = (kappa^2/4 pi) F",
      f"EL(T0) = {el_T0}, EL(T1) = {el_T1}: {m1}; phi on shell = root at alpha(Lambda_0): {m2}; dL_M/dLambda = "
      f"(kappa^2/4pi) F: {m3}; d_m T^m in Lambda's equation: {m4}", m1 and m2 and m3 and m4,
      "d Lambda = 0 is a field equation, not an assumption: a0 = alpha(Lambda) c^2 is constant on every solution")
# T1b the clock and FP5 D3's obstruction
sigF = sp.Function('sigma', positive=True)(t_, xx_)
EL_sig = euler_equations(gdet * (-2 * L0 + L_M(sigF)), [sigF, phF], [t_, xx_])
sig_s = sp.Symbol('sigma_s', positive=True)
F_sig = (sx / sig_s ** 2) * sp.diff(Jc(s_), s_).subs(s_, sx / sig_s ** 2) - Jc(sx / sig_s ** 2)
m5_e = (EL_sig[0].lhs.subs(sigF, sig_s).subs(phx, sp.sqrt(sx)).doit() - gdet * 4 * sig_s * F_sig).subs(gdet, sp.Rational(11, 10))
m5 = max(abs(complex(sp.N(m5_e.subs({sig_s: sv_, sx: xv_}), 30))) for sv_, xv_ in ((0.3, 0.01), (0.2, 0.005), (0.5, 0.05))) < 1e-12
clock = {f: {y: EPS[f] * F_p2(y) for y in (1e-3, 0.01, 0.1, 1.0, 10.0, 100.0)} for f in A0}
P("    the unimodular clock d_m T^m = sqrt(-g)[1 - (kappa^2/8pi) F(y)]: rate shift (kappa^2/8pi) F at y = 1e-3, 0.01, 0.1, 1, 10, 100:")
for f in A0:
    P(f"      {f:9s} " + ", ".join(f"{v:.2e}" for v in clock[f].values()))
check("T1b THE CLOCK: d_m T^m = sqrt(-g) [1 - (kappa^2/8 pi) F]: the MOND sector's dL/dLambda goes only there.  FP5 D3's "
      "obstruction, re-derived for the root: a FREE alpha-field sigma obeys sqrt(-g) 4 sigma F = 0, i.e. F = 0 (no MOND, "
      "since F > 0 for every y > 0); in T1 the same term is absorbed by the multiplier's divergence",
      f"free-field equation = sqrt(-g) 4 sigma F: {m5}; clock shift at the RAR knee (y = 1): {clock['canonical'][1.0]:.2e} / "
      f"{clock['alt'][1.0]:.2e} (can/alt), at y = 100: {clock['canonical'][100.0]:.2e} / {clock['alt'][100.0]:.2e}",
      m5 and m3, "T^m appears nowhere else, so the clock is unobservable; only its global charge (the total 4-volume, "
                 "conjugate to Lambda_0) is physical")
OUT["numbers"]["T1_clock"] = {f: {str(k): v for k, v in c_.items()} for f, c_ in clock.items()}
# T1c the Dirac count on a periodic lattice (generic first-order pair (Q_j, P_j), constraints P_{j+1} - P_j)
NL = 5
Qs = sp.symbols(f"Q_0:{NL}"); Ps = sp.symbols(f"P_0:{NL}"); phs = sp.symbols(f"phi_0:{NL}"); pis = sp.symbols(f"pi_0:{NL}")
hl = sp.Symbol('h', positive=True)
Jl = sp.Function('J')


def PB(A_, B_):
    return sp.expand(sum(sp.diff(A_, Qs[j]) * sp.diff(B_, Ps[j]) - sp.diff(A_, Ps[j]) * sp.diff(B_, Qs[j])
                         + sp.diff(A_, phs[j]) * sp.diff(B_, pis[j]) - sp.diff(A_, pis[j]) * sp.diff(B_, phs[j])
                         for j in range(NL)))


Cn = [(Ps[(j + 1) % NL] - Ps[j]) / 2 for j in range(NL)]                  # HT: P_j = 2 Lambda_j is T0_j's momentum
alph_l = lambda Pj: kap_s * sp.sqrt(Pj / 2 / (8 * sp.pi))
H_l = sum(pis[j] ** 2 / (8 * lamI) + 2 * alph_l(Ps[j]) ** 2 * Jl(((phs[(j + 1) % NL] - phs[j]) / hl) ** 2 / alph_l(Ps[j]) ** 2)
          + Ps[j] for j in range(NL))
CCm = sp.Matrix(NL, NL, lambda i, j: PB(Cn[i], Cn[j]))
CHv = [sp.simplify(PB(Cn[i], H_l)) for i in range(NL)]
Jac = sp.Matrix([[sp.diff(C_, v_) for v_ in list(Qs) + list(Ps)] for C_ in Cn])
rk = Jac.rank()
dims = 2 * NL - 2 * rk
xi_ = sp.symbols(f"xi_0:{NL}")
gauge = [sp.simplify(PB(Qs[k], sum(xi_[j] * Cn[j] for j in range(NL)))) for k in range(NL)]
m6 = CCm == sp.zeros(NL, NL) and all(v == 0 for v in CHv) and rk == NL - 1 and dims == 2
check("T1c THE DIRAC COUNT (periodic lattice, N = 5; the same algebra holds for T2's (A, Pi) pair): {C_i, C_j} = 0 (first "
      "class), {C_i, H} = 0 with the MOND coupling alpha(Lambda) in H (no secondary constraint), rank N - 1, so the "
      "(T0, Lambda) sector keeps 2N - 2(N - 1) = 2 phase-space dimensions: ONE global degree of freedom, no local mode",
      f"brackets zero {CCm == sp.zeros(NL, NL)}; {{C, H}} = {CHv}; rank {rk}; physical dims {dims}; gauge shift of T0_k: "
      f"{gauge[1]}", m6, "the root's count (FP7 E1: 2 tensor + khronon + MOND scalar = 4) is unchanged; the global pair is "
                         "(Lambda_0, the total 4-volume)")
# T1d FRW and PPN
gsym = sp.Symbol('g_s', positive=True)
L_HT_g = gsym * (-2 * Ls + LM_s) + 2 * Ls * sp.Symbol('divT')
L_root_g = gsym * (-2 * Ls + LM_s)
m7 = sp.simplify(sp.diff(L_HT_g, gsym) - sp.diff(L_root_g, gsym)) == 0 and not sp.Symbol('divT') in sp.diff(L_HT_g, gsym).free_symbols
check("T1d FRW AND PPN: the HT term 2 Lambda d_m T^m contains no metric (T^m is a density), so the metric's equations are "
      "the root's at Lambda = Lambda_0, alpha = alpha(Lambda_0): FP7 B1 (the FRW background is GR + Lambda, a0 absent) and "
      "D2 (gamma = 1, alpha_3 = 0, the khronometric alpha_1, alpha_2) carry over exactly",
      f"d/dg of the HT Lagrangian = d/dg of the root's: {m7}", m7)
# T1e the vacuum-energy caveat (reported)
vac = {r_: 0.5 * math.log10(1 - r_) for r_ in (1e-3, 1e-2, 0.1, 0.5)}
P("    with a matter vacuum energy rho_vac: Lambda_obs = Lambda_HT + 8 pi G rho_vac/c^2 while alpha reads Lambda_HT;")
P("    Delta log a0 at rho_vac/rho_Lambda,obs = 1e-3, 1e-2, 0.1, 0.5: " + ", ".join(f"{v:+.4f}" for v in vac.values()) + " dex")
check("T1e (reported) THE VACUUM-ENERGY CAVEAT: the tie is to the HT integration constant; a vacuum energy of the matter "
      "sector adds to the observed Lambda but not to a0, so a0 = kappa c sqrt(G rho_Lambda,obs) needs |rho_vac| << "
      "rho_Lambda (the cosmological-constant problem, now shared by a0; unchanged from P1 as declared)",
      f"Delta log a0 = {vac[0.1]:+.4f} dex at rho_vac = 0.1 rho_Lambda", True, load_bearing=False)
OUT["numbers"]["T1_vacuum"] = vac

# ================================================================================================ T2 four-form (BT)
banner("T2  BROWN-TEITELBOIM: a four-form F = dA, (Z_q/2) q^2, alpha = beta |q| (Z_q: the four-form's stiffness, not Z)")
A0F, A1F = sp.Function('A0')(t_, xx_), sp.Function('A1')(t_, xx_)
Zq, bet = sp.symbols('Z_q beta', positive=True)
qF = sp.diff(A1F, t_) - sp.diff(A0F, xx_)                                    # the top form's dual in 1+1
L_BT = Zq / 2 * qF ** 2 + L_M(bet * qF)
EL2 = euler_equations(L_BT, [A0F, A1F, phF], [t_, xx_])
qs_, Pi0 = sp.symbols('q Pi_0', positive=True)
Lq_expr = sp.diff(Zq / 2 * qs_ ** 2 - 2 * (bet * qs_) ** 2 * Jc(sx / (bet * qs_) ** 2), qs_)
F_q = (sx / (bet * qs_) ** 2) * sp.diff(Jc(s_), s_).subs(s_, sx / (bet * qs_) ** 2) - Jc(sx / (bet * qs_) ** 2)
n1 = sp.simplify(Lq_expr - (Zq * qs_ + 4 * bet ** 2 * qs_ * F_q)) == 0
# EL(A0) = -d_x(dL/dA0_x), EL(A1) = -d_t(dL/dA1_t), and dL/dA0_x = -dL/dA1_t = -L_q: one conserved quantity, L_q
dL_dA0x = sp.diff(L_BT, sp.diff(A0F, xx_))
dL_dA1t = sp.diff(L_BT, sp.diff(A1F, t_))
_fx, _ov = {Zq: 1, bet: 1, lamI: sp.Rational(7, 10)}, {sp.diff(A1F, t_): 2}          # q = A1_t - A0_x ~ 1.7-1.95
n2a, _w1 = num_zero(dL_dA0x + dL_dA1t, _fx, _ov)
n2b1, _w2 = num_zero(EL2[0].lhs + sp.diff(dL_dA0x, xx_), _fx, _ov)
n2b2, _w3 = num_zero(EL2[1].lhs + sp.diff(dL_dA1t, t_), _fx, _ov)
Lq_check = dL_dA1t.subs(sp.diff(A1F, t_), qs_ + sp.diff(A0F, xx_)).subs(phx, sp.sqrt(sx))
n2c_e = Lq_check - (Zq * qs_ + 4 * bet ** 2 * qs_ * F_q)
n2c = max(abs(complex(sp.N(n2c_e.subs({Zq: 1, bet: 0.1, qs_: qv, sx: xv}), 30))) for qv, xv in ((1.0, 1e-3), (0.8, 1e-3), (1.3, 2e-3))) < 1e-12
n2 = n2a and n2b1 and n2b2 and n2c
# minisuperspace: the four-form's gravitating energy is the Legendre form q P' - P
tq, Nq_, aq = sp.symbols('t N a', positive=True)
Adot = sp.Symbol('Adot'); Pf = sp.Function('P')
LN = Nq_ * aq ** 3 * Pf(Adot / (Nq_ * aq ** 3))
dLdN = sp.simplify(sp.diff(LN, Nq_).subs(Adot, sp.Symbol('q_') * Nq_ * aq ** 3).doit())
qq = sp.Symbol('q_')
n3 = sp.simplify(dLdN - aq ** 3 * (Pf(qq) - qq * sp.Subs(sp.Derivative(Pf(zeta), zeta), zeta, qq)).doit()) == 0
Lam_eff = sp.simplify((qs_ * sp.diff(Zq / 2 * qs_ ** 2, qs_) - Zq / 2 * qs_ ** 2) / 2)
eps_sym = sp.simplify((bet * qs_) ** 2 / Lam_eff)
Fsym = sp.Symbol('F', positive=True)
rsol = sp.solve(sp.Eq(Zq * qs_ + 4 * bet ** 2 * qs_ * Fsym, Zq * sp.Symbol('q_0', positive=True)), qs_)[0] / sp.Symbol('q_0', positive=True)
n4 = sp.simplify(Lam_eff - Zq * qs_ ** 2 / 4) == 0 and sp.simplify(eps_sym - 4 * bet ** 2 / Zq) == 0 and \
    sp.simplify(rsol - 1 / (1 + (4 * bet ** 2 / Zq) * Fsym)) == 0
check("T2a BT VARIED: the 3-form's equations are d_x(L_q) = d_t(L_q) = 0, so the CONJUGATE Pi = L_q = Z_q q + 4 beta^2 q F "
      "is constant, not q; the four-form gravitates through the Legendre form q P' - P, Lambda_eff = Z_q q^2/4; the flux "
      "amplitude cancels, alpha_0^2/Lambda_0 = 4 beta^2/Z_q = kappa^2/8 pi (one coupling, beta^2/Z_q = kappa^2/32 pi); "
      "locally a0_loc/a0 = q/q_0 = 1/(1 + (kappa^2/8 pi) F(y_loc))",
      f"L_q form {n1}; EL(A0), EL(A1) total derivatives of L_q {n2}; Legendre energy {n3}; Lambda_eff = {Lam_eff}, "
      f"alpha^2/Lambda = {eps_sym}, q/q_0 = {rsol}: {n4}", n1 and n2 and n3 and n4,
      "the root's alpha-derivative (A) is the four-form's source: where the MOND sector is active, q (and a0) drop")
OUT["numbers"]["T2a"] = dict(Zq_over_beta2_for_kappa_half=float(128 * math.pi))
# T2b local a0 and the RAR shift
F_scalar = F_p2
rows_b = {}
for f in A0:
    rr = []
    for y in (0.01, 0.1, 1.0, YE[f], 10.0, 30.0, 100.0):
        r = bt_family(y, EPS[f], F_scalar)
        u = r * x_p2(y / r) if r > 0 else 0.0
        rr.append((y, r, u, math.log10((y + u) / (y + x_p2(y)))))
    rows_b[f] = rr
    P(f"    {f:9s} y, a0_loc/a0, scalar force/a0 (P2: x(y)), Delta log g_obs [dex]:")
    for y, r, u, dl in rr:
        P(f"        y = {y:8.4f}: a0_loc/a0 = {r:.5f}, u = {u:.5f} (P2 {x_p2(y):.5f}), {dl:+.5f} dex")
knee = {f: rows_b[f][2][1] for f in A0}
check("T2b (reported) THE LOCAL a0 in the root's spherical law (both footings): a0 is lowest where the MOND sector's "
      "alpha-conjugate density F is largest; at the RAR knee (y = 1) and the Sun's Galactic field",
      f"a0_loc/a0 at y = 1: {knee['canonical']:.5f} / {knee['alt']:.5f} (can/alt); at the Sun's y_e = "
      f"{YE['canonical']:.3f}: {rows_b['canonical'][3][1]:.5f}; at y = 100: {rows_b['canonical'][6][1]:.4f} / "
      f"{rows_b['alt'][6][1]:.4f}", True, load_bearing=False)
OUT["numbers"]["T2b"] = {f: [dict(y=y, a0_ratio=r, u=u, dlog_gobs=dl) for y, r, u, dl in v] for f, v in rows_b.items()}
# the four-form's effective law as an interpolant (for SPARC), exact solves at test points
YOFF = {f: 2.0 / EPS[f] for f in A0}


def build_bt_interp(eps, Ffun, yoff):
    yg = np.logspace(-6, math.log10(yoff * (1 - 1e-7)), 8000)
    ru = np.array([bt_family(y, eps, Ffun) for y in yg])
    ratio = np.array([(r * x_p2(y / r)) / x_p2(y) if r > 0 else 0.0 for y, r in zip(yg, ru)])
    lg = np.log10(yg)
    spl = CubicSpline(lg, ratio)

    def nu_bt(y):
        y = np.maximum(np.asarray(y, float), 1e-300)
        ly = np.log10(y)
        rat = np.where(ly < lg[0], 1.0, np.where(y >= yoff, 0.0, spl(np.clip(ly, lg[0], lg[-1]))))
        xv = y / (np.sqrt(y * y + y) + y)
        return 1.0 + rat * xv / y
    return nu_bt, yg, ru


NU_BT, BT_GRID = {}, {}
for f in A0:
    NU_BT[f], yg_, ru_ = build_bt_interp(EPS[f], F_scalar, YOFF[f])
    BT_GRID[f] = (yg_, ru_)
interp_err = 0.0
for yt in (0.0137, 0.52, 3.3, 17.0, 88.0):
    r = bt_family(yt, EPS["canonical"], F_scalar)
    exact = 1 + r * x_p2(yt / r) / yt
    interp_err = max(interp_err, abs(float(NU_BT["canonical"](yt)) / exact - 1))
# T2c SPARC
sp_rows = {}
for f in A0:
    Sp, Wp = gal_sums(nu_p2, A0[f]); Sb, Wb = gal_sums(NU_BT[f], A0[f])
    msep = Sp.sum(0) / Wp.sum(0); mseb = Sb.sum(0) / Wb.sum(0)
    ip, ib = int(np.argmin(msep)), int(np.argmin(mseb))
    shifts, band_frac = [], {}
    for U in (0.5, 0.7, 0.9):
        yy = []
        for (R, Vobs, eV, Vgas, Vdisk, Vbul) in GAL:
            gb = (np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2) * 1e6 / (R * kpc)
            ok = (gb > 0) & np.isfinite(gb) & (Vobs > 0)
            yy += list(gb[ok] / A0[f])
        yy = np.array(yy)
        if U == 0.7:
            shifts = np.abs(np.log10(NU_BT[f](yy) / nu_p2(yy)))
        band_frac[U] = None
        sp_rows.setdefault(f, {})[f"y_{U}"] = yy
    sp_rows[f].update(rms70_p2=math.sqrt(msep[iu70]), rms70_bt=math.sqrt(mseb[iu70]), best_p2=(math.sqrt(msep[ip]), float(UPS[ip])),
                      best_bt=(math.sqrt(mseb[ib]), float(UPS[ib])), max_shift=float(np.max(shifts)),
                      med_shift=float(np.median(shifts)))
    P(f"    {f:9s} RAR rms at Upsilon = 0.70: P2 {sp_rows[f]['rms70_p2']:.5f}, four-form {sp_rows[f]['rms70_bt']:.5f} dex; best "
      f"Upsilon: P2 {sp_rows[f]['best_p2'][0]:.5f} ({sp_rows[f]['best_p2'][1]:.2f}), four-form {sp_rows[f]['best_bt'][0]:.5f} "
      f"({sp_rows[f]['best_bt'][1]:.2f}); per-point |shift| max {sp_rows[f]['max_shift']:.5f}, median {sp_rows[f]['med_shift']:.2e} dex")
t2c_ok = all(sp_rows[f]["max_shift"] < 0.01 and abs(sp_rows[f]["rms70_bt"] - sp_rows[f]["rms70_p2"]) < 1e-3 for f in A0) and interp_err < 1e-5
check("T2c = H2a SPARC: with the four-form's local a0 the RAR moves by < 0.01 dex at every SPARC point and the C0 statistic "
      "by < 0.001 dex, both footings (vs the median per-point error 0.037 dex and the RAR scatter 0.108 dex)",
      f"max per-point shift {sp_rows['canonical']['max_shift']:.4f} / {sp_rows['alt']['max_shift']:.4f} dex; rms change "
      f"{sp_rows['canonical']['rms70_bt'] - sp_rows['canonical']['rms70_p2']:+.5f} / "
      f"{sp_rows['alt']['rms70_bt'] - sp_rows['alt']['rms70_p2']:+.5f} dex (can/alt); interpolant vs exact {interp_err:.1e}",
      t2c_ok, "invisible in the RAR -- as k04 found for its kernel; the question is the health of the slaved kernel (T2d)")
OUT["numbers"]["T2c"] = {f: {k: v for k, v in d_.items() if not k.startswith("y_")} for f, d_ in sp_rows.items()}


# T2d the fold
def fold_analytic(eps):
    g_ = lambda Y: 1.0 + eps * (F_p2(Y) - x_p2(Y) ** 3 / om_p2(Y) ** 2)
    Yf = brentq(g_, 1.0, 1e8, xtol=1e-14, rtol=1e-15)
    rf = 1.0 / (1.0 + eps * F_p2(Yf))
    return Yf * rf, Yf, rf


def Lqq_fd(y, eps):
    """route (ii): L(q, Y) = q^2/2 - 2 beta^2 q^2 J_P2(Y/(beta^2 q^2)), Z_q = 1, beta^2 = eps/4, at the family's point;
    the second q-derivative at fixed Y by 40-digit central differences of the action's own J_P2."""
    mp.mp.dps = 40
    r = bt_family(y, eps, F_p2)
    b2 = mp.mpf(eps) / 4
    Yg = (mp.sqrt(b2) * r * mp.mpf(x_p2(y / r))) ** 2
    Lf = lambda q: q ** 2 / 2 - 2 * b2 * q ** 2 * J_P2(Yg / (b2 * q ** 2))
    h = mp.mpf(r) * mp.mpf("1e-12")
    q0 = mp.mpf(r)
    return float((Lf(q0 + h) - 2 * Lf(q0) + Lf(q0 - h)) / h ** 2)


FOLD = {}
for f in A0:
    yf_i, Yf_i, rf_i = fold_analytic(EPS[f])
    ygrid = np.logspace(0, math.log10(YOFF[f] * 0.9), 40)
    sg_ = [Lqq_fd(y, EPS[f]) for y in ygrid]
    k_ = next(i for i in range(len(sg_) - 1) if sg_[i] > 0 >= sg_[i + 1])
    yf_ii = brentq(lambda y: Lqq_fd(y, EPS[f]), ygrid[k_], ygrid[k_ + 1], xtol=1e-12, rtol=1e-13)
    # route (iii): C_L,eff = dy/du along the family, sampled below and on the band
    u_of = lambda y: (lambda r: r * x_p2(y / r) if r > 0 else 0.0)(bt_family(y, EPS[f], F_p2))
    below = np.logspace(-2, math.log10(0.97 * yf_i), 40)
    band = np.logspace(math.log10(1.03 * yf_i), math.log10(0.97 * YOFF[f]), 60)
    dudy = lambda y: (u_of(y * (1 + 1e-6)) - u_of(y * (1 - 1e-6))) / (2e-6 * y)
    dl_below, dl_band = [dudy(y) for y in below], [dudy(y) for y in band]
    r_edge = bt_family(0.999 * YOFF[f], EPS[f], F_p2)
    FOLD[f] = dict(y_fold=yf_i, Y_fold=Yf_i, r_fold=rf_i, u_fold=rf_i * x_p2(Yf_i), y_fold_fd=yf_ii, y_off=YOFF[f],
                   dudy_below_min=float(min(dl_below)), dudy_band_max=float(max(dl_band)), r_at_0p999_off=r_edge,
                   CL_eff_band_max=float(max(1 / v for v in dl_band)), u_at={str(y): u_of(y) for y in (20.0, 50.0, 100.0)})
    P(f"    {f:9s} fold (i) du/dy = 0: y = {yf_i:.8f} (y_loc = {Yf_i:.6f}, a0_loc/a0 = {rf_i:.6f}, u_max = {FOLD[f]['u_fold']:.5f}); "
      f"(ii) L_qq|_Y = 0 by 40-digit differences: y = {yf_ii:.8f}; switch-off y_off = 2/eps = 16 pi/kappa^2 = {YOFF[f]:.3f} "
      f"(a0_loc/a0 at 0.999 y_off = {r_edge:.2e}); du/dy min below the fold {FOLD[f]['dudy_below_min']:.3e}, max on the band "
      f"{FOLD[f]['dudy_band_max']:.3e}; u at y = 20, 50, 100: " + ", ".join(f"{v:.4f}" for v in FOLD[f]["u_at"].values()))
t2d_ok = all(abs(FOLD[f]["y_fold_fd"] / FOLD[f]["y_fold"] - 1) < 1e-6 and FOLD[f]["dudy_below_min"] > 0 and FOLD[f]["dudy_band_max"] < 0
             and FOLD[f]["r_at_0p999_off"] < 0.01 for f in A0)
check("T2d THE FOLD, located two independent ways: the four-form's Legendre map q -> Pi at fixed Y (L_qq|_Y, 40-digit "
      "differences of J_P2 itself) degenerates exactly where the slaved scalar force u(y) = (a0_loc/a0) x(y_loc) peaks; "
      "below it C_L,eff = dy/du > 0, on the whole band from the fold to the switch-off y_off = 16 pi/kappa^2 C_L,eff < 0",
      f"y_fold = {FOLD['canonical']['y_fold']:.4f} / {FOLD['alt']['y_fold']:.4f} (can/alt), routes agree to "
      f"{max(abs(FOLD[f]['y_fold_fd'] / FOLD[f]['y_fold'] - 1) for f in A0):.1e}; y_off = {YOFF['canonical']:.2f} / "
      f"{YOFF['alt']:.2f}; du/dy > 0 below: {all(FOLD[f]['dudy_below_min'] > 0 for f in A0)}; du/dy < 0 on the band: "
      f"{all(FOLD[f]['dudy_band_max'] < 0 for f in A0)}", t2d_ok,
      "past the fold the scalar's force DEcreases as g_N grows: the non-monotone kernel the record built nu_mono to exclude "
      "(FP7 C1: healthy iff C_phi > 0 in each channel) -- a gradient instability with growth ~ k (Hadamard), as FP5 G-2f")
OUT["numbers"]["T2d"] = FOLD
# T2d2 the consequence in FP7's own reduced quadratic form (T, V of FP7 C1, read from its committed output)
mT = re.search(r"system after the lapse and shift constraints: T = (\[\[.*?\]\])", fp7_out)
mV = re.search(r"\n\s*V = (\[\[.*?\]\]);", fp7_out)
Tm = sp.Matrix(sp.sympify(mT.group(1).replace("lambda", "lam_"))) if mT else None
Vm = sp.Matrix(sp.sympify(mV.group(1).replace("lambda", "lam_"))) if mV else None
w2s, Cph = sp.symbols("w2 C_phi")
ins = {}
if Tm is not None and Vm is not None:
    Vm = Vm.subs(sp.Symbol("C_phi"), Cph)
    for f in A0:
        yb = 20.0
        u_of = lambda y: (lambda r: r * x_p2(y / r) if r > 0 else 0.0)(bt_family(y, EPS[f], F_p2))
        C_eff = 1.0 / ((u_of(yb * (1 + 1e-6)) - u_of(yb * (1 - 1e-6))) / (2e-6 * yb))       # C_L,eff = dy/du (slaved q)
        x0 = x_p2(yb); C_fix = 2 * x0 * (1 - x0) / (1 - 2 * x0) ** 2                        # FP7's C_L = (x mu_s)' (fixed alpha)
        vals = {sp.Symbol("alpha_c"): sp.Float(3.2e-9), sp.Symbol("c_2"): sp.Float(7.2888e-3), sp.Symbol("lam_"): 1,
                sp.Symbol("sigma"): 1, sp.Symbol("k"): 1}
        roots = {}
        for lab, Cv in (("slaved", C_eff), ("fixed alpha", C_fix)):
            poly = sp.Poly(sp.expand((Vm - w2s * Tm).subs(vals).subs(Cph, sp.Float(Cv)).det()), w2s)
            roots[lab] = sorted(float(sp.re(r_)) for r_ in poly.nroots(n=30))
        grow = math.sqrt(-min(roots["slaved"])) if min(roots["slaved"]) < 0 else 0.0
        # the same at FP7's sigma_8 edge of the scalar's inertia (lambda_eff >= 1.07e7, FP7 T): the rate scales as k/sqrt(lambda)
        poly7 = sp.Poly(sp.expand((Vm - w2s * Tm).subs({**vals, sp.Symbol("lam_"): sp.Float(1.07e7)}).subs(Cph, sp.Float(C_eff)).det()), w2s)
        r7 = sorted(float(sp.re(r_)) for r_ in poly7.nroots(n=30))
        grow7 = math.sqrt(-min(r7)) if min(r7) < 0 else 0.0
        ins[f] = dict(y=yb, C_eff=C_eff, C_fixed=C_fix, w2_over_k2_slaved=roots["slaved"], w2_over_k2_fixed=roots["fixed alpha"],
                      growth_over_kc=grow, efold_yr_at_kpc=(3.0857e19 / (grow * c_SI) / 3.15576e7) if grow > 0 else None,
                      growth_over_kc_lambda_1e7=grow7, efold_yr_at_kpc_lambda_1e7=(3.0857e19 / (grow7 * c_SI) / 3.15576e7) if grow7 > 0 else None)
        P(f"    {f:9s} y = {yb:g}: C_L,eff (slaved q) = {C_eff:.4g} vs FP7's C_L at fixed alpha {C_fix:.4g}; omega^2/(c k)^2 roots: "
          f"slaved {', '.join(f'{v:.4g}' for v in roots['slaved'])}; fixed {', '.join(f'{v:.4g}' for v in roots['fixed alpha'])}; "
          f"growth rate {grow:.3g} c k at lambda = 1 (e-fold {ins[f]['efold_yr_at_kpc']:.3g} yr at k = 1/kpc), {grow7:.3g} c k at "
          f"lambda = 1.07e7 (e-fold {ins[f]['efold_yr_at_kpc_lambda_1e7']:.3g} yr at k = 1/kpc); both grow ~ k")
t2d2 = bool(ins) and all(min(v["w2_over_k2_slaved"]) < 0 and min(v["w2_over_k2_fixed"]) > 0 and v["growth_over_kc_lambda_1e7"] > 0
                         for v in ins.values())
check("T2d2 THE FOLD'S CONSEQUENCE IN FP7'S OWN QUADRATIC FORM (T and V of FP7 C1, read from its committed output; alpha_c = "
      "3.2e-9, c_2 = 7.29e-3, lambda = 1, unfiltered sigma = 1): on the band (y = 20) the slaved coefficient makes one "
      "omega^2 negative, proportional to k^2 (growth ~ k: Hadamard); CONTROL: at fixed alpha (the root) both roots are positive",
      "; ".join(f"{f}: slaved min omega^2/(ck)^2 {min(v['w2_over_k2_slaved']):.3g}, fixed min {min(v['w2_over_k2_fixed']):.3g}"
                for f, v in ins.items()) if ins else "FP7's T, V not found", t2d2,
      "the four-form's feedback turns the root's healthy MOND scalar into a gradient-unstable one wherever the band reaches")
OUT["numbers"]["T2d2"] = ins
# T2d3 the same on FP14's zero-knob root (lambda = 0; c_2 finite and c_2 -> oo): FP14 L2's own one-mode formulas, read
# from its committed output, cross-checked against FP7's T, V at lambda = 0
fp14_out = rd("real_research/derivation_chain_2026/FP14_zero_knob_core.out") or ""
w14 = {}
if "omega^2 = " in fp14_out and " (c_2 -> oo)" in fp14_out and ins:
    seg = fp14_out[fp14_out.index("omega^2 = ", fp14_out.index("lambda = 0: phi auxiliary")) + len("omega^2 = "):]
    e_c2, rest = seg.split(" (c_2), ", 1)
    e_inf = rest.split(" (c_2 -> oo)", 1)[0]
    W14 = {"c_2": sp.sympify(e_c2), "c_2 -> oo": sp.sympify(e_inf)}
    xchk = None
    if Tm is not None:
        vals0 = {sp.Symbol("alpha_c"): sp.Float(3.2e-9), sp.Symbol("c_2"): sp.Float(7.2888e-3), sp.Symbol("lam_"): 0,
                 sp.Symbol("sigma"): 1, sp.Symbol("k"): 1}
        poly0 = sp.Poly(sp.expand((Vm - w2s * Tm).subs(vals0).subs(Cph, sp.Float(ins["canonical"]["C_eff"])).det()), w2s)
        xchk = [float(sp.re(r_)) for r_ in poly0.nroots(n=30)]
    for f in A0:
        for lab, e_ in W14.items():
            base = {sp.Symbol("alpha_c"): sp.Float(3.2e-9), sp.Symbol("c_2"): sp.Float(7.2888e-3), sp.Symbol("sigma"): 1, sp.Symbol("k"): 1}
            w14[(f, lab)] = dict(slaved=float(e_.subs(base).subs(sp.Symbol("C_phi"), sp.Float(ins[f]["C_eff"]))),
                                 fixed=float(e_.subs(base).subs(sp.Symbol("C_phi"), sp.Float(ins[f]["C_fixed"]))))
    P(f"    FP14's lambda = 0 root, omega^2/(c k)^2 at y = 20 (slaved / fixed alpha): " + "; ".join(
        f"{f} {lab}: {v['slaved']:.4g} / {v['fixed']:.4g}" for (f, lab), v in w14.items())
      + (f"; FP7's T, V at lambda = 0 give {xchk[0]:.6g} (canonical, finite c_2)" if xchk else ""))
t2d3 = bool(w14) and all(v["slaved"] < 0 < v["fixed"] for v in w14.values()) and \
    (xchk is not None and abs(xchk[0] / w14[("canonical", "c_2")]["slaved"] - 1) < 1e-9)
check("T2d3 ON FP14'S ZERO-KNOB ROOT (lambda = 0, c_2 finite and c_2 -> oo; FP14 L2's one-mode formulas read from its committed "
      "output, cross-checked against FP7's T, V at lambda = 0): the slaved coefficient makes the one remaining scalar's omega^2 "
      "negative (growth ~ k); CONTROL: at fixed alpha it is positive -- the four-form's failure does not depend on the MOND "
      "scalar's inertia or on c_2",
      "; ".join(f"{f} {lab}: {v['slaved']:.3g} (fixed {v['fixed']:.3g})" for (f, lab), v in w14.items()) if w14 else
      "FP14's formulas not found", t2d3)
OUT["numbers"]["T2d3"] = {f"{k_[0]}|{k_[1]}": v for k_, v in w14.items()}
# T2e where the band sits (reported; = H2b as it falls)
wh = {}
for f in A0:
    yf, yo = FOLD[f]["y_fold"], YOFF[f]
    fr = {U: float(np.mean((sp_rows[f][f'y_{U}'] > yf) & (sp_rows[f][f'y_{U}'] < yo))) for U in (0.5, 0.7, 0.9)}
    r_fold_AU = math.sqrt(GM_SUN / (yf * A0[f])) / AU
    r_off_AU = math.sqrt(GM_SUN / (yo * A0[f])) / AU
    wb = []
    for kau in (2, 3, 5, 10, 20):
        yi = 1.5 * GM_SUN / (kau * 1e3 * AU) ** 2 / A0[f]
        for lab, yv in (("internal", yi), ("with Galaxy", math.hypot(yi, YE[f]))):
            r = bt_family(yv, EPS[f], F_p2)
            wb.append(dict(kAU=kau, case=lab, y=yv, a0_ratio=r, in_band=bool(yf < yv < yo)))
    wh[f] = dict(sparc_frac=fr, r_fold_AU=r_fold_AU, r_off_AU=r_off_AU, wb=wb)
    P(f"    {f:9s} SPARC points in the band (y_fold, y_off) at Upsilon = 0.5/0.7/0.9: " + "/".join(f"{v:.3f}" for v in fr.values())
      + f"; a 1-Msun star: MOND off inside {r_off_AU:.0f} AU, unstable shell {r_off_AU:.0f}-{r_fold_AU:.0f} AU")
    P("              wide binary (1.5 Msun): " + "; ".join(f"{w['kAU']} kAU {w['case']}: y = {w['y']:.2f}, a0_loc/a0 = {w['a0_ratio']:.3f}"
                                                        f"{' [band]' if w['in_band'] else ''}" for w in wb))
check("T2e = H2b (pre-declared EXPECT FALSE, reported as it falls): the slaved kernel stays monotone up to the switch-off -- "
      "it does NOT: the band y_fold < y < y_off holds a fraction of SPARC's inner points, a shell around every solar-mass "
      "star, and wide binaries at 2-3 kAU",
      f"SPARC fraction in band (Upsilon 0.7): {wh['canonical']['sparc_frac'][0.7]:.3f} / {wh['alt']['sparc_frac'][0.7]:.3f}; "
      f"1-Msun shell {wh['canonical']['r_off_AU']:.0f}-{wh['canonical']['r_fold_AU']:.0f} AU (canonical)",
      all(FOLD[f]['y_fold'] >= YOFF[f] for f in A0), load_bearing=False)
OUT["numbers"]["T2e"] = {f: {k: (v if k != "sparc_frac" else {str(a): b for a, b in v.items()}) for k, v in d_.items()} for f, d_ in wh.items()}
# T2f the same test on nu_mono (C-H core) and on k04's kernel (reported)
alt_k = {}
for lab, Ffun, hfun in (("nu_mono (C-H core, FP5)", F_mono, h_mono), ("k04's saturated nu_RAR", F_k04, k04_Dl)):
    for f in A0:
        u_of2 = lambda y: (lambda r: r * hfun(y / r) if r > 0 else 0.0)(bt_family(y, EPS[f], Ffun))
        ys_ = np.logspace(-1, math.log10(0.9 * YOFF[f]), 400)
        us_ = np.array([u_of2(y) for y in ys_])
        i_pk = int(np.argmax(us_))
        alt_k[(lab, f)] = dict(y_peak=float(ys_[i_pk]), u_peak=float(us_[i_pk]), u_at_100=u_of2(100.0))
    P(f"    {lab:26s}: the slaved boost u(y) peaks at y = {alt_k[(lab, 'canonical')]['y_peak']:.2f} (canonical) / "
      f"{alt_k[(lab, 'alt')]['y_peak']:.2f} (alt) and falls beyond it (u(100) = {alt_k[(lab, 'canonical')]['u_at_100']:.3f})")
check("T2f (reported) THE SAME FOLD ON THE RECORD'S OTHER KERNELS: the C-H core's nu_mono and k04's saturated nu_RAR also "
      "turn non-monotone under the four-form's feedback (k04 F6's Z_eff > 0 is the flux stiffness at fixed s; it does not "
      "test the slaved kernel's monotonicity) -- a reading note for kappa_closure/k04, not an edit",
      "; ".join(f"{k_[0]} {k_[1]}: peak y = {v['y_peak']:.2f}" for k_, v in alt_k.items()), True, load_bearing=False)
OUT["numbers"]["T2f"] = {f"{k_[0]}|{k_[1]}": v for k_, v in alt_k.items()}
# T2g power-law four-forms (reported)
pw = {}
for n in (1.5, 2.0, 3.0):
    eps = EPS["canonical"]

    def ar_of(y, n=n, eps=eps):
        f_ = lambda a: a ** (2 * (n - 1) / n) * (1 + (n - 1) * eps * F_p2(y / a)) - 1.0
        ag = np.logspace(0, -13, 261)              # the physical branch: the first crossing below a = 1
        prev = f_(ag[0])
        for i in range(1, len(ag)):
            cur = f_(ag[i])
            if cur < 0 <= prev:
                return brentq(f_, ag[i], ag[i - 1], xtol=1e-15)
            prev = cur
        return 0.0
    ys_ = np.logspace(-1, 3, 600)
    us_ = np.array([(lambda a: a * x_p2(y / a) if a > 0 else 0.0)(ar_of(y)) for y in ys_])
    pw[n] = float(ys_[int(np.argmax(us_))])
P("    power-law four-forms P ~ q^n with alpha ~ q^(n/2) (a0 ~ sqrt(rho_Lambda)), canonical: the slaved force peaks at y = "
  + ", ".join(f"{v:.2f} (n = {k})" for k, v in pw.items()))
check("T2g (reported) the fold is not special to the quadratic four-form: every power law P ~ q^n (n = 1.5, 2, 3) folds at "
      "y ~ 5-9; the HT tie (T1) is not a limit of these -- it reads the conserved conjugate, not the field strength",
      f"peaks at y = {', '.join(f'{v:.2f}' for v in pw.values())}", True, load_bearing=False)
OUT["numbers"]["T2g"] = {str(k): v for k, v in pw.items()}
# T2h FRW and DOF
n5 = F_p2(0.0) == 0.0 and Jsym.subs(s_, 0) == 0
check("T2h FRW AND DOF: on the homogeneous background Y = 0, so F = 0 and J = 0: q = q_0, Lambda_eff = Z_q q_0^2/4 is constant, "
      "the background is GR + Lambda and a0(z) is flat; the (A, Pi) pair counts as T1c (one global degree of freedom, no "
      "local mode) wherever the Legendre map is invertible -- it is not at the fold (T2d)",
      f"F(0) = {F_p2(0.0)}, J(0) = {Jsym.subs(s_, 0)}", n5)

# ================================================================================================ T3 khronon K
banner("T3  THE KHRONON'S LEAF CURVATURE: alpha = kappa_K K")
tF = sp.Symbol('t'); aF = sp.Function('a', positive=True)(tF); NF = sp.Function('N', positive=True)(tF)
sqrtg = NF * aF ** 3
K_frw = sp.simplify(sp.diff(sqrtg * (1 / NF), tF) / sqrtg)                   # K = (1/sqrt(-g)) d_t(sqrt(-g) n^t), n^t = 1/N
k1 = sp.simplify(K_frw - 3 * sp.diff(aF, tF) / (aF * NF)) == 0
KAPK = {f: a / (3 * c_SI * H0) for f, a in A0.items()}                     # alpha_0 = kappa_K K_0 / c, K_0 = 3 H0
trackK = {z: E_of(z) for z in (0.5, 1.0, 2.5, 5.0)}
l37 = rd("fable_independent_2026/L37_recombination_footing.out") or ""
l37_dead = re.search(r"^\s*\[FAIL\] S8b\s+VERDICT: does the RIVAL footing", l37, re.M) is not None
check("T3a/T3b THE K TIE IS THE RIVAL LAW: on FRW K = nabla.n = 3 adot/(a N) (sympy), so a0 = kappa_K c K gives "
      "a0(z)/a0(0) = H(z)/H0 = E(z) whatever kappa_K is -- +0.576 dex at z = 2.5 on both footings (FP5 D4), the rho_total "
      "rival that L37 kills at recombination (committed S8b FAIL): this candidate FAILS the flat law",
      f"K_FRW = {K_frw}: {k1}; kappa_K = {KAPK['canonical']:.5f} / {KAPK['alt']:.5f}; a0(z)/a0(0) at z = 0.5, 1, 2.5, 5: "
      + ", ".join(f"{v:.3f}" for v in trackK.values()) + f" (+{math.log10(trackK[2.5]):.3f} dex at 2.5); L37 S8b FAIL found {l37_dead}",
      k1 and abs(math.log10(trackK[2.5]) - 0.576) < 1e-3 and l37_dead)
# T3c local structure (reported)
C2_WIN = {"FP2 tracking floor": 7.2888e-3, "L340 upper window": 0.067}
kl = []
for y in (0.1, 1.0, 10.0):
    x = x_p2(y); Fv = F_p2(y); dlam = 2 * KAPK["canonical"] ** 2 * (x ** 3 / om_p2(y) ** 2 - Fv)
    dK = {k_: 2 * KAPK["canonical"] ** 2 * Fv / v for k_, v in C2_WIN.items()}
    kl.append(dict(y=y, dlambda=dlam, dK_over_K=dK))
    P(f"    y = {y:5.1f}: the MOND term shifts the khronon's lambda by 2 kappa_K^2 (x^3/(1-2x)^2 - F) = {dlam:.3e}; leaf-harmonic "
      f"delta K/K = 2 kappa_K^2 F/c_2 = " + ", ".join(f"{v:.3f} ({k_})" for k_, v in dK.items()))
check("T3c (reported) the K tie is not locally constant either: the MOND term now depends on K, shifting the khronon's "
      "lambda by O(c_2) at the RAR knee and by >> c_2 at y ~ 10, and (following CV4 K1's leaf-harmonic K) sourcing "
      "delta K/K = 2 kappa_K^2 F/c_2 -- a few to ~20 percent at the knee over L340's c_2 window, non-perturbative near stars "
      "(F ~ y/2); the full khronon equation with the tie is not solved here",
      f"at y = 1: delta lambda = {kl[1]['dlambda']:.2e}, delta K/K = {kl[1]['dK_over_K']['L340 upper window']:.3f}-"
      f"{kl[1]['dK_over_K']['FP2 tracking floor']:.3f}", True, load_bearing=False)
OUT["numbers"]["T3"] = dict(kappa_K=KAPK, track=trackK, local=kl)

# ================================================================================================ T4 sequestering
banner("T4  SEQUESTERING (Kaloper-Padilla): global Lambda and lambda; alpha of a global variable")
Lg, lg_, mu_, Vol, IT = sp.symbols('Lambda_s lambda mu Vol I_T', positive=True)
sig = sp.Function('sigma')
Mfun = sp.Function('M')
S_glob = -Lg * Vol + Mfun(lg_) + sig(Lg / (lg_ ** 4 * mu_ ** 4))
eqL = sp.diff(S_glob, Lg)
eqlam = sp.diff(S_glob, lg_).subs(sp.Derivative(Mfun(lg_), lg_), IT / lg_)   # d/dlambda Int sqrt(-g) lambda^4 L = (1/lambda) Int sqrt(-g) T
sig1 = sp.Symbol('sigma1', positive=True)


def _sigma_prime(e):
    for a_ in list(e.atoms(sp.Subs)) + list(e.atoms(sp.Derivative)):
        if a_.has(sig):
            e = e.subs(a_, sig1)
    return e


eqL_s = _sigma_prime(eqL)
eqlam_s = _sigma_prime(eqlam)
sol_sig = sp.solve(eqL_s, sig1)[0]
Lam_s = sp.solve(eqlam_s.subs(sig1, sol_sig), Lg)[0]
s1 = sp.simplify(Lam_s - IT / (4 * Vol)) == 0 and sp.simplify(sol_sig - lg_ ** 4 * mu_ ** 4 * Vol) == 0
# the matter-scaling identity on a scalar field: d/dlambda[lambda^4 L(lambda^-2 g)] = lambda^3 T~
lm, X2, Uv = sp.symbols('lambda_m X U_v', real=True)
Lm_ = lambda ginvfac: -sp.Rational(1, 2) * ginvfac * X2 - Uv            # L_m = -(1/2) g~^{mn} d psi d psi - U, X = g^{mn} dpsi dpsi
lhs_s = sp.diff(lm ** 4 * Lm_(lm ** -2), lm)
Ttil = -lm ** -2 * X2 - 4 * Uv                                              # T~ = g~^{mn} T~_mn = -g~X - 4U
s2 = sp.simplify(lhs_s - lm ** 3 * Ttil) == 0
# vacuum energy: T = -4 V_vac + tau -> Lambda_s = -V_vac + <tau>/4; Einstein: T_mn - Lambda_s g_mn = tau_mn - (<tau>/4) g_mn
Vv, tau_avg = sp.symbols('V_vac tau_avg', real=True)
Lam_s_v = sp.simplify((-4 * Vv + tau_avg) / 4)
resid = sp.simplify(-Vv - Lam_s_v)                                         # coefficient of g_mn: -V_vac (in T) - Lambda_s
s3 = sp.simplify(resid + tau_avg / 4) == 0 and sp.diff(Lam_s_v, Vv) == -1
wv = sp.symbols('w', real=True)
tau_w = -(1 - 3 * wv)                                                      # tau/rho for a fluid of equation of state w
s4 = sp.solve(sp.Gt(tau_w, 0), wv)
check("T4a/T4b SEQUESTERING VARIED: the global equations give Lambda_s = <T>/4 and sigma' = lambda^4 mu^4 Vol (the "
      "lambda-scaling identity d/dlambda[lambda^4 L(lambda^-2 g)] = lambda^3 T~ holds on a scalar field); with T = -4 V_vac "
      "+ tau the Einstein equation keeps only tau_mn - (<tau>/4) g_mn (the vacuum energy cancels) while Lambda_s = -V_vac + "
      "<tau>/4 carries it (dLambda_s/dV_vac = -1); tau = -rho(1 - 3w) > 0 only for w > 1/3",
      f"Lambda_s = {Lam_s}, sigma' = {sol_sig}: {s1}; scaling identity {s2}; residual coefficient {resid} = -<tau>/4 and "
      f"dLambda_s/dV_vac = -1: {s3}; tau > 0 needs {s4}", s1 and s2 and s3,
      "alpha(Lambda_s) is exactly constant (a global number) but reads -V_vac + <tau>/4: it inherits the matter vacuum "
      "energy the construction exists to cancel, and with ordinary matter (w <= 1/3) the residual the Einstein equation "
      "keeps is <= 0 -- the observed positive rho_Lambda must then come from another (dynamical) sector (see part 2)")
k02 = rd("kappa_closure/k02_global_constraint_average.out") or ""
k02_g2 = re.search(r"\[FAIL\] G2 \[today\].*\(largest = ([0-9.e+-]+)\)", k02)
k02_g3 = re.search(r"\[FAIL\] G3 \[future\].*ratio\(10 t0 / t0\) = ([0-9.e+-]+)-([0-9.e+-]+)", k02)
check("T4c (record) k02's committed magnitudes for the one sequestering-type construction on the MOND scalar's OWN "
      "spacetime average: <= 2.3e-5 of rho_Lambda today, and the de Sitter future drives the average to zero",
      f"k02 G2 largest = {k02_g2.group(1) if k02_g2 else 'NOT FOUND'}; G3 ratio(10 t0/t0) = "
      f"{(k02_g3.group(1) + '-' + k02_g3.group(2)) if k02_g3 else 'NOT FOUND'}", k02_g2 is not None and k02_g3 is not None)

# ================================================================================================ HEADLINE-FLAT
banner("HEADLINE-FLAT  the headline tie on the solutions of its own field equations" + ("  [MUTATE: the tie reads K]" if MUTATE else ""))
# T1's multiplier equations (from T1a's Euler-Lagrange output): d_t Lambda = -EL(T0)/2 - d_t Lambda + d_t Lambda ... = 0.
dLdt = sp.lambdify((), sp.solve(sp.Eq(el_T0, 0), sp.diff(LamF, t_))[0] if sp.solve(sp.Eq(el_T0, 0), sp.diff(LamF, t_)) else 0)
dLdx = sp.lambdify((), sp.solve(sp.Eq(el_T1, 0), sp.diff(LamF, xx_))[0] if sp.solve(sp.Eq(el_T1, 0), sp.diff(LamF, xx_)) else 0)
K_num = sp.lambdify((sp.Symbol('Hs'),), K_frw.subs({sp.diff(aF, tF): sp.Symbol('Hs') * aF, NF: 1}))
zs = [0.0, 0.5, 1.0, 2.5, 5.0, 1100.0]
tz = [quad(lambda zz: 1 / ((1 + zz) * H0 * E_of(zz)), z, 1e4)[0] for z in zs]    # cosmic time (to a fixed early origin)
solT = solve_ivp(lambda t, L: [float(dLdt())], (tz[-1], tz[0]), [LAM_SI], t_eval=sorted(tz), rtol=1e-12, atol=0)
Lam_t = dict(zip(sorted(tz), solT.y[0]))
x_gal = np.linspace(0.0, 100.0, 11) * 3.0857e19                              # 0-100 kpc across a galaxy
solX = solve_ivp(lambda x, L: [float(dLdx())], (x_gal[0], x_gal[-1]), [LAM_SI], t_eval=x_gal, rtol=1e-12, atol=0)
a0_tie = lambda Lam: KAP["canonical"] * c_SI ** 2 * math.sqrt(Lam / (8 * math.pi))
if not MUTATE:
    a0z = {z: a0_tie(Lam_t[t]) for z, t in zip(zs, tz)}
    a0x = [a0_tie(L_) for L_ in solX.y[0]]
else:                                                                         # the tie reads the leaf's K = 3H(z)
    a0z = {z: KAPK["canonical"] * c_SI * float(K_num(H0 * E_of(z))) for z in zs}
    a0x = [a0z[0.0] for _ in x_gal]                                            # (K's local response is T3c's; not needed to fail)
ratio_z = {z: a0z[z] / a0z[0.0] for z in zs}
flat_ok = max(abs(v - 1) for v in ratio_z.values()) < 1e-12 and max(abs(v / a0x[0] - 1) for v in a0x) < 1e-12 and \
    abs(a0z[0.0] / A0["canonical"] - 1) < 1e-12
check("HEADLINE-FLAT the headline tie evaluated on the solutions of its own field equations: a0(z)/a0(0) = 1 at z = 0.5, 1, "
      "2.5, 5, 1100 and a0 uniform across a galaxy, to 1e-12, with a0(0) = the canonical 9.3603e-11",
      "a0(z)/a0(0) = " + ", ".join(f"{ratio_z[z]:.6f}" for z in zs[1:]) + f"; across 0-100 kpc max |dev| "
      f"{max(abs(v / a0x[0] - 1) for v in a0x):.1e}; a0(0) = {a0z[0.0]:.6e}", flat_ok,
      "T1: d Lambda = 0 integrated in time and across a galaxy leaves Lambda, and so a0, unchanged" if not MUTATE else
      "MUTATE: reading K ties a0 to the expansion rate: the rival law")
OUT["numbers"]["headline"] = dict(ratio_z={str(k): v for k, v in ratio_z.items()}, a0_0=a0z[0.0])

# ================================================================================================ W ledger
banner("W   THE LEDGER: which tie makes a0 and Lambda one field, and at what price")
LEDGER = [
    ("X20-T1", "HT unimodular: a0 = kappa c sqrt(G rho_Lambda) holds on every solution; Lambda (and a0) exactly constant in "
     "space and time; the MOND sector's dL/dLambda feeds only the unimodular clock; 0 local DOF (+1 global); FRW and PPN = FP7's",
     "TIED", "T1a-T1d, HEADLINE-FLAT; kappa stays a coupling (FITTED), the sqrt(Lambda) power is dimensional (FP0 C1)"),
    ("X20-T1v", "the HT tie is to the integration constant, not to the total observed Lambda: a matter vacuum energy moves "
     "Lambda_obs but not a0", "CONSTRAINT", "T1e: |rho_vac| << rho_Lambda (the cosmological-constant problem, shared)"),
    ("X20-T2", f"BT four-form: tied (flux amplitude cancels, one coupling), local a0 {(1 - knee['canonical']) * 100:.3f}% / "
     f"{(1 - knee['alt']) * 100:.3f}% low at the RAR knee, RAR shift "
     f"<= {max(sp_rows[f]['max_shift'] for f in A0):.4f} dex; BUT the slaved kernel folds at y = "
     f"{FOLD['canonical']['y_fold']:.2f} / {FOLD['alt']['y_fold']:.2f} and is non-monotone up to y_off = "
     f"{YOFF['canonical']:.0f} / {YOFF['alt']:.0f} (can/alt)", "FAILS",
     "T2d-T2e: C_L,eff < 0 on the band (FP7 C1's health condition), which holds SPARC inner points, a shell around every star, "
     "wide binaries at 2-3 kAU"),
    ("X20-T3", "khronon K: a0 = kappa_K c K = a0 E(z) on FRW", "FAILS", "T3b: the rho_total rival (+0.576 dex at z = 2.5; L37)"),
    ("X20-T4", "sequestering: alpha of a global variable is exactly constant, but Lambda_s = -V_vac + <tau>/4 and the kept "
     "residual is <= 0 for ordinary matter", "NOT TIED", "T4a-T4c: constant, not tied to the observed rho_Lambda"),
    ("L2b", "a0 as a field (FP0/FP5): tied to Lambda by T1's multiplier; still a coupling function written into the action",
     "TIED (T1)", "was POSTULATED (FP5 D1-D5); the relation is now a consequence of the field equations given alpha(Lambda)"),
    ("L0c", "kappa = 1/2 (Z = 5.7888)", "FITTED", "unchanged: no tie here fixes it (k01-k03)"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:8s} {st_:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)
TABLE = [
    ("T1 HT", "0 (+1 global)", "unchanged", "unchanged", "0 (exact)", "flat (exact)", "TIED"),
    ("T2 BT", "0 (+1 global)", "unchanged", "unchanged at 1 AU (off inside r_off)", f"{(1 - knee['canonical']) * 100:.3f}% at the knee; fold y ~ "
     f"{FOLD['canonical']['y_fold']:.1f}", "flat", "FAILS (health)"),
    ("T3 K", "0", "background unchanged", "not established", "O(0.1-1) (T3c)", "E(z): +0.576 dex at 2.5", "FAILS (flat law)"),
    ("T4 seq.", "0 (global numbers)", "residual <tau>/4 <= 0 kept", "unchanged", "0", "flat", "NOT TIED"),
]
P("\n    tie        local DOF       FRW                         PPN                                local a0                        a0(z)                  status")
for r_ in TABLE:
    P("    " + " | ".join(f"{c_:s}" for c_ in r_))
OUT["numbers"]["table"] = TABLE

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P("  T1 (Henneaux-Teitelboim) TIES a0 to Lambda without touching the flat law: d Lambda = 0 is a field equation, so a0 is exactly\n"
  "  constant in space and time; the MOND sector's dL/dLambda goes into the unimodular clock, which nothing observes; no local\n"
  "  mode is added; the metric equations, FRW and PPN are FP7's.  It is a tie, not a derivation: alpha(Lambda) = kappa\n"
  "  sqrt(Lambda/8 pi) is a coupling function written into the action, kappa stays fitted, and the tie is to the HT integration\n"
  "  constant (a matter vacuum energy would move the observed Lambda but not a0).\n"
  f"  T2 (Brown-Teitelboim) ties them too and leaves the RAR untouched (<= {max(sp_rows[f]['max_shift'] for f in A0):.4f} dex), but "
  "the four-form's Legendre map folds\n"
  f"  at y = {FOLD['canonical']['y_fold']:.2f} (canonical) / {FOLD['alt']['y_fold']:.2f} (alt): past it the slaved scalar force falls "
  f"as g_N grows, up to the switch-off at y = {YOFF['canonical']:.0f} / {YOFF['alt']:.0f} --\n"
  "  the non-monotone kernel FP7's health condition forbids.  T3 (K) is the rival law.  T4 (sequestering) is constant but not\n"
  "  tied to the observed rho_Lambda.  The closure target stays OPEN; kappa = 1/2 stays FITTED.")
OUT["verdict"] = dict(n_checks=len(CH), n_fail_load_bearing=n_fail)
json.dump(OUT, open(JSN, "w"), indent=1, default=str)
rc = 0 if n_fail == 0 else 1
P(f"\n  {len(CH) - sum(1 for _, ok, _l in CH if not ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{os.path.basename(JSN)}  ({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")
TEE.flush(); sys.stdout = sys.__stdout__; TEE.close()
sys.exit(rc)
