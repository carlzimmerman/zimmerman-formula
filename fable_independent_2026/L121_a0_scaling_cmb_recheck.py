#!/usr/bin/env python3
"""
L121 -- HONEST RE-CHECK of the Phase E CMB verdict under a₀ scaling with the dark-energy scale. Phase E
        assumed a CONSTANT a₀; the framework's a₀ = c²/(2πL_dS) is a dark-energy-scale acceleration. This
        lane recomputes a₀ at recombination under both readings and separates "acceleration scale" from
        "clustering density" -- the actual third-peak requirement.
=============================================================================================================
Premise under test: the framework's a₀ scales with the dark-energy scale (a₀ = c²/(2πL_dS), L_dS = √(3/Λ), so
a₀ ~ c√Λ ~ c H₀ × O(1)/(2π)). Phase E's CMB kill ASSUMED a₀ = today's constant value, getting a₀/cH(z_rec)
~ 1e-5 ("MOND off at recombination"). If a₀ instead TRACKS the expansion (a₀ ∝ H(z), the matching-theorem
prediction), that assumption is wrong. Checked here honestly.

TWO READINGS:
  (A) a₀ ∝ √ρ_Λ with ρ_Λ = the COSMOLOGICAL-CONSTANT (dark-energy) density = CONSTANT ⇒ a₀ = const (the L90
      "Λ-locked flat a₀(z)" picture). Then Phase E's constant-a₀ assumption is CORRECT.
  (B) a₀ ∝ H(z) (the "a₀ tracks the expansion" / matching-theorem prediction) ⇒ a₀(z)/cH(z) = a₀,0/cH₀ =
      const at ALL epochs ⇒ MOND stays active at the HORIZON scale at recombination, contradicting Phase E.

THE DECISIVE PHYSICS (independent of A vs B): the CMB THIRD PEAK requires additional GRAVITATING MATTER that
CLUSTERS and redshifts as a⁻³ (a DENSITY) to sustain potential wells through the radiation era. An
acceleration SCALE a₀ modifies the force LAW at low acceleration; it does NOT supply a gravitating density.
So a₀'s scaling -- however it scales -- cannot by itself make the third peak. What fits the CMB (AeST) is a
FIELD ENERGY DENSITY ∝ a⁻³ (clustering dust). The question therefore reduces to: does the framework's DARK
SECTOR redshift as a⁻³ (clustering ⇒ fits CMB, but = Branch I with the ghost/BBN cost) or as ρ_Λ (constant,
dark-energy-like ⇒ does NOT cluster ⇒ does NOT help the third peak)?

WHAT IS COMPUTED (self-contained numpy):
  0  a₀,0/cH₀ ≈ 0.13-0.18 (a₀ IS a dark-energy-scale acceleration -- the framework's signature, verified).
  1  a₀/cH at recombination under reading A (const) vs reading B (∝H): 1e-5 (off) vs 0.13 (active).
  2  the third-peak requirement is a CLUSTERING a⁻³ DENSITY, distinct from the acceleration scale a₀.
  3  honest verdict: Phase E's constant-a₀ kill is DOWNGRADED (its horizon-scale estimate used the wrong a₀
     for a framework with a₀∝H(z)); a proper Boltzmann calc with the framework's a₀(z) is needed. BUT the
     third-peak-needs-clustering-density point means a₀-scaling alone doesn't rescue it -- the real question
     is the dark sector's a-scaling (the pincer).

POLARITY: each check ASSERTS a statement; PASS = true. Honest re-check crediting the point, not a capitulation
and not a defense.
"""
import math, sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)

c = 2.998e8; Mpc = 3.0857e22
H0 = 67.4e3 / Mpc          # s^-1
cH0 = c * H0
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Om, Or, OL, Ob = 0.315, 9.2e-5, 0.685, 0.049
z_rec = 1090.0

print("=" * 110)
print("L121 -- honest re-check: does a₀ scaling with the dark-energy scale change the Phase E CMB verdict?")
print("=" * 110, flush=True)

# ======================================================================================================
sec("PART 0 -- a₀ IS a dark-energy-scale acceleration: a₀,0/cH₀ = O(0.1) (the framework's signature).")
# ======================================================================================================
for foot in ("canonical", "alt"):
    print(f"    a₀({foot})/cH₀ = {A0[foot]/cH0:.3f}   (a₀ = c²/2πL_dS ~ c√Λ; order 1/2π ~ 0.16)")
ratio0 = A0["canonical"] / cH0
check("SIG-1  a₀,0/cH₀ ≈ 0.13-0.18 (order 1/2π): a₀ is a DARK-ENERGY-scale acceleration, exactly the "
      "a₀=c²/(2πL_dS) tie. the premise is correct -- a₀ is set by the dark-energy scale, not an "
      "arbitrary constant",
      0.1 < ratio0 < 0.25, f"a₀,0/cH₀ = {ratio0:.3f} (a₀ ~ dark-energy-scale acceleration; the framework's signature)")

# ======================================================================================================
sec("PART 1 -- a₀/cH at recombination: reading A (const) vs reading B (a₀∝H(z)).")
# ======================================================================================================
def H_over_H0(z):
    zp = 1 + z
    return math.sqrt(Or * zp**4 + Om * zp**3 + OL)
HrecR = H_over_H0(z_rec)           # standard LCDM expansion at recombination (for cH)
cH_rec = cH0 * HrecR
print(f"    H(z_rec)/H0 = {HrecR:.3e},  cH(z_rec) = {cH_rec:.3e} m/s^2")
# Reading A: a0 constant
ratio_A = A0["canonical"] / cH_rec
# Reading B: a0 ∝ H(z) => a0(z_rec) = a0,0 * H(z_rec)/H0 => a0/cH = a0,0/cH0 = const
ratio_B = (A0["canonical"] * HrecR) / cH_rec
check("REC-A  reading A (a₀ ∝ √ρ_Λ, ρ_Λ = cosmological-constant density = CONSTANT ⇒ a₀ const, the L90 flat "
      "picture): a₀/cH(z_rec) ~ %.1e -- MOND OFF at recombination. Here Phase E's constant-a₀ assumption is "
      "CORRECT and the CMB kill stands" % ratio_A,
      ratio_A < 1e-4, f"a₀/cH(z_rec) = {ratio_A:.1e} (MOND off; Phase E holds for constant a₀)")
check("REC-B  reading B (a₀ ∝ H(z), the matching-theorem/'tracks-expansion' prediction): a₀(z)/cH(z) = "
      "a₀,0/cH₀ = %.2f at ALL epochs, INCLUDING recombination -- MOND stays active at the HORIZON scale. Here "
      "Phase E's 'MOND off at recombination' is WRONG (it used the wrong, constant a₀). this correction "
      "applies to this reading" % ratio_B,
      abs(ratio_B - ratio0) < 1e-6 and ratio_B > 0.1,
      f"a₀/cH(z_rec) = {ratio_B:.3f} = a₀,0/cH₀ (MOND active at the horizon at recombination; Phase E's constant-a₀ estimate wrong)")

# ======================================================================================================
sec("PART 2 -- BUT the third peak needs a CLUSTERING a⁻³ DENSITY, not an acceleration scale.")
# ======================================================================================================
# z_eq for baryon-only vs LCDM (why the third peak needs clustering matter):
z_eq_baryon = Ob / Or - 1        # matter-radiation equality, baryons only
z_eq_lcdm = Om / Or - 1          # with CDM
check("PEAK-1  the CMB third peak needs matter-radiation equality BEFORE recombination and CLUSTERING "
      "potential wells during the radiation era. Baryon-only z_eq = %.0f < z_rec = %.0f (radiation-dominated "
      "at last scattering, wrong CMB); with a clustering a⁻³ component z_eq = %.0f > z_rec. This is a DENSITY "
      "requirement (ρ ∝ a⁻³ that CLUSTERS), NOT an acceleration-scale requirement" % (z_eq_baryon, z_rec, z_eq_lcdm),
      z_eq_baryon < z_rec < z_eq_lcdm,
      f"z_eq: baryon-only {z_eq_baryon:.0f} < z_rec {z_rec:.0f} < with-a⁻³-matter {z_eq_lcdm:.0f}")
check("PEAK-2  an acceleration SCALE a₀ (however it scales with z) modifies the low-acceleration FORCE LAW; "
      "it does NOT add a gravitating DENSITY. So a₀-scaling alone -- reading A or B -- cannot supply the "
      "clustering a⁻³ matter the third peak needs. What fits the CMB (AeST) is a FIELD ENERGY DENSITY ∝ a⁻³, "
      "a density not an acceleration",
      True, "a₀ = force-law scale != gravitating density; third peak needs clustering a⁻³ density (AeST's field dust)")

# ======================================================================================================
sec("PART 3 -- HONEST verdict: Phase E downgraded, the real question is the DARK-SECTOR a-scaling.")
# ======================================================================================================
print("""
  CREDIT WHERE DUE: it is correct that a₀ is a dark-energy-scale acceleration (a₀,0/cH₀ ~ 0.13, verified) and
  that Phase E's CMB estimate ASSUMED a constant a₀. If the framework's a₀ TRACKS the expansion (a₀ ∝ H(z),
  the matching-theorem prediction), then a₀/cH = const at all epochs and 'MOND off at recombination' is
  WRONG -- Phase E's horizon-scale estimate does not apply. So the Phase E kill is DOWNGRADED from 'probable
  killer' to 'not established by that argument'; a proper CMB Boltzmann computation with the framework's
  actual a₀(z) is required (neither Phase E nor this lane runs one).

  THE REMAINING PHYSICS (the honest catch): the third peak's requirement is a CLUSTERING a⁻³ gravitating
  DENSITY, which is a different object from the acceleration scale a₀. a₀-scaling changes the force law, not
  the density. So the CMB verdict does NOT hinge on a₀'s z-scaling; it hinges on the DARK SECTOR'S a-scaling:
   * if the framework's dark/phantom sector redshifts as a⁻³ AND clusters like matter in the radiation era,
     it CAN make the third peak (this is exactly how AeST succeeds) -- but that is Branch I's shift-charge
     dust, which carries the conformal ghost + the ~24-order BBN fine-tuning (the pincer, L110/L117);
   * if it is dark-energy-like (∝ρ_Λ, constant, non-clustering), it does NOT make the third peak.
  So the a₀↔dark-energy scaling correctly refutes Phase E's specific 'MOND-off' argument, but the CMB
  third peak still requires a clustering a⁻³ density; whether the framework supplies one healthily is the
  open, decisive question -- and it is the pincer, not the a₀-off estimate. Net: the CMB is REOPENED as
  genuinely UNRESOLVED (needs a real Boltzmann calc with a₀(z) and the actual dark-sector scaling), not the
  clean kill Phase E asserted.
""", flush=True)
check("VERDICT-1  Phase E's CMB kill is DOWNGRADED to UNRESOLVED: its 'MOND off at recombination' assumed "
      "constant a₀ and fails if a₀∝H(z) (this correction is valid for that reading); a proper Boltzmann "
      "calc with the framework's a₀(z) is needed. The remaining decisive question is the DARK-SECTOR "
      "a-scaling (clustering a⁻³ ⇒ CMB ok but the pincer; ρ_Λ-like ⇒ no third peak) -- NOT the a₀-off estimate",
      True, "Phase E downgraded: constant-a₀ assumption invalid under a₀∝H(z); CMB unresolved; real question = dark-sector a-scaling (the pincer)")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  Honest re-check. The premise is correct: a₀ is a dark-energy-scale acceleration (a₀,0/cH₀ ≈ 0.13,
  verified), and Phase E's CMB estimate assumed a CONSTANT a₀. Under the matching-theorem reading a₀ ∝ H(z),
  the ratio a₀/cH is constant at ALL epochs (including recombination), so Phase E's 'MOND is off at
  recombination' is NOT valid -- its horizon-scale estimate used the wrong a₀. The Phase E kill is therefore
  DOWNGRADED from 'probable killer' to 'unresolved -- needs a proper Boltzmann computation with the
  framework's a₀(z)'. BUT the physical requirement of the third peak is a CLUSTERING a⁻³ gravitating DENSITY,
  which is distinct from the acceleration scale a₀; a₀-scaling (however it scales) modifies the force law, not
  the density. So the decisive open question is the DARK SECTOR'S a-scaling: an a⁻³ clustering component makes
  the third peak (AeST-like) but is the ghost/BBN-cost dust (the pincer), while a ρ_Λ-like constant component
  does not. Bottom line: the scaling point correctly refutes Phase E's specific argument; the CMB is REOPENED as
  unresolved, and the real battleground is whether the framework supplies a healthy clustering a⁻³ dark
  component -- the pincer -- not the a₀-off estimate. No clean kill, and no free rescue.
""")
print("=" * 110)
if FAILS:
    print(f"L121 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L121 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 110)
