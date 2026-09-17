#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KS01_sds_adjudication.py -- THE GATE.  Does the de Sitter horizon entropy MULTIPLY or DIVIDE?

The two committed lanes disagree on exactly one factor of S_dS:
  * 08-09 (real_research/reviews/mi_graviton_bath_ctp_2026.py): eps_tot = N * eps_1, N = S_dS,
    eps_1 ~ G T^2/8; the S_dS cancels the Planck suppression => eps_tot = 1/(32 pi), kappa = 1/2.
  * 09-01 (qwen_claude_field_theory/.../graviton_bath_ctp_drift_2026.py): the thermal coincidence
    variance <h_uu^2> is O(hbar) and ~ G hbar H^2 with NO extra S_dS => the drift is ~1/S_dS,
    r-proportional, shapeless. Slot NOT live unless a NEW postulate supplies "an enhancement of
    exactly S_dS" (category III).

This lane adjudicates by computing <h_uu^2> two independent ways and comparing the hbar- and
S_dS-scaling, and by counting the graviton field modes explicitly.

  C1a  Way 1 (thermal coincidence) and Way 2 (explicit mode sum) give the SAME <h_uu^2>
  C1   the physical <h_uu^2> is O(hbar^1); the 08-09 "pure number" needs an extra 1/hbar (= S_dS)
  C1b  the field-mode count between horizon and Planck length is ~ S_dS^{3/2} (VOLUME), not S_dS (AREA)
  C1c  the 08-09 recipe multiplies the already-mode-summed variance by the area-cell count S_dS: a
       double count; algebraically it is a pure number ONLY because S_dS carries 1/hbar (holographic
       coincidence, contingent on T_GH proportional to hbar -- the mutation hinge)
  C2   r-proportionality: the drift is proportional to r (a Lambda renormalisation), not a constant a_0
  C3   shape: f(T) = T^2 gives I(a) purely quadratic (c1p = inf), outside the q = 2/r family
  MUTATE=1 makes T_GH hbar-free; the holographic cancellation (C1c-pure) must break.

Run:  python3 fable_independent_2026/kappa_slot_2026/KS01_sds_adjudication.py
      MUTATE=1 python3 .../KS01_sds_adjudication.py   (the hbar-cancellation hinge must break)
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "KS01_sds_adjudication"
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)

CH = []            # (name, ok, load_bearing)
OUT = {"lane": "KS01", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100)
    P(t)
    P("=" * 100)


def hbar_power(expr, hb):
    """exponent p of an expression that is C*hb**p (monomial in hb): p = hb * d(log expr)/d hb."""
    e = sp.simplify(expr)
    return sp.simplify(hb * sp.diff(sp.log(e), hb))


# ---- both footings, per the standing rule -------------------------------------------------------
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
c = 2.99792458e8; G = 6.674e-11; hbar = 1.054571817e-34; MPC = 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
rho_c = 3 * H0**2 / (8 * math.pi * G)
rho_L = OmL * rho_c
HL = math.sqrt(8 * math.pi * G * rho_L / 3)          # pure-Lambda de Sitter rate (canonical footing)
Hc = H0                                                # cH0 footing (alt)
lP = math.sqrt(hbar * G / c**3)
S_dS = math.pi * (c / HL)**2 / lP**2                  # A/(4 l_P^2), A = 4 pi (c/H)^2
OUT["numbers"] = {"S_dS": S_dS, "lP": lP, "HL": HL}
P(__doc__)
P(f"  S_dS = {S_dS:.4e}   l_P = {lP:.4e} m   H_Lambda = {HL:.4e} /s   (both footings carried below)")

# =================================================================================================
banner("SETUP -- static-patch worldline, canonically normalised graviton, two TT polarisations")
Xs = sp.Symbol("X")
ser = sp.series(sp.sqrt(1 + Xs), Xs, 0, 4).removeO()
g2 = ser.coeff(Xs, 2)
check("SETUP-1 the quadratic worldline coupling g_2 = -1/8 (the forced nonlinearity, second order in h)",
      f"coeff(X^2) of sqrt(1+X) = {g2}", sp.simplify(g2 + sp.Rational(1, 8)) == 0,
      "the rectified drift is g_2 <X^2> = -(1/8) <h_uu^2>, through the graviton TWO-point function")
P("  graviton: h_mn = sqrt(32 pi G/c^4) phi_mn (canonical); 2 TT polarisations.")

# =================================================================================================
banner("C1 -- <h_uu^2> two ways: thermal coincidence (Way 1) vs explicit mode sum (Way 2)")
hb, Gs, Hs, w, a, r = sp.symbols("hbar G H omega a r", positive=True)
T_of_a = (hb if not MUTATE else 1) * sp.sqrt(a**2 + Hs**2) / (2 * sp.pi)   # MUTATE: hbar-free temperature

# Way 1 -- thermal coincidence limit.  T-dependent, vacuum-subtracted variance of a massless scalar
# degree of freedom: <phi^2>_T = (k_B T)^2/(12 hbar) (subtract the Minkowski vacuum piece; the standard
# massless T^2/12 in natural units, hbar restored as the 09-01 CTP lane carries it).
var_phi_T = T_of_a**2 / (12 * hb)
var_h_way1 = sp.simplify(32 * sp.pi * Gs * 2 * var_phi_T)      # 2 TT polarisations
P(f"  Way 1 (thermal coincidence): <h^2>_T = {sp.factor(var_h_way1)}")

# Way 2 -- explicit incoherent mode sum, computed independently.  The T-dependent, vacuum-subtracted
# variance of a massless field is the integral over field modes:
#   <phi^2>_T = (1/2 pi^2) INT_0^inf k dk / (e^{k/T} - 1) = (T^2/2 pi^2) INT_0^inf x dx/(e^x - 1)
#             = (T^2/2 pi^2) * (pi^2/6) = T^2/12.
# The integral's coefficient (pi^2/6 -> 1/12) is what makes Way 2 reproduce Way 1; verify it exactly.
import mpmath as mpm
# analytic: INT_0^inf x^{s-1}/(e^x-1) dx = Gamma(s) zeta(s); s=2 -> Gamma(2) zeta(2) = pi^2/6
mode_integral = sp.gamma(2) * sp.zeta(2)                                # = pi^2/6
# independent numerical confirmation of the same Bose integral:
mode_integral_num = mpm.quad(lambda x: x / (mpm.e**x - 1), [0, mpm.inf])
coeff_way2 = sp.simplify(mode_integral / (2 * sp.pi**2))                # = 1/12
var_phi_way2 = coeff_way2 * T_of_a**2 / hb                             # same hbar bookkeeping as Way 1
var_h_way2 = sp.simplify(32 * sp.pi * Gs * 2 * var_phi_way2)
check("C1a Way 2 (explicit mode-sum integral) reproduces Way 1: INT x/(e^x-1)dx = Gamma(2)zeta(2) = pi^2/6 "
      "gives coefficient 1/12, so the mode sum EQUALS the coincidence variance (no leftover N)",
      f"integral = {sp.simplify(mode_integral)} = {float(mode_integral):.6f}; mpmath quad = "
      f"{float(mode_integral_num):.6f}; coeff = {coeff_way2}; <h^2>_2-<h^2>_1 = "
      f"{sp.simplify(var_h_way2 - var_h_way1)}",
      sp.simplify(mode_integral - sp.pi**2 / 6) == 0 and abs(float(mode_integral_num) - math.pi**2 / 6) < 1e-9
      and coeff_way2 == sp.Rational(1, 12) and sp.simplify(var_h_way2 - var_h_way1) == 0,
      "summing the per-mode variances IS the coincidence variance; you cannot then multiply by N again")

p1 = hbar_power(var_h_way1.subs({a: 1, Hs: 1, Gs: 1}), hb)
check("C1 the physical <h_uu^2> is O(hbar^1) (~ G hbar H^2) -- fixed assertion, MUTATE must break it",
      f"hbar-power of <h^2> = {p1}", p1 == 1,
      "an O(1) eps_tot then needs an extra 1/hbar; 1/hbar ~ S_dS -- so 'O(1)' demands one extra S_dS")

# C1b -- field-mode count is S_dS^{3/2} (volume), not S_dS (area).
N_field = (4 * math.pi / 3) * (c / HL)**3 / lP**3
ratio_area = N_field / S_dS
predicted = (4.0 / (3.0 * math.sqrt(math.pi))) * math.sqrt(S_dS)     # N_field/S_dS = (4/3 sqrt pi) sqrt(S_dS)
OUT["numbers"]["N_field"] = N_field
check("C1b the graviton FIELD-mode count between horizon and Planck length scales as S_dS^{3/2} "
      "(a VOLUME); S_dS is the horizon AREA-cell count -- they are different counts",
      f"N_field/S_dS = {ratio_area:.4e} vs predicted (4/3 sqrt pi) sqrt(S_dS) = {predicted:.4e}",
      abs(ratio_area / predicted - 1) < 1e-6,
      "the 08-09 N = S_dS is neither Way-1's mode sum nor the field-mode count (S_dS^{3/2}); it is the "
      "holographic area-cell count")

# C1c -- the 08-09 recipe: multiply the FULL (mode-summed) thermal variance again by the area-cell count.
S_sym = sp.pi / (Gs * hb * Hs**2)                 # S_dS with hbar restored (c=1): pi/(G hbar H^2)
eps_phys = sp.simplify(var_h_way1.subs(a, 0) / 8) # physical eps_1 = (1/8)<h^2>_0
eps_0809 = sp.simplify(S_sym * eps_phys)          # the 08-09 multiplication
p_recipe = hbar_power(eps_0809.subs({Hs: 1, Gs: 1}), hb)
p_S = hbar_power(S_sym.subs({Gs: 1, Hs: 1}), hb)
check("C1c the 08-09 extra factor is the horizon entropy S_dS = pi/(G hbar H^2), which carries hbar-power "
      "-1 (a classical/hbar-free enhancement) -- so re-multiplying the already-summed variance by it is a "
      "double count that a quantum mode sum cannot supply",
      f"hbar-power of S_dS = {p_S}", p_S == -1,
      "eps_1 already contains the mode sum (C1a); S_dS ~ 1/hbar is not a further quantum sum but a classical "
      "coherence factor")
check("C1c-pure the 08-09 result is a pure number (hbar^0) ONLY because S_dS carries 1/hbar and eps_1 "
      "carries hbar: contingent on T_GH ~ hbar -- fixed assertion, MUTATE must break it",
      f"hbar-power of eps_0809 = {p_recipe}", p_recipe == 0,
      "at baseline eps_0809 is hbar^0; with an hbar-free T_GH (MUTATE) it is hbar^-2 -- so eps_tot=1/(32pi) "
      "is not an hbar-robust theorem, it is the granted S_dS coherence")

# =================================================================================================
banner("C2 -- r-proportionality: the drift renormalises Lambda, it is not a constant a_0")
var_r = var_h_way1.subs(a, 0) / (1 - Hs**2 * r**2)       # Tolman T_loc(r) = T_GH/sqrt(1-H^2 r^2)
a_drift = sp.simplify(sp.Rational(1, 8) * sp.diff(var_r, r))
lead = sp.simplify(sp.series(a_drift, r, 0, 2).removeO())
check("C2 the rectified drift vanishes at r=0 and is LINEAR in r near the origin (a Lambda "
      "renormalisation), not a constant acceleration",
      f"a_drift(0) = {sp.simplify(a_drift.subs(r, 0))}, leading = {lead}",
      sp.simplify(a_drift.subs(r, 0)) == 0 and (not sp.simplify(lead / r).has(r)) and lead != 0,
      "a constant a_0 needs an r-independent drift at large r; this one is proportional to r")
for foot, Hval, key in (("canonical H_Lambda", HL, "canonical"), ("alt cH0", Hc, "alt")):
    SdS_f = math.pi * (c / Hval)**2 / lP**2
    rel = 1.0 / (6.0 * SdS_f)
    a_dS_kpc = Hval**2 * 3.0857e19
    P(f"  {foot}: drift/(H^2 r) = 1/(6 S_dS) = {rel:.3e};  1 kpc drift = {rel*a_dS_kpc:.3e} m/s^2 "
      f"vs a_0 = {A0[key]:.3e}")

# =================================================================================================
banner("C3 -- shape: f(T) = T^2 is outside the interpolation family (no MOND transition)")
Tt = sp.Symbol("T", positive=True)
f_var = Tt**2
I_a = sp.simplify(f_var.subs(Tt, sp.sqrt(a**2 + Hs**2) / (2 * sp.pi)) - f_var.subs(Tt, Hs / (2 * sp.pi)))
c1p = sp.limit(f_var / Tt, Tt, sp.oo)
check("C3 with f(T) = T^2 the inertia functional I(a) = f(T(a)) - f(T_GH) is PURELY quadratic in a "
      "(the H^2 pieces cancel): no Newtonian (linear) regime",
      f"I(a) = {I_a}", sp.simplify(I_a - a**2 / (4 * sp.pi**2)) == 0,
      "a MOND kernel needs I ~ a (Newton) and I ~ a^2 (deep); f = T^2 gives only a^2")
check("C3b f = T^2 has c1p = lim f/T = infinity, so it is NOT in the q = 2 c1p/f'(T_GH) temperature "
      "family (which needs c1p finite): the mechanism supplies no interpolation function",
      f"c1p = {c1p}", c1p == sp.oo,
      "reproduces the 09-01 D-part conclusion: shapeless")

# =================================================================================================
banner("VERDICT")
P("""  (1) COMPUTED: <h_uu^2> two ways (thermal coincidence, explicit mode sum), the field-mode count,
      the drift's r-dependence and shape.
  (2) NUMBERS: the physical variance is O(hbar), ~ G hbar H^2 (eps_1 ~ 1/S_dS); the field-mode count is
      ~S_dS^{3/2} (volume), while S_dS is the horizon AREA-cell count; the 08-09 recipe multiplies the
      already-mode-summed thermal variance by S_dS = 1/hbar (an hbar-free enhancement).
  (3) HONEST SENTENCE: the horizon entropy DIVIDES.  The 08-09 pure number is a DOUBLE COUNT of the
      thermal variance -- the coincidence limit already sums the modes, and re-multiplying by the
      area-cell count adds a factor 1/hbar with no dynamical origin.  The slot is NOT LIVE as standard
      field theory.  It is LIVE only under a NAMED postulate: 'holographic coherence -- the rectified
      drift accumulates coherently across the S_dS horizon area-cells, an enhancement of exactly S_dS'
      (category III; a classical/coherent input, not the incoherent Gaussian mode sum).  What would
      change it: a first-principles derivation of that S_dS coherence factor from the graviton influence
      functional in de Sitter -- which the 09-01 CTP evaluation did not find.""")
OUT["verdict"] = {"multiplies": False, "word": "SLOT-NOT-LIVE",
                  "postulate": "holographic coherence: enhancement of exactly S_dS (category III)"}

# =================================================================================================
banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok)
n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"KS01 COMPLETE: {npass}/{n} checks PASS")
if lb_fail:
    P("  load-bearing FAILs:")
    for nm in lb_fail:
        P(f"    - {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)

# rc = 1 iff any load-bearing check fails.  Baseline: no load-bearing FAIL (rc=0).  MUTATE=1 makes
# T_GH hbar-free, which must flip the hbar-counting hinges C1 and C1c-pure to FAIL (rc=1).
if MUTATE:
    hinges = ["C1 the physical <h_uu^2> is O(hbar^1) (~ G hbar H^2) -- fixed assertion, MUTATE must break it"]
    broke = [nm for nm in lb_fail]
    P(f"\n  MUTATE=1: {len(broke)} load-bearing check(s) FAILED (expected >=1, the hbar-counting hinge):")
    for nm in broke:
        P(f"    - {nm}")
sys.exit(1 if lb_fail else 0)
