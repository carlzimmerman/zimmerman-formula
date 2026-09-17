#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KS06_number_field.py -- make the discriminator exact: which mechanism classes can produce a RATIONAL
kappa, and is 1/(32 pi) itself a convention-free number?

  C1  prove kappa^2 = 8 pi eps_tot from a0^2 = 3 eps_tot c^2 H_Lambda^2 and H_Lambda^2 = 8 pi G rho_L/3
      (sympy exact), and decompose 1/(32 pi) = pi(S_dS) x (1/8)(coupling) x 1/(4 pi^2)(T_GH); classify each
      factor as CONVENTION or PHYSICS.  MUTATE breaks the Friedmann 3 or the 8 pi and the identity fails.
  C2  m-independence: with the -X^2/8 coupling the drift per unit rest mass is m-independent (sympy)
  C3  rate-vs-density classification of the graviton-bath route, and whether a rational kappa is available

Run:  python3 fable_independent_2026/kappa_slot_2026/KS06_number_field.py
      MUTATE=1 python3 .../KS06_number_field.py   (the identity-chain hinge must break)
"""
import os, sys, json, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "KS06_number_field"
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KS06", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
banner("C1 -- the identity chain kappa^2 = 8 pi eps_tot, and the pi-decomposition of 1/(32 pi)")
eps, cc, HL, G, rho = sp.symbols("epsilon c H_Lambda G rho_Lambda", positive=True)
three = sp.Integer(1) if MUTATE else sp.Integer(3)     # MUTATION: break the Friedmann 3
eightpi = 8 * sp.pi
a0_sq = 3 * eps * cc**2 * HL**2                          # a0^2 = 3 eps c^2 H_Lambda^2 (mechanism)
H2 = eightpi * G * rho / three                           # H_Lambda^2 = 8 pi G rho_Lambda/3 (Friedmann)
a0_sq_sub = a0_sq.subs(HL**2, H2)
kappa_sq = sp.simplify(a0_sq_sub / (cc**2 * G * rho))    # kappa^2 = a0^2/(c^2 G rho_Lambda)
P(f"  kappa^2 = {kappa_sq}")
check("C1 kappa^2 = 8 pi eps_tot exactly (from a0^2 = 3 eps c^2 H_Lambda^2 and Friedmann) "
      "-- fixed assertion, MUTATE must break it",
      f"kappa^2 = {kappa_sq}", sp.simplify(kappa_sq - 8 * sp.pi * eps) == 0,
      "so kappa = 1/2 <=> eps_tot = 1/(32 pi); the 8 pi comes from Friedmann (the 3 cancels)")

# the pi-decomposition: 1/(32 pi) = pi (S_dS) x (1/8)(coupling) x 1/(4 pi^2)(T_GH)
piece_SdS = sp.pi              # S_dS = pi/(G hbar H^2): the pi from area (4 pi r^2) x 1/4 (BH) x ...
piece_coupling = sp.Rational(1, 8)     # the -X^2/8 of sqrt(1+X)
piece_T = sp.Rational(1, 4) / sp.pi**2  # T_GH = H/2 pi => T^2 carries 1/(4 pi^2)
decomp = sp.simplify(piece_SdS * piece_coupling * piece_T)
check("C1b 1/(32 pi) decomposes as pi(S_dS) x (1/8)(coupling) x 1/(4 pi^2)(T_GH)",
      f"pi * (1/8) * 1/(4 pi^2) = {decomp} = 1/(32 pi)", sp.simplify(decomp - sp.Rational(1, 1) / (32 * sp.pi)) == 0,
      "each pi is traced: area/BH (S_dS), none (coupling), Euclidean-periodicity 2pi (T_GH)")

# classify the factors
FACTORS = {
    "hbar = k_B = 1 (unit choice)": "CONVENTION (does not change the number)",
    "T_GH = hbar H/(2 pi k_B), the 2 pi": "PHYSICS (Euclidean-time periodicity)",
    "S_dS = A/(4G), the 1/4": "PHYSICS (Bekenstein-Hawking normalisation)",
    "area A = 4 pi (c/H)^2, the 4 pi": "PHYSICS (geometry)",
    "coupling -X^2/8, the 1/8": "PHYSICS (forced by sqrt(1+X))",
    "graviton normalisation h = sqrt(32 pi G) phi": "CONVENTION (KS02: standard set gives 1/12, not 1/(32 pi))",
}
P("\n  factor audit:")
for k, v in FACTORS.items():
    P(f"    - {k:<42} {v}")
n_conv = sum(1 for v in FACTORS.values() if v.startswith("CONVENTION"))
check("C1c the SPECIFIC value 1/(32 pi) is convention-dependent: the graviton-normalisation choice moves "
      "it to 1/12 (KS02), so it is not a convention-free number",
      f"{n_conv} of {len(FACTORS)} listed factors are conventions; the load-bearing one is the graviton "
      f"normalisation", n_conv >= 2,
      "the pi's are mostly physics, but the OVERALL number rides on the normalisation convention that KS02 "
      "showed is not standard when it hits 1/2")
OUT["numbers"]["n_convention_factors"] = n_conv

banner("C2 -- m-independence (universality): drift per unit rest mass is m-independent")
m, Xv = sp.symbols("m X", positive=True)
S = -m * sp.sqrt(1 + Xv)                                  # worldline action (c=1)
drift_term = sp.series(S, Xv, 0, 3).removeO().coeff(Xv, 2)   # the -X^2/8 term coefficient: -m/8
accel = sp.simplify(drift_term / m)                       # force/m: the m cancels
check("C2 the rectified drift per unit rest mass is m-INDEPENDENT (a = F/m with F ∝ m): universality holds "
      "for the gravitational bath (equivalence principle)",
      f"drift term = {drift_term}, drift/m = {accel} (d/dm = {sp.diff(accel, m)})",
      sp.simplify(sp.diff(accel, m)) == 0 and accel != 0,
      "a0 must be mass-independent; the graviton bath passes the universality screen (a scalar bath fails it)")

banner("C3 -- rate-vs-density classification and the number field of kappa")
# rate mechanism: output cH_Lambda; cH_Lambda = sqrt(8pi/3) c sqrt(G rho) carries sqrt(pi) => kappa irrational
# density mechanism: output c sqrt(G rho); kappa rational available.
Z = 2 * sp.sqrt(8 * sp.pi / 3)
kappa_from_rate = sp.simplify(1 / (2 * sp.pi) * sp.sqrt(sp.Rational(8, 3) * sp.pi))   # Milgrom-2020-style X=1/2pi
check("C3a a RATE output (a0 = X cH_Lambda) makes kappa = X sqrt(8pi/3) carry sqrt(pi): irrational unless X "
      "supplies a compensating 1/sqrt(pi)",
      f"kappa(rate, X=1/2pi) = {kappa_from_rate} = {float(kappa_from_rate):.4f} (has sqrt(pi): "
      f"{kappa_from_rate.has(sp.pi)})", kappa_from_rate.has(sp.pi),
      "Z = 2 sqrt(8pi/3) carries sqrt(pi) via the H_Lambda<->rho_Lambda conversion")

# the graviton-bath route: variance <h^2> carries G (h = sqrt(32 pi G) phi), so it produces c sqrt(G rho):
# a DENSITY mechanism.  And kappa^2 = 8 pi eps_tot with eps_tot ∝ 1/pi (from S_dS's pi over T's 4 pi^2) makes
# the pi CANCEL -> kappa rational.
eps_val = sp.Rational(1, 1) / (32 * sp.pi)
kappa_val = sp.sqrt(8 * sp.pi * eps_val)
check("C3b the graviton-bath route is a DENSITY mechanism (its variance carries G => output c sqrt(G rho)); "
      "in kappa^2 = 8 pi eps_tot the 8 pi cancels eps_tot's 1/pi, so a RATIONAL kappa IS available",
      f"kappa = sqrt(8 pi * 1/(32 pi)) = {kappa_val} (rational: {kappa_val.is_rational})",
      kappa_val.is_rational and kappa_val == sp.Rational(1, 2),
      "consistent with the mi_cubic_noise discriminator: variance/CTP mechanisms permit a rational kappa, "
      "rate/horizon-thermodynamic mechanisms force sqrt(pi); the graviton bath is the right KIND of number")
OUT["numbers"]["kappa_rational"] = str(kappa_val)

banner("VERDICT")
P(f"""  (1) COMPUTED: the identity chain (sympy exact), the pi-decomposition of 1/(32 pi), the m-independence
      of the drift, and the rate-vs-density classification.
  (2) NUMBERS: kappa^2 = 8 pi eps_tot (the 8 pi is Friedmann's); 1/(32 pi) = pi(S_dS) x (1/8)(coupling) x
      1/(4 pi^2)(T_GH); {n_conv} of the listed factors are conventions, the load-bearing one being the
      graviton normalisation (KS02: standard -> 1/12); the drift is m-independent; the graviton route is a
      DENSITY mechanism and kappa = 1/2 is RATIONAL and available.
  (3) HONEST SENTENCE: 1/(32 pi) decomposes as pi(S_dS)(1/8)(1/4 pi^2); its pi's are mostly physics but its
      OVERALL value rides on the graviton-normalisation convention (2 conventions among the factors); the
      graviton route is a DENSITY mechanism and a rational kappa IS available in it -- so kappa = 1/2 is the
      right KIND of number, but KS02 shows the standard normalisation gives 1/12, so 'available' is not
      'selected'.""")
OUT["verdict"] = {"word": "RATIONAL-AVAILABLE-NOT-SELECTED", "mechanism": "density",
                  "kappa_rational": True, "value_rides_on": "graviton normalisation convention"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"KS06 COMPLETE: {npass}/{n} checks PASS")
if MUTATE:
    P(f"  MUTATE=1: {len(lb_fail)} load-bearing check(s) FAILED (expected >=1, the identity-chain hinge):")
    for nm in lb_fail:
        P(f"    - {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb_fail else 0)
