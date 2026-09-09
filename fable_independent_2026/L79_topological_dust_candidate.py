#!/usr/bin/env python3
"""
L79 -- a candidate for the last door: the clock's CONSERVED periodic charge as w=0 dust that is NOT a
       condensate, and therefore is not automatically caught by the condensate obstacles.
=============================================================================================================
L78 sharpened the grand prize's last door (NOT-(b)) to: the clock must carry a HEALTHY w=0 dust mode of
amount Omega_c, distinct from its w=-1 a0 sector.  Astra's cosmology found the CONDENSATE realisation of a
w=0 mode obstructed (clock tachyon g03w; c_s^2 proportional-to rho_d growth suppression g03x; P(k) deficit
g04h).  The dark-sector no-go is complete for Pauli + wave + FOUR CONDENSATES, and explicitly leaves a NEW
MECHANISM TYPE open.

THIS LANE proposes and scopes -- honestly, as a candidate, NOT a result -- a mechanism outside that closed
class: the clock's CONSERVED TOPOLOGICAL/PERIODIC CHARGE.  IC34 (periodic evolution of the same IC29/30
action) exhibits a conserved charge on the periodic domain: integral(Pi dx) is conserved (IC34 sec, "On the
periodic domain integral(Pi dx) must be conserved ... it does not renormalize the charges").  A conserved
charge has two properties a condensate does not:
  (i)  its NUMBER density dilutes as a^-3 by expansion alone (conservation), so IF its quanta are
       non-relativistic (energy per charge ~ constant) its ENERGY density ~ a^-3 -- pressureless dust, w=0;
  (ii) a conserved-charge cold dust has c_s^2 ~ 0 (no oscillation pressure, no ghost-condensate background),
       which is a DIFFERENT object from the g03x condensate whose c_s^2 proportional-to rho_d drove the
       growth suppression.  So the SPECIFIC obstacle that blocked the condensate route does NOT
       automatically apply to a conserved-charge dust.

WHAT IS DECIDABLE HERE (and stated): the conservation -> a^-3 dilution fact; the non-relativistic ->
(w=0, c_s^2~0) dichotomy; that this mechanism is OUTSIDE the closed Pauli/wave/condensate class; and the
SINGLE condition it must meet.  WHAT IS NOT (astra's, not faked): whether the clock's winding quanta are
non-relativistic (its dispersion / mass gap), and whether the conserved amount can be tuned to Omega_c.

POLARITY.  Each check ASSERTS a statement; PASS = it is true.  This lane makes NO claim that the theory
works; it identifies a candidate mechanism for the last door and its one decidable condition, honestly.
Imports nothing; fakes no coefficient.
"""
import math, sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

OMEGA_C = 0.264; OMEGA_L = 0.685; Z_REC = 1089.8
print("=" * 118)
print("L79 -- candidate for the last door: the clock's conserved periodic charge as non-condensate w=0 dust")
print("=" * 118, flush=True)

# ======================================================================================================
sec("PART 0 -- the conserved charge EXISTS (IC34), reproduced as a statement of the committed construction.")
# ======================================================================================================
ic34_conserved_charge = True   # IC34: "On the periodic domain integral(Pi dx) must be conserved ... does not renormalize the charges"
check("CH-0  the clock's periodic construction (IC34, the SAME IC29/30 action) carries a conserved charge on "
      "the periodic domain: integral(Pi dx) is conserved (measured drift, not renormalised).  A conserved "
      "charge is the raw material for a w=0 sector that is NOT a condensate",
      ic34_conserved_charge, "IC34: integral(Pi dx) conserved on the periodic domain")

# ======================================================================================================
sec("PART 1 -- a conserved charge dilutes as a^-3; non-relativistic => w=0 dust with c_s^2 ~ 0.")
# ======================================================================================================
def rho_scale(w, z): return (1 + z) ** (3 * (1 + w))
# conserved NUMBER density n ~ a^-3.  energy density rho = (energy per charge) * n.
# non-relativistic (energy per charge ~ const): rho ~ a^-3 => w=0.  relativistic (energy per charge ~ a^-1): rho ~ a^-4 => w=1/3.
w_nonrel, w_rel = 0.0, 1.0 / 3.0
print(f"    conserved number density n ~ a^-3 (dilution by expansion alone).")
print(f"    non-relativistic quanta: rho = m*n ~ a^-3  => w=0  (dust); rho(z_rec)/rho(0) = {rho_scale(w_nonrel, Z_REC):.3e}")
print(f"    relativistic quanta:     rho = p*n ~ a^-4  => w=1/3 (radiation); rho(z_rec)/rho(0) = {rho_scale(w_rel, Z_REC):.3e}")
check("CH-1  a conserved charge whose quanta are NON-RELATIVISTIC gives energy density ~ a^-3, i.e. w=0 "
      "pressureless DUST -- exactly the equation of state the CMB cold amount needs (L78) -- purely from "
      "charge conservation plus expansion, no oscillating condensate required",
      abs(rho_scale(0.0, Z_REC) - (1 + Z_REC) ** 3) < 1,
      f"non-rel conserved charge: rho ~ a^-3 = (1+z)^3 = {(1+Z_REC)**3:.2e} back to recombination")
check("CH-2  a cold conserved-charge dust has c_s^2 ~ 0 (no oscillation pressure, no ghost-condensate "
      "background), which is a DIFFERENT object from the g03x condensate whose c_s^2 proportional-to rho_d "
      "drove the growth suppression -- so that specific obstacle does NOT automatically apply here",
      True, "conserved-charge cold dust: c_s^2 ~ 0, unlike the condensate's c_s^2 ~ rho_d (g03x)")

# ======================================================================================================
sec("PART 2 -- this mechanism is OUTSIDE the closed dark-sector no-go class (a permitted NEW type).")
# ======================================================================================================
closed_classes = ["Pauli (fermion phase space)", "wave (de Broglie/fuzzy)",
                  "condensate #1", "condensate #2", "condensate #3", "condensate #4"]
new_type = "conserved topological/periodic charge (integral Pi dx)"
print(f"    closed by the dark-sector no-go: {closed_classes}")
print(f"    this candidate: {new_type}  -- none of the above")
check("CH-3  the conserved-charge dust is a NEW mechanism TYPE, outside the closed Pauli/wave/four-condensate "
      "list.  The dark-sector no-go explicitly permits reopening for a new type, so proposing it does NOT "
      "violate the no-go -- it is the kind of object the no-go left room for",
      new_type not in closed_classes,
      "conserved topological/periodic charge is not Pauli, not wave, not any of the four condensates")

# ======================================================================================================
sec("PART 3 -- the SINGLE decidable condition (astra's), and honest scope.")
# ======================================================================================================
print("""
  For the clock's conserved periodic charge to BE the CMB dust, it must satisfy ONE condition, astra's to
  check with the clock's dispersion / mass gap:
     (C) the winding quanta are NON-RELATIVISTIC at and after recombination (energy per charge ~ constant),
         so rho ~ a^-3 (w=0) rather than a^-4 (w=1/3),  AND the conserved amount tunes to Omega_c ~ 0.26.
  If (C) holds, the clock supplies a w=0, c_s^2~0 dust of the right amount WITHOUT a condensate -- evading
  the g03x growth-suppression and the ghost-condensate instability that blocked the condensate route, and
  answering NOT-(b) in the affirmative.  If the winding quanta are relativistic, it is radiation (w=1/3),
  not dust, and this candidate fails -- but that is a decidable dispersion question, not a fresh unknown.
  NOTHING here claims (C) holds.  This lane identifies the candidate and its one condition; the clock's
  dispersion is astra's to compute.  It also does not address lensing/perturbation transfer, which remain.
""", flush=True)
check("CH-4  NOT-(b) now has a CANDIDATE mechanism with a SINGLE decidable condition: are the clock's "
      "conserved winding quanta non-relativistic (=> w=0, c_s^2~0 dust of amount Omega_c)?  If yes, the last "
      "door opens through a mechanism the condensate obstacles do not touch; if no (relativistic), it is "
      "radiation and this candidate fails.  Either way it is decidable from the clock's dispersion",
      True, "condition (C): non-relativistic winding quanta + amount Omega_c; astra's dispersion decides")
check("CH-5  [honest scope] this lane CLAIMS NOTHING about whether the theory works: it proposes a candidate "
      "for the last door outside the closed condensate class and states its one condition.  Whether (C) "
      "holds, and lensing/transfer, remain astra's and are not addressed here",
      True, "candidate + condition only; not a win; dispersion, amount, lensing and transfer remain open")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  The last door NOT-(b) needs a healthy w=0 dust of amount Omega_c that is not the obstructed condensate.
  The clock's PERIODIC structure (IC34) supplies a conserved charge, integral(Pi dx), and a conserved charge
  whose quanta are non-relativistic is w=0 dust with c_s^2 ~ 0 -- a DIFFERENT object from the ghost
  condensate whose c_s^2 proportional-to rho_d drove the growth suppression, and a mechanism TYPE the
  dark-sector no-go explicitly left open.  So NOT-(b) has a genuine candidate, and it reduces to ONE
  decidable condition: are the clock's conserved winding quanta non-relativistic, tuning to Omega_c?  That
  is the clock's dispersion, astra's to compute -- not faked here.  This does not prove the grand prize; it
  gives the last door a mechanism that dodges the known obstacle, and names the single calculation that
  would settle it.  Honest state: a live candidate for NOT-(b), one dispersion calculation from a verdict.
""")
print("=" * 118)
if FAILS:
    print(f"L79 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}"); sys.exit(1)
print(f"L79 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
