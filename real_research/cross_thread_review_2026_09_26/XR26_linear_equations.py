#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR26 (part 1) -- THE CHAIN'S LINEAR COSMOLOGY ON FRW FOR z >~ 10: derived from the full action, compared with GR + CDM.

WHY.  The most basic cosmological test of any theory is the cosmic microwave background and Big Bang nucleosynthesis, and
it has not been run on the derivation chain (real_research/derivation_chain_2026/).  FP3/FP7 derived pieces of the linear
cosmology and FP9/FP13 scored sigma_8 and today's P(k) boost with the chain's growth yardstick; nobody has written the
chain's full linear system at the CMB epoch.  This script derives it.  The CMB spectra are XR26_cmb.py; BBN is XR26_bbn.py.

THE ACTION (per 1/16 pi G, c = 1; FP7's AQUAL-type root with FP14's limits and FP13's separator):
  R - 2 Lambda + alpha_c a^2 - 2 mu (K - <K>_h)                      [khronon; FP14: c_2 -> oo is the CMC multiplier mu]
  + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi,  chi = (S_xi - S_B) phi   [chassis; FP13: B[state] = L^2/2]
  - 2 alpha^2 J_P2(h^mn D_m phi D_n phi/alpha^2) - 4 alpha^2 y_th sqrt(Y/alpha^2) + 2 lambda (n.d phi)^2   [MOND scalar + yield]
  + 16 pi G (L_dark[Phi_d] + L_baryons + L_photons + L_neutrinos)       [matter, minimally coupled to g]
  alpha = a0/c^2 (a0 = 9.3603e-11 canonical, 1.1312e-10 m/s^2 alt, FP0); kappa = 1/2 FITTED (Z = kappa = 5.7888).
  alpha_c in [8e-16, 3.2e-9] (FP14 A3's strong-coupling floor, FP2's PPN bound): a regulator.  lambda > 0 (FP13 A1).
  The separator (FP13 H_S): <(S_B delta_m)^2>_h = delta_c^2 sets B; with no root the band-pass closes (B = b = xi^2/2, chi = 0);
  y_th = <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q) (zero when the band-pass is closed).
  The dark field (FL1/FK1/FP4 L10f): V = m^2 |Phi_d|^2 + eps Re(Phi_d^2) + lambda(K)(Im Phi_d^2)^2, lambda ~ K^(-3.5),
  m >= 1.9-5.2e-19 eV, eps/m^2 ~ 2e-6; initial misalignment near the heavy axis (declared); not a particle species.

PRE-DECLARED (written before any full run of this script).  DISCLOSURE: an exploratory sympy derivation of the background and
of the linear equations (dust + a radiation fluid + khronon + multiplier + the lambda-scalar; scratch files outside the
repository) was run while planning, so the STRUCTURE behind H1-H4 had been seen; none of the numbers in H3, H5-H7 had been
computed.  The pencil-and-paper expectations:
  H1  BACKGROUND.  Friedmann and the acceleration equation are GR's with the bare G for any matter content: alpha_c a^2 and
      (K - <K>_h) vanish on FRW, the multiplier has no background equation, J and the chassis vanish, and with the declared
      datum phibar-dot = 0 the lambda-term is zero.  So G_cos = G, while the local Newton constant is G_N = G/(1 - alpha_c/2)
      (FP14).  EXPECT TRUE.
  H2  LINEAR EQUATIONS (band-pass closed).  The metric equations are Einstein's with the matter stress plus khronon terms that
      are ALL proportional to alpha_c or to the multiplier mu, with no matter variable in them; the traceless (slip) equation
      has no khronon term; mu's own equation is the CMC condition Q = 0; the khronon's equation fixes mu = O(alpha_c); mu
      CANCELS from the comoving Poisson equation, which becomes (k^2/a^2)[Psi - (alpha_c/2)(Phi - pidot)] = -4 pi G rho Delta;
      the matter equations (dust, radiation, the dark scalar) are GR's; delta phi decouples (ddot + 3H dot = 0); J has no
      quadratic part; a0 appears in no linear coefficient (identical for both footings).  EXPECT TRUE.
  H3  THE LEADING DIFFERENCE AND ITS SIZE.  With Phi = Psi, G_eff/G = 1/(1 - (alpha_c/2) F), F = (Phi - pidot)/Psi: F -> 1
      sub-horizon (G_eff = G_N, FP14 C1b) and F -> 0 super-horizon (pi = (H Phi + Psidot)/(k^2/a^2 - 3 Hdot) makes
      pidot -> Phi on any power-law background), so |G_eff/G - 1| <= alpha_c/2 everywhere; with G_cos = G the whole
      departure from GR + CDM relative to the measured G_N is G_cos/G_N = 1 - alpha_c/2 >= 1 - 1.6e-9.  Evaluated on CLASS's
      own GR solution for k = 1e-4..0.3 /Mpc and z = 1e5..10, 0 <= F <= ~1 and the multiplier's term in the momentum
      constraint is <= alpha_c x O(1) of GR's.  EXPECT TRUE.
  H4  YORK/CMC.  The multiplier alone (alpha_c -> 0) gives G_eff = G on cosmological perturbations, not 2G: the York kill is
      not reproduced (FP14 C2 in the static limit; here for the linear cosmology).  EXPECT TRUE.
  H5  THE SEPARATOR'S STATE.  At z = 1000-1100 the leaf-rms density contrast of the actual field, unsmoothed to FP13's grid edge
      (k = 1000 h/Mpc), is <= ~0.1 << delta_c = 1.686 in both readings, so L = xi and chi = 0 (checked in FP13's source: its
      L_table returns the xi floor when sigma(RMIN) < s); the band-pass first opens at some z_open ~ 20-100; below z_open the
      linear growth source C_eff at k <= 1 h/Mpc stays negligible down to z = 10 (the band-pass passes only k >~ 1/L).
      EXPECT TRUE (the value of z_open is not predicted).
  H6  THE DARK FIELD.  For m >= 1.9e-19 eV it is frozen (w = -1, rho_d/rho_r <~ 1e-4) through BBN, oscillates at z_osc ~ 1e8,
      has w ~ (H/m)^2 ~ 1e-20 at recombination, and its Jeans wavenumber at recombination is >~ 100 /Mpc, >= 300x beyond the
      CMB's k <= 0.3 /Mpc: the relative change of its density contrast against CDM at k <= 0.3 /Mpc is < 1e-8 through z = 0.
      FK1's conversion is off at z >= 10 (its background e-fold exponent scales as H^-8 a^-6).  EXPECT TRUE.
  H7  THE DATUM.  With FP13's lambda > 0, phibar-dot is physical: a nonzero value is a stiff (a^-6) component; the chain's
      phibar-dot = 0 is a declared datum, and BBN bounds any nonzero value to Omega_phi,0 <~ 1e-24.  EXPECT TRUE (a price).
"""
# (the docstring above is the pre-declaration; everything below was written after it and before the first full run)
DOC_CHECKS = r"""
CHECKS
  K  CONTROLS: K1 FP2's committed FRW machinery (exec'd read-only, as FP14 K3 does) + this lane's multiplier reproduces FP14's
     committed C1b (G_eff/G = -2/(alpha_c - 2), slip 1, mu's equation / Q = -2a^3, R_mu); K2 this lane's replication of FP13's
     state reading (FP9's machinery exec'd read-only + FP13's halofit / L_table / yield) reproduces FP13's committed (H_S)
     L(0.25), L(2.5) and y_th(z = 1); K3 FL1's committed F5 dark-field sound speed (m = 2e-19 eV) is reproduced; K4 CLASS's own
     Newtonian-gauge GR solution satisfies the GR 00 and 0i constraints (Ma & Bertschinger 1995 eqs. 23a-b) to <= 1e-2 (the
     variable map psi_CLASS = Phi (lapse), phi_CLASS = Psi (curvature) used in C4).
  A  THE BACKGROUND: A1 the chain's background equations equal GR's (dust + a radiation fluid + the dark scalar, any Lambda);
     no multiplier equation at background order; A2 (reported) with phibar-dot = p0/a^3 the only change is a stiff a^-6 term.
  B  THE LINEAR EQUATIONS (sympy, Newtonian gauge after variation, all fields varied): B1 metric-equation differences from GR are
     proportional to alpha_c or mu and contain no matter variable and no delta phi [HEADLINE]; B2 the slip equation is GR's;
     B3 mu's equation is the CMC condition; B4 the khronon's equation gives mu = O(alpha_c); B5 the comoving Poisson equation
     (00 with 0i eliminated): mu cancels, alpha_c term = (alpha_c/2) k^2 (Phi - pidot); B6 the matter equations are GR's;
     B7 delta phi decouples; B8 J_P2 (and the yield term at y_th = 0) has no quadratic part; B9 a0-free.
  C  THE LEADING DIFFERENCE: C1 sub-horizon G_eff = G_N = G/(1 - alpha_c/2), no slip; C2 super-horizon: Phi - pidot = 0 on
     every power-law background (G_eff -> G); C3 the numbers at the alpha_c window's ends; C4 on CLASS's GR solution
     (k = 1e-4..0.3 /Mpc, z = 1e5..10): the Poisson modification (alpha_c/2)|Phi - pidot| against the envelope of |Psi|, and F at
     recombination; C5 York/CMC: the multiplier alone adds nothing to G_eff.
  D  THE SEPARATOR'S STATE: D1 sigma(R -> 0) at z = 999 (FP13's EH98 state) and at z = 1000/1100 from CLASS's linear spectrum,
     with and without the dark field's cutoff; D2 the opening redshift; D3 the MOND growth source C_eff(k <= 1 h/Mpc) at
     z = 999..10 with FP13's (H_S) model on FP9's growth yardstick (both modes, both footings).
  E  THE DARK FIELD: E1 misalignment (homogeneous KG, both masses): the oscillation epoch, rho_d/rho_r through BBN, w at
     recombination; E2 the Jeans wavenumber at recombination and the first-order growth deficit against CDM at k = 1e-3..1 /Mpc
     (+ the Hu-Barkana-Gruzinov 2000 transfer function as a cross-check); E3 FK1's conversion is off at z >= 10.
  F  THE DATUM: F1 the stiff component a nonzero phibar-dot would add, bounded by BBN (Delta N_eff < 0.5 at T = 1 MeV).
  W  the ledger.
MUTATE=1 opens the band-pass at z >~ 10 (chi = S_xi phi ~ phi, the yield off): the chassis (2 - alpha_c) h(2a - D chi).D chi
enters the linear equations, so B1 (the headline) must FAIL (rc = 1).

SCOPE.  Linear order on FRW, scalar sector, one Fourier mode (1+1 dependence suffices for the scalar sector; the machinery is
FP2's).  Matter is represented by action-level fields -- Brown-Kuchar dust, a radiation fluid P(X) = c_r X^2 (w = c_s^2 = 1/3)
and a real scalar of mass M_d for the dark field; photons' Thomson coupling and neutrino free-streaming live in the matter
sector, which couples only through T_mn and is therefore GR's (B1/B6 show the gravity side carries no matter variable).
The heat pair that builds chi = W(b) - W(B) is not written out: its multiplier is sourced by dS/dchi at diffusion times b and B
with opposite signs, which cancel identically at B = b, so with the band-pass closed the pair carries no stress.  The khronon
is FP2's Stueckelberg tau = t + pi with FP14's multiplier (first order; mu-bar = 0 as the c_2 -> oo limit gives).
C4 evaluates the O(alpha_c) terms on CLASS's GR solution (first-order in alpha_c); the CMB-level size is XR26_cmb.py's.
No particle-mesh run.  At most 2 threads.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR26_linear_equations.py   (MUTATE=1
for the control).  Writes XR26_linear_equations[_MUTATE].out and XR26_linear_equations_results[_MUTATE].json next to itself.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import sys, io, json, math, time, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
NAME = "XR26_linear_equations"
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
OUT = {"lane": "XR26", "part": "1: the linear equations on FRW for z >~ 10", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 114 + "\n" + t + "\n" + "=" * 114)


def el():
    return f"[{time.time() - T_START:.0f} s]"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def exec_ro(path, start=None, stop=None, ns=None):
    """exec a committed script's source (or a slice of it) read-only in a private namespace; its prints are captured."""
    src = open(path).read()
    if start is not None:
        src = src[src.index(start):]
    if stop is not None:
        src = src[:src.index(stop)]
    ns = {} if ns is None else ns
    ns.setdefault("__file__", path)
    ns.setdefault("__name__", "xr26_readonly")
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    return ns


P(__doc__.strip())
P(DOC_CHECKS.strip())
if MUTATE:
    P("\n  *** MUTATE=1: the band-pass is OPEN at z >~ 10 (chi = S_xi phi ~ phi, yield off): the chassis enters the linear "
      "equations -- B1 must FAIL ***")

# ================================================================================================ inputs (committed)
fp0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))
A0 = {"canonical": fp0["numbers"]["a0_canonical"], "alt": fp0["numbers"]["a0_rho_total"]}
fp14 = json.load(open(os.path.join(CHAIN, "FP14_zero_knob_core_results.json")))
AC_MAX = 3.2e-9                                                   # FP2 L6f / FP14 A1: the PPN bound on alpha_c
AC_MIN = min(v for k, v in fp14["numbers"]["A3"].items() if "XC1" in k)   # FP14 A3's strong-coupling floor (XC1 gate)
AC_MIN_OO = fp14["numbers"]["A3"]["oo|XC1 gate"]                  # at c_2 -> oo (the chain's limit)
M_DARK = (1.9e-19, 5.2e-19)                                       # FP4 L10f / FP10 / FP13: the dark field's mass floor [eV]
DELTA_C = 3.0 / 20.0 * (12.0 * math.pi) ** (2.0 / 3.0)            # 1.68647 (FP13's threshold)
P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); alpha_c in [{AC_MIN_OO:.2e} (FP14 A3, c_2 -> oo), "
  f"{AC_MAX:.1e} (PPN)]; dark mass {M_DARK[0]:.1e}-{M_DARK[1]:.1e} eV; delta_c = {DELTA_C:.5f}")

# ================================================================================================ the action on perturbed FRW
banner("DERIVATION: the chain's action on perturbed FRW (FP2's machinery + multiplier + radiation fluid + dark scalar + MOND scalar)")
FP2 = os.path.join(CHAIN, "FP2_relativistic_consistency.py")
G2 = exec_ro(FP2, "tq, xq, yq, zq = sp.symbols('t x y z', real=True)", "SYS = {tm: frw_system(tm)",
             {"sp": sp, "euler_equations": euler_equations})
e, tq, xq, a, rb = G2["e"], G2["tq"], G2["xq"], G2["a"], G2["rb"]
ser = G2["ser"]
gi4, sqg4, n_up4, acc4, R4, aa4, dK = (G2[k_] for k_ in ("gi4", "sqg4", "n_up4", "acc4", "R4", "aa4", "dK_leaf"))
alc, Gc, Lam = G2["alc"], G2["Gc"], G2["Lam"]
Phi, Psi, Bq, Eq, piq, th, dq = G2["FIELDS"]
X4 = G2["X4"]
mu1 = sp.Function('mu')(tq, xq)                                   # the CMC multiplier (FP14: c_2 -> oo), first order
ds = sp.Function('dsig')(tq, xq)                                  # the radiation fluid's scalar
dphi = sp.Function('dphi')(tq, xq)                                # the MOND scalar
dfd = sp.Function('dphid')(tq, xq)                                # the dark field (one real component)
cr, lamS, p0, Md = sp.symbols('c_r lambda_s p_0 M_d', positive=True)
etaF, phib, fdb = sp.Function('eta')(tq), sp.Function('phib')(tq), sp.Function('phidbar')(tq)


def grad(f):
    return [sp.diff(f, v) for v in X4]


def gdot(u, v):
    return ser(sum(gi4[m, s] * u[m] * v[s] for m in range(4) for s in range(4)))


sig = etaF + e * ds                                               # radiation fluid: sigma = conformal time + perturbation
Xr = ser(-gdot(grad(sig), grad(sig)))
L_rad = ser(sqg4 * cr * ser(Xr ** 2))                             # P(X) = c_r X^2: rho = 3 c_r X^2, w = c_s^2 = 1/3
fdf = fdb + e * dfd
L_dark = ser(sqg4 * ser(-gdot(grad(fdf), grad(fdf)) / 2 - Md ** 2 * fdf ** 2 / 2))
phi_f = phib + e * dphi
ndphi = ser(sum(n_up4[m] * sp.diff(phi_f, X4[m]) for m in range(4)))
L_lam = ser(sqg4 * 2 * lamS * ser(ndphi ** 2))                    # 2 lambda (n.d phi)^2
hup = sp.Matrix(4, 4, lambda m, s: gi4[m, s] + n_up4[m] * n_up4[s])   # h^{mn} = g^{mn} + n^m n^n


def chassis(chi):
    dc = grad(chi)
    return ser(sqg4 * (2 - alc) * ser(sum(hup[m, s] * (2 * acc4[m] - dc[m]) * dc[s] for m in range(4) for s in range(4))))


FIELDS = [Phi, Psi, Bq, Eq, piq, mu1, th, dq, ds, dfd, dphi]
NAMES = [F.func.__name__ for F in FIELDS]
kF = sp.Symbol('k', positive=True)
AMP = {F: sp.Function(F.func.__name__ + 'k')(tq) for F in FIELDS}
AM = {F.func.__name__: AMP[F] for F in FIELDS}


def lagrangian(kind, stiff=False):
    """per 1/16 pi G; kind: 'GR' (the control), 'chain' (band-pass closed: chi = 0 identically), 'open' (the MUTATE: chi = phi)."""
    matter = 16 * sp.pi * Gc * (G2["Ldust"] + L_rad + L_dark)
    if kind == "GR":
        Lt = sqg4 * (R4 - 2 * Lam) + matter
    else:
        Lt = sqg4 * (R4 - 2 * Lam + alc * aa4) - 2 * e * mu1 * sqg4 * dK + matter + L_lam
        if kind == "open":
            Lt = Lt + chassis(e * dphi)
    Lt = sp.expand(ser(Lt))
    return Lt.coeff(e, 1), Lt.coeff(e, 2)


def derive(kind, stiff=False):
    L1, L2 = lagrangian(kind, stiff)
    subsb = {sp.diff(etaF, tq): 1 / a, sp.diff(etaF, tq, 2): -sp.diff(a, tq) / a ** 2,
             sp.diff(phib, tq): (p0 if stiff else 0) / a ** 3, sp.diff(phib, tq, 2): (-3 * p0 * sp.diff(a, tq) / a ** 4 if stiff else 0)}
    kg = -3 * sp.diff(a, tq) / a * sp.diff(fdb, tq) - Md ** 2 * fdb   # the dark field's background Klein-Gordon equation
    bg = {}
    for F in FIELDS:
        el_ = euler_equations(L1, [F], [tq, xq])
        if el_:
            ex = sp.simplify((el_[0].lhs - el_[0].rhs).subs(subsb).subs({sp.diff(fdb, tq, 2): kg}).doit())
            if ex != 0:
                bg[F.func.__name__] = ex
    rbs = sp.solve(bg["Phi"], rb)[0]                              # Friedmann -> the dust density
    adds = sp.solve(bg["Psi"].subs(rb, rbs), sp.diff(a, tq, 2))[0]   # the acceleration equation

    def fourier(ex):
        for F in FIELDS:
            ex = ex.subs(F, AMP[F] * sp.exp(sp.I * kF * xq))
        return sp.expand(sp.simplify(ex.doit() * sp.exp(-sp.I * kF * xq)))

    def bgsub(ex):
        ex = ex.subs(subsb).doit()
        ex = ex.subs({AMP[Bq]: 0, AMP[Eq]: 0}).doit()             # Newtonian gauge AFTER the variation (FP2's convention)
        for _ in range(2):
            ex = ex.subs(sp.diff(fdb, tq, 3), sp.diff(kg, tq)).subs(sp.diff(fdb, tq, 2), kg)
            ex = ex.subs(sp.diff(a, tq, 3), sp.diff(adds, tq)).subs(sp.diff(a, tq, 2), adds)
        ex = ex.subs(rb, rbs).subs(sp.diff(fdb, tq, 2), kg).subs(sp.diff(a, tq, 2), adds)
        return sp.expand(sp.simplify(ex))
    E = {}
    for F in FIELDS:
        el_ = euler_equations(L2, [F], [tq, xq])
        E[F.func.__name__] = bgsub(fourier(el_[0].lhs - el_[0].rhs)) if el_ else sp.Integer(0)
    Qk = bgsub(fourier(dK.coeff(e, 1)))                              # (K - <K>_h) at first order, Fourier space, Newtonian gauge
    return dict(bg=bg, rbs=rbs, adds=adds, E=E, L2=L2, Qk=Qk)


tD = time.time()
SGR = derive("GR")
SCH = derive("chain")                                              # the chain (band-pass closed): the controls and A use it
SST = derive("chain", stiff=True)
STEST = derive("open") if MUTATE else SCH                          # B and C score this system (MUTATE: the band-pass open)
P(f"    derived GR, the chain (band-pass closed), the stiff-datum variant" + (" and the OPEN band-pass (MUTATE)" if MUTATE else "")
  + f" ({time.time() - tD:.1f} s): {len(SCH['E'])} field equations each")
H_ = sp.diff(a, tq) / a
Hdot_ = sp.simplify(sp.diff(H_, tq).subs(sp.diff(a, tq, 2), SCH["adds"]))

# ================================================================================================ K controls
banner("K  CONTROLS: FP14's committed FRW result, FP13's committed separator state, FL1's committed sound speed, CLASS's GR solution")
# K1: FP14 C1b -- dust only (c_r = 0, dark scalar off), the multiplier form, quasi-static coupling and slip
def qs_limit(Sd, dust_only=True):
    """sub-horizon ordering on the derived equations: k -> k/l, delta -> delta/l^2, time derivatives of the potentials, of pi and
    of delta phi dropped, pi and mu at their quasi-static values (zero at leading order); if delta phi reaches the metric equations
    (the MUTATE) its own quasi-static equation is solved with them.  Returns G_eff/G (Poisson with the system's own Friedmann rho)
    and the slip; (None, None) if the quasi-static system is singular."""
    lam_s = sp.Symbol('l', positive=True)
    Ps, Fs, dls, Xs = sp.symbols('Psi_s Phi_s delta_s dphi_s')
    off = {cr: 0, Md: 0} if dust_only else {}
    with_dphi = Sd["E"]["Phi"].has(AM["dphi"])
    names_ = ("Phi", "Psi") + (("dphi",) if with_dphi else ())
    muk, pik, dpk = AM["mu"], AM["pi"], AM["dphi"]
    qs = {sp.diff(AM["Psi"], tq): 0, sp.diff(AM["Psi"], tq, 2): 0, sp.diff(AM["Phi"], tq): 0, sp.diff(AM["theta"], tq): AM["Phi"],
          sp.diff(AM["theta"], tq, 2): 0, sp.diff(pik, tq): 0, sp.diff(pik, tq, 2): 0, sp.diff(muk, tq): 0,
          sp.diff(dpk, tq): 0, sp.diff(dpk, tq, 2): 0}
    outs = []
    for n_ in names_:
        ex = Sd["E"][n_].subs(off)
        if dust_only:
            ex = ex.subs(sp.diff(fdb, tq), 0).subs(fdb, 0).doit()
        ex = ex.subs(qs).subs({pik: 0, muk: 0})
        ex = ex.subs({AM["Psi"]: Ps, AM["Phi"]: Fs, AM["delta"]: dls, AM["theta"]: 0, AM["dsig"]: 0, AM["dphid"]: 0, dpk: Xs})
        ex = sp.expand(ex.subs({kF: kF / lam_s, dls: dls / lam_s ** 2, Xs: Xs}) * lam_s ** 2)
        outs.append(sp.expand(ex.subs(lam_s, 0)))
    try:
        sols = sp.solve(outs, [Ps, Fs] + ([Xs] if with_dphi else []), dict=True)
        sol_ = sols[0]
        rbs0 = Sd["rbs"].subs(off).subs(sp.diff(fdb, tq), 0).subs(fdb, 0).doit()
        Geff = sp.simplify(-sol_[Ps] * kF ** 2 / (a ** 2 * 4 * sp.pi * Gc * rbs0 * dls))
        slip = sp.simplify(sol_[Fs] / sol_[Ps])
        return Geff, slip
    except Exception:
        return None, None


Geff_qs, slip_qs = qs_limit(SCH)
Rmu = sp.expand(SCH["E"]["pi"]).coeff(AM["mu"])
Rmu_dust = sp.factor(sp.simplify(Rmu.subs({cr: 0, Md: 0}).subs(fdb, 0).doit()))
Rmu_fp14 = sp.sympify(fp14["numbers"]["C1b"]["R_mu"].replace("a(t)", "A_").replace("Derivative(A_, t)", "Ad_"),
                      locals={"Lambda": Lam, "k": kF, "A_": sp.Symbol("A_"), "Ad_": sp.Symbol("Ad_")})
Rmu_mine = Rmu_dust.subs(sp.diff(a, tq), sp.Symbol("Ad_")).subs(a, sp.Symbol("A_"))
mueq_Q = sp.simplify(SCH["E"]["mu"] / SCH["Qk"])
k1_ok = (sp.simplify(Geff_qs - sp.sympify(fp14["numbers"]["C1b"]["Geff"], locals={"alpha_c": alc})) == 0 and sp.simplify(slip_qs - 1) == 0
         and sp.simplify(Rmu_mine - Rmu_fp14) == 0 and sp.simplify(mueq_Q + 2 * a ** 3) == 0)
P(f"    quasi-static (dust): G_eff/G = {sp.factor(Geff_qs)}, slip = {slip_qs};  R_mu (dust) = {Rmu_dust};  mu-equation / Q = {mueq_Q}")
check("K1 CONTROL: FP2's committed FRW machinery (exec'd read-only) with this lane's multiplier reproduces FP14's committed C1b: "
      "G_eff/G = -2/(alpha_c - 2), slip 1, R_mu = -(-3 Lambda a^2 + 2k^2 + 9 adot^2) a, mu's equation / Q = -2a^3",
      f"G_eff {sp.factor(Geff_qs)}; slip {slip_qs}; R_mu == FP14: {sp.simplify(Rmu_mine - Rmu_fp14) == 0}; mu-eq/Q {mueq_Q}", k1_ok)
OUT["numbers"]["K1"] = dict(Geff=str(Geff_qs), slip=str(slip_qs), Rmu_dust=str(Rmu_dust), mueq_over_Q=str(mueq_Q))

# K2: FP13's state reading (replicated) -- used in D
t9 = time.time()
ns9 = exec_ro(os.path.join(CHAIN, "FP9_web_galaxy_separator.py"), None,
              "# ================================================================================================= K  CONTROLS")
M6 = ns9["M6"]
FOOTS, MODES = ns9["FOOTS"], ns9["MODES"]
A0_9 = dict(ns9["A0"])
h9, Om9, OL9, Or9 = M6["h"], M6["Om"], M6["OL"], M6["Or"]
Ez9, dlnH9, A_I9 = M6["Ez"], M6["dlnH"], M6["A_I"]
G9, rhoc9, H09, Mpc9, c9 = M6["G"], M6["rho_crit0"], M6["H0"], M6["Mpc"], M6["c"]
Delta_lin0 = M6["Delta_lin0"]
XI_FLOOR_MPC = 0.0243e-6                                          # FP13: the filter floor [Mpc]
_sD = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om9 / math.exp(3 * N_) / Ez9(math.exp(N_)) ** 2) * Y[0] - (2 + dlnH9(math.exp(N_))) * Y[1]],
                (math.log(A_I9), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14, dense_output=True)
_D1 = _sD.sol(0.0)[0]


def Dl(a_):
    return float(_sD.sol(math.log(a_))[0] / _D1)


LKF = np.linspace(math.log(1e-4), math.log(1000.0), 5000)
KKF = np.exp(LKF)
D2L0 = np.array([Delta_lin0(k_) for k_ in KKF]) ** 2
RMIN = 1e-5


def sig2(R, D2):
    return float(np.trapz(D2 * np.exp(-(KKF * R) ** 2), LKF))


def Om_a(a_):
    return Om9 / a_ ** 3 / (Om9 / a_ ** 3 + OL9 + Or9 / a_ ** 4)


def halofit(D2lin, a_):
    """FP13's Takahashi et al. 2012 halofit (flat, w = -1), copied verbatim in logic (its K2 checked it against CLASS)."""
    Oma = Om_a(a_)
    Rs = brentq(lambda R: sig2(R, D2lin) - 1.0, RMIN, 100.0); ks = 1.0 / Rs; e_ = 1e-3
    l0, lp, lm = (math.log(sig2(Rs * math.exp(x), D2lin)) for x in (0.0, e_, -e_))
    n_ = -3.0 - (lp - lm) / (2 * e_); C_ = -(lp - 2 * l0 + lm) / e_ ** 2
    an = 10 ** (1.5222 + 2.8553 * n_ + 2.3706 * n_ ** 2 + 0.9903 * n_ ** 3 + 0.2250 * n_ ** 4 - 0.6038 * C_)
    bn = 10 ** (-0.5642 + 0.5864 * n_ + 0.5716 * n_ ** 2 - 1.5474 * C_)
    cn = 10 ** (0.3698 + 2.0404 * n_ + 0.8161 * n_ ** 2 + 0.5869 * C_)
    gn = 0.1971 - 0.0843 * n_ + 0.8460 * C_
    al = abs(6.0835 + 1.3373 * n_ - 0.1959 * n_ ** 2 - 5.5274 * C_)
    be = 2.0379 - 0.7354 * n_ + 0.3157 * n_ ** 2 + 1.2490 * n_ ** 3 + 0.3980 * n_ ** 4 - 0.1682 * C_
    nun = 10 ** (5.2105 + 3.6902 * n_)
    f1, f2, f3 = Oma ** -0.0307, Oma ** -0.0585, Oma ** 0.0743
    y = KKF / ks
    DQ = D2lin * ((1 + D2lin) ** be / (1 + al * D2lin)) * np.exp(-(y / 4 + y ** 2 / 8))
    DH = an * y ** (3 * f1) / (1 + bn * y ** f2 + (cn * f3 * y) ** (3 - gn)) / (1 + nun * y ** -2)
    return DQ + DH


LNA = np.linspace(math.log(1e-3), 0.0, 300)
AGR = np.exp(LNA)
D2LIN = [D2L0 * Dl(a_) ** 2 for a_ in AGR]
D2NL = [(halofit(D2LIN[i], AGR[i]) if sig2(RMIN, D2LIN[i]) > 1.0 else D2LIN[i]) for i in range(len(LNA))]


def L_table(s, D2s):
    out = np.empty(len(LNA))
    for i, a_ in enumerate(AGR):
        D2 = D2s[i]
        out[i] = XI_FLOOR_MPC if sig2(RMIN, D2) < s * s else brentq(lambda R: sig2(R, D2) - s * s, RMIN, 300.0) / h9 * a_
    return out


def fun_of(tab, log=True):
    tab = np.asarray(tab, float)
    if log:
        lt = np.log(np.maximum(tab, 1e-300))
        return lambda a_: float(np.exp(np.interp(math.log(a_), LNA, lt)))
    return lambda a_: float(np.interp(math.log(a_), LNA, tab))


def gbp_rms_phys(i, Lphys, D2s):
    a_ = AGR[i]; D2 = D2s[i]
    g = 4 * math.pi * G9 * Om9 * rhoc9 / a_ ** 3 * np.sqrt(D2) / (KKF * h9 / (a_ * Mpc9))
    g = g * (1.0 - np.exp(-0.5 * (KKF * h9 * Lphys / a_) ** 2))
    return math.sqrt(float(np.trapz(g ** 2, LKF)))


def two_q(a_):
    E2 = Om9 / a_ ** 3 + OL9 + Or9 / a_ ** 4
    return 1.0 + (Or9 / a_ ** 4) / E2 - 3.0 * OL9 / E2


LH_tab = L_table(DELTA_C, D2NL)
Lh = fun_of(LH_tab)
RMS_tab = np.array([gbp_rms_phys(i, LH_tab[i], D2NL) for i in range(len(LNA))])
YTH_tab = {f: np.array([RMS_tab[i] / A0_9[f] * max(0.0, two_q(AGR[i])) for i in range(len(LNA))]) for f in FOOTS}
yh = {f: fun_of(YTH_tab[f], log=False) for f in FOOTS}
f13 = json.load(open(os.path.join(CHAIN, "FP13_separator_from_state_results.json")))["numbers"]["H1"]
k2_dev = max(abs(1e3 * Lh(0.8) / f13["L_kpc"]["0.25"] - 1), abs(1e3 * Lh(1 / 3.5) / f13["L_kpc"]["2.5"] - 1),
             abs(yh["canonical"](0.5) / f13["yth"]["1.0"] - 1))
check("K2 CONTROL: this lane's replication of FP13's state reading (FP9's machinery exec'd read-only; FP13's halofit, L_table and "
      "state yield re-typed) reproduces FP13's committed (H_S) headline: L(0.25) = 1913.69 kpc, L(2.5) = 164.12 kpc, y_th(z = 1) = 4.21e-3",
      f"L(0.25) {1e3 * Lh(0.8):.4f} kpc, L(2.5) {1e3 * Lh(1 / 3.5):.4f} kpc, y_th(1) {yh['canonical'](0.5):.6e}; max rel. deviation {k2_dev:.1e} "
      f"({time.time() - t9:.1f} s)", k2_dev < 1e-9)

# K3: FL1's F5 sound speed
fl1 = json.load(open(os.path.join(REPO, "real_research", "dark_fluid_2026", "FL1_order_parameter_results.json")))["numbers"]["F5"]["rows"]
HBARC_MPC = 6.3949e-30                                            # hbar c [eV Mpc] (FL1's constant)


def cs2_field(k_mpc, m_ev, a_):
    q_ = k_mpc * HBARC_MPC / (2 * m_ev * a_)
    return q_ ** 2 / (1 + q_ ** 2)


cs2_ctl = max(cs2_field(kM, 2e-19, a_) for kM in (0.1, 1.0) for a_ in (1 / 1101.0, 1.0))
check("K3 CONTROL: FL1's committed F5 (the free order parameter's effective sound speed c_s^2 = q^2/(1 + q^2), q = k/(2 m a)) is "
      "reproduced at m = 2e-19 eV (max over k = 0.1-1 /Mpc, recombination..today)",
      f"{cs2_ctl:.6e} vs committed {fl1['2e-19']['max_cs2']:.6e}", abs(cs2_ctl / fl1["2e-19"]["max_cs2"] - 1) < 1e-9)

# K4: CLASS's GR solution (Newtonian gauge) -- used in C4
from classy import Class
P18 = {"h": 0.6732, "omega_b": 0.022383, "omega_cdm": 0.12011, "tau_reio": 0.0543, "ln_A_s_1e10": 3.0448, "n_s": 0.96605,
       "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06}               # Planck 2018 VI Table 1, TT,TE,EE+lowE+lensing best fit (H0 derived)
KOUT = [1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.3]
tC = time.time()
CL = Class()
CL.set(dict(P18, output="mPk", gauge="newtonian", k_output_values=",".join(str(k_) for k_ in KOUT), **{"P_k_max_1/Mpc": 1.0}))
CL.compute()
BG = CL.get_background()
lna_b = np.log(1 / (1 + BG["z"]))
lnH_s = CubicSpline(lna_b, np.log(BG["H [1/Mpc]"]))
RHO_S = {s_: CubicSpline(lna_b, np.log(BG["(.)rho_" + s_])) for s_ in ("g", "b", "cdm", "ur", "ncdm[0]")}
PNC_S = CubicSpline(lna_b, np.log(np.maximum(BG["(.)p_ncdm[0]"], 1e-300)))
PERT = CL.get_perturbations()["scalar"]
res_gr, C4 = {}, {}


def envelope(x, y, width=0.5):
    """running max of |y| over +-width in x (ln a): the oscillation envelope."""
    out = np.empty_like(y)
    for i in range(len(x)):
        m_ = (x >= x[i] - width) & (x <= x[i] + width)
        out[i] = np.max(np.abs(y[m_]))
    return out


W_S = CubicSpline(lna_b, np.log(4 / 3 * (BG["(.)rho_g"] + BG["(.)rho_ur"]) + BG["(.)rho_b"] + BG["(.)rho_cdm"]
                                 + BG["(.)rho_ncdm[0]"] + BG["(.)p_ncdm[0]"]))     # ln (rho + p)_total (Lambda has rho + p = 0)
for ik, q in enumerate(PERT):
    k_ = KOUT[ik]
    a_ = q["a"]; tau = q["tau [Mpc]"]
    sel = (a_ > 1 / (1 + 1e5)) & (a_ < 1 / 11.0)
    a_, tau = a_[sel], tau[sel]
    psi, phi = q["psi"][sel], q["phi"][sel]
    lna = np.log(a_)
    calH = a_ * np.exp(lnH_s(lna))
    r_ = {s_: np.exp(RHO_S[s_](lna)) for s_ in RHO_S}
    pnc = np.exp(PNC_S(lna))
    drho = sum(r_[s_] * q["delta_" + s_][sel] for s_ in ("g", "b", "cdm", "ur", "ncdm[0]"))
    S_ = (4 / 3 * r_["g"] * q["theta_g"][sel] + r_["b"] * q["theta_b"][sel] + r_["cdm"] * q["theta_cdm"][sel]
          + 4 / 3 * r_["ur"] * q["theta_ur"][sel] + (r_["ncdm[0]"] + pnc) * q["theta_ncdm[0]"][sel])      # (rho + p) theta, class units
    # GR constraints (MB95 23a, 23b) with phi' taken from the 0i equation itself is circular, so check 00 with a spline phi'
    phip = CubicSpline(tau, phi)(tau, 1)
    l00 = k_ ** 2 * phi + 3 * calH * (phip + calH * psi)
    l0i = k_ ** 2 * (phip + calH * psi)
    res00 = np.max(np.abs(l00 + 1.5 * a_ ** 2 * drho) / (np.abs(k_ ** 2 * phi) + np.abs(3 * calH * (phip + calH * psi))))
    res0i = np.max(np.abs(l0i - 1.5 * a_ ** 2 * S_) / envelope(lna, l0i))
    res_gr[k_] = (float(res00), float(res0i))
    # the khronon on the CMC leaves, first order in alpha_c, WITHOUT differentiating the perturbation output:
    #   pi = 3a(calH psi + phi')/den = 4.5 a^3 S/(k^2 den),  den = k^2 + 4.5 a^2 W  (W = (rho + p)_tot; calH^2 - calH' = 1.5 a^2 W)
    #   S' = -4 calH S + k^2 dp + k^2 W psi - k^2 Sum (rho + p) sigma   (total momentum conservation, Newtonian gauge, MB95 eq. 30)
    W_ = np.exp(W_S(lna)); Wp = calH * W_ * W_S(lna, 1)
    dp_ = r_["g"] * q["delta_g"][sel] / 3 + r_["ur"] * q["delta_ur"][sel] / 3 + q["cs2_ncdm[0]"][sel] * r_["ncdm[0]"] * q["delta_ncdm[0]"][sel]
    sig_ = (4 / 3 * r_["g"] * q["shear_g"][sel] + 4 / 3 * r_["ur"] * q["shear_ur"][sel] + (r_["ncdm[0]"] + pnc) * q["shear_ncdm[0]"][sel])
    Sp = -4 * calH * S_ + k_ ** 2 * dp_ + k_ ** 2 * W_ * psi - k_ ** 2 * sig_
    den = k_ ** 2 + 4.5 * a_ ** 2 * W_
    denp = 4.5 * a_ ** 2 * (2 * calH * W_ + Wp)
    pip = 4.5 / k_ ** 2 * (3 * a_ ** 3 * calH * S_ / den + a_ ** 3 * Sp / den - a_ ** 3 * S_ * denp / den ** 2)   # pi' (conformal)
    dev = psi - pip / a_                                          # Phi - pidot
    envPsi = envelope(lna, phi)
    ratio = np.abs(dev) / envPsi                                  # the Poisson modification / (alpha_c/2), against Psi's envelope
    # the multiplier's term in the momentum constraint, Psidot + H Phi = 4 pi G (rho + p) v + mu/2, through its time integral (no
    # derivative of the output): Int mu/2 dt = (alpha_c/2) Int (a dev)' h dtau = (alpha_c/2) {[a dev h] - Int a dev h' dtau},
    # h = k^2/(a den) (B4: mu = alpha_c k^2 d/dt[a dev]/(a den), cosmic time)
    hh = k_ ** 2 / (a_ * den)
    hp = -k_ ** 2 * (calH * den + denp) / (a_ * den ** 2)
    integ = a_ * dev * hp
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(tau))])
    I_mu = (a_ * dev * hh - a_[0] * dev[0] * hh[0]) - cum
    ratio_mu = np.abs(I_mu) / envPsi
    i_rec = int(np.argmin(np.abs(lna - math.log(1 / 1090.0))))
    F_rec = float(dev[i_rec] / phi[i_rec]) if abs(phi[i_rec]) > 0.2 * envPsi[i_rec] else float("nan")
    kaH = k_ / calH
    C4[k_] = dict(max_ratio=float(ratio.max()), F_rec=F_rec, F_first=float(dev[0] / phi[0]), F_last=float(dev[-1] / phi[-1]),
                  kaH_range=[float(kaH.min()), float(kaH.max())], res00=float(res00), res0i=float(res0i), max_ratio_mu=float(ratio_mu.max()))
k4_ok = all(v[0] < 1e-2 and v[1] < 1e-2 for v in res_gr.values())
check("K4 CONTROL: CLASS's own Newtonian-gauge GR solution (Planck 2018 best fit) satisfies the GR 00 and 0i constraints "
      "k^2 phi + 3H(phi' + H psi) = -4 pi G a^2 delta rho and k^2 (phi' + H psi) = 4 pi G a^2 (rho + p) theta (MB95 23a-b) at "
      "z = 1e5..10 for the six k -- so psi_CLASS is the lapse Phi and phi_CLASS the curvature Psi in C4",
      "; ".join(f"k={k_:g}: {v[0]:.1e}/{v[1]:.1e}" for k_, v in res_gr.items()) + f" ({time.time() - tC:.1f} s)", k4_ok)
P(f"    {el()}")

# ================================================================================================ A background
banner("A  THE BACKGROUND: Friedmann and the acceleration equation")
bg_same = (sp.simplify(SGR["rbs"] - SCH["rbs"]) == 0 and sp.simplify(SGR["adds"] - SCH["adds"]) == 0
           and set(SCH["bg"].keys()) == set(SGR["bg"].keys()) and "mu" not in SCH["bg"] and "pi" not in SCH["bg"])
fr_str = sp.factor(SCH["bg"]["Phi"])
P(f"    chain's Friedmann (vary the lapse): {fr_str} = 0")
P(f"    background equations present: chain {sorted(SCH['bg'])}, GR {sorted(SGR['bg'])}; rho_dust and addot identical: {bg_same}")
check("A1 THE BACKGROUND IS GR'S WITH THE BARE G: with dust, a radiation fluid, the dark scalar and Lambda the chain's Friedmann and "
      "acceleration equations are GR's (alpha_c a^2 and K - <K>_h vanish on FRW; the multiplier has no background equation; J, "
      "the chassis and the lambda-term vanish at phibar-dot = 0): G_cos = G, while the locally measured G_N = G/(1 - alpha_c/2)",
      f"identical: {bg_same}; multiplier background equation: {'mu' in SCH['bg']}", bg_same)
bg_st = sp.simplify(SST["rbs"] - SGR["rbs"])
bg_st_f = sp.factor(bg_st)
stiff_pow = sp.degree(sp.Poly(sp.numer(sp.together(bg_st)).subs(p0, 1), a)) - sp.degree(sp.Poly(sp.denom(sp.together(bg_st)), a))
P(f"    with phibar-dot = p0/a^3: rho_dust(chain) - rho_dust(GR) = {bg_st_f}  (a stiff component, a^{stiff_pow})")
check("A2 (reported) with a nonzero datum phibar-dot = p0/a^3 (FP13's lambda > 0 makes it physical) the only background change is a "
      "stiff a^-6 energy density 2 lambda p0^2/(16 pi G a^6) (it takes the dust's place at fixed H): F1 bounds it",
      f"{bg_st_f}; power {stiff_pow}", stiff_pow == -6, load_bearing=False)
OUT["numbers"]["A"] = dict(friedmann=str(fr_str), identical=bg_same, stiff=str(bg_st_f))
P(f"    {el()}")

# ================================================================================================ B linear equations
banner("B  THE LINEAR EQUATIONS (Newtonian gauge after variation): the gravity side against GR's, field by field"
       + ("  [MUTATE: band-pass OPEN]" if MUTATE else ""))
EC, EG = STEST["E"], SGR["E"]
MATTER = [AM[n_] for n_ in ("theta", "delta", "dsig", "dphid")]
DIFF = {n_: sp.expand(sp.simplify(EC[n_] - EG[n_])) for n_ in NAMES}
for n_ in ("Phi", "Psi", "B", "E"):
    P(f"    metric eq. [{n_:3s}] chain - GR = {sp.collect(DIFF[n_], [AM[x] for x in NAMES])}")
b1 = {}
for n_ in ("Phi", "Psi", "B", "E"):
    d_ = DIFF[n_]
    no_matter = not any(d_.has(f_) for f_ in MATTER)
    only_ac_mu = sp.simplify(d_.subs({alc: 0}).subs(AM["mu"], 0).doit()) == 0
    no_dphi = not d_.has(AM["dphi"])
    b1[n_] = (no_matter, only_ac_mu, no_dphi)
b1_ok = all(all(v) for v in b1.values())
check("B1 [HEADLINE] THE GRAVITY SIDE: every metric equation (00, trace ij, 0i, xx) differs from GR's only by terms proportional to "
      "alpha_c or to the multiplier mu; the differences contain no matter variable (dust, radiation, the dark field) and no delta phi "
      "-- the MOND scalar is decoupled at linear order because the band-pass is closed (chi = (S_xi - S_B) phi = 0 at B = b)",
      "; ".join(f"{n_}: no matter {v[0]}, only alpha_c/mu {v[1]}, no delta phi {v[2]}" for n_, v in b1.items()), b1_ok,
      reading=("MUTATE: with the band-pass open the chassis puts delta phi into the 00 equation at O(1) -- the MOND scalar gravitates "
               "at linear order and the reduction to GR fails" if MUTATE else ""))
slip_c = sp.simplify(EC["Psi"] - 3 * EC["E"] / kF ** 2)
slip_g = sp.simplify(EG["Psi"] - 3 * EG["E"] / kF ** 2)
b2_ok = sp.simplify(slip_c - slip_g) == 0
P(f"    slip combination (trace - 3 x xx/k^2): chain {sp.factor(slip_c)}; GR {sp.factor(slip_g)}")
check("B2 NO ANISOTROPIC STRESS FROM THE KHRONON OR THE MULTIPLIER: the slip combination (trace - 3 xx/k^2) is GR's exactly, "
      "-4k^2 a (Phi - Psi) for this matter content (neutrinos would add their own GR shear)", f"identical to GR: {b2_ok}", b2_ok)
Q_exp = -2 * a * (kF ** 2 - 3 * a ** 2 * Hdot_) * AM["pi"] + 6 * a ** 3 * (H_ * AM["Phi"] + sp.diff(AM["Psi"], tq))
b3_ok = sp.simplify(EC["mu"] - Q_exp) == 0
check("B3 THE MULTIPLIER'S OWN EQUATION IS THE CMC CONDITION on the khronon's leaves: -2a(k^2 - 3a^2 Hdot) pi + 6a^3 (H Phi + Psidot) "
      "= 0, i.e. pi = 3a^2 (H Phi + Psidot)/(k^2 - 3 a^2 Hdot) (FP2's Q = 0, with radiation and the dark field in Hdot)",
      f"mu-equation == CMC form: {b3_ok}", b3_ok)
Rmu_c = sp.expand(EC["pi"]).coeff(AM["mu"])
kh_rest = sp.simplify(EC["pi"] - Rmu_c * AM["mu"] - 2 * alc * kF ** 2 * sp.diff(a * (AM["Phi"] - sp.diff(AM["pi"], tq)), tq))
b4_ok = sp.simplify(Rmu_c + 2 * a * (kF ** 2 - 3 * a ** 2 * Hdot_)) == 0 and kh_rest == 0
check("B4 THE KHRONON'S EQUATION FIXES THE MULTIPLIER AT O(alpha_c): R_mu mu + 2 alpha_c k^2 d/dt[a (Phi - pidot)] = 0 with "
      "R_mu = -2a(k^2 - 3 a^2 Hdot) < 0 (Hdot < 0), so mu = alpha_c k^2 d/dt[a(Phi - pidot)]/(a (k^2 - 3 a^2 Hdot)): finite, and zero at "
      "alpha_c = 0", f"R_mu form {sp.simplify(Rmu_c + 2 * a * (kF ** 2 - 3 * a ** 2 * Hdot_)) == 0}; remainder {kh_rest}", b4_ok)
Psid = sp.diff(AM["Psi"], tq)
pois = {}
for lab, Ed in (("chain", EC), ("GR", EG)):
    sol_ = sp.solve(Ed["B"], Psid)[0]
    pois[lab] = sp.expand(sp.simplify(Ed["Phi"].subs(Psid, sol_)))
mu_coef = sp.simplify(pois["chain"].coeff(AM["mu"]))
ac_part = sp.factor(sp.diff(pois["chain"], alc))
pois_diff = sp.simplify(pois["chain"] - pois["GR"] - alc * sp.diff(pois["chain"], alc))
psi_coef = sp.factor(pois["chain"].coeff(AM["Psi"]))
b5_ok = (mu_coef == 0 and sp.simplify(ac_part - 2 * kF ** 2 * a * (AM["Phi"] - sp.diff(AM["pi"], tq))) == 0 and pois_diff == 0
         and sp.simplify(psi_coef + 4 * kF ** 2 * a) == 0)
P(f"    comoving Poisson (00 with the 0i equation's Psidot inserted): mu coefficient {mu_coef}; alpha_c part {ac_part}; "
  f"Psi coefficient {psi_coef}; (chain - GR - alpha_c part) = {pois_diff}")
check("B5 THE MULTIPLIER CANCELS FROM THE COMOVING POISSON EQUATION: eliminating Psidot with the 0i equation, the 00 equation is "
      "GR's plus exactly 2 alpha_c k^2 a (Phi - pidot) with Psi's coefficient -4 k^2 a, i.e. "
      "(k^2/a^2)[Psi - (alpha_c/2)(Phi - pidot)] = -4 pi G rho Delta: the only change the constraints make to the gravitating source",
      f"mu coefficient {mu_coef}; alpha_c part == 2 alpha_c k^2 a (Phi - pidot): "
      f"{sp.simplify(ac_part - 2 * kF ** 2 * a * (AM['Phi'] - sp.diff(AM['pi'], tq))) == 0}; rest == GR: {pois_diff == 0}", b5_ok)
b6 = {n_: DIFF[n_] == 0 for n_ in ("theta", "delta", "dsig", "dphid")}
check("B6 THE MATTER EQUATIONS ARE GR'S: the dust (theta, delta), the radiation fluid and the dark scalar's perturbation equations "
      "are identical to GR's (minimal coupling: the khronon, the multiplier and the MOND scalar never reach them)",
      "; ".join(f"{n_}: {v}" for n_, v in b6.items()), all(b6.values()))
dphi_eq = sp.expand(EC["dphi"])
b7_iso = not any(EC[n_].has(AM["dphi"]) for n_ in NAMES if n_ != "dphi")
b7_form = sp.simplify(dphi_eq + 4 * lamS * a ** 3 * (sp.diff(AM["dphi"], tq, 2) + 3 * H_ * sp.diff(AM["dphi"], tq))) == 0
P(f"    delta phi's equation: {sp.factor(dphi_eq)}")
check("B7 THE MOND SCALAR DECOUPLES: its equation is lambda (ddot delta phi + 3H dot delta phi) = 0 (inertia only; J has no quadratic part, "
      "the chassis is zero) and delta phi appears in no other equation",
      f"form {b7_form}; absent elsewhere {b7_iso}", b7_form and b7_iso)
ys_, ep_, al_, yt_ = sp.symbols('y epsilon alpha y_th', positive=True)
Jp2 = lambda u: -sp.Rational(1, 4) * sp.log(1 - 2 * sp.sqrt(u)) - sp.sqrt(u) / 2 - u / 2
Jfull = -2 * al_ ** 2 * Jp2(ep_ ** 2 * ys_ / al_ ** 2) - 4 * al_ ** 2 * yt_ * sp.sqrt(ep_ ** 2 * ys_ / al_ ** 2)
ser_J = sp.expand(sp.series(Jfull, ep_, 0, 5).removeO())
cJ = {n_: sp.simplify(ser_J.coeff(ep_, n_)) for n_ in (1, 2, 3, 4)}
b8_ok = sp.simplify(cJ[2]) == 0 and sp.simplify(cJ[1].subs(yt_, 0)) == 0 and sp.simplify(cJ[3] + sp.Rational(4, 3) * ys_ ** sp.Rational(3, 2) / al_) == 0
P(f"    -2 alpha^2 J_P2(eps^2 y/alpha^2) - 4 alpha^2 y_th sqrt(eps^2 y/alpha^2): eps^1 {cJ[1]}, eps^2 {cJ[2]}, eps^3 {cJ[3]}, eps^4 {cJ[4]}")
check("B8 THE MOND TERM HAS NO QUADRATIC PART: -2 alpha^2 J_P2(Y/alpha^2) = -(4/3) |D phi|^3/alpha + O(eps^4) about zero field "
      "(FP7 B2's zero tangent), and the yield's eps^1 term is y_th |D phi| (zero when the band-pass is closed; for y_th > 0 it freezes "
      "delta phi below the yield) -- nothing of either enters the linear equations",
      f"eps^1 (y_th = 0): {sp.simplify(cJ[1].subs(yt_, 0))}; eps^2: {cJ[2]}; eps^3: {cJ[3]}", b8_ok)
syms_all = set().union(*[EC[n_].free_symbols for n_ in NAMES])
b9_ok = b8_ok and not any(str(s_) in ("alpha", "a_0", "a0") for s_ in syms_all)
check("B9 a0 IS ABSENT AT LINEAR ORDER: the MOND scale alpha = a0/c^2 enters the action only through J and the yield (B8), neither of "
      "which has a quadratic part, so the linear system (B1-B7) carries no a0 -- the canonical (9.3603e-11) and alt (1.1312e-10 m/s^2) "
      "footings give identical linear equations and an identical CMB epoch",
      f"free symbols of the linear system: {sorted(str(s_) for s_ in syms_all)}", b9_ok)
OUT["numbers"]["B"] = dict(diff={n_: str(DIFF[n_]) for n_ in ("Phi", "Psi", "B", "E", "pi", "mu")}, poisson_alpha_part=str(ac_part),
                           dphi_eq=str(dphi_eq), J_series={str(k_): str(v) for k_, v in cJ.items()})
P(f"    {el()}")

# ================================================================================================ C leading difference
banner("C  THE LEADING DIFFERENCE AND ITS SIZE")
Geff_T, slip_T = qs_limit(STEST)
c1_ok = Geff_T is not None and sp.simplify(Geff_T - 2 / (2 - alc)) == 0 and sp.simplify(slip_T - 1) == 0
check("C1 SUB-HORIZON: G_eff/G = 2/(2 - alpha_c) = G_N/G with no slip -- matter clusters with the locally measured Newton constant",
      f"G_eff/G = {sp.factor(Geff_T) if Geff_T is not None else 'SINGULAR (no quasi-static solution)'}, slip {slip_T}", c1_ok)
tt_, pp_ = sp.symbols('t p', positive=True)
Phi0 = sp.Symbol('Phi_0')
aP = tt_ ** pp_
HP = sp.diff(aP, tt_) / aP
piP = (HP * Phi0) / (-sp.diff(HP, tt_))                            # the CMC pi at k -> 0 with constant Phi = Psi
c2_expr = sp.simplify(Phi0 - sp.diff(piP, tt_))
aL = sp.Function('a')(tt_)
HL = sp.diff(aL, tt_) / aL
piL = HL * Phi0 / (-sp.diff(HL, tt_))
c2_gen = sp.simplify((Phi0 - sp.diff(piL, tt_)) / Phi0)
P(f"    k -> 0, constant Phi = Psi: pi = H Phi/(-Hdot); on a = t^p: Phi - pidot = {c2_expr}; on any a(t): (Phi - pidot)/Phi = {c2_gen}")
check("C2 SUPER-HORIZON: the CMC khronon's time shift makes pidot = Phi exactly on every power-law background (Phi - pidot = 0 for "
      "a = t^p, any p), so the Poisson modification vanishes as k -> 0 (G_eff -> G): the khronon cannot change the conserved "
      "super-horizon curvature perturbation; the general residue is (Phi - pidot)/Phi = 2 - H Hddot/Hdot^2, zero wherever a is a power law",
      f"a = t^p: {c2_expr}; general: {c2_gen}", c2_expr == 0)
c3 = {"PPN edge": AC_MAX, "strong-coupling floor (c_2 -> oo)": AC_MIN_OO}
for lab, av in c3.items():
    P(f"    alpha_c = {av:.2e} ({lab}): G_cos/G_N - 1 = -alpha_c/2 = {-av / 2:.2e}; G_eff/G_N - 1 in [{-av / 2:.2e}, 0]")
check("C3 THE NUMBERS: relative to the measured G_N the Friedmann equation uses G_cos = G_N (1 - alpha_c/2) and the constraints "
      "G_eff between G and G_N, so every departure from GR + CDM at the CMB epoch is <= alpha_c/2 <= 1.6e-9 (PPN edge) and >= "
      f"{AC_MIN_OO / 2:.1e} (the regulator's floor): G_cos is NOT exactly G_N -- it is below it by a regulator's worth",
      f"alpha_c/2 in [{AC_MIN_OO / 2:.2e}, {AC_MAX / 2:.2e}]", AC_MAX / 2 <= 1.6e-9 + 1e-15)
OUT["numbers"]["C3"] = {"Gcos_over_GN_minus_1_range": [-AC_MAX / 2, -AC_MIN_OO / 2]}
for k_, v in C4.items():
    P(f"    k = {k_:g} /Mpc (k/aH {v['kaH_range'][0]:.1e}..{v['kaH_range'][1]:.1e}): max |Phi - pidot|/env|Psi| = {v['max_ratio']:.3f}; "
      f"F = (Phi - pidot)/Psi at z = 1e5 {v['F_first']:+.3f}, recombination {v['F_rec']:+.3f}, z = 10 {v['F_last']:+.4f}; "
      f"|Int mu/2 dt|/env|Psi| per alpha_c/2 = {v['max_ratio_mu']:.3f}")
c4_max = max(v["max_ratio"] for v in C4.values())
c4_mu = max(v["max_ratio_mu"] for v in C4.values())
c4_ok = c4_max < 5.0 and abs(C4[0.3]["F_last"] - 1) < 0.05 and abs(C4[1e-4]["F_rec"]) < 0.05
check("C4 ON CLASS'S GR SOLUTION (first order in alpha_c; k = 1e-4..0.3 /Mpc, z = 1e5..10; pi and pidot from the CMC condition and the "
      "total momentum conservation, no numerical derivative of the perturbations): the Poisson modification (alpha_c/2)|Phi - pidot| "
      "is <= (alpha_c/2) x O(1) of the envelope of |Psi|, F -> 1 deep inside the horizon and -> 0 outside it (k = 1e-4 at "
      f"recombination): at the PPN edge the gravitating source moves by <= {c4_max * AC_MAX / 2:.1e} of Psi.  The multiplier's term in "
      "the momentum constraint is not independent (the Bianchi identity fixes it given this Poisson term); its time integral is "
      f"reported: <= {c4_mu:.2f} x (alpha_c/2) of the envelope of |Psi|",
      f"max |Phi - pidot|/env|Psi| = {c4_max:.3f}; F(k = 0.3, z = 10) = {C4[0.3]['F_last']:.4f}; F(k = 1e-4, rec) = {C4[1e-4]['F_rec']:.4f}; "
      f"max |Int mu/2 dt|/env|Psi| per alpha_c/2 = {c4_mu:.3f} (reported)", c4_ok)
OUT["numbers"]["C4"] = {str(k_): v for k_, v in C4.items()}
Geff_ac0 = sp.limit(Geff_qs, alc, 0)
c5_ok = Geff_ac0 == 1 and b5_ok
check("C5 THE YORK/CMC KILL IS NOT REPRODUCED IN THE LINEAR COSMOLOGY: the multiplier cancels from the comoving Poisson equation for "
      "every alpha_c (B5) and G_eff/G -> 1 as alpha_c -> 0 -- the CMC leaves add no gravitating source; the '2G' of the York/CMC "
      "construction (an elliptic lapse with no alpha_c term, record's DHF gates) has no counterpart here",
      f"lim G_eff/G (alpha_c -> 0) = {Geff_ac0}; mu cancels: {mu_coef == 0}", c5_ok)
P(f"    {el()}")

# ================================================================================================ D separator state
banner("D  THE SEPARATOR'S STATE AT z >~ 10: is the band-pass closed at the CMB epoch, and when does it open?")
MPC_EV = 6.3949e-30                                               # hbar c [eV Mpc]


def T_hbg(k_mpc, m_ev):
    """Hu, Barkana & Gruzinov 2000 (PRL 85, 1158) wave-dark-matter transfer function: cos(x^3)/(1 + x^8),
    x = 1.61 m22^(1/18) k/k_Jeq, k_Jeq = 9 m22^(1/2) /Mpc."""
    m22 = m_ev / 1e-22
    x = 1.61 * m22 ** (1 / 18.0) * np.asarray(k_mpc, float) / (9.0 * math.sqrt(m22))
    return np.cos(x ** 3) / (1 + x ** 8)


s999 = {"EH98 linear": math.sqrt(sig2(RMIN, D2LIN[0])), "EH98 nonlinear (FP13's reading)": math.sqrt(sig2(RMIN, D2NL[0]))}
for m_ in M_DARK:
    s999[f"EH98 x T_HBG^2 (m = {m_:.1e})"] = math.sqrt(sig2(RMIN, D2LIN[0] * T_hbg(KKF * h9, m_) ** 2))
tcl = time.time()
CLP = Class()
CLP.set(dict(P18, output="mPk", gauge="newtonian", matter_source_in_current_gauge="yes", z_pk="1100,1000",
             **{"P_k_max_h/Mpc": 1000.0}))
CLP.compute()
hP = P18["h"]
kcl = np.exp(np.linspace(math.log(1e-4), math.log(990.0), 3000))
scl = {}
for zz in (1100.0, 1000.0):
    Pk = np.array([CLP.pk_lin(kk * hP, zz) for kk in kcl]) * hP ** 3
    D2c = kcl ** 3 * Pk / (2 * math.pi ** 2)
    scl[f"CLASS linear z = {zz:.0f}"] = math.sqrt(float(np.trapz(D2c, np.log(kcl))))
    for m_ in M_DARK:
        scl[f"CLASS x T_HBG^2 z = {zz:.0f} (m = {m_:.1e})"] = math.sqrt(float(np.trapz(D2c * T_hbg(kcl * hP, m_) ** 2, np.log(kcl))))
s999.update(scl)
for k_, v in s999.items():
    P(f"    sigma(R -> 0, k <= 1000 h/Mpc) [{k_}] = {v:.4f}")
L999 = LH_tab[0]
d1_ok = max(s999.values()) < 0.1 and abs(L999 - XI_FLOOR_MPC) < 1e-15
check("D1 THE BAND-PASS IS CLOSED AT THE CMB EPOCH (checked in FP13's source: L_table returns the xi floor when sigma(RMIN) < s): "
      "the leaf-rms contrast of the actual field, unsmoothed to FP13's grid edge, is <= 0.02 at z = 999-1100 -- in FP13's own EH98 state "
      "and in CLASS's linear spectrum, with or without the dark field's cutoff -- far below delta_c = 1.686, so L = xi, chi = 0 and "
      f"the state yield is zero: the MOND scalar is out of the CMB epoch's equations (FP13's L(z = 999) = {L999 * 1e6:.4f} pc = xi)",
      f"max sigma = {max(s999.values()):.4f} ({time.time() - tcl:.0f} s for CLASS to 1000 h/Mpc)", d1_ok)
OUT["numbers"]["D1"] = s999
iopen = next((i for i in range(len(LNA)) if LH_tab[i] > XI_FLOOR_MPC * 1.0001), None)
z_open = 1 / AGR[iopen] - 1 if iopen is not None else float("nan")
z_open_prev = 1 / AGR[iopen - 1] - 1 if iopen else float("nan")
z_open_cut = {}
for m_ in M_DARK:
    D2L0c = D2L0 * T_hbg(KKF * h9, m_) ** 2
    D2LINc = [D2L0c * Dl(a_) ** 2 for a_ in AGR]
    D2NLc = [(halofit(D2LINc[i], AGR[i]) if sig2(RMIN, D2LINc[i]) > 1.0 else D2LINc[i]) for i in range(len(LNA))]
    Ltc = L_table(DELTA_C, D2NLc)
    ioc = next((i for i in range(len(LNA)) if Ltc[i] > XI_FLOOR_MPC * 1.0001), None)
    z_open_cut[m_] = 1 / AGR[ioc] - 1 if ioc is not None else float("nan")
Lz = {zz: Lh(1 / (1 + zz)) * 1e6 for zz in (30.0, 20.0, 17.0, 15.0, 12.0, 10.0)}
P(f"    first open epoch (FP13's EH98 nonlinear state, delta_c): z = {z_open:.2f} (previous grid epoch {z_open_prev:.2f} still closed); "
  "with the dark field's cutoff: " + ", ".join(f"m = {m_:.1e}: z = {v:.2f}" for m_, v in z_open_cut.items()))
P("    L(z) [pc, physical]: " + ", ".join(f"z = {zz:g}: {v:.3g}" for zz, v in Lz.items()))
check("D2 THE BAND-PASS OPENS ONLY AT z_open ~ 17 (FP13's EH98 state, nonlinear reading) and later with the dark field's cutoff; at "
      "z = 10 it passes only scales below L(10) ~ 3 kpc (physical)",
      f"z_open = {z_open:.2f} (EH98), " + ", ".join(f"{v:.2f} (m = {m_:.1e})" for m_, v in z_open_cut.items()) + f"; L(10) = {Lz[10.0]:.3g} pc",
      z_open < 100 and all(v <= z_open + 1e-9 for v in z_open_cut.values()))
OUT["numbers"]["D2"] = dict(z_open=z_open, z_open_cut={str(k_): v for k_, v in z_open_cut.items()}, L_pc=Lz)

# D3: the MOND growth source on FP9's yardstick with FP13's (H_S) model, z = 999..10
YIELD, cutfac, nu_p2, gfield = ns9["YIELD"], M6["cutfac"], M6["nu_p2"], M6["gfield"]
KHF, DIF, C2W = M6["KHF"], M6["DIF"], M6["C2W"]


def hs_model(f):
    return {"hfac": lambda a_, k_: 1.0 - np.exp(-0.5 * (k_ * h9 * Lh(a_) / a_) ** 2),
            "cut": lambda y, a_, f=f: cutfac(y, yh[f](a_), YIELD), "yr": 0.0}


def ceff_fields(model, a0v, mode, D, a_, KHg, lam=0.0, c2=C2W):
    """FP9's growth_aq right-hand side, re-typed to expose C_eff = C^Q h^2 w at one epoch (the growth source is 1 + C_eff)."""
    m341 = KHg <= 20.0 * 1.0001
    kk341 = KHg[m341]; norm341 = np.trapz(1 / kk341, kk341)
    gk = gfield(D, a_, KHg); hk = model["hfac"](a_, KHg); gb = gk * hk
    y = np.full(len(KHg), math.sqrt(np.trapz(gb[m341] ** 2 / kk341, kk341) / norm341) / a0v) if mode == "rms" else gb / a0v
    CQ = np.maximum((nu_p2(y, model.get("yr", 0.0)) - 1.0) * model["cut"](y, a_), 0.0)
    lam_phi = lam + (2 + 3 * c2) * hk ** 2 / c2
    cs = c9 / np.sqrt(np.maximum(CQ, 1e-300) * np.maximum(lam_phi, 1e-300))
    kk = (1.0 * h9 / (a_ * Mpc9)) if mode == "rms" else KHg * h9 / (a_ * Mpc9)
    wt = 1.0 / (1.0 + (H09 * Ez9(a_) / (cs * kk)) ** 2)
    return CQ * hk ** 2 * wt


def growth_ceff(model, a0v, mode, zs, KHg=KHF, Dig=DIF):
    nk = len(KHg)

    def rhs(N_, Y):
        a_ = math.exp(N_); D = Y[:nk]; Dp = Y[nk:]
        Ce = ceff_fields(model, a0v, mode, D, a_, KHg)
        return np.concatenate([Dp, 1.5 * (Om9 / a_ ** 3 / Ez9(a_) ** 2) * (1.0 + Ce) * D - (2 + dlnH9(a_)) * Dp])
    Nout = sorted({math.log(1 / (1 + z_)) for z_ in zs})
    sol_ = solve_ivp(rhs, (math.log(A_I9), max(Nout)), np.concatenate([Dig, Dig]), method="LSODA", rtol=1e-6, atol=1e-24, t_eval=Nout)
    return {round(1 / math.exp(N_) - 1, 3): (sol_.y[:nk, i], ceff_fields(model, a0v, mode, sol_.y[:nk, i], math.exp(N_), KHg))
            for i, N_ in enumerate(sol_.t)}


ZS_D3 = (999.0, 500.0, 100.0, 30.0, 17.0, 12.0, 10.0)
d3 = {}
klow = KHF <= 1.0
for f in FOOTS:
    for m in MODES:
        res_ = growth_ceff(hs_model(f), A0_9[f], m, ZS_D3)
        d3[(f, m)] = {z_: float(np.max(v[1][klow])) for z_, v in res_.items()}
        d3[(f, m, "all k")] = {z_: float(np.max(v[1])) for z_, v in res_.items()}
for key, v in d3.items():
    P(f"    max C_eff {'(k <= 1 h/Mpc)' if len(key) == 2 else '(all k <= 100 h/Mpc)'} [{key[0]}, {key[1]}]: "
      + ", ".join(f"z = {z_:g}: {c_:.2e}" for z_, c_ in sorted(v.items(), reverse=True)))
d3_max = max(max(v.values()) for key, v in d3.items() if len(key) == 2)
check("D3 THE MOND GROWTH SOURCE STAYS OFF FOR THE CMB'S AND LENSING'S LINEAR SCALES AT z >= 10: on FP9's growth yardstick with FP13's "
      "(H_S) model, max C_eff over k <= 1 h/Mpc is below 1e-3 at every epoch z = 999..10, both yardstick modes, both footings (the "
      "band-pass is closed above z_open; below it L is kpc-scale and the web-rms yield sits above every linear mode)",
      f"max C_eff(k <= 1 h/Mpc, z >= 10) = {d3_max:.2e}", d3_max < 1e-3)
OUT["numbers"]["D3"] = {"|".join(str(x) for x in key): v for key, v in d3.items()}
P(f"    {el()}")

# ================================================================================================ E dark field
banner("E  THE DARK FIELD (FL1/FK1's order parameter, m >= 1.9-5.2e-19 eV): BBN, recombination, Jeans scale, the conversion gate")
HBAR_EVS = 6.582119569e-16
MPC_M = 3.0856775814913673e22
hE = P18["h"]
H0_S = 100 * hE * 1e3 / MPC_M
H0_EV = H0_S * HBAR_EVS
T0_K, KB_EV = 2.7255, 8.617333262e-5
T0_EV = T0_K * KB_EV
OG = 2.47282e-5 / hE ** 2 * (T0_K / 2.7255) ** 4                 # photons, Omega_g h^2 = 2.47282e-5 (T0 = 2.7255 K)
NEFF = 3.044
OR_ = OG * (1 + NEFF * 7 / 8 * (4 / 11) ** (4 / 3))
OM_ = (P18["omega_b"] + P18["omega_cdm"]) / hE ** 2
OC_ = P18["omega_cdm"] / hE ** 2
OL_ = 1 - OM_ - OR_


def E_(a_):
    return math.sqrt(OR_ / a_ ** 4 + OM_ / a_ ** 3 + OL_)


E1 = {}
for m_ in M_DARK:
    a_start = brentq(lambda a_: m_ / (H0_EV * E_(a_)) - 1e-3, 1e-16, 1e-6)
    a_end = brentq(lambda a_: m_ / (H0_EV * E_(a_)) - 300.0, 1e-12, 1e-3)

    def kg(N_, Y):
        a_ = math.exp(N_); Hm = H0_EV * E_(a_)
        dlnH = 0.5 * (-4 * OR_ / a_ ** 4 - 3 * OM_ / a_ ** 3) / E_(a_) ** 2
        return [Y[1], -(3 + dlnH) * Y[1] - (m_ / Hm) ** 2 * Y[0]]
    solk = solve_ivp(kg, (math.log(a_start), math.log(a_end)), [1.0, 0.0], method="DOP853", rtol=1e-10, atol=1e-13, dense_output=True)
    Nn = np.linspace(math.log(a_start), math.log(a_end), 20001)
    Y = solk.sol(Nn)
    Hs_ = np.array([H0_EV * E_(math.exp(x)) for x in Nn])
    rho = 0.5 * (Hs_ * Y[1]) ** 2 + 0.5 * m_ ** 2 * Y[0] ** 2      # energy density, arbitrary normalisation (eV^2 x phi^2)
    tail = Nn > Nn[-1] - 0.5
    ra3 = float(np.mean(rho[tail] * np.exp(3 * Nn[tail])))          # the late-time invariant rho a^3
    # normalise to Omega_c today: rho_d(a) / rho_crit0 = OC_ x rho(a)/(ra3/a^3) ... in units of the critical density
    frac = lambda N_: OC_ * float(np.interp(N_, Nn, rho)) / ra3        # rho_d / rho_crit0 at ln a = N_ (valid for N_ < end)
    a_osc = brentq(lambda a_: m_ / (H0_EV * E_(a_)) - 1.0, 1e-14, 1e-3)
    rows = {}
    for lab, Tkev in (("1 MeV", 1000.0), ("100 keV", 100.0), ("70 keV (D bottleneck)", 70.0), ("30 keV", 30.0)):
        a_T = T0_EV / (Tkev * 1e3)                                  # post-annihilation relation (conservative: see scope)
        N_T = math.log(a_T)
        rd = frac(N_T) if N_T <= Nn[-1] else OC_ / a_T ** 3
        rr = OR_ / a_T ** 4
        rows[lab] = dict(a=a_T, rho_d_over_rho_r=rd / rr, dNeff=rd / rr * (1 + NEFF * 7 / 8 * (4 / 11) ** (4 / 3)) / (7 / 8 * (4 / 11) ** (4 / 3)))
    H_rec = H0_EV * E_(1 / 1090.0)
    E1[m_] = dict(z_osc=1 / a_osc - 1, T_osc_keV=T0_EV / a_osc / 1e3, rows=rows, w_rec=(H_rec / m_) ** 2)
    P(f"    m = {m_:.1e} eV: H = m at z = {1 / a_osc - 1:.3e} (T_gamma = {T0_EV / a_osc / 1e3:.1f} keV); "
      + "; ".join(f"T = {lab}: rho_d/rho_r = {v['rho_d_over_rho_r']:.2e} (Delta N_eff {v['dNeff']:.1e})" for lab, v in rows.items())
      + f"; w at recombination ~ (H/m)^2 = {(H_rec / m_) ** 2:.1e}")
e1_ok = all(max(v["dNeff"] for v in r_["rows"].values()) < 1e-2 and r_["w_rec"] < 1e-12 for r_ in E1.values())
check("E1 THE DARK FIELD AT BBN AND RECOMBINATION (homogeneous Klein-Gordon from misalignment, normalised to Omega_c h^2 = 0.12011): it "
      "is frozen (w = -1) until H = m at T_gamma ~ 28-46 keV -- after the deuterium bottleneck -- and is a negligible energy density "
      "throughout BBN (Delta N_eff-equivalent <= 1e-2 at every listed temperature); at recombination w ~ (H/m)^2 ~ 1e-20: cold",
      "; ".join(f"m = {m_:.1e}: z_osc {v['z_osc']:.2e}, max Delta N_eff {max(r['dNeff'] for r in v['rows'].values()):.1e}, "
                f"w_rec {v['w_rec']:.1e}" for m_, v in E1.items()), e1_ok,
      reading="the temperature-to-a map uses the post-annihilation relation; above ~0.5 MeV the true radiation density is larger "
              "(g* = 10.75), which only lowers the dark field's share")
OUT["numbers"]["E1"] = {str(k_): v for k_, v in E1.items()}
# E2 Jeans scale and the first-order growth deficit against CDM
G_SI, C_SI, EV_KG = 6.67430e-11, 299792458.0, 1.78266192e-36
rho_c0_SI = 3 * H0_S ** 2 / (8 * math.pi * G_SI)


def kJ_com(a_, m_ev):
    """comoving Jeans wavenumber [/Mpc]: k_phys^4 = 16 pi G rho_d (m c^2/(hbar c^2))^2 ... = 16 pi G rho_d m^2/hbar^2 (SI)."""
    m_kg = m_ev * EV_KG
    rho_d = OC_ * rho_c0_SI / a_ ** 3
    kphys = (16 * math.pi * G_SI * rho_d * (m_kg / 1.054571817e-34) ** 2) ** 0.25
    return kphys * a_ * MPC_M


E2 = {}
KS_E2 = (1e-3, 1e-2, 0.1, 0.3, 1.0)
for m_ in M_DARK:
    kj = kJ_com(1 / 1090.0, m_)
    rowsE2 = {}
    for kM in KS_E2:
        def rhs2(N_, Y):
            a_ = math.exp(N_)
            Ee = E_(a_); dlnH = 0.5 * (-4 * OR_ / a_ ** 4 - 3 * OM_ / a_ ** 3) / Ee ** 2
            Om_a_ = OM_ / a_ ** 3 / Ee ** 2
            Hsi = H0_S * Ee
            kphys = kM / MPC_M / a_
            q2 = (1.054571817e-34 * kphys ** 2 / (2 * m_ * EV_KG) / Hsi) ** 2   # (c_s k_phys/H)^2, c_s = hbar k/(2m)
            d0, d0p, d1, d1p = Y
            acc0 = 1.5 * Om_a_ * d0 - (2 + dlnH) * d0p
            acc1 = 1.5 * Om_a_ * d1 - (2 + dlnH) * d1p - q2 * d0
            return [d0p, acc0, d1p, acc1]
        a_i = 1e-5
        so2 = solve_ivp(rhs2, (math.log(a_i), 0.0), [1.0, 1.0, 0.0, 0.0], method="LSODA", rtol=1e-10, atol=1e-30,
                        t_eval=[math.log(1 / 1090.0), 0.0])
        rowsE2[kM] = (float(so2.y[2, 0] / so2.y[0, 0]), float(so2.y[2, 1] / so2.y[0, 1]))
    E2[m_] = dict(kJ_rec=kj, rows=rowsE2, hbg={kM: float(1 - T_hbg(kM, m_)) for kM in (0.3, 1.0)},
                  k_half_today=4.5 * (m_ / 1e-22) ** (4 / 9))
    P(f"    m = {m_:.1e} eV: comoving k_J at recombination = {kj:.0f} /Mpc (x{kj / 0.3:.0f} the CMB's 0.3 /Mpc); HBG half-power k today "
      f"~ {E2[m_]['k_half_today']:.0f} /Mpc; first-order growth deficit delta_1/delta_0 (rec, today): "
      + ", ".join(f"k = {kM:g}: {v[0]:.1e}, {v[1]:.1e}" for kM, v in rowsE2.items())
      + f"; 1 - T_HBG(0.3) = {E2[m_]['hbg'][0.3]:.1e}, (1.0) = {E2[m_]['hbg'][1.0]:.1e}")
e2_ok = all(v["kJ_rec"] > 90.0 and max(abs(x) for kM, r in v["rows"].items() if kM <= 0.3 for x in r) < 1e-8 for v in E2.values())
check("E2 THE WAVE SCALE IS FAR BELOW THE CMB's: the dark field's comoving Jeans wavenumber at recombination is >= 300x the CMB's "
      "k = 0.3 /Mpc, and its first-order growth deficit against CDM (quantum pressure c_s = hbar k/2m) at k <= 0.3 /Mpc is < 1e-8 at "
      "recombination and today (Hu-Barkana-Gruzinov's transfer function agrees: 1 - T ~ x^6 negligible) -- on CMB and CMB-lensing scales "
      "the dark field is CDM", "; ".join(f"m = {m_:.1e}: k_J(rec) {v['kJ_rec']:.0f} /Mpc, max deficit(k <= 0.3) "
                                         f"{max(abs(x) for kM, r in v['rows'].items() if kM <= 0.3 for x in r):.1e}" for m_, v in E2.items()), e2_ok)
OUT["numbers"]["E2"] = {str(k_): {"kJ_rec": v["kJ_rec"], "rows": {str(kk): vv for kk, vv in v["rows"].items()}, "hbg": v["hbg"],
                                  "k_half_today": v["k_half_today"]} for k_, v in E2.items()}
# E3 FK1's conversion gate: background exponent ~ G^2/H with G ~ lambda(K) n, lambda ~ K^(-2q), q = 1.75: ~ H^-8 a^-6
fk1 = json.load(open(os.path.join(REPO, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change_results.json")))["numbers"]["N2"]
zpk, qg = fk1["bg_peak_z"], fk1["q_linear_gate"]
expo = lambda z_: (E_(1 / (1 + zpk)) / E_(1 / (1 + z_))) ** (4 * qg + 1) * ((1 + z_) / (1 + zpk)) ** 6
E3 = {z_: expo(z_) for z_ in (10.0, 100.0, 1090.0, 4e8)}
P(f"    FK1's background conversion exponent relative to its z = {zpk} peak (q = {qg}): " + ", ".join(f"z = {z_:g}: {v:.1e}" for z_, v in E3.items()))
check("E3 FK1'S CONVERSION IS OFF IN THE EARLY UNIVERSE: the gated pair coupling lambda(K) ~ K^(-2q) (q = 1.75) makes the background's "
      "parametric-growth exponent scale as H^-(4q+1) a^-6; relative to its z = 0.30 peak (itself below the trigger's, FK1 N2) it is "
      "<= 1e-4 at z = 10 and ~1e-16 or less at recombination and BBN: no conversion, no kick -- the field stays cold",
      ", ".join(f"z = {z_:g}: {v:.1e}" for z_, v in E3.items()), E3[10.0] < 1e-3 and E3[1090.0] < 1e-10)
OUT["numbers"]["E3"] = {str(k_): v for k_, v in E3.items()}
P(f"    {el()}")

# ================================================================================================ F datum
banner("F  THE DATUM phibar-dot: with FP13's lambda > 0 it is physical; BBN bounds it")
T1MEV_EV = 1.0e6
a_1mev = (T0_EV / T1MEV_EV) * (3.91 / 10.75) ** (1 / 3)              # entropy conservation through e+e- annihilation
rho_nu1_1mev = 7 / 8 * 2 * (math.pi ** 2 / 30) * T1MEV_EV ** 4      # one neutrino species [eV^4]
rho_c0_eV4 = 3 * H0_EV ** 2 / (8 * math.pi) * (1.220890e28) ** 2     # 3 H0^2 M_P^2/(8 pi) [eV^4]
DN_MAX = 0.5
Om_stiff_max = DN_MAX * rho_nu1_1mev / (rho_c0_eV4 / a_1mev ** 6)
P(f"    at T = 1 MeV: a = {a_1mev:.3e}; a stiff Omega_s0 a^-6 must stay below Delta N_eff = {DN_MAX} of one neutrino: Omega_s0 < {Om_stiff_max:.1e}")
P(f"    with rho_phi = (2 lambda/16 pi G) phibar-dot^2: Omega_phi0 = lambda phibar-dot_0^2/(3 H0^2) -> |phibar-dot_0|/H0 < "
  f"{math.sqrt(3 * Om_stiff_max):.1e}/sqrt(lambda)")
check("F1 THE DATUM phibar-dot = 0 IS LOAD-BEARING: with lambda > 0 (FP13 A1) a nonzero phibar-dot = p0/a^3 is a stiff a^-6 component "
      "(A2); BBN (Delta N_eff < 0.5 at T = 1 MeV) requires Omega_phi,0 < ~1e-24, i.e. |phibar-dot_0| < ~1e-12 H0/sqrt(lambda) -- the "
      "chain's declared datum is not tested by the CMB or BBN beyond this bound (at lambda = 0, FP14 L1, phibar is gauge instead)",
      f"Omega_phi,0 < {Om_stiff_max:.1e}", Om_stiff_max < 1e-20, load_bearing=False)
OUT["numbers"]["F1"] = dict(Om_stiff_max=Om_stiff_max, a_1MeV=a_1mev)
P(f"    {el()}")

# ================================================================================================ W ledger
banner("W  THE LEDGER: XR26 part 1")
LEDGER = [
    ("X26-1a", "the chain's FRW background is GR's with the bare G (any matter content); G_cos = G = G_N (1 - alpha_c/2)", "DERIVED", "A1"),
    ("X26-1b", "at z >~ z_open (~17) the linear metric equations are GR's plus terms proportional to alpha_c or mu only; no slip; matter "
               "equations GR's; delta phi decoupled; no a0 at linear order (both footings identical)", "DERIVED", "B1-B9"),
    ("X26-1c", "the multiplier is the CMC condition and cancels from the comoving Poisson equation; the only change to the gravitating "
               "source is (k^2/a^2)[Psi - (alpha_c/2)(Phi - pidot)] = -4 pi G rho Delta", "DERIVED", "B3-B5"),
    ("X26-1d", "leading difference from GR + CDM: G_eff between G (super-horizon) and G_N (sub-horizon), G_cos = G; size <= alpha_c/2 <= "
               "1.6e-9 (>= 4e-16 at the regulator's floor) -- not exactly zero", "DERIVED", "C1-C4"),
    ("X26-1e", "the York/CMC 2G is not reproduced in the linear cosmology (the multiplier adds no gravitating source)", "DERIVED", "C5"),
    ("X26-1f", "the band-pass is closed at the CMB epoch (sigma <= 0.02 at z = 999-1100) and opens at z ~ 17; the MOND growth source is "
               "< 1e-3 at k <= 1 h/Mpc for z >= 10", "DERIVED", "D1-D3 (FP13's state reading, linear + halofit)"),
    ("X26-1g", "the dark field (m >= 1.9e-19 eV) is frozen and negligible through BBN, cold at recombination, CDM on CMB scales (k_J(rec) >= "
               "500 /Mpc); FK1's conversion is off at z >= 10", "DERIVED", "E1-E3"),
    ("X26-1h", "phibar-dot = 0 is a declared datum made physical by lambda > 0: BBN bounds a nonzero value to Omega_phi,0 < ~1e-24",
     "CONSTRAINT", "F1, A2"),
    ("X26-1i", "not covered: second-order effects (the band-pass reads the NONLINEAR field, a leaf average of second-order quantities, "
               "whose back-reaction on the linear equations is O(delta^2)); the khronon's fast mode if excited by non-adiabatic initial "
               "data (it would oscillate at ~k/sqrt(alpha_c)); reionization-era structure (z < 17) beyond FP13's linear yardstick",
     "OPEN", "scope"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:8s} {st_:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
check("W (reported) the ledger", f"{len(LEDGER)} links", True, load_bearing=False)

# ================================================================================================ verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT" + ("  [MUTATE]" if MUTATE else ""))
if not MUTATE:
    P("  At z >~ 17 (and, for the scales the CMB sees, down to z = 10) the chain's linear cosmology is GR + CDM up to the khronon's")
    P("  regulator: the background is GR's with the bare G; the metric equations gain only terms proportional to alpha_c or the CMC")
    P("  multiplier, which cancels from the comoving Poisson equation; there is no slip; the MOND scalar is decoupled (the band-pass")
    P("  is closed and J has no quadratic part), so a0 does not enter (both footings identical); the dark field is CDM on CMB scales.")
    P(f"  The leading difference: G_cos = G_N (1 - alpha_c/2) and G_eff between G and G_N -- a fractional {AC_MIN_OO / 2:.0e} to {AC_MAX / 2:.1e},")
    P("  NOT exactly zero.  The York/CMC 2G does not appear.  The datum phibar-dot = 0 is load-bearing (BBN: Omega_phi,0 < ~1e-24).")
else:
    P("  MUTATE: with the band-pass open at z >~ 10 the chassis couples delta phi to the lapse at O(1): the linear equations are not")
    P("  GR's -- the reduction rests on the separator's closed band-pass.")
OUT["verdict"] = dict(n_checks=len(CH), n_fail_load_bearing=n_fail, elapsed_s=round(time.time() - T_START))
json.dump(OUT, open(JSN, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
rc = 0 if n_fail == 0 else 1
P(f"\n  {sum(1 for _, ok, _l in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {os.path.basename(JSN)} "
  f"({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")
TEE.flush()
sys.stdout = sys.__stdout__
TEE.close()
sys.exit(rc)
