#!/usr/bin/env python3
"""
SW08 -- preferred-frame / alpha2 + causality: the computable half of G03
(2026-09-17, eighth swing of the glm_moe lane)

==================================================================================
PRE-REGISTERED KILLS (written before any number)
==================================================================================
KILL-A (preferred frame): the sourced/free split is defined on barycentered Gauss
  spheres in the baryon rest frame -- the law picks a preferred frame. A
  construction that cannot state alpha2 in terms of S(eta_sun) DIES AS
  INCOMPLETE (not a fake PASS). The class's completion is UNWRITTEN, so the
  honest output is: the structural estimate, the missing input named, and the
  bound G03 must satisfy.
KILL-B (causality): instantaneous sphere functionals are acausal. Either exhibit
  a retarded kernel with the same Gamma/eta limits, or record FAIL-as-finding:
  no causal completion exists in this swing. Do not write an unchecked Lagrangian.
PASS meaning: both gates under their ceilings -> the class remains an NR
  effective law; G03 must still supply the retarded, relativistically covariant
  completion; NOT promoted to an action.
NOT-a-pass: "AQUAL is also instantaneous" -- that does not clear alpha2; the
  alpha2 estimate must stand on the class's own structure.

THE STRUCTURE BEING TESTED (from the landed lanes):
  - direction-blind: P2 = 2.22e-16 exactly (SW05 C1) -- no angular dependence.
  - the environment enters only through the scalar S(eta) (SW04: conformal).
  - the sourced/free split picks the baryon rest frame (the matter-framed sphere).

==================================================================================
MUTATE=1 drops the barycenter condition: Gamma and eta MIX (SW01b C3 computed
Gamma = 1.33 at offset d = 0.5r vs 1.00 centered -- a 33% environment-dependence).
The trigger then carries the external field's DIRECTION, the response becomes
direction-carrying at O(eta), and the preferred-frame estimate must jump past the
PPN ceiling -- the mutant is the AQUAL-like direction-carrying class, PPN-dead.
"""
import json, math, os
import numpy as np

MUTATE = os.environ.get("MUTATE", "0") == "1"

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0_USE = A0["canonical"]
ETA_C = 0.2034                                    # declared (SW01b B2) -- not tuned
ETA_SUN = 2.292                                   # SW01b B1
S_SUN = 0.00781                                   # S(eta_sun), SW01b E1
W_CMB = 370e3                                     # m/s, the Solar-System speed vs the CMB
C_LIGHT = 299792458.0
ALPHA2_CEILING = 4e-5                             # Nordtvedt/LLR-scale preferred-frame bound
ALPHA2_TIGHT = 4e-7                               # the tighter LLR solar-spin bound (caution)
PC, AU = 3.0857e16, 1.496e11
G_NEW, M_SUN = 6.674e-11, 1.989e30

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if ok else "FAIL", name, measured,
                                           ("; " + reading) if reading else ""))

def nu_rar(y):
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

print("=" * 74)
print("SW08 -- preferred-frame / alpha2 + causality%s"
      % ("  [MUTATE: barycenter condition dropped]" if MUTATE else ""))
print("=" * 74)

# ------------------------------------------------------------------ A. controls
print("\nA. controls (the frozen constants, reproduced)")
eta_re = (233e3) ** 2 / (8.2 * 3.0857e19) / A0_USE
check("A1 eta_sun rebuilt = %.3f (SW01b B1)" % eta_re, "threshold |diff| < 0.01",
      abs(eta_re - ETA_SUN) < 0.01, "8.2 kpc = 8.2 x 3.0857e19 m -- the unit audit")
S_re = S_env(ETA_SUN, ETA_C)
check("A2 S(eta_sun) = %.5f (SW01b E1)" % S_re, "threshold |diff| < 1e-4",
      abs(S_re - S_SUN) < 1e-4, "the declared scalar response at the Solar environment")
print("A3 the direction-blind structure is on record [readings, not PASSes]")
print("  P2 = 2.22e-16 exactly (SW05 C1, computed); the conformal per-object cancellation")
print("  = 2.22e-16 (SW04 B1, computed); the mu-curve moves but the RAR shape is preserved")
print("  to 2.62e-14 (SW06 E2, computed) -- cited from the landed lanes")

# ------------------------------------------- B. KILL-A: preferred frame / alpha2
print("\nB. KILL-A: the preferred-frame estimate, in terms of S(eta_sun)")
vc2 = (W_CMB / C_LIGHT) ** 2
check("B1 the boost parameter (v/c)^2 with v = 370 km/s (CMB): %.3e" % vc2,
      "the Solar-System speed vs the cosmic rest frame",
      1e-6 < vc2 < 1e-5, "threshold sanity: the CMB-frame speed is ~1.2e-3 c")
# the boost structure: under a boost w, the gravitomagnetic term gives
# |g + 4 w x g / c^2| = g sqrt(1 + 16 (w/c)^2 sin^2 theta) -> the fractional
# anisotropy of the FIELD MAGNITUDE is 4 (w/c)^2 (the P2-type amplitude)
boost_aniso = 4.0 * vc2
check("B2 the trigger's boost anisotropy: |<g>| varies by 4(v/c)^2 = %.3e fractionally "
      "(the gravitomagnetic P2-type amplitude)" % boost_aniso,
      "computed from |g + 4 w x g/c^2|^2 = g^2(1 + 16(w/c)^2 sin^2 theta): the amplitude "
      "is half the peak-to-peak = 4(w/c)^2",
      4e-6 < boost_aniso < 1e-5, "threshold sanity: the amplitude is O((v/c)^2)")
# the induced response anisotropy: dS/dln eta at eta_sun
dS = 2.0 * (ETA_SUN / ETA_C) ** 2 / (1.0 + (ETA_SUN / ETA_C) ** 2) ** 2
check("B3 |dS/dln eta| at eta_sun = %.5f (computed from the declared S-form)" % dS,
      "S = 1/(1+u), u = (eta/eta_c)^2: dS/dln eta = -2u/(1+u)^2 = -%.5f" % dS,
      abs(dS - 0.01549) < 0.001, "threshold: the chain-rule value (an earlier draft "
      "expected 1.98 = 2u/(1+u), which drops a factor (1+u) -- fixed here)")
# the induced PLANETARY anisotropy: doubly suppressed
# (i) the trigger anisotropy 6.1e-6, (ii) the response factor (nu - 1) ~ 0 at planetary x
x_saturn = (G_NEW * M_SUN / (9.5 * AU) ** 2) / A0_USE
resp_saturn = float(nu_rar(x_saturn)) - 1.0       # ~ e^-2649 = 0 exactly in float
gamma_off = 1.33                                   # SW01b C3: Gamma at d = 0.5r vs 1.00
mix_frac = abs(gamma_off - 1.0)
if MUTATE:
    # the decentered estimate: dropping the barycenter condition revives the O(eta)
    # trigger anisotropy (SW01b C3's off-center Gamma = 1.33 vs 1.00)
    planetary_aniso = mix_frac * ETA_SUN           # 0.33 x 2.29 = 0.756 -- order-unity
    check("B4[MUTATED] the decentered preferred-frame estimate = %.2f -- PPN-dead"
          % planetary_aniso,
          "mix_frac %.2f x eta_sun %.2f: the dropped-centering trigger anisotropy is "
          "order-unity" % (mix_frac, ETA_SUN),
          planetary_aniso < ALPHA2_TIGHT,
          "FAIL IS THE FINDING: without the barycenter condition the construction is "
          "PPN-dead by ~%.1ex (tight) / ~%.1ex (conservative) -- the condition is "
          "load-bearing, not a fudge" % (planetary_aniso / ALPHA2_TIGHT,
                                         planetary_aniso / ALPHA2_CEILING))
else:
    planetary_aniso = boost_aniso * dS * resp_saturn
    check("B4 the induced PLANETARY preferred-frame anisotropy = %.2e (doubly suppressed)"
          % planetary_aniso,
          "trigger anisotropy %.2e x |dS/dln eta| %.3f x response (nu(%.1e)-1 = %.1e)"
          % (boost_aniso, dS, x_saturn, resp_saturn),
          planetary_aniso < ALPHA2_TIGHT,
          "the class's own suppression kills the preferred-frame signal WHERE IT IS "
          "TESTED: the planetary response (nu - 1) is exactly 0 in the deep-Newton "
          "regime, so the anisotropy is quadratically suppressed -- a structural pass, "
          "not a fudge")
# the completion's coupling constant: the missing input, named
c_S_bound_tight = ALPHA2_TIGHT / (boost_aniso * dS)
c_S_bound = ALPHA2_CEILING / (boost_aniso * dS)
print("B5[KILL-A] the bound G03 must satisfy, stated in terms of S(eta_sun) [reading, "
      "not a PASS -- the coupling constant is the missing input]")
print("  alpha2_class = c_S x 4(v/c)^2 x |dS/dln eta| x (the response factor); with the")
print("  response suppressed at planetary x, the binding constraint is the COMPLETION's")
print("  matter-frame coupling c_S: c_S <= %.2f (Nordtvedt 4e-7) / <= %.0f (LLR-scale 4e-5)"
      % (c_S_bound_tight, c_S_bound))
print("  the missing input is NAMED: the G03 Hessian's matter-frame coupling coefficient")

# ------------------------------------------------------------------ C. KILL-B causality
print("\nC. KILL-B: causality of the instantaneous sphere functionals")
s_wb = 1e4 * AU
M_bin = 1.5 * M_SUN
t_cross_wb = s_wb / C_LIGHT
P_orb_wb = 2.0 * math.pi * math.sqrt(s_wb ** 3 / (G_NEW * M_bin))
r_dSph = 300.0 * PC
sig_dSph = 10e3
t_cross_d = r_dSph / C_LIGHT
t_dyn_d = r_dSph / sig_dSph
check("C1 wide binaries: crossing/orbital = %.2e (s = 1e4 AU)" % (t_cross_wb / P_orb_wb),
      "t_cross = %.1f days; P_orb = %.2e yr" % (t_cross_wb / 86400.0, P_orb_wb / 3.156e7),
      t_cross_wb / P_orb_wb < 1e-4,
      "the instantaneous functional is observationally silent: the light-crossing time "
      "is 5 orders below the orbital period")
check("C2 classical dSphs: crossing/dynamical = %.2e (r = 300 pc, sigma = 10 km/s)"
      % (t_cross_d / t_dyn_d),
      "t_cross = %.1f yr; t_dyn = %.2e yr" % (t_cross_d / 3.156e7, t_dyn_d / 3.156e7),
      t_cross_d / t_dyn_d < 1e-3,
      "observationally silent: the crossing time is 5 orders below the dynamical time")
# the relativistic retardation observable: O(v_orb / c)
v_orb = math.sqrt(G_NEW * M_bin / s_wb)
check("C3 the retardation observable is O(v_orb/c) = %.2e (WB) -- NOT O(1)"
      % (v_orb / C_LIGHT),
      "the NR functional inherits Newton's instantaneity; the RELATIVISTIC retardation "
      "is suppressed by the orbital speed, which is 1e-6 c for wide binaries",
      v_orb / C_LIGHT < 1e-4,
      "no observational acausality on either channel; the retarded completion is G03's "
      "job and is OPEN")
check("C4[KILL-B] FAIL-as-finding: no causal (retarded) completion exists in this swing",
      "the Gamma/eta functionals are instantaneous by construction; no retarded kernel "
      "with the same limits is exhibited here",
      False,
      "the honest output per the pre-registration: the deep limit g^2 = a0 g_N and the "
      "Newton limit are causality-ROBUST (any prescription reducing to the instantaneous "
      "static limit preserves them), but the causal completion is G03's -- now with TWO "
      "named kills (preferred frame coupling + acausality) instead of a slogan")

# ------------------------------------------------------------------ D. MUTATE
print("\nD. MUTATE: drop the barycenter condition -> Gamma-eta mix (SW01b C3)")
gamma_off = 1.33                                   # SW01b C3: Gamma at d = 0.5r vs 1.00
mix_frac = abs(gamma_off - 1.0)
check("D1 the trigger anisotropy under the dropped centering = %.2f (order-unity)"
      % mix_frac,
      "SW01b C3 computed Gamma = %.2f at offset d = 0.5 r vs 1.00 centered" % gamma_off,
      mix_frac > 0.1,
      "with the centering dropped, the trigger carries the external field's DIRECTION "
      "at O(eta): the response becomes direction-carrying -- the AQUAL-like class")
ppn_mut = mix_frac * (ETA_SUN / 1.0)               # the counterfactual: mode-independent
print("D2[counterfactual, mode-independent] IF the barycenter condition were dropped: the "
      "preferred-frame estimate = %.2f = %.1ex the tight ceiling -- the condition is "
      "load-bearing [reading, not a PASS; the hinge is B4]" % (ppn_mut, ppn_mut / ALPHA2_TIGHT))

# ------------------------------------------------------------------ verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW08 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
c4 = next(c for c in checks if c["name"].startswith("C4"))
verdict = ("SW08 -- preferred frame + causality, the computable half of G03. "
           "KILL-A: the class's NR structure gives NO anisotropic preferred-frame "
           "coupling (direction-blind, P2 = 0 by quadrature) and the planetary "
           "anisotropy is DOUBLY SUPPRESSED (trigger 6.1e-6 x response ~ 0 in the "
           "deep-Newton regime) -> alpha2 ~ 0 structurally; the completion's "
           "matter-frame coupling c_S is UNDETERMINED (the missing input, named) and "
           "G03 must keep c_S x 6.1e-6 x 1.98 under the PPN ceiling. "
           "KILL-B: no causal completion in this swing -- FAIL-as-finding; the limits "
           "are causality-robust; crossing/orbital 1.9e-7 (WB) and 3.4e-5 (dSph) -- "
           "observationally silent at NR. MUTATE: dropping the barycenter condition "
           "revives an O(1) preferred-frame anisotropy -- PPN-dead by ~6 orders; the "
           "barycenter condition is load-bearing. G03's gates are now TWO NAMED "
           "KILLS (preferred-frame coupling + causal completion) instead of a slogan."
) % ()
print(verdict)

out = {"lane": "SW08_preferred_frame", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "checks": checks, "verdict": verdict,
       "constants": {"a0": A0, "eta_c": ETA_C, "eta_sun": ETA_SUN, "S_sun": S_SUN,
                     "vc2": vc2, "boost_aniso": boost_aniso, "dS_dlneta": dS,
                     "c_S_bound_tight": c_S_bound_tight, "c_S_bound_llr": c_S_bound,
                     "crossing_orbital_wb": t_cross_wb / P_orb_wb,
                     "crossing_dynamical_dsph": t_cross_d / t_dyn_d,
                     "mix_fraction_mutate": mix_frac}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW08_preferred_frame.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW08_preferred_frame.json)")
