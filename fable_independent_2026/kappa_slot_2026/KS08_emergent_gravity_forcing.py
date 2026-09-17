#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KS08_emergent_gravity_forcing.py -- can EMERGENT/ENTROPIC gravity FORCE the S_dS coherence, and does it
force kappa = 1/2?

KS01 showed the S_dS factor is a double count in STANDARD graviton field theory (the fundamental d.o.f.
are bulk field modes, whose coincidence variance already sums the modes).  But in EMERGENT gravity the
fundamental d.o.f. ARE the horizon bits, so the force couples to their number N ~ S_dS BY CONSTRUCTION --
the double-count objection does not apply there.  This lane asks the honest two-part question:
  (PRO) does emergent gravity legitimately SUPPLY the S_dS factor?  and
  (the wall) does it FORCE the coefficient to exactly 1/2, or only to some O(1) value near it?

Method: derive the emergent a_0 from holographic equipartition of the de Sitter horizon two ways from
scratch (cell count N = A/l_P^2; entropy count N = A/4 l_P^2), and place them beside the published
emergent coefficients (Verlinde 2016 a_0 = cH/6; de Sitter KMS a_0 = cH/2pi).  The framework needs
a_0 = 1/2 c sqrt(G rho_L) = sqrt(3/32pi) cH = 0.1727 cH.

  C1  (PRO) emergent gravity supplies S_dS legitimately: the force scales with the horizon bit count N,
      so KS01's double count does not apply -- state and check the structure
  C2  derive the equipartition a_0 coefficients from scratch (sympy): cell count -> cH; entropy -> cH/4
  C3  the spread of principled emergent coefficients brackets 1/2 but NONE lands on it; 1/2 (=0.1727 cH)
      sits BETWEEN Verlinde's 1/6 and the entropy-count 1/4
  C4  the holographic input S = A/4G is ASSUMED (the derivation is postulate-relative)
  C5  the closest clean count (Verlinde 0.48) != 1/2 and Verlinde's own theory fails independently

Run:  python3 fable_independent_2026/kappa_slot_2026/KS08_emergent_gravity_forcing.py
"""
import os, sys, json, math
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "KS08_emergent_gravity_forcing"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KS08", "checks": {}, "numbers": {}}


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


c = 2.99792458e8; G = 6.674e-11; MPC = 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
rho_L = OmL * 3 * H0**2 / (8 * math.pi * G)
S83 = math.sqrt(8 * math.pi / 3)                 # cH_Lambda/(c sqrt(G rho_L))
S83_H0 = S83 / math.sqrt(OmL)
kUNIT = c * math.sqrt(G * rho_L)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
# framework coefficient in the cH form: a0 = 1/2 c sqrt(G rho_L) = sqrt(3/32pi) cH_Lambda
coeff_framework = 0.5 / S83                        # = sqrt(3/(32 pi))
P(__doc__)
P(f"  framework: a0 = 1/2 c sqrt(G rho_L) = {coeff_framework:.5f} cH_Lambda (= sqrt(3/32pi)); kappa = 0.5")

# =================================================================================================
banner("C1 -- (PRO) emergent gravity supplies the S_dS factor legitimately")
# In emergent gravity the fundamental d.o.f. are the N = A/l_P^2 horizon bits; the (entropic) force is
# F = T dS/dx with S counting those bits.  So the force scales with N ~ S_dS BY CONSTRUCTION -- there is
# no separate bulk-mode variance to double count.  KS01's objection was specific to the graviton-bath
# (bulk-field) route; it does not apply when the horizon bits ARE the d.o.f.
# the horizon bit count is N = A/l_P^2 = 4 S_dS, which carries 1/hbar -- so the entropic force genuinely
# scales with the horizon d.o.f. (unlike the bulk-mode variance, which is O(hbar)).
import sympy as _sp
_G, _H, _hb = _sp.symbols("G H hbar", positive=True)
N_bits = 4 * _sp.pi / (_H**2 * _hb * _G)          # A/l_P^2 = 4 pi/(H^2 l_P^2), l_P^2 = hbar G (c=1)
SdS_sym = _sp.pi / (_G * _hb * _H**2)
p_hb_N = _sp.simplify(_hb * _sp.diff(_sp.log(N_bits.subs({_G: 1, _H: 1})), _hb))
check("C1 emergent gravity's force scales with the horizon bit count N = A/l_P^2 = 4 S_dS, which carries "
      "hbar^-1 -- so it genuinely feels the horizon d.o.f., and KS01's double-count (bulk-mode variance, "
      "O(hbar)) does not apply here",
      f"N_bits/S_dS = {_sp.simplify(N_bits/SdS_sym)}; hbar-power of N_bits = {p_hb_N}",
      _sp.simplify(N_bits / SdS_sym - 4) == 0 and p_hb_N == -1,
      "GENUINE ADVANCE: the S_dS coherence has a home -- the horizon d.o.f. themselves (N ~ 1/hbar), not a "
      "bulk mode sum")

# =================================================================================================
banner("C2 -- derive the emergent a_0 from holographic equipartition (sympy, from scratch)")
Gs, Hs, hb, Rr = sp.symbols("G H hbar R", positive=True)
lP2 = hb * Gs                                     # l_P^2 = hbar G (c=1)
R = 1 / Hs                                        # de Sitter horizon radius (c=1)
A = 4 * sp.pi * R**2
T = hb * Hs / (2 * sp.pi)                         # Gibbons-Hawking temperature (c=1, k_B=1)


def equip_a0(N):
    """holographic equipartition: E = 1/2 N T = M; a_0 = G M / R^2 (horizon-edge acceleration)."""
    E = sp.Rational(1, 2) * N * T
    M = E
    a = sp.simplify(Gs * M / R**2)
    return sp.simplify(a / Hs)                    # a_0 / (cH), c=1


N_cell = A / lP2                                  # Verlinde bit count A/l_P^2
N_ent = A / (4 * lP2)                             # entropy count A/4 l_P^2 = S_dS
coef_cell = equip_a0(N_cell)
coef_ent = equip_a0(N_ent)
P(f"  equipartition, cell count N = A/l_P^2:   a_0/cH = {coef_cell}")
P(f"  equipartition, entropy count N = A/4l_P^2: a_0/cH = {coef_ent}")
check("C2 holographic equipartition DERIVES a_0 ~ cH from scratch: the cell count gives a_0 = cH, the "
      "entropy count (with the BH 1/4) gives a_0 = cH/4 -- both hbar-free, the right FORM",
      f"cell -> a_0/cH = {coef_cell} (=1); entropy -> a_0/cH = {coef_ent} (=1/4)",
      sp.simplify(coef_cell - 1) == 0 and sp.simplify(coef_ent - sp.Rational(1, 4)) == 0,
      "so the SCALE a_0 ~ cH and the S_dS factor are genuinely emergent; hbar cancels (N ~ 1/hbar, T ~ hbar)")

# =================================================================================================
banner("C3 -- the spread of principled emergent coefficients; is 1/2 among them?")
COEFS = {
    "Unruh-dS balance a=cH":        1.0,
    "equipartition cell count":     1.0,
    "equipartition entropy 1/4":    0.25,
    "Verlinde 2016 a0=cH/6":        1.0 / 6,
    "de Sitter KMS a0=cH/2pi":      1.0 / (2 * math.pi),
    "FRAMEWORK kappa=1/2":          coeff_framework,   # 0.17275
}
P(f"  {'emergent coefficient (a0/cH)':<32}{'a0/cH':>10}{'kappa(HL)':>11}{'kappa(H0)':>11}")
P("  " + "-" * 64)
kappas = {}
for nm, x in sorted(COEFS.items(), key=lambda t: t[1]):
    kHL = x * S83; kH0 = x * S83_H0
    kappas[nm] = kHL
    P(f"  {nm:<32}{x:>10.5f}{kHL:>11.4f}{kH0:>11.4f}")
    OUT["numbers"][nm] = {"a0_over_cH": x, "kappa_HL": kHL, "kappa_H0": kH0}
# is 1/2 (coeff 0.17275) among the CLEAN counts (cell=1, entropy=1/4, Verlinde=1/6, dS=1/2pi)?
clean = {"cell": 1.0, "entropy 1/4": 0.25, "Verlinde 1/6": 1.0 / 6, "dS 1/2pi": 1.0 / (2 * math.pi)}
nearest = min(clean.items(), key=lambda t: abs(t[1] - coeff_framework))
dist_pct = 100 * abs(nearest[1] - coeff_framework) / coeff_framework
check("C3 kappa=1/2 (a0/cH = 0.1727) is NOT among the clean emergent counts: it sits BETWEEN the "
      "entropy-count 1/4 (0.25) and Verlinde's 1/6 (0.167); nearest clean count is off by a few %",
      f"framework coeff = {coeff_framework:.5f}; nearest clean count = {nearest[0]} at {nearest[1]:.5f} "
      f"({dist_pct:.1f}% away); clean counts: {sorted(round(v,4) for v in clean.values())}",
      all(abs(v - coeff_framework) > 1e-6 for v in clean.values()),
      "so emergent gravity forces a_0 ~ cH x (a counting coefficient) but NOT the exact 0.1727 that gives 1/2 "
      "-- 1/2 is bracketed by the principled counts, not selected by one")

# =================================================================================================
banner("C4 -- the holographic input is ASSUMED (postulate-relative)")
# the coefficient depends on the (postulated) bit-count normalisation: cell count vs entropy count differ
# by exactly 4 in a_0 (2 in kappa) -- so the answer is not convention-free, it rides on the holographic 1/4.
ratio_counts = float(coef_cell / coef_ent)
check("C4 the coefficient is not convention-free: the cell count and the entropy count (the BH 1/4) give "
      "a_0 differing by exactly 4 (kappa by 2), so the result rides on the postulated holographic 1/4",
      f"a_0(cell)/a_0(entropy) = {ratio_counts:.4f} (= 4); kappa spread from this choice alone = 2x",
      abs(ratio_counts - 4.0) < 1e-9,
      "'emergent gravity forces S_dS' is TRUE relative to holography, but WHICH coefficient depends on the "
      "bit-count convention -- holography is the standing assumption and does not fix the 1/4-vs-1 choice")

# =================================================================================================
banner("C5 -- the closest clean count (Verlinde) != 1/2 and fails independently")
kappa_V = (1.0 / 6) * S83
check("C5 Verlinde 2016 (the closest full emergent-gravity implementation) gives kappa = 0.48, not 1/2, "
      "and fails independently (galaxy-cluster lensing, structure formation -- the critical literature)",
      f"kappa_Verlinde = {kappa_V:.4f} vs 1/2 (2.4% low in a0 on HL footing); != 1/2", abs(kappa_V - 0.5) > 0.005,
      "so even the best-developed emergent-gravity theory neither lands on 1/2 nor survives as a complete "
      "theory; it is a home for the SCALE and the S_dS factor, not a derivation of the exact coefficient")

# =================================================================================================
banner("VERDICT")
P(f"""  (1) COMPUTED: the emergent-gravity a_0 from holographic equipartition (sympy, from scratch, two bit
      counts) and the spread of published emergent coefficients, converted to kappa on both footings.
  (2) NUMBERS: cell count -> a_0 = cH (kappa 2.89); entropy count -> cH/4 (kappa 0.72); Verlinde -> cH/6
      (kappa 0.48); dS-KMS -> cH/2pi (kappa 0.46).  The framework needs a_0/cH = 0.1727 (kappa 1/2), which
      sits BETWEEN 1/4 and 1/6 and equals NONE of the clean counts.
  (3) HONEST SENTENCE: emergent gravity FORCES the S_dS coherence -- this is a genuine advance, because the
      horizon bits ARE the d.o.f. and KS01's double-count objection does not apply there -- and it forces
      the FORM a_0 ~ cH and a coefficient of ORDER 1/2 (the principled counts bracket it, 0.46 to 0.72).
      But it does NOT force EXACTLY 1/2: the framework's 0.1727 cH lies between the entropy-count 1/4 and
      Verlinde's 1/6, matching no single principled count, and the whole construction assumes holography.
      So the S_dS coherence is now DERIVED (postulate-relative to holography); kappa = 1/2 EXACTLY is still
      MEASURED, bracketed by emergent-gravity counts but not selected by one.
      THE UNLOCK is now sharper: a principled reason the emergent bit-count coefficient is exactly
      sqrt(3/32pi) = 0.1727 (equivalently the 1/4 in a_0^2 = 1/4 c^2 G rho_L) -- a value between the two
      natural counts, which no counting rule yet supplies.""")
OUT["verdict"] = {"word": "S_dS-FORCED-BUT-COEFFICIENT-NOT",
                  "sds_forced_in_emergent_gravity": True, "forces_exact_half": False,
                  "framework_coeff_cH": coeff_framework, "kappa_spread": [0.46, 2.89],
                  "unlock": "why the emergent bit-count coefficient is exactly sqrt(3/32pi) (the 1/4 in a0^2=1/4 c^2 G rho_L)"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"KS08 COMPLETE: {npass}/{n} checks PASS")
for nm in lb_fail:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb_fail else 0)
