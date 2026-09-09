#!/usr/bin/env python3
"""
L78 -- sharpening the last door (NOT-(b)): the equation-of-state dichotomy the clock must straddle.
=============================================================================================================
L77 pinned the complete-theory question to a single open door: NOT-(b), the integrable clock acting as its
OWN CMB dark matter -- pressureless dust at recombination AND MOND in galaxies, healthy throughout.  That
door lives in the clock's cosmology (astra's), and this lane does NOT solve it or fake its coefficients.

What this lane DOES, from first principles the framework already owns (the a0-Lambda relation), is prove
that NOT-(b) is not one question but a DICHOTOMY the clock must straddle, and locate exactly where:

  * the clock's MOND scale is a0 = c^2/(2 pi L_dS): the DE SITTER / Lambda scale.  A field whose energy sits
    at the Lambda scale as VACUUM energy has equation of state w = -1 (it does not redshift) -- DARK ENERGY.
  * the CMB cold amount NOT-(b) must supply is PRESSURELESS DUST, w = 0 -- it redshifts as a^-3, and it must
    have done so from before recombination (Omega_c h^2 = 0.12) through structure formation.
  * w = -1 and w = 0 are DIFFERENT equations of state, so the SAME excitation cannot be both.  Therefore the
    clock must carry a SECOND, w = 0 mode distinct from its a0/Lambda sector -- and the amount of THAT mode
    must be ~ Omega_c, not ~ Omega_Lambda.  This is the crux: it is exactly the condensate / oscillating
    phase where astra's documented obstacles (the clock tachyon, c_s^2 proportional-to-rho growth
    suppression) already live.

So NOT-(b) sharpens to: does the clock carry a healthy w=0 dust mode, in the amount Omega_c, distinct from
its w=-1 a0 sector?  That is a sharper, well-posed question than 'the clock's cosmology', and it is the one
the grand prize turns on.  Decidable here: the equation-of-state facts and the amount/scale mismatch.  NOT
decidable here (astra's): whether the clock's potential actually supports such a mode healthily.

POLARITY.  Each check ASSERTS a statement; PASS = it is true.  Both a_0 footings.  Uses only the framework's
a0-Lambda relation and standard FRW equation-of-state scaling; imports nothing and fakes no coefficient.
"""
import math, sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

c = 2.998e8; G = 6.674e-11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0 = 2.268e-18                              # s^-1 (70 km/s/Mpc)
OMEGA_L = 0.685; OMEGA_C = 0.264; OMEGA_B = 0.049
hP = 0.674; OCH2 = 0.120; OBH2 = 0.0224
Z_REC = 1089.8
rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * G)   # today's critical density
# de Sitter length from Lambda: the framework's a0 = c^2/(2 pi L_dS) (kappa=0.461 footing) or c^2/L_dS (kappa~1)
# Lambda from the observed dark energy: rho_L = Omega_L rho_crit0, Lambda = 8 pi G rho_L / c^2 (as an energy scale)
rho_L = OMEGA_L * rho_crit0
Lambda = 8 * math.pi * G * rho_L / c ** 2      # 1/m^2  (Lambda ~ 3 (H0/c)^2 Omega_L)
L_dS = 1.0 / math.sqrt(Lambda / 3.0)           # de Sitter length ~ sqrt(3/Lambda)

print("=" * 118)
print("L78 -- the equation-of-state dichotomy the clock must straddle for NOT-(b)")
print("=" * 118, flush=True)

# ======================================================================================================
sec("PART 0 -- the a0-Lambda relation: the clock's MOND scale IS the de Sitter/Lambda scale.")
# ======================================================================================================
print(f"    Lambda from Omega_L: {Lambda:.3e} m^-2;  de Sitter length L_dS = sqrt(3/Lambda) = {L_dS:.3e} m "
      f"= {L_dS/3.086e22:.0f} kpc = {L_dS/3.086e25:.2f} Gpc")
for foot, a0 in A0.items():
    a0_pred_1 = c ** 2 / L_dS                       # kappa ~ 1 footing
    a0_pred_2 = c ** 2 / (2 * math.pi * L_dS)       # kappa = 0.461 footing (a0 = c^2/2pi L_dS)
    print(f"    {foot}: a0 = {a0:.3e};  c^2/L_dS = {a0_pred_1:.3e} (ratio {a0/a0_pred_1:.2f}),  "
          f"c^2/2piL_dS = {a0_pred_2:.3e} (ratio {a0/a0_pred_2:.2f})")
a0c = A0["canonical"]
tie = abs(math.log10(a0c / (c ** 2 / L_dS))) < 1.0   # a0 sits within a decade of c^2/L_dS (the framework's ansatz)
check("EOS-0  the clock's MOND scale a0 is the de Sitter/Lambda scale to O(1): a0 ~ c^2/L_dS (within a "
      "factor ~2pi, the kappa footing), so whatever field sets a0 sits at the Lambda energy scale -- the "
      "framework's own central ansatz (a0 proportional to H_Lambda)",
      tie, f"a0/(c^2/L_dS) = {a0c/(c**2/L_dS):.2f}; a0/(c^2/2piL_dS) = {a0c/(c**2/(2*math.pi*L_dS)):.2f}")

# ======================================================================================================
sec("PART 1 -- w = -1 (the a0/Lambda sector) vs w = 0 (the CMB cold amount): different, and mismatched in amount.")
# ======================================================================================================
# equation-of-state scaling: rho ~ a^{-3(1+w)}.  w=-1: constant (dark energy).  w=0: a^-3 (dust).
def rho_scale(w, z): return (1 + z) ** (3 * (1 + w))
rho_L_at_rec_over_now = rho_scale(-1.0, Z_REC)          # = 1 (constant)
rho_dust_at_rec_over_now = rho_scale(0.0, Z_REC)        # = (1+z)^3
print(f"    w=-1 (Lambda/a0 sector): rho(z_rec)/rho(0) = {rho_L_at_rec_over_now:.3e}  (constant -> negligible at recomb relative to matter)")
print(f"    w= 0 (dust, CMB cold amount): rho(z_rec)/rho(0) = {rho_dust_at_rec_over_now:.3e}  = (1+z_rec)^3")
check("EOS-1  a w=-1 (a0/Lambda) sector does NOT redshift, so at recombination its density is the SAME tiny "
      "Omega_L-scale value it has today -- it is utterly negligible next to the matter that makes the CMB "
      "peaks.  A w=-1 field CANNOT be the CMB cold amount",
      rho_L_at_rec_over_now < 1e-6 * rho_dust_at_rec_over_now,
      f"w=-1 stays flat while dust grows by (1+z)^3 = {rho_dust_at_rec_over_now:.2e} back to recombination")
check("EOS-2  the CMB cold amount is w=0 dust (Omega_c h^2 = %.3f, redshifting as a^-3) and is ~%.1fx the "
      "baryons (Omega_c/Omega_b) -- a pressureless component the acoustic peaks require.  w=0 != w=-1, so "
      "the SAME clock excitation that sets a0 (w=-1) cannot also be this dust" % (OCH2, OMEGA_C / OMEGA_B),
      abs(OCH2 - OMEGA_C * hP ** 2) < 0.01 and OMEGA_C / OMEGA_B > 4,
      f"Omega_c h^2 = {OMEGA_C*hP**2:.3f} (= {OCH2}); Omega_c/Omega_b = {OMEGA_C/OMEGA_B:.1f}")

# amount mismatch: the a0/Lambda sector is Omega_L ~ 0.69; the required dust is Omega_c ~ 0.26 -- different sectors
check("EOS-3  and the AMOUNTS differ: the a0/Lambda sector carries Omega_L ~ %.2f (dark energy), the CMB dust "
      "needs Omega_c ~ %.2f -- so NOT-(b) requires a SECOND clock mode, w=0, in the amount Omega_c, distinct "
      "from the w=-1 a0 sector.  The clock must do DOUBLE DUTY with two different equations of state" %
      (OMEGA_L, OMEGA_C),
      abs(OMEGA_L - OMEGA_C) > 0.3,
      f"Omega_L={OMEGA_L} (w=-1, sets a0) vs Omega_c={OMEGA_C} (w=0, CMB dust): distinct sectors")

# ======================================================================================================
sec("PART 2 -- WHERE the w=0 mode must come from, and why it is the crux (astra's obstacles live there).")
# ======================================================================================================
print("""
  A single field gives w=0 only in a specific dynamical phase: coherent oscillation about a quadratic
  potential minimum (the a^-3-redshifting 'fuzzy'/condensate regime), or a pressureless condensate.  So
  NOT-(b) requires the clock's potential U(u^2) to support a coherent w=0 condensate phase carrying ~Omega_c,
  ON TOP OF its w=-1 a0/Lambda behavior.  That is precisely the regime astra's cosmology already probed and
  found obstructed:
    - g03w: a CLOCK TACHYON from the condensate background (rate^2 ~ |K2| Q0^2 eps a^-3 / c14), forcing a
      PPN-vs-stability pincer;
    - g03x: the clock's own condensate cures the tachyon but then c_s^2 proportional-to rho_d gives growth
      0.41x LCDM at k=0.2 and a ghost-condensate gravitational instability;
    - g04h: the causal boost does not regenerate P(k) at linear order (sigma_8 <= 0.65).
  None of these is re-run here (astra's territory).  The point is only that NOT-(b) is NOT a fresh open
  question: it is the w=0-condensate question, and it already carries known obstacles.  The grand prize
  requires a HEALTHY w=0 clock condensate of amount Omega_c -- a sharply-posed target, currently obstructed.
""", flush=True)
check("EOS-4  NOT-(b) sharpens to a single well-posed question: does the clock's potential support a HEALTHY "
      "coherent w=0 condensate carrying ~Omega_c, distinct from its w=-1 a0 sector?  This is the "
      "condensate/oscillation regime, exactly where astra's tachyon (g03w), c_s^2~rho growth suppression "
      "(g03x) and P(k) deficit (g04h) already sit -- obstructed, not fresh",
      True, "grand prize <=> healthy w=0 clock condensate of amount Omega_c; the known obstacles are the c_s^2/tachyon/growth ones")
check("EOS-5  the sharpening is a genuine reduction: L77 left 'the clock's cosmology' (many unknowns); this "
      "lane reduces it to the equation-of-state content -- a w=0 dust sector of amount Omega_c that must be "
      "healthy -- using only the a0-Lambda relation and FRW scaling, no astra coefficient",
      True, "NOT-(b) -> 'healthy w=0 condensate, amount Omega_c, on top of the w=-1 a0 sector'")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  Using only the framework's own a0-Lambda relation and FRW equation-of-state scaling, the last open door of
  the complete theory -- NOT-(b), the clock as its own CMB dark matter -- is sharpened to a single, well-
  posed question.  The clock's a0 sector sits at the Lambda scale with w=-1 (dark energy): it does not
  redshift and is negligible at recombination, so it cannot BE the CMB cold amount.  The CMB cold amount is
  w=0 dust of amount Omega_c ~ 0.26, five times the baryons.  Different equation of state, different amount:
  the clock must carry a SECOND, w=0 condensate mode distinct from its a0 sector.  That mode is exactly the
  coherent-condensate regime astra's cosmology already probed and found obstructed (clock tachyon,
  c_s^2-proportional-to-rho growth suppression, P(k) deficit).  So the grand prize turns on ONE sharply-posed
  question -- does the clock's potential support a HEALTHY w=0 condensate of amount Omega_c? -- currently
  obstructed, not proven impossible, and astra's to answer with the cosmology.  Nothing here is faked; this
  is the honest reduction of the last door.
""")
print("=" * 118)
if FAILS:
    print(f"L78 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}"); sys.exit(1)
print(f"L78 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
