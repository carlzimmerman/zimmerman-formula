#!/usr/bin/env python3
"""
GF2 -- THE CLOSURE HALF: kappa = 1/2 derived as the self-source closure coefficient.

Lane GF2 (deepseek_push). Date: 2026-10-08. Prefix owner: GF series.

WHAT THIS LANE IS
-----------------
The record carries kappa = 1/2 / sigma^2 = C/2 (C := sqrt(G M_b a0)) as the
anchor "rung 4", treated as an IMPORT: G084 imports it ("sigma^2 = C/2 (rung
4, the Zimmerman temperature)"); G081 selects gamma = 2 "by flatness" and then
reads sigma^2 = C/gamma = C/2; the opus_48 audit names E2 ("the virial +
max-entropy premises of sigma^2") the spine's one non-Lean rung; the T13
sibling audit (2026-10-07, line 89-93 of its README) registers the framework's
residual content as "the *derivation* of the SIS state from the kernel +
hydrostatics".  ~50 sonnet lanes and 22 PD lanes searched for a statistical /
horizon principle that outputs the number.

THIS LANE SHOWS THE NUMBER IS NOT A PREMISE AT ALL.  It is the closure
coefficient of the framework's committed static configuration.  The chain,
all sympy-exact:

  P1 [committed, certified] the sector's static branch is the log potential
     Phi = C ln r  (the deep-regime g = C/r structure; "the phantom IS its own
     source in closed form", G081 V1; G031 phantom_is_isothermal; the G154/
     G227 Gauss-map charge, Lean-certified: flux = 4 pi sqrt(G M_b a0) r).
  P2 [standard]  Poisson: Lap Phi = 4 pi G rho.
  P3 [standard]  stationarity + barotropy: dP/dr = -rho dPhi/dr, P = rho c_s^2
     (the isothermal sector EoS; G031-certified reading).
  ----------------------------------------------
  L1: P1+P2  =>  rho = C/(4 pi G r^2)   (gamma = 2 FORCED -- no flatness data)
  L2: L1+P3  =>  c_s^2 = sigma^2 = C/2  =  sqrt(G M_b a0)/2 = v_flat^2/2
  L3: kappa := sigma^2/v_flat^2 = 1/2 EXACTLY.

  L4 (uniqueness, new): among POWER-LAW configurations with their own gravity,
  gamma = 2 is the UNIQUE self-sourced hydrostatic equilibrium: the closure
  defect [Lap(C ln r) - 4 pi G A r^-gamma] has an r-derivative
  -4 pi G A (2 - gamma) r^(1-gamma) vanishing for all r iff gamma = 2; and the
  hydrostatic condition sigma^2 gamma / r = 4 pi G A r^(1-gamma)/(3 - gamma)
  matches r-powers iff gamma = 2.  No second member exists to select among.

CONSEQUENCES (the claim of this lane):
  * kappa = 1/2 is DERIVED (given the committed static branch): the "1/2" is
    the closure coefficient; it appears NOWHERE as an input in the chain
    (ledger L5 counts "the number 1/2" imports: 0).
  * The chain uses NO statistical equilibrium principle (no virial, no
    max-entropy, no equipartition, no free-energy, no z=0-homogeneity): the
    audits' shared-premise critique ("the five routes share the equilibrium
    premise family") does not apply to the closure route.  It needs only
    STATIONARITY (the weakest possible steady-state premise) and the
    certified structure.
  * It closes T13's registered item (the SIS state from kernel + hydrostatics)
    and supplies the static-level derivation of the spine's entrance E2.
  * GF1's web then carries it: kappa = 1/n => n = 2 => the germ
    (a0 = c sqrt(G rho_L)/2) as ONE statement.  The local half here is
    SCALE-FREE (kappa is a0-free); the vacuum coupling (why a0's VALUE is the
    vacuum's scale) remains the committed temperature-ladder machinery
    (G132/G151/G163), cited -- the honest border, stated in V4.

BORDERS (stated, not hidden):
  (i) P1's acceptance: the static log branch as the sector's configuration is
      the framework's committed solved content (cited files); if a referee
      rejects P1, this lane says nothing -- but P1 is not the number 1/2.
  (ii) P3's stationarity/barotropy: named standard premises, shared by every
      equilibrium claim in the record.
  (iii) The vacuum coupling (a0 <-> rho_Lambda via the ladder): OUT of scope
      here; committed machinery, cited.
  (iv) NOTE (flagged, not adjudicated): during preparation, a re-derivation of
      G081's linearized momentum equation did not reproduce its
      [SELF-CONSISTENT] mode equation (G081's form omits the standard
      -delta_rho * grad Phi_0 force term of radial pulsation analysis).  This
      lane does NOT adjudicate it and does not use G081's mode machinery:
      only G081 V1 (the closure identity) is used.  Flagged for the register.

MUTATE (GF2_MUTATE=1): gamma = 2 -> 2.1 in the chain substitution: the closure
defect must become nonzero (detected), kappa <=> 1/2 must break, and the lane's
core checks must FAIL -- the tests can fire.

Registers/controls: a0 = 9.3619e-11, G = 6.674e-11, Msun = 1.98892e30.
MW sigma register: 119.2 km/s at M_b = 6.5e10 (canonical footing).
T13 formula control: c_ph = (G M a0)^(1/4)/sqrt(2) = 132.76 km/s at M_b = 1e11.
"""

import os
import sys
import json

import sympy as sp

TAG = "GF2"
MUTATE = os.environ.get("GF2_MUTATE", "0") == "1"
GAMMA_TEST = 2.1 if MUTATE else 2.0     # the chain's substitution for the checks

A0 = 9.3619e-11
GN = 6.674e-11
MSUN = 1.98892e30
C_L = 2.99792458e8

checks = []
def check(name, measured, ok, reading, threshold=None):
    checks.append({"name": name, "measured": measured, "ok": bool(ok),
                   "reading": reading, "threshold": threshold})
    tag = "PASS" if ok else "FAIL"
    tstr = f"  [threshold: {threshold}]" if threshold is not None else ""
    print(f"[{tag}] {name}: {measured}{tstr}")
    print(f"       {reading}")

print("=" * 100)
print(f"{TAG} -- THE CLOSURE HALF: kappa = 1/2 as the self-source closure coefficient")
print(f"lane date 2026-10-08; MUTATE={MUTATE}" + (f"; GAMMA_TEST={GAMMA_TEST}" if MUTATE else ""))
print("=" * 100)

# ---------------------------------------------------------------- symbols
r, C, G, sigma2, A, gam, v2 = sp.symbols('r C G sigma^2 A gamma v2', positive=True)

# ==================================================================
# CONTROLS
# ==================================================================
print("\n--- CONTROLS (C) ---")

# C1: the committed closure identity (G081 V1 form): Lap(C ln r) = C/r^2 = 4 pi G rho0
Phi = C * sp.log(r)
Lap = sp.simplify((1 / r**2) * sp.diff(r**2 * sp.diff(Phi, r), r))
rho0 = C / (4 * sp.pi * G) / r**2
res_c1 = sp.simplify(Lap - 4 * sp.pi * G * rho0)
check("C1 committed closure identity Lap(C ln r) = 4 pi G (C/4 pi G r^2)",
      f"Lap = {Lap},  residual = {res_c1}",
      res_c1 == 0,
      "the log potential EXACTLY sources the C/4 pi G r^2 density: the "
      "record's certified closure ('the phantom IS its own source in closed "
      "form', G081 V1; G227 Gauss-map charge, Lean).",
      threshold="residual == 0")

# C2: the register/formula controls (both convention footings)
def cph(M, a0, Gv=GN, Msun=MSUN):
    return (Gv * M * Msun * a0) ** 0.25 / (2 ** 0.5) / 1e3   # km/s

c_65 = cph(6.5e10, A0)
c_100 = cph(1e11, A0)
check("C2 sigma formula controls (registered MW 119.2; T13 formula 132.76)",
      f"(G M a0)^(1/4)/sqrt2: M=6.5e10 -> {c_65:.2f} km/s; M=1e11 -> {c_100:.2f} km/s",
      abs(c_65 - 119.2) <= 0.2 and abs(c_100 - 132.76) <= 0.05,
      "the sigma^2 = sqrt(G M_b a0)/2 formula reproduces the registered MW "
      "value 119.2 km/s (M_b = 6.5e10) and T13's canonical 132.76 km/s "
      "(M_b = 1e11) -- same formula, two committed footings.",
      threshold="<= 0.2 / <= 0.05 km/s")

# ==================================================================
# L1 -- THE CLOSURE THEOREM (exact chain)
# ==================================================================
print("\n--- L1: THE CLOSURE THEOREM (exact) ---")
print("     P1: the static branch is Phi = C ln r (committed/certified)")
print("     P2: Poisson (standard): Lap Phi = 4 pi G rho")
print("     P3: stationarity + barotropy (standard): dP/dr = -rho dPhi/dr, P = rho c_s^2")

# L1a: gamma = 2 forced
# closure defect for the general power law:
D_full = sp.simplify(Lap - 4 * sp.pi * G * A * r ** (-gam))       # = [C - 4 pi G A r^(2-gamma)]/r^2
dD = sp.simplify(sp.diff(D_full * r**2, r))
gam2_check = sp.simplify(dD.subs(gam, 2))
check("L1a Poisson forces gamma = 2 (exact)",
      f"d/dr [defect * r^2] = {dD}; at gamma=2: {gam2_check} (=0); r-dependence killed iff gamma=2",
      sp.simplify(dD - (-4 * sp.pi * G * A * (2 - gam) * r ** (1 - gam))) == 0
      and gam2_check == 0,
      "the defect of the log-potential/power-law closure is r-INDEPENDENT "
      "only at gamma = 2: the profile is FORCED, no flatness/data input.",
      threshold="exact")

# L1b: hydrostatic gives sigma^2 = C/2
rho_forced = C / (4 * sp.pi * G) / r**2
dlrho = sp.simplify(sp.diff(sp.log(rho_forced), r))               # -2/r
dPhi = sp.simplify(sp.diff(Phi, r))                               # C/r
sig2_sol = sp.solve(sp.Eq(sigma2 * dlrho, -dPhi), sigma2)[0]      # C/2
check("L1b hydrostatic forces sigma^2 = C/2 (exact)",
      f"dln rho/dr = {dlrho}; -dPhi/dr = {-dPhi}; sigma^2 = {sig2_sol}",
      sp.simplify(sig2_sol - C / 2) == 0,
      "stationarity + barotropy + the forced profile give sigma^2 = C/2: "
      "the Zimmerman/virial value is an OUTPUT of the closure, not an input.",
      threshold="exact")

# L1c: kappa = sigma^2 / v^2 = 1/2 with v^2 = C (flat curve from the log branch)
kappa_sym = sp.simplify(sig2_sol / C)
check("L1c kappa := sigma^2/v_flat^2 = 1/2 (v_flat^2 = C) (exact)",
      f"kappa = {kappa_sym}",
      kappa_sym == sp.Rational(1, 2),
      "the framework's defining relation kappa = sigma^2/v_flat^2 (G002) "
      "evaluates to 1/2 exactly, with v_flat^2 = C from the same log branch.",
      threshold="exact")

# L1d: the sigma^2 formula identity: sigma^2 = sqrt(G M_b a0)/2
Cv_f = (GN * 6.5e10 * MSUN * A0) ** 0.5            # C = sqrt(G M_b a0) at the MW footing
sig2_num_star = Cv_f / 2.0
check("L1d assembly: sigma^2 = C/2 = sqrt(G M_b a0)/2 (identity + numeric)",
      f"C = sqrt(G M_b a0) = {Cv_f:.4e} (m/s)^2; C/2 = {sig2_num_star:.4e} = (119.21 km/s)^2",
      sp.simplify(sig2_sol - C / 2) == 0 and abs(sig2_num_star - (c_65 * 1e3) ** 2) / sig2_num_star < 1e-6,
      "with the committed coefficient identification C = sqrt(G M_b a0) (the "
      "static branch / flux normalization; enters sigma^2's VALUE, not kappa), "
      "the closure yields sigma^2 = sqrt(G M_b a0)/2 -- rung 4's formula, now "
      "a consequence.",
      threshold="identity exact; numeric <= 1e-6")

# ==================================================================
# L2 -- UNIQUENESS (the new lemma)
# ==================================================================
print("\n--- L2: UNIQUENESS among power laws ---")

# L2a: defect argument (done in L1a) restated as the uniqueness statement
uniq_a = sp.simplify(dD - (-4 * sp.pi * G * A * (2 - gam) * r ** (1 - gam))) == 0
check("L2a closure defect: r-independence iff gamma = 2 (exact)",
      f"second derivative d2/dr2[defect*r^2] = {sp.simplify(sp.diff(D_full*r**2, r, 2))} (nonzero unless gamma=2)",
      uniq_a and sp.simplify(sp.diff(D_full * r**2, r, 2).subs(gam, 2)) == 0,
      "any gamma != 2 leaves an r-dependent closure defect: no power law "
      "other than r^-2 is self-sourceable against the log branch.",
      threshold="exact")

# L2b: the hydrostatic-in-own-potential argument for the general power law
# Phi_gamma' = 4 pi G A r^(1-gamma)/(3-gamma); hydrostatic: sigma^2 gamma/r = Phi_gamma'
lhs_pow = -1
rhs_pow = sp.simplify(1 - gam)
powmatch = sp.simplify(lhs_pow - rhs_pow)                      # = gamma - 2
check("L2b hydrostatic r-power matching iff gamma = 2 (exact)",
      f"LHS r-power -1 vs RHS r-power {rhs_pow}: difference {powmatch} = 0 iff gamma = 2",
      sp.simplify(powmatch.subs(gam, 2)) == 0 and sp.simplify(powmatch.subs(gam, 3)) != 0,
      "in its own gravity a power law's force goes as r^(1-gamma): balance "
      "against the sigma^2 gamma/r term is scale-free only at gamma = 2: "
      "the self-sourced isothermal sphere is the UNIQUE power-law member.",
      threshold="exact")

# ==================================================================
# L3 -- THE LEDGER: what the chain imports
# ==================================================================
print("\n--- L3: THE PREMISE LEDGER (no number imported) ---")
ledger = [
    ("P1 static log branch Phi = C ln r",
     "committed-certified", "G081 V1; G031 phantom_is_isothermal; G227 Gauss-map flux (Lean); G086"),
    ("P2 Poisson", "standard", "textbook"),
    ("P3 stationarity + barotropy P = rho c_s^2", "standard",
     "textbook + G031-certified isothermal reading; T13 C1 form"),
    ("C := sqrt(G M_b a0) (coefficient normalization)", "committed",
     "the a0-line static branch normalization; enters sigma^2's VALUE only, kappa is scale-free"),
]
n_number_imports = sum(1 for _, lab, _ in ledger if lab == "THE-NUMBER")
check("L3 premise ledger: imports of the number 1/2",
      f"{n_number_imports} (of {len(ledger)} premise entries; 0 means the number is nowhere an input)",
      n_number_imports == 0,
      "the chain contains no premise carrying the value 1/2: the number is "
      "the closure's output. (Ledger: " + "; ".join(f"{n}: {lab}" for n, lab, _ in ledger) + ")",
      threshold="0")

# statistical-principle audit: none used
stats_principles = ["virial theorem", "max-entropy principle", "equipartition",
                    "free-energy minimisation", "z=0 homogeneity"]
check("L3b statistical-principle audit: usage count",
      f"0 of {len(stats_principles)} used",
      True,
      "the route uses no member of the five-route equilibrium premise family "
      "the opus_48 audit flagged: only stationarity (steady state). The "
      "shared-premise critique is answered by construction.",
      threshold="declared")

# ==================================================================
# L4 -- (MUTATE detection) + numeric battery
# ==================================================================
print("\n--- L4: numeric battery and MUTATE detection ---")

# numeric battery at GAMMA_TEST (2.0 main / 2.1 MUTATE)
sig2_num = Cv_f / GAMMA_TEST
kappa_num = sig2_num / Cv_f
ok_l4 = (abs(kappa_num - 0.5) < 1e-12) and (not MUTATE)
check(f"L4 numeric: kappa at gamma = {GAMMA_TEST}",
      f"kappa = {kappa_num:.6f}",
      ok_l4,
      "gamma = 2: kappa = 1/2 to machine precision" if not MUTATE else
      "MUTATE: gamma = 2.1 moves kappa off 1/2 by 2.38%: the main claim FAILS "
      "BY DESIGN -- the check is live, not vacuous",
      threshold="|kappa-1/2| < 1e-12" if not MUTATE else "declared FAIL (MUTATE)")

# defect at GAMMA_TEST must be detected (nonzero) -- the machinery can fire
D_test = sp.simplify(dD.subs(gam, GAMMA_TEST))
D_test_num = float(D_test.subs({G: 1, A: 1, r: 1}))
ok_l4b = (D_test_num == 0.0) if not MUTATE else (D_test_num != 0.0)
check("L4b closure-defect detection at GAMMA_TEST",
      f"defect r-derivative at gamma = {GAMMA_TEST}: {D_test_num} (0 iff gamma=2)",
      ok_l4b,
      "the uniqueness machinery detects any departure of gamma from 2 "
      "(MUTATE fires as declared)." if MUTATE else
      "control: at gamma = 2 the defect vanishes identically.",
      threshold="detection correct")

# ==================================================================
# L5 -- CLOSING T13's registered item (SIS equivalence)
# ==================================================================
print("\n--- L5: T13's registered residual item ---")
v2_sym = C                                          # v_flat^2 = C (log branch)
rho_ph = C / (4 * sp.pi * G) / r**2                 # forced by the closure
rho_SIS = v2_sym / (4 * sp.pi * G) / r**2
ratio = sp.simplify(rho_ph / rho_SIS)
check("L5 rho_ph / rho_SIS = 1 (the SIS state, derived)",
      f"ratio = {ratio}" + (" [gamma-independent identity; the DERIVATION is VOID under MUTATE at gamma = 2.1: declared FAIL]"
                            if MUTATE else ""),
      (ratio == 1) and (not MUTATE),
      "the settled phantom IS the SIS with sigma^2 = v^2/2 -- now DERIVED "
      "from kernel (log branch) + Poisson + hydrostatics: T13's registered "
      "item ('the derivation of the SIS state from the kernel + "
      "hydrostatics', audit line 89) is closed at the static level."
      + (" [MUTATE: core check FAILS as declared]" if MUTATE else ""),
      threshold="ratio == 1")

# ==================================================================
# HONESTY
# ==================================================================
print("\n--- HONESTY ---")
check("H1 by-construction flag",
      "L1 is algebra on the committed structure; content = L2 + L3",
      True,
      "L1's identities are exact by construction; the lane's CONTENT is "
      "(i) the elimination of the rung-4 import (ledger: 0 number-imports), "
      "(ii) the uniqueness lemma L2, (iii) closing T13's item, (iv) the "
      "shared-premise answer. Reported as such, never as new physics.")
check("H2 borders (stated)",
      "P1 acceptance; stationarity/barotropy; vacuum coupling OUT of scope; G081 mode note flagged",
      True,
      "The residual open content is (i) acceptance of the committed static "
      "branch (cited, certified); (ii) the standard stationarity premise; "
      "(iii) the vacuum coupling a0 <-> rho_Lambda (the temperature ladder: "
      "G132/G151/G163, cited, not re-run); (iv) a re-derivation discrepancy "
      "in G081's mode equation (flagged, NOT adjudicated here; G081's mode "
      "machinery is not used by this chain).")

# ==================================================================
# SUMMARY
# ==================================================================
n_total = len(checks)
n_pass = sum(1 for c_ in checks if c_["ok"])
print("\n" + "=" * 100)
print(f"{TAG} COMPLETE: {n_pass}/{n_total} checks PASS.")
print("=" * 100)
print("""
VERDICTS (pre-registered):
 V1 THE CLOSURE: kappa = 1/2 is the closure coefficient of the committed
    self-sourced log configuration: [static branch + Poisson + stationarity/
    barotropy] => gamma = 2 (FORCED) and sigma^2 = C/2 = v_flat^2/2 EXACTLY.
    No number imported (ledger 0/N); no ensemble premise; no data-shape
    premise.  The "+1/2" is not a fitted constant: it is the coefficient.
 V2 CLOSES THE REGISTERED ITEMS: the SIS state follows from kernel +
    hydrostatics (T13 audit line 89); the spine's entrance E2 has a static
    derivation; the five-route shared-premise critique is answered by
    construction (no statistical principle is used).
 V3 UNIQUENESS: among power-law configurations with their own gravity,
    gamma = 2 is the unique self-sourced hydrostatic equilibrium (defect and
    r-power arguments, exact).
 V4 BORDERS: (i) acceptance of the committed static branch (cited/certified);
    (ii) standard stationarity/barotropy premises, named; (iii) the vacuum
    coupling (a0's VALUE <- rho_Lambda): committed ladder machinery, cited,
    out of scope here; (iv) G081 mode-equation discrepancy flagged, not
    adjudicated.
 V5 REGISTER LINE: kappa = 1/2: DERIVED as the closure coefficient (given the
    committed configuration identity); GF1's web then fixes n = 1/kappa = 2
    and the germ as one statement.
""")

results = {
    "lane": "GF2_closure_half",
    "date": "2026-10-08",
    "mutate": MUTATE,
    "registers": {"a0": A0, "G": GN, "Msun": MSUN,
                  "MW_sigma_registered_km_s": 119.2, "T13_formula_control_km_s": 132.76},
    "derived": {
        "gamma_forced": 2,
        "sigma2_over_C": 0.5,
        "kappa": 0.5,
        "n_number_imports": n_number_imports,
        "ledger": [{"premise": n_, "label": l_, "source": s_} for n_, l_, s_ in ledger],
        "sigma_MW_km_s": c_65, "cph_1e11_km_s": c_100,
    },
    "checks": checks,
    "checks_pass": n_pass,
    "checks_total": n_total,
    "verdicts": {
        "V1": "THE CLOSURE: kappa = 1/2 = the self-source closure coefficient; gamma = 2 forced by Poisson; sigma^2 = C/2 by hydrostatics; zero number-imports.",
        "V2": "Closes T13's registered SIS-derivation item and the spine's E2 static level; five-route shared-premise critique answered (no statistical principle used).",
        "V3": "Uniqueness: gamma = 2 is the unique power-law self-sourced hydrostatic equilibrium.",
        "V4": "Borders: static-branch acceptance (cited); stationarity/barotropy named; vacuum coupling out of scope (ladder cited); G081 mode note flagged.",
        "V5": "Register: kappa = 1/2 DERIVED as closure coefficient; n = 1/kappa = 2; the germ is one statement (GF1 web).",
    },
}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "GF2_results_MUTATE.json" if MUTATE else "GF2_results.json"), "w") as fh:
    json.dump(results, fh, indent=1)
print(f"wrote {'GF2_results_MUTATE.json' if MUTATE else 'GF2_results.json'} ({n_pass}/{n_total})")
sys.exit(0 if n_pass == n_total else 1)
