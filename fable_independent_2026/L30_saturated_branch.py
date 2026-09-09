#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L30 -- J(Y) beyond saturation: is the carried kernel's saturated branch repairable, and at what price?
======================================================================================================
L13's check P9 found that the action as published is NOT twice-differentiable at the background the
Solar System sits on.  The carried kernel (THE_ACTION 2026-09-05 section 3) is

    nu_RAR,  g = g_N / (1 - e^{-sqrt(s)}),  s = g_N/a0,   i.e.   Delta(s) = s/(e^{sqrt(s)} - 1)

up to s_sat = 2.540 and SATURATED, Delta = C = 0.6476, above it.  On the saturated branch Delta'(s) = 0
identically, so the MOND scalar's longitudinal stiffness Sigma_par = 1/Delta' is INFINITE and its cubic
action cannot be written.  The saturation is not optional: PAPER5's bounded-boost / carrier theorem
(g03x Y1) proves that a matter-sourced scalar obeying div[J_Y grad phi] = 4 pi G rho satisfies
J_Y(g_phi) g_phi = g_N, so g_phi must be a single-valued monotone function of g_N, and Delta bounded
therefore forces saturation at its own maximum.  The theory is required to saturate AND required to
have finite stiffness, and the published kernel does the first by violating the second.

THE QUESTION.  What is J(Y) beyond saturation, and can it be bounded AND C^2 with Sigma_par > 0?

WHAT IS DONE HERE.
  1. Sigma_par and Sigma_perp written from J(Y) exactly, and the cubic vertex, showing precisely which
     coefficient diverges when Delta' -> 0.
  2. The conditions a continuation must meet, and a structural theorem about what they cost.
  3. Three explicit continuations, each C^2, bounded, strictly increasing, constructed and verified.
  4. Each one run through the repository's OWN Solar-System gate (the g02/g03b filtered-phantom
     machinery that produced the standing floors, imported unedited exactly as g03x imports it), and
     then through the EXACT fourth-order spherical equation of the carrier reading -- the equation that
     only exists once a continuation is supplied.
  5. The SPARC Newtonian-limit statistic, which is the one observable a constant residual force touches.

CONTROLS (must pass, or nothing below counts)
  K0  the carried kernel's saturation point s_sat = 2.540 and boost ceiling C = 0.6476 (THE_ACTION s3)
  K1  PAPER5 Table 1's five kernel ceilings
  K2  the stiffness identities Sigma_par = 1/Delta' = J_Y + 2 Y J_YY and Sigma_perp = J_Y = s/Delta
  K3  the filtered-phantom gate reproduces g03x's published floors for nu_RAR CARRIED (0.10 / 0.15 pc)
  K4  the fourth-order solver's stencil reproduces the exact biharmonic cone w = GM/(2 xi^2)
  K5  the same solver at xi -> 0 reproduces the algebraic law w = a0 Delta(s)
  K6  all 54 exact solves reproduce the analytic interior prediction min[GM/(2 xi^2), C_inf a0]

FINDINGS (checks that can fail)
  P1-P3  the published kernel's Sigma_par, the injectivity of s -> Y, and the cubic vertex J_YY
  T1-T3  the conditions, their mutual satisfiability, and the residual force they force
  E*     each candidate continuation against every condition
  G1     do the standing gates discriminate between the continuations and the published kernel?
  G2     the exact fourth-order carrier equation: the Solar-System residual and the xi floor
  S1     are the two placements of the coherence operator (inside / outside J) equivalent?
  G3     the SPARC Newtonian-limit statistic against the constant residual
  G4     where the saturated branch is actually realised, given the coherence length

Both a0 footings throughout.  An admissible continuation repairs a real hole; a proof that none is
admissible is sharper.  Neither is assumed.
"""
import os, sys, io, math, glob, time, contextlib, warnings
import numpy as np
import sympy as sp
import scipy.sparse as sps
import scipy.sparse.linalg as spl
warnings.filterwarnings("ignore")

T0 = time.time()
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CLOS = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026")

PC = 3.0857e16; AU = 1.495978707e11; G = 6.6743e-11; MSUN = 1.98892e30; GM = 1.32712440018e20
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
kpc = 3.0857e19

print("=" * 122)
print("L30 -- J(Y) beyond saturation: conditions, explicit continuations, and the Solar-System price")
print("=" * 122, flush=True)

# =====================================================================================================
# 0.  the carried kernel and its saturation  (CONTROLS K0, K1)
# =====================================================================================================
print("\n0.  THE CARRIED KERNEL AND ITS SATURATION  (controls)")

def D_rar_raw(s):
    """Delta(s) = s/(e^sqrt(s) - 1) for nu_RAR, g = g_N/(1 - e^{-sqrt(s)}).  Unsaturated."""
    s = np.asarray(s, float)
    return np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)

SS = np.logspace(-8, 8, 800001)
D_rar_tab = D_rar_raw(SS)
i_r = int(np.nanargmax(D_rar_tab))
S_SAT = float(SS[i_r]); C_SAT = float(D_rar_tab[i_r])
print(f"    nu_RAR:  maximum of Delta at s_sat = {S_SAT:.4f},  ceiling C = {C_SAT:.4f}")
check("K0 [control] the carried kernel's saturation point and boost ceiling reproduce THE_ACTION section 3 "
      "(s_sat = 2.540, C = 0.6476)",
      abs(S_SAT - 2.540) < 0.005 and abs(C_SAT - 0.6476) < 0.0005, f"s_sat = {S_SAT:.4f}, C = {C_SAT:.4f}")

def sup_delta(nu):
    d = SS*(nu(SS) - 1.0)
    return float(np.nanmax(d))
KERNELS_C = {
    "deep-MOND sqrt": (lambda s: 1.0/np.sqrt(s), 0.2500),
    "standard mu":    (lambda s: np.sqrt(0.5 + 0.5*np.sqrt(1 + 4/s**2)), 0.3003),
    "exponential":    (None, 0.3679),
    "nu_RAR":         (lambda s: 1/(1 - np.exp(-np.sqrt(s))), 0.6476),
    "simple mu":      (lambda s: 0.5 + 0.5*np.sqrt(1 + 4/s), 1.0000),
}
tabC = {}
for nm, (fn, ref) in KERNELS_C.items():
    if fn is None:
        tabC[nm] = (1/math.e, ref)                                # exact: Delta = y e^{-y}, max 1/e
    else:
        tabC[nm] = (sup_delta(fn), ref)
print("    PAPER5 Table 1, recomputed:  " + ",  ".join(f"{nm} {v:.4f} (ref {r:.4f})" for nm, (v, r) in tabC.items()))
check("K1 [control] the five kernel ceilings of PAPER5 Table 1 are reproduced to 0.5%",
      all(abs(v/r - 1) < 0.005 for v, r in tabC.values()))

# the published carried kernel
def Delta_published(s):
    s = np.asarray(s, float)
    return np.where(s > S_SAT, C_SAT, D_rar_raw(s))

# =====================================================================================================
# 1.  Sigma_par, Sigma_perp and the cubic vertex, from J(Y)   (K2, P1-P3)
# =====================================================================================================
print("\n1.  THE STIFFNESSES AND THE CUBIC VERTEX, WRITTEN FROM J(Y)")
print("""    Action:  L_phi = 2(2-K_B) J^mu d_mu phi - (2-K_B) J(Y),  Y = V.V = |grad phi|^2  (THE_ACTION s1).
    Static variation (PAPER5 s7, g03x's own equation):   div[ J_Y(Y) grad phi ] = 4 pi G rho,
    so on a sphere  J_Y(g_phi) g_phi = g_N.  With g_phi = a0 Delta(s), s = g_N/a0:

        J_Y(s)      = s/Delta(s)                                  [the transverse stiffness Sigma_perp]
        Sigma_par   = J_Y + 2 Y J_YY = d g_N/d g_phi = 1/Delta'(s)
        L_2         = Sigma_par (d_par dphi)^2 + Sigma_perp |d_perp dphi|^2
        L_3         = 2 J_YY (Vbar.d dphi) |d dphi|^2 + (4/3) J_YYY (Vbar.d dphi)^3
        J_YY        = (Delta - s Delta') / (2 a0^2 Delta^3 Delta')

    Every cubic coefficient carries J_YY, whose denominator is Delta'.  Delta' -> 0 is therefore not a
    modelling nicety: it is the point at which the quadratic action degenerates (Sigma_par -> infinity,
    the longitudinal mode becomes a constraint) and the cubic action ceases to exist.""")

def num_d(f, s, h=1e-6):
    s = np.asarray(s, float)
    return (f(s*(1 + h)) - f(s*(1 - h)))/(2*s*h)

# K2: verify the identities on the UNSATURATED branch, where everything is finite
s_test = np.array([0.05, 0.2, 0.6, 1.2, 2.0])
a0c = A0["canonical"]
Dv = D_rar_raw(s_test); Dp = num_d(D_rar_raw, s_test)
JY = s_test/Dv
gN = a0c*s_test; gphi = a0c*Dv
dgN_dgphi = num_d(lambda x: a0c*x/D_rar_raw(x), a0c*Dv)  # placeholder, replaced below by the direct ratio
# direct: d g_N / d g_phi = (d g_N/ds)/(d g_phi/ds) = a0/(a0 Delta') = 1/Delta'
dgN_dgphi = 1.0/Dp
Y = gphi**2
JYY = (Dv - s_test*Dp)/(2*a0c**2*Dv**3*Dp)
Sig_par_id = JY + 2*Y*JYY
err_id = float(np.max(np.abs(Sig_par_id/dgN_dgphi - 1)))
print(f"    Sigma_par two ways (5 points on the unsaturated branch): max relative difference {err_id:.2e}")
check("K2 [control] Sigma_par = J_Y + 2 Y J_YY and Sigma_par = 1/Delta'(s) agree to 1e-5, and Sigma_perp = J_Y = s/Delta",
      err_id < 1e-5 and np.allclose(JY, s_test/Dv), f"max rel diff {err_id:.2e}")

# P1: the published kernel's longitudinal stiffness
s_solar = {"Saturn (9.54 AU)": GM/((9.54*AU)**2*a0c), "Earth (1 AU)": GM/(AU**2*a0c),
           "inner galaxy (g_N = 10 a0)": 10.0, "inner galaxy (g_N = 100 a0)": 100.0}
print("    the published carried kernel, at four backgrounds:")
for nm, sv in s_solar.items():
    dp = float(num_d(Delta_published, np.array([sv]))[0])
    print(f"        s = {sv:11.4g}  ({nm:28s}):  Delta = {float(Delta_published(sv)):.4f},  Delta' = {dp:.3e},  "
          f"Sigma_par = {'INFINITE' if abs(dp) < 1e-14 else f'{1/dp:.3e}'}")
dp_sat = float(num_d(Delta_published, np.array([s_solar['Saturn (9.54 AU)']]))[0])
check("P1 the published carried kernel has a FINITE longitudinal stiffness Sigma_par = 1/Delta' at the "
      "Solar-System background (Saturn's orbit)",
      abs(dp_sat) > 1e-14, f"Delta'(s = {s_solar['Saturn (9.54 AU)']:.3g}) = {dp_sat:.1e} exactly, so Sigma_par is infinite -- L13's P9 reproduced")

# P2: injectivity of s -> Y
dY_ds = 2*a0c**2*Delta_published(SS)*num_d(Delta_published, SS)
frac_zero = float(np.mean(np.abs(dY_ds[SS > S_SAT]) < 1e-40*a0c**2))
check("P2 the map s -> Y = (a0 Delta)^2 is injective, so J_Y is a genuine FUNCTION of Y over the whole "
      "acceleration range the theory must cover",
      frac_zero < 0.01,
      f"dY/ds = 0 on {100*frac_zero:.0f}% of s > s_sat: J_Y(Y) is a VERTICAL SEGMENT at Y = (C a0)^2 = "
      f"{(C_SAT*a0c)**2:.3e} (m/s^2)^2, not a function")

# P3: the cubic vertex
print("    the cubic vertex J_YY = (Delta - s Delta')/(2 a0^2 Delta^3 Delta'), approaching s_sat from BELOW "
      "on the\n    published nu_RAR branch (so this is not an artefact of the splice):")
for f_ in (0.99, 0.999, 0.9999, 1.0):
    sv = S_SAT*f_
    dp = float(num_d(D_rar_raw, np.array([sv]))[0]) if f_ < 1.0 else 0.0
    dv = float(D_rar_raw(sv))
    jyy = (dv - sv*dp)/(2*a0c**2*dv**3*dp) if dp > 0 else float("inf")
    print(f"        s = {f_:.4f} s_sat:  Delta' = {dp:.3e},  J_YY = {jyy:.3e}")
JYY_solar = float("inf")
check("P3 the cubic vertex coefficient J_YY is finite at the background the published carried kernel puts "
      "the Solar System on, so the MOND scalar's cubic action can be written there",
      math.isfinite(JYY_solar),
      "J_YY diverges like 1/Delta' and Delta' = 0 identically for s > s_sat; the divergence is the MAXIMUM "
      "of Delta, approached from below on nu_RAR's own branch, so no choice of 'what happens above s_sat' "
      "removes it without moving the maximum")

# =====================================================================================================
# 2.  the conditions, and what they cost   (T1-T4)
# =====================================================================================================
print("\n2.  THE CONDITIONS A CONTINUATION MUST SATISFY, AND THE STRUCTURAL THEOREM")
print("""    C1  bounded boost          Delta(s) <= C_max for all s          (PAPER5's theorem)
    C2  single-valued carrier   s -> Delta(s) invertible               (the carrier theorem)
    C3  positive stiffness      Delta'(s) > 0 strictly, all s          (well-posedness of the static PDE)
    C4  C^2                     Delta in C^2, equivalently J in C^3 on its domain
    C5  Newtonian limit         the residual force a0 Delta(s) must not GROW at high acceleration

    THEOREM L30-1 (satisfiable, at a price).  C1 + C3 force Delta to be strictly increasing and bounded,
    hence to converge to a finite limit C_inf = sup Delta > 0.  Therefore
        (a) the conditions ARE mutually satisfiable (constructed below), and
        (b) the residual scalar force tends to the CONSTANT C_inf a0, never to zero.
    Corollary: NO kernel whose excess vanishes in the Newtonian limit -- nu_RAR itself included, whose
    Delta -> 0 like s e^{-sqrt s} -- can be carried by a matter-sourced scalar, because Delta(1) > 0 and
    Delta -> 0 force Delta' < 0 somewhere.  C5 is satisfied ("does not grow") but the stronger and more
    natural reading ("vanishes") is INCOMPATIBLE with C3.  The published saturated kernel already pays
    this price; the continuation does not add it.

    THEOREM L30-2 (the shape of J).  C1 + C3 require J_Y(Y) -> +infinity as Y -> Y_max = (C_inf a0)^2,
    because J_Y(g_phi) g_phi = g_N must run to infinity while g_phi stays below C_inf a0.  So J is defined
    only on [0, Y_max) with a vertical asymptote at the endpoint: the scalar's gradient is bounded by
    construction, a Born-Infeld-like structure, and |grad phi| < C_inf a0 is a hard kinematic bound.""")

# T3 checked here on the published kernel; T1/T2 after the candidates are built
Dp_rar = num_d(D_rar_raw, SS)
check("T3 the kernel THE_ACTION carries satisfies all five conditions",
      bool(np.any(num_d(Delta_published, SS[SS > S_SAT]) > 0)),
      "the PUBLISHED (saturated) kernel meets C1, C2 and C5 but violates C3 (Delta' = 0 identically above "
      f"s_sat) and C4; the UNSATURATED nu_RAR meets C4 and C5 in its stronger form but violates C2 and C3 "
      f"(Delta' < 0 on {100*np.mean(Dp_rar < 0):.0f}% of the range, minimum {float(np.nanmin(Dp_rar)):.4f}). "
      "Neither is admissible, and they fail on complementary conditions")

# =====================================================================================================
# 3.  three explicit continuations
# =====================================================================================================
print("\n3.  THREE EXPLICIT CONTINUATIONS")

# ---- candidate A: a pole in J_Y, closed form.  J_Y(u) = u/(1 - (u/Cinf)^p),  u = Delta
def make_A(Cinf, p, N=200001):
    """J_Y(u) = u/(1 - (u/C)^p) with u = Delta, so s(u) = u^2/(1 - (u/C)^p) exactly.  The inverse is
    tabulated in TWO charts -- u for the deep branch, eps = 1 - u/C for the near-ceiling branch, where
    1 - (u/C)^p = -expm1(p log1p(-eps)) is evaluated without cancellation -- so Delta and Delta' come
    from the SAME eps and are consistent to machine precision over 300 decades in s."""
    u_lo = Cinf*np.logspace(-14, math.log10(0.5), N)
    omz_lo = 1 - (u_lo/Cinf)**p
    s_lo = u_lo**2/omz_lo
    ep_hi = np.logspace(-300, math.log10(0.5), N)[::-1]                          # eps decreasing -> s increasing
    u_hi = Cinf*(1 - ep_hi)
    omz_hi = -np.expm1(p*np.log1p(-ep_hi))
    s_hi = u_hi**2/omz_hi
    S_MID = float(s_lo[-1])
    L_lo, LU_lo = np.log(s_lo), np.log(u_lo)
    L_hi, LE_hi = np.log(s_hi), np.log(ep_hi)
    def _eps_u(s):
        """table seed + 6 Newton refinements IN THE RIGHT CHART, so both Delta and Delta' are exact to
        machine precision on either side of the seam and the seam leaves no trace."""
        s = np.asarray(np.maximum(s, 1e-300), float); ls = np.log(s)
        lo = s <= S_MID
        lu = np.interp(ls, L_lo, LU_lo)                                          # log u, deep chart
        for _ in range(3):                                                       # s = u^2/(1-(u/C)^p)
            uu = np.exp(lu); zz = (uu/Cinf)**p
            f = 2*lu - np.log1p(-zz) - ls
            df = 2 + p*zz/(1 - zz)
            lu = lu - f/df
        le = np.interp(ls, L_hi, LE_hi)                                          # log eps, ceiling chart
        for _ in range(3):                                                       # s = C^2(1-e)^2/omz(e)
            ee = np.clip(np.exp(le), 1e-320, 1 - 1e-16); om = -np.expm1(p*np.log1p(-ee))
            f = 2*np.log(Cinf*(1 - ee)) - np.log(om) - ls
            dfde = -2/(1 - ee) - p*(1 - om)/((1 - ee)*om)
            le = le - f/(dfde*ee)
        eps = np.where(lo, 1 - np.exp(lu)/Cinf, np.exp(le))
        return eps, np.where(lo, np.exp(lu), Cinf*(1 - np.exp(le)))
    def Delta(s):
        s = np.asarray(s, float)
        _, uu = _eps_u(s)
        return np.where(s <= 0, 0.0, uu)
    def JY_of_u(uu):                                                             # exact, no inversion needed
        uu = np.asarray(uu, float); zz = (np.minimum(uu, Cinf*(1 - 1e-15))/Cinf)**p
        return uu/np.maximum(1 - zz, 1e-300)
    def log10_dD(s):
        eps, uu = _eps_u(s)
        omz = np.where(eps > 1e-8, 1 - (np.minimum(uu, Cinf)/Cinf)**p, -np.expm1(p*np.log1p(-eps)))
        omz = np.maximum(omz, 1e-320)
        ds_du = (2*uu*omz + p*uu*(1 - omz))/omz**2
        return -np.log10(ds_du)
    return Delta, JY_of_u, log10_dD, dict(Cinf=Cinf, p=p)

# fit (Cinf, p) to nu_RAR over the range the data constrain
s_fit = np.logspace(-3, math.log10(S_SAT), 400)
tgt = D_rar_raw(s_fit)
best = None
for Cinf in np.linspace(0.60, 1.30, 71):
    for p in np.linspace(0.5, 8.0, 76):
        Df = make_A(Cinf, p, 6001)[0]
        e = float(np.max(np.abs(Df(s_fit) - tgt)))
        if best is None or e < best[0]: best = (e, Cinf, p)
errA, CinfA, pA = best
Delta_A, JYu_A, LD_A, parA = make_A(CinfA, pA)
print(f"    A  pole family   J_Y(u) = u/(1 - (u/C_inf)^p)   ->  s(u) = u^2/(1 - (u/C_inf)^p)")
print(f"       fitted to nu_RAR over 1e-3 <= s <= s_sat:  C_inf = {CinfA:.4f}, p = {pA:.3f}, "
      f"max |Delta_A - Delta_RAR| = {errA:.4f} (in units of a0)")

# ---- candidate B: Delta_B(s) = C_inf tanh(sqrt(s)/C_inf), closed form both ways
def make_B(Cinf):
    def Delta(s):
        s = np.asarray(s, float); return Cinf*np.tanh(np.sqrt(np.maximum(s, 0.0))/Cinf)
    def JY_of_u(uu):
        uu = np.asarray(uu, float); x = np.minimum(uu/Cinf, 1 - 1e-15)
        return np.where(uu > 0, Cinf**2*np.arctanh(x)**2/np.maximum(uu, 1e-300), 0.0)
    def log10_dD(s):
        """Delta' = sech^2(x)/(2 sqrt s), x = sqrt(s)/C_inf.  For x > 20 sech^2 underflows: use 4 e^{-2x}."""
        s = np.asarray(np.maximum(s, 1e-300), float); x = np.sqrt(s)/Cinf
        small = np.log10(np.where(x < 20, 1.0/np.cosh(np.minimum(x, 20.0))**2, 1.0)) - np.log10(2*np.sqrt(s))
        large = math.log10(4.0) - 2*x*math.log10(math.e) - np.log10(2*np.sqrt(s))
        return np.where(x < 20, small, large)
    return Delta, JY_of_u, log10_dD, dict(Cinf=Cinf)
bestB = None
for Cinf in np.linspace(0.50, 1.30, 801):
    Df = make_B(Cinf)[0]
    e = float(np.max(np.abs(Df(s_fit) - tgt)))
    if bestB is None or e < bestB[0]: bestB = (e, Cinf)
errB, CinfB = bestB
Delta_B, JYu_B, LD_B, parB = make_B(CinfB)
print(f"    B  saturating tanh   Delta_B(s) = C_inf tanh(sqrt(s)/C_inf)   (exact deep-MOND limit by construction)")
print(f"       fitted C_inf = {CinfB:.4f},  max |Delta_B - Delta_RAR| over the same range = {errB:.4f}")

# ---- candidate C: the MINIMAL repair.  exactly nu_RAR below s1, C^2 rational tail above
ssym = sp.symbols('s', positive=True)
Dsym = ssym/(sp.exp(sp.sqrt(ssym)) - 1)
D1f = sp.lambdify(ssym, Dsym, "numpy")
D1p = sp.lambdify(ssym, sp.diff(Dsym, ssym), "numpy")
D1pp = sp.lambdify(ssym, sp.diff(Dsym, ssym, 2), "numpy")
S1 = 2.0; MTAIL = 2.0
d1, d1p, d1pp = float(D1f(S1)), float(D1p(S1)), float(D1pp(S1))
beta = -d1pp/((MTAIL + 1)*d1p)
Aamp = d1p/(MTAIL*beta)
Dinf_C = d1 + Aamp
def Delta_C(s):
    s = np.asarray(s, float)
    lo = D_rar_raw(s)
    hi = Dinf_C - Aamp*(1 + beta*np.maximum(s - S1, 0.0))**(-MTAIL)
    return np.where(s <= S1, lo, hi)
def LD_C(s):
    s = np.asarray(np.maximum(s, 1e-300), float)
    deep = 1.0/(2*np.sqrt(s))                                       # Delta ~ sqrt(s) - s/2 as s -> 0
    mid = np.abs(D1p(np.clip(s, 1e-10, S1)))
    lo = np.where(s < 1e-8, deep, mid)
    hi = MTAIL*Aamp*beta*(1 + beta*np.maximum(s - S1, 0.0))**(-MTAIL - 1)
    return np.log10(np.where(s <= S1, lo, hi))
# J_Y as a function of u for candidate C: nu_RAR inverted on a table below s1, ANALYTIC above it
S_LOW = SS[SS <= S1]
U_LOW = D_rar_raw(S_LOW)
def JYu_C(uu):
    uu = np.asarray(uu, float)
    ss_lo = np.interp(uu, U_LOW, S_LOW)
    ss_lo = np.where(uu < U_LOW[0], uu**2, ss_lo)
    gap = np.maximum(Dinf_C - np.minimum(uu, Dinf_C*(1 - 1e-16)), 1e-300)
    ss_hi = S1 + ((Aamp/gap)**(1.0/MTAIL) - 1.0)/beta                 # exact inverse of the C^2 tail
    ss = np.where(uu <= d1, ss_lo, ss_hi)
    return np.where(uu > 0, ss/np.maximum(uu, 1e-300), 0.0)
errC = float(np.max(np.abs(Delta_C(s_fit) - tgt)))
print(f"    C  minimal C^2 repair:  Delta_C = Delta_RAR exactly for s <= s1 = {S1};  above it")
print(f"       Delta_C(s) = D_inf - A (1 + beta (s - s1))^-{MTAIL:.0f}  with  D_inf = {Dinf_C:.6f}, "
      f"A = {Aamp:.6e}, beta = {beta:.6f}")
print(f"       (the three constants are fixed uniquely by matching Delta, Delta', Delta'' at s1: "
      f"Delta = {d1:.6f}, Delta' = {d1p:.6e}, Delta'' = {d1pp:.6e})")
print(f"       max |Delta_C - Delta_RAR| over 1e-3 <= s <= s_sat = {errC:.4f};  "
      f"max |Delta_C - Delta_published| over ALL s = {float(np.max(np.abs(Delta_C(SS) - Delta_published(SS)))):.4f}")

CAND = [("A  pole", Delta_A, LD_A, JYu_A, CinfA, errA),
        ("B  tanh", Delta_B, LD_B, JYu_B, CinfB, errB),
        ("C  minimal C2", Delta_C, LD_C, JYu_C, Dinf_C, errC)]

print("""
    Each candidate against the five conditions.  Delta' is the ANALYTIC derivative throughout (a finite
    difference underflows once Delta' < 1e-16, which is not the same as Delta' = 0), and it is validated
    against a central difference of Delta over 0.2 <= s <= 5, the window where the difference is
    well conditioned (further out Delta' is small enough that the difference is pure round-off).  C^2 is
    settled analytically, not by differencing: A and B are single closed-form expressions (A is the inverse
    of a strictly monotone analytic map, so the inverse function theorem gives C^infinity wherever
    ds/du > 0), and C is the only piecewise one, so for C the three matching conditions at s1 are checked
    directly against both branch formulas.""")
sfd = np.geomspace(0.2, 5.0, 400)
for nm, Df, LDf, _, Cinf, errf in CAND:
    dv = Df(SS); ld = LDf(SS)
    bounded = bool(np.all(dv <= Cinf*(1 + 1e-6)))
    mono_ok = bool(np.all(np.isfinite(ld)))
    dfd = num_d(Df, sfd); dan = np.power(10.0, LDf(sfd))
    dchk = float(np.max(np.abs(dan/dfd - 1)))
    if nm.startswith("C"):
        eps_ = 1e-7
        jump = max(abs(float(Delta_C(S1 + eps_)) - float(Delta_C(S1 - eps_))),
                   abs(float(np.power(10.0, LD_C(np.array([S1 + eps_]))[0])) - d1p),
                   abs(float(-MTAIL*(MTAIL + 1)*Aamp*beta**2) - d1pp))
        smooth = jump < 1e-6
        cnote = f"Delta, Delta', Delta'' match at s1 to {jump:.1e}"
    else:
        smooth = mono_ok
        cnote = "closed form, C^infinity wherever ds/du > 0"
    sm = np.array([1e-6, 1e-5, 1e-4])
    dm = float(np.max(np.abs(Df(sm)/np.sqrt(sm) - 1)))
    print(f"      {nm:14s}: C_inf = {Cinf:.4f} | bounded {bounded} | Delta' > 0 everywhere {mono_ok} "
          f"(min log10 Delta' = {float(np.min(ld)):+.1f} at s = 1e8) | C^2 {smooth} ({cnote}) | "
          f"analytic vs finite-difference Delta' agree to {dchk:.1e} | "
          f"|Delta/sqrt(s) - 1| <= {dm:.1e} at s <= 1e-4 | residual at s = 1e8: {float(Df(1e8)):.4f} a0")
    check(f"E[{nm.split()[0]}] the continuation satisfies C1 (bounded), C2/C3 (Delta' > 0 strictly everywhere), "
          f"C4 (C^2) and C5 (residual does not grow)",
          bounded and mono_ok and smooth and dm < 0.05 and dchk < 1e-3,
          f"bounded {bounded}, monotone {mono_ok}, C2 {smooth}, deep-MOND error {dm:.1e}, "
          f"Delta' cross-check {dchk:.1e}, max |Delta - Delta_RAR| on the fitted range {errf:.4f}")

n_adm = sum(1 for nm, Df, LDf, _, Cinf, _ in CAND
            if np.all(np.isfinite(LDf(SS))) and np.all(Df(SS) <= Cinf*(1 + 1e-6)))
check("T1 [THEOREM L30-1a] the five conditions are mutually satisfiable: at least one bounded, strictly "
      "increasing, C^2 continuation exists",
      n_adm >= 1, f"{n_adm} of 3 constructed candidates satisfy all five; the minimal repair C reproduces the "
                  f"published kernel to within "
                  f"{float(np.max(np.abs(Delta_C(SS) - Delta_published(SS)))):.4f} a0 at EVERY s")
c_inf_min = min(c for *_, c, _ in CAND)
check("T2 [THEOREM L30-1b] some admissible continuation has a residual force that VANISHES at high "
      "acceleration (Delta -> 0), i.e. a true Newtonian limit",
      c_inf_min < 1e-3,
      f"every admissible continuation has Delta -> C_inf >= {c_inf_min:.4f}, a PERMANENT residual force of "
      f"at least {c_inf_min*a0c:.3e} m/s^2 (canonical, {c_inf_min*A0['alt']:.3e} alt); a vanishing residual "
      f"needs Delta' < 0 somewhere, which C3 forbids.  The published saturated kernel already pays exactly "
      f"this price, so the continuation does not add it")

print("\n    the longitudinal stiffness each continuation implies, as log10 Sigma_par = -log10 Delta' "
      "(canonical footing):")
print(f"      {'background':34s} {'s':>12s} " + " ".join(f"{nm.split()[0]:>16s}" for nm, *_ in CAND))
for nm_bg, sv in s_solar.items():
    row = [f"{-float(LDf(np.array([sv]))[0]):16.1f}" for _, _, LDf, _, _, _ in CAND]
    print(f"      {nm_bg:34s} {sv:12.4g} " + " ".join(row))
print("      (the published kernel gives log10 Sigma_par = +infinity in every row with s > 2.540.  The RATE at "
      "which Delta\n       approaches its ceiling is a real physical output: a power-law approach gives Sigma_par "
      "~ s^2-s^3, an\n       exponential approach gives Sigma_par ~ e^{2 sqrt s} -- formally finite, but at "
      "10^1100 it is not an\n       effective field theory anyone can expand in.  Candidate B is admissible on "
      "the letter of C3-C4 and\n       useless in practice; A and C are not.)")

# =====================================================================================================
# 4.  GATE 1 -- the repository's own filtered-phantom Solar-System gate (g02 machinery, unedited)
# =====================================================================================================
print("\n4.  GATE 1 -- the standing Solar-System gate (g02/g03b filtered-phantom machinery, imported unedited)")
src = open(os.path.join(CLOS, "g02_filtered_efe.py")).read()
head = src[:src.index("# ---------------------------------------------------------------- 3. the scans")]
gg = {"__file__": os.path.join(CLOS, "g02_filtered_efe.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "g02head", "exec"), gg)
eN_of, phantom_density, observables = gg["eN_of"], gg["phantom_density"], gg["observables"]
Q2_CEIL, M_SAT_BOUND, A_SUNWARD = gg["Q2_CEIL"], gg["M_SAT_BOUND"], gg["A_SUNWARD"]
PLANETS, R_SAT = gg["PLANETS"], gg["R_SAT"]
NU_EXP = gg["nu"]

XIS = np.array([0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.3, 1.0])*PC
FIELDS = (("2.00", 2.00e-10), ("2.32", 2.32e-10), ("2.64", 2.64e-10))
def run_gate(nufun, label, verbose_foot=None):
    gg["nu"] = nufun
    out = {}
    for foot, a0 in A0.items():
        rM = math.sqrt(GM/a0); adm = {}
        for tag, gobs in FIELDS:
            eN = eN_of(gobs, a0)
            for xi in XIS:
                r, th, rho = phantom_density(MSUN, 0.0, "gauss", eN, a0, 1e-4*rM, 1e4*rM)
                ob = observables(r, th, rho, xi, "helmholtz", a0)
                Msat = float(np.interp(R_SAT, r, ob["Menc"]))
                gr = max(abs(float(np.interp(rp, r, ob["g_r"]))) for rp in PLANETS.values())
                adm[(tag, xi)] = (abs(ob["Q2"]) < Q2_CEIL and Msat < M_SAT_BOUND and gr < A_SUNWARD)
                if verbose_foot == foot and tag == "2.32" and xi/PC in (0.07, 0.1, 0.15):
                    print(f"      {label:16s} {foot:9s} xi = {xi/PC:5.2f} pc: Q2/ceil {abs(ob['Q2'])/Q2_CEIL:7.3f} | "
                          f"M/bound {Msat/M_SAT_BOUND:7.3f} | g_r/gate {gr/A_SUNWARD:7.3f}  "
                          f"{'admissible' if adm[(tag, xi)] else 'EXCLUDED'}", flush=True)
        ok = [xi for xi in XIS if all(adm[(t, xi)] for t, _ in FIELDS)]
        out[foot] = min(ok)/PC if ok else None
    gg["nu"] = NU_EXP
    return out

nu_published = lambda s: 1.0 + Delta_published(s)/np.maximum(np.asarray(s, float), 1e-300)
F_pub = run_gate(nu_published, "published", verbose_foot="canonical")
print(f"      floors, published carried kernel: canonical {F_pub['canonical']} pc, alt {F_pub['alt']} pc "
      f"   (g03x published 0.1 and 0.15)")
check("K3 [control] the imported gate reproduces g03x's published floors for nu_RAR CARRIED (0.10 pc "
      "canonical, 0.15 pc alt)",
      F_pub["canonical"] == 0.1 and F_pub["alt"] == 0.15, f"{F_pub}")

FL = {"published": F_pub}
for nm, Df, _, _, _, _ in CAND:
    nuf = (lambda D: (lambda s: 1.0 + D(s)/np.maximum(np.asarray(s, float), 1e-300)))(Df)
    FL[nm] = run_gate(nuf, nm)
    print(f"      floors, continuation {nm:14s}: canonical {FL[nm]['canonical']} pc, alt {FL[nm]['alt']} pc")
same = all(FL[nm]["canonical"] == F_pub["canonical"] and FL[nm]["alt"] == F_pub["alt"] for nm, *_ in CAND)
check("G1 the standing Solar-System gate DISCRIMINATES between the published saturated kernel and the "
      "continuations that repair it",
      not same,
      "every continuation returns the identical floor: this gate applies a linear filter to the QUMOND "
      "phantom density and never evaluates Delta' at all, so the term Delta' = 0 removed is not a term it uses")

# =====================================================================================================
# 5.  GATE 2 -- the EXACT fourth-order equation of the carrier reading
# =====================================================================================================
print("\n5.  GATE 2 -- the exact fourth-order equation the continuation makes writable for the first time")
print("""    The action's static scalar equation with the coherence operator outside J (THE_ACTION s1, s4; the
    placement g03c certifies as uniformly elliptic) is

        div[ J_Y(Y) grad phi ] - xi^2 Laplacian^2 phi = 4 pi G rho .

    In spherical symmetry, with u = r^2 w and w = |grad phi| = g_phi, one integration gives EXACTLY

        J_Y(w) u  -  xi^2 ( u'' - 2 u'/r )  =  G M .

    This equation requires J_Y as a FUNCTION of w.  The published saturated kernel does not supply one
    (P2): J_Y is a vertical segment at w = C a0.  So this equation cannot be written down at all until a
    continuation is chosen -- which is exactly the missing input L13 named.  It is solved here.""")

NS_GRID = 4000
def grid_of(a0, xi, NS=NS_GRID):
    rmin = 1e-4*AU; rmax = 1e5*max(xi, math.sqrt(GM/a0))
    t = np.linspace(math.log(rmin), math.log(rmax), NS); h = t[1] - t[0]; r = np.exp(t)
    coef = xi**2/r**2
    return r, h, (-coef*(1/h**2 + 3/(2*h)), 2*coef/h**2, -coef*(1/h**2 - 3/(2*h)))

def solve_biharmonic(a0, xi):
    """CONTROL: the same stencil with J_Y switched off.  Exact solution u = GM r^2/(2 xi^2)."""
    r, h, (lo_d, dg_d, up_d) = grid_of(a0, xi)
    NS = len(r); u_out = GM*r[-1]**2/(2*xi**2)
    main = dg_d.copy(); low = lo_d[1:].copy(); upp = up_d[:-1].copy()
    rhs = np.full(NS, GM)
    main[0] = 1.0; upp[0] = 0.0; rhs[0] = 0.0
    main[-1] = 1.0; low[-1] = 0.0; rhs[-1] = u_out
    u = spl.spsolve(sps.diags([low, main, upp], [-1, 0, 1], format="csr"), rhs)
    return r, u/r**2

def solve_carrier(Dfun, LDfun, JYu, a0, xi, itmax=250, tol=1e-11):
    """Damped NEWTON on the exact first integral, in the variable q(r) = s(w(r)), i.e. the Newtonian
    acceleration the scalar's own local gradient corresponds to:

        a0 q r^2  -  xi^2 ( U'' - 2 U'/r )  =  G M ,     U = r^2 a0 Delta(q) = r^2 w .

    Choosing q rather than w is what makes the problem solvable.  The Jacobian is
        dR_i/dq_i = a0 r_i^2 + (stencil) x r_i^2 a0 Delta'(q_i) ,
    so the CONTINUATION'S Delta' is the whole nonlinear content, and where Delta' -> 0 (the saturated
    branch) the Jacobian is perfectly conditioned while the equation loses all memory of the kernel.
    In the w variable the same Jacobian is Sigma_par = 1/Delta', which is where the divergence sits; a
    lagged-J_Y (Picard) scheme has amplification 1 - Sigma_par/Sigma_perp and diverges there outright.
    Either way the solve is impossible without the missing input."""
    r, h, (lo_d, dg_d, up_d) = grid_of(a0, xi)
    NS = len(r); r2 = r**2
    q_alg = GM/(r2*a0)                                   # exact at xi = 0
    q_out = float(q_alg[-1])
    # start from the smaller of the unscreened law and the biharmonic cone: both limits are known
    u_st = np.minimum(Dfun(q_alg), GM/(2*xi**2*a0))
    q = np.maximum(JYu(u_st)*u_st, 1e-30)
    q[0] = 0.0; q[-1] = q_out
    def Uof(qq): return r2*a0*Dfun(np.maximum(qq, 0.0))
    def resid(qq):
        U = Uof(qq)
        R = a0*np.maximum(qq, 0.0)*r2 - GM
        R[1:-1] += lo_d[1:-1]*U[:-2] + dg_d[1:-1]*U[1:-1] + up_d[1:-1]*U[2:]
        R[0] = qq[0] - 0.0; R[-1] = qq[-1] - q_out
        return R
    sc = GM + a0*np.abs(q_alg)*r2
    R = resid(q); nrm = float(np.max(np.abs(R)/sc)); it = 0
    for it in range(1, itmax + 1):
        if nrm < tol: break
        dU = r2*a0*np.power(10.0, np.clip(np.nan_to_num(LDfun(np.maximum(q, 1e-30)), nan=-300.0), -300, 300))
        main = a0*r2 + dg_d*dU
        low = (lo_d[1:]*dU[:-1]).copy(); upp = (up_d[:-1]*dU[1:]).copy()
        main[0] = 1.0; main[-1] = 1.0; low[-1] = 0.0; upp[0] = 0.0
        d = spl.spsolve(sps.diags([low, main, upp], [-1, 0, 1], format="csr"), -R)
        lam = 1.0
        for _ in range(50):
            qn = np.maximum(q + lam*d, 0.0)
            Rn = resid(qn); nn = float(np.max(np.abs(Rn)/sc))
            if nn < nrm or lam < 1e-12: break
            lam *= 0.5
        q, R, nrm = qn, Rn, nn
    w = a0*Dfun(q)
    return r, w, r2*w, it, nrm

# K4: the pure biharmonic cone -- the stencil alone, kernel switched off
xi_t = 0.1*PC
r_b, w_b = solve_biharmonic(a0c, xi_t)
w0_pred = GM/(2*xi_t**2)
w0_num = float(np.interp(9.54*AU, r_b, w_b))
print(f"    K4 pure biharmonic control (J_Y = 0), xi = 0.1 pc: w(Saturn) numerical {w0_num:.6e}, "
      f"analytic GM/(2 xi^2) = {w0_pred:.6e} m/s^2")
check("K4 [control] with J_Y set to zero the solver's stencil reproduces the exact biharmonic cone "
      "w = GM/(2 xi^2) to 1%",
      abs(w0_num/w0_pred - 1) < 0.01, f"ratio {w0_num/w0_pred:.5f}")

# K5: xi -> 0 reproduces the algebraic law
r_a, w_a, u_a, it_a, res_a = solve_carrier(Delta_C, LD_C, JYu_C, a0c, 1e-6*math.sqrt(GM/a0c))
rt = math.sqrt(GM/a0c)
s_here = GM/(rt**2*a0c)
w_alg_here = a0c*float(Delta_C(s_here))
w_num_here = float(np.interp(rt, r_a, w_a))
print(f"    K5 xi -> 0 control at r = r_M: numerical w = {w_num_here:.6e}, algebraic a0 Delta(s = "
      f"{s_here:.3f}) = {w_alg_here:.6e} m/s^2")
check("K5 [control] at xi -> 0 the solver reproduces the algebraic carrier law w = a0 Delta(g_N/a0) to 1%",
      abs(w_num_here/w_alg_here - 1) < 0.01, f"ratio {w_num_here/w_alg_here:.5f}")

XI_SCAN = np.array([0.03, 0.1, 0.3, 1.0, 2.0, 4.0, 6.0, 10.0, 30.0])*PC
print("\n    the exact equation solved for each continuation.  Gates: Pitjev-Pitjeva M_ph(<Saturn) < "
      "6.7e-11 M_sun,\n    and the alpha = 1 sunward ephemeris gate 3.66e-14 m/s^2 on the largest planetary "
      "residual.")
print("    Every row also reports w(Saturn) divided by min[ GM/(2 xi^2), C_inf a0 ] -- the analytic interior\n"
      "    prediction (the biharmonic cone, capped by Theorem L30-2's kinematic ceiling).  It is an internal\n"
      "    control on every single solve, not a fit.")
print(f"      {'continuation':14s} {'footing':10s} {'xi [pc]':>8s} {'w(Saturn) [m/s^2]':>18s} {'/analytic':>10s} "
      f"{'M_ph/bound':>11s} {'g_r max/gate':>13s}  verdict")
FLOOR2 = {}; CONE_ERR = []
for nm, Df, LDf, JYu, Cinf, _ in CAND:
    for foot, a0 in A0.items():
        floor = None
        for xi in XI_SCAN:
            r, w, u, it, res = solve_carrier(Df, LDf, JYu, a0, xi)
            Msat_over = float(np.interp(R_SAT, r, u))/GM/6.7e-11
            grmax = max(float(np.interp(rp, r, w)) for rp in PLANETS.values())
            wS = float(np.interp(R_SAT, r, w))
            pred = min(GM/(2*xi**2), Cinf*a0)
            CONE_ERR.append(abs(wS/pred - 1))
            adm = (Msat_over < 1.0) and (grmax < A_SUNWARD)
            if adm and floor is None: floor = xi/PC
            if foot == "canonical" or adm:
                print(f"      {nm:14s} {foot:10s} {xi/PC:8.2f} {wS:18.4e} {wS/pred:10.4f} "
                      f"{Msat_over:11.3e} {grmax/A_SUNWARD:13.3e}  {'admissible' if adm else 'EXCLUDED'}",
                      flush=True)
        FLOOR2[(nm, foot)] = floor
        print(f"      {nm:14s} {foot:10s} -> smallest admissible tabulated xi = "
              f"{floor if floor is not None else 'NONE <= 30 pc'} pc")
check("K6 [control] every one of the 54 exact solves reproduces the analytic interior prediction "
      "min[GM/(2 xi^2), C_inf a0] to 1%",
      max(CONE_ERR) < 0.01, f"worst deviation {100*max(CONE_ERR):.3f}% over {len(CONE_ERR)} solves")

xi_sun = math.sqrt(GM/(2*A_SUNWARD))
xi_an = R_SAT/math.sqrt(2*6.7e-11)
print(f"\n    the number is analytic and kernel-free.  Inside the healing length the source term dominates "
      f"and the\n    equation degenerates to the biharmonic cone w = GM/(2 xi^2), so M_ph(<r)/M = r^2/(2 xi^2) "
      f"EXACTLY --\n    independent of the kernel, of the continuation, of a0 and even of the Sun's mass.  The "
      f"Pitjev-Pitjeva\n    bound then reads  xi >= r_Saturn/sqrt(2 x 6.7e-11) = {xi_an/PC:.2f} pc, against "
      f"{xi_sun/PC:.2f} pc from the\n    alpha = 1 sunward gate alone: SATURN BINDS, by a factor "
      f"{xi_an/xi_sun:.1f}.  Neither number contains a0.")

# the other placement of the coherence operator: inside J, as section 1 writes it literally
print("""
    THE OTHER PLACEMENT.  THE_ACTION s1 writes the operator INSIDE J, as J(Y + xi^2 |grad_perp V|^2), and
    calls the two placements "equivalent" (identical PPN; g03c notes only that the inside placement is
    degenerate at zero field).  They are not equivalent here.  Inside J the interior balance is
    -xi^2 J_Y(w) Laplacian^2 phi = 4 pi G rho with J_Y at the SCREENED (small) gradient, so
        w = GM/(2 xi^2 J_Y(w)),  and on the deep-MOND branch J_Y = w/a0,  hence  w = sqrt(GM a0/2)/xi.
    This is an asymptotic balance, not a solve; what is CHECKED is its self-consistency (that the resulting
    w really does sit on the deep-MOND branch, where J_Y = w/a0) and the floor it implies.""")
for foot, a0 in A0.items():
    xi_in = R_SAT**2*math.sqrt(a0/(2*GM))/6.7e-11
    w_in = math.sqrt(GM*a0/2)/xi_in
    JY_dm = w_in/a0
    JY_true = float(JYu_C(np.array([w_in/a0]))[0])
    print(f"      {foot:10s}: floor xi = r_Sat^2 sqrt(a0/2GM)/6.7e-11 = {xi_in/PC:.0f} pc; at that floor "
          f"w = {w_in:.3e} m/s^2 = {w_in/a0:.2e} a0,\n                  J_Y there = {JY_true:.3e} against the "
          f"deep-MOND value w/a0 = {JY_dm:.3e} (ratio {JY_true/JY_dm:.4f})")
    check(f"S1 [{foot}] the inside-J placement of the coherence operator is equivalent to the outside-J one, "
          f"as THE_ACTION section 1 states",
          abs(xi_in/xi_an - 1) < 0.5,
          f"its Saturn floor is {xi_in/PC:.0f} pc against {xi_an/PC:.2f} pc outside J, a factor "
          f"{xi_in/xi_an:.0f}; the deep-MOND identification is self-consistent to "
          f"{abs(JY_true/JY_dm - 1)*100:.2f}%, so the estimate stands.  BOTH placements fail the standing "
          f"floor; the conclusion does not depend on which is adopted, but they are not interchangeable")
floors2 = [v for v in FLOOR2.values() if v is not None]
best2 = min(floors2) if floors2 else None
check("G2 the exact fourth-order carrier equation admits the repository's standing coherence-length floor "
      "(xi <= 0.15 pc) for at least one continuation",
      best2 is not None and best2 <= 0.15,
      f"the smallest admissible xi over all continuations and both footings is {best2} pc, "
      f"{(best2/0.15 if best2 else float('nan')):.0f}x the standing floor; analytic floor "
      f"{xi_an/PC:.2f} pc from the Saturn bound alone")

# what that floor would do to the wide-binary prediction
wb_max = 30e3*AU
print(f"\n    consequence, stated not claimed: the wide-binary sample's largest separation is 30 kAU = "
      f"{wb_max/PC:.3f} pc,\n    which is {xi_an/wb_max:.0f}x SMALLER than this floor.  At xi >= {xi_an/PC:.0f} pc "
      f"every pair in the DR4 window sits\n    deep inside the healing length, where the scalar force is the "
      f"biharmonic cone rather than the MOND field.\n    The registered arm-B value gamma_v = 1.045/1.030 was "
      f"computed at xi = 0.10/0.15 pc.  Recomputing it at this\n    floor is not done here; the direction is "
      f"unambiguous (towards Newton), the magnitude is not asserted.")

# =====================================================================================================
# 6.  GATE 3 -- the SPARC Newtonian limit, the one observable a constant residual touches
# =====================================================================================================
print("\n6.  GATE 3 -- the SPARC Newtonian-limit statistic against the permanent residual force")
UPS_D, UPS_B = 0.5, 0.7
pts = []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0]*kpc; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3
    Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    m = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    for i in np.where(m)[0]:
        pts.append((Vb2[i]/r[i], Vo[i]**2/r[i]))
pts = np.array(pts)
print(f"    SPARC: {len(pts)} points (Upsilon_d = 0.5, Upsilon_b = 0.7, dV/V < 0.10)")
rng = np.random.default_rng(30)
for foot, a0 in A0.items():
    for thr in (10.0, 30.0):
        sel = pts[:, 0] > thr*a0
        if sel.sum() < 10: continue
        gb, go = pts[sel, 0], pts[sel, 1]
        ratio = go/gb
        med = float(np.median(ratio))
        boot = np.array([float(np.median(rng.choice(ratio, ratio.size))) for _ in range(2000)])
        se = float(np.std(boot))
        s_here = gb/a0
        pred = {"published": float(np.median(1 + Delta_published(s_here)/s_here)),
                "nu_RAR unsat": float(np.median(1 + D_rar_raw(s_here)/s_here))}
        for nm, Df, _, _, _, _ in CAND:
            pred[nm] = float(np.median(1 + Df(s_here)/s_here))
        print(f"      {foot:10s} g_bar > {thr:4.0f} a0  (n = {sel.sum():4d}, median s = {np.median(s_here):6.1f}):  "
              f"measured median g_obs/g_bar = {med:.4f} +- {se:.4f}")
        print("                 predicted: " + ",  ".join(f"{k} {v:.4f}" for k, v in pred.items())
              + f"   |   tension of the carried class: {abs(med - pred['published'])/max(se, 1e-9):.1f} sigma, "
                f"of unsaturated nu_RAR: {abs(med - pred['nu_RAR unsat'])/max(se, 1e-9):.1f} sigma")
        if thr == 10.0:
            z = abs(med - pred["published"])/max(se, 1e-9)
            zr = abs(med - pred["nu_RAR unsat"])/max(se, 1e-9)
            check(f"G3 [{foot}] the permanent residual C_inf a0 that EVERY carriable kernel leaves -- the "
                  f"published saturated one and all three continuations alike -- is consistent with the SPARC "
                  f"Newtonian-limit median at g_bar > 10 a0 (within 3 bootstrap sigma)",
                  z < 3.0,
                  f"measured {med:.4f} +- {se:.4f}; carried class predicts {pred['published']:.4f} ({z:.1f} "
                  f"sigma high), unsaturated nu_RAR predicts {pred['nu_RAR unsat']:.4f} ({zr:.1f} sigma). "
                  f"The bootstrap error excludes the 0.1 dex stellar-population spread and the Upsilon "
                  f"freedom, so this is a DIAGNOSTIC of the direction, not a fit-quality statement; it is "
                  f"reported because it is the ONE observable the permanent residual touches")

# =====================================================================================================
# 7.  where the saturated branch actually lives
# =====================================================================================================
print("\n7.  WHERE THE SATURATED BRANCH IS ACTUALLY REALISED")
for foot, a0 in A0.items():
    r_sat_sun = math.sqrt(GM/(S_SAT*a0))
    r_sat_gal = math.sqrt(GM*1e11/(S_SAT*a0))
    print(f"    {foot:10s}: around the Sun, g_N > s_sat a0 only inside r = {r_sat_sun/PC:.4f} pc "
          f"({r_sat_sun/AU:.3g} AU);\n                around a 1e11 M_sun galaxy, inside "
          f"{r_sat_gal/kpc:.1f} kpc.")
r_sat_sun = math.sqrt(GM/(S_SAT*a0c))
check("G4 the saturated branch is realised UNSCREENED around the Sun, i.e. the coherence-length floor is "
      "smaller than the radius inside which g_N > s_sat a0",
      0.10*PC < r_sat_sun,
      f"the standing floor xi = 0.10 pc already EXCEEDS r_sat(Sun) = {r_sat_sun/PC:.4f} pc, so the scalar "
      f"never sits on the saturated branch near the Sun: L13's P9 background is the INNER GALAXY "
      f"(r < {math.sqrt(GM*1e11/(S_SAT*a0c))/kpc:.0f} kpc for a 1e11 M_sun galaxy) and cluster cores, "
      f"not the Solar System")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   ({time.time() - T0:.0f} s)")
sys.exit(0)
