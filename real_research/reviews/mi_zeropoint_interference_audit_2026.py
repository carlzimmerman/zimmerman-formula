#!/usr/bin/env python3
r"""mi_zeropoint_interference_audit_2026.py -- audits a proposed DERIVATION of kappa = 1/2 (the "zero-point
kinematic interference" argument), which would close section 3.3's open question. VERDICT: it does not work, for
four independent reasons, and one of them is a theorem the corpus already owns.

THE PROPOSAL. Two "distinct fundamental scales" are posited: a matter kinematic frequency-squared
omega_rho^2 = G rho, and a vacuum one omega_Lambda^2 = c^2 Lambda. Their interference is taken as the geometric
mean, omega_int^2 = sqrt(omega_rho^2 omega_Lambda^2), and the floor is then the harmonic-oscillator zero-point
half-weight, Floor = (1/2) omega_int^2 = (1/2) c sqrt(G rho Lambda). This is claimed to force kappa = 1/2 and to
exclude the bare c H_Lambda floor, on the physical ground that a real detector or baryonic core HAS a density and
therefore couples to the background, whereas c H_Lambda assumes a massless test particle in an empty universe.

WHAT IS RIGHT ABOUT IT, and it is worth saying first: the INSTINCT is the correct shape of question. Section 3.3's
open item is exactly whether the floor is a bare-horizon property (c H_Lambda, which Deser-Levin derive) or a
matter-coupled local response, and sqrt(G rho) IS the natural local response rate. The direction is right.

WHAT IS WRONG WITH IT:
  G1  DIMENSIONS. omega_int^2 = sqrt(G rho * c^2 Lambda) has dimensions of s^-2, a frequency-squared. A floor is
      an ACCELERATION, m s^-2. "Floor = (1/2) omega_int^2" equates objects of different dimension.
  G2  Taken literally the number is not a0. It is ~1e-36 s^-2, not 9.36e-11 m s^-2.
  G3  The CHARITABLE REPAIR -- redo it with accelerations, a_rho = c sqrt(G rho_L) and a_Lambda = c^2 sqrt(Lambda),
      whose geometric mean IS an acceleration -- gives (1/2) sqrt(a_rho a_Lambda) = 1.118 c sqrt(G rho_L), i.e.
      (8 pi)^(1/4) = 2.236 times TOO BIG. So the repaired argument does not deliver kappa = 1/2 either.
  G4  *** THE STRUCTURAL KILLER. The two "distinct" scales are ONE scale. Lambda = 8 pi G rho_Lambda / c^2
      identically, so omega_rho^2 = omega_Lambda^2/(8 pi) EXACTLY -- a pure number, no new content. A geometric
      mean of two proportional quantities is just either one times a power of 8 pi. The construction therefore
      cannot EXCLUDE c H_Lambda, because c H_Lambda is the same scale times sqrt(8 pi/3). This is the corpus's
      own kappa-linear relabelling theorem (2026-08-02) in new dress: the whole family relabels and can never
      FORCE kappa. ***
  G5  AND THE PHYSICAL STORY, TAKEN SERIOUSLY, IS FALSIFIED. The argument's motivation is the DETECTOR's own
      density -- "a galactic baryonic core". If rho means the local baryonic density, a0 scales as
      sqrt(G rho_local) and is ~1e3 times too large in the solar neighbourhood, varying by orders between
      galaxies. Setting rho = rho_Lambda instead rescues the number but abandons the physical story that was
      supposed to exclude c H_Lambda.
  G6  And the 1/2 lands on the WRONG OBJECT. The framework's floor is a0/2 = (1/4) c sqrt(G rho_L), not
      a0 = (1/2) c sqrt(G rho_L). So even granting everything, the derived quantity is off by a factor 2 from what
      section 3.3 needs -- the same Z-vs-2Z slip this corpus made earlier the same day.

Exit 0 = every check held. No check(True); every condition below can fail.
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


G = 6.67430e-11
c = 2.99792458e8
Lam = 1.0908e-52                              # m^-2, from Milgrom 1994's a_lambda = c^2 sqrt(L/3) = 5.419e-10
rho_L = Lam * c**2 / (8 * math.pi * G)        # kg m^-3
Z = 2 * math.sqrt(8 * math.pi / 3)
a0 = 0.5 * c * math.sqrt(G * rho_L)           # the framework, kappa = 1/2
cHL = c**2 * math.sqrt(Lam / 3)

print(f"  inputs: Lambda = {Lam:.4e} m^-2 -> rho_Lambda = {rho_L:.4e} kg/m^3")
print(f"  a0 = (1/2) c sqrt(G rho_L) = {a0:.4e} m/s^2   (canonical 9.3614e-11)")
print(f"  c H_Lambda                 = {cHL:.4e} m/s^2   ratio a0/cH_L = {a0/cHL:.8f}  1/Z = {1/Z:.8f}")
check(abs(a0 / 9.3614e-11 - 1) < 3e-3 and abs(a0 / cHL * Z - 1) < 3e-3,
      f"G0 the setup is anchored: (1/2) c sqrt(G rho_Lambda) reproduces the framework's canonical a0 to "
      f"{abs(a0/9.3614e-11-1)*100:.2f}% and a0/cH_Lambda = 1/Z to {abs(a0/cHL*Z-1)*100:.2f}%, so any failure "
      f"below is the proposal's and not a units error of mine")

# ---- G1/G2  dimensions and the literal number ------------------------------------
m, s, kg = sp.symbols("m s kg", positive=True)
dim = {"G": m**3 / (kg * s**2), "rho": kg / m**3, "c": m / s, "Lam": 1 / m**2}
w_rho2 = dim["G"] * dim["rho"]                                  # G rho
w_Lam2 = dim["c"] ** 2 * dim["Lam"]                             # c^2 Lambda
w_int2 = sp.sqrt(sp.simplify(w_rho2 * w_Lam2))
accel = m / s**2
print(f"\n  [omega_rho^2] = {sp.simplify(w_rho2)}   [omega_Lambda^2] = {sp.simplify(w_Lam2)}")
print(f"  [omega_int^2] = {sp.simplify(w_int2)}      but a floor must have [{accel}]")
check(sp.simplify(w_rho2 - 1 / s**2) == 0 and sp.simplify(w_Lam2 - 1 / s**2) == 0
      and sp.simplify(w_int2 - 1 / s**2) == 0 and sp.simplify(w_int2 - accel) != 0,
      f"G1 both posited scales, and hence their geometric mean, are frequency-SQUARED (s^-2). A floor is an "
      f"ACCELERATION (m s^-2). 'Floor = (1/2) omega_int^2' equates two different dimensions, so the argument "
      f"cannot be evaluated as written")
lit = 0.5 * math.sqrt((G * rho_L) * (c**2 * Lam))               # the literal (1/2) omega_int^2, in s^-2
check(abs(lit / a0) < 1e-20,
      f"G2 and the literal number is {lit:.3e} s^-2 against a0 = {a0:.3e} m s^-2 -- a ratio of {lit/a0:.2e}, so "
      f"the apparent match is an artefact of reading 'c sqrt(G rho Lambda)' as the framework's "
      f"'c sqrt(G rho_Lambda)'. They are different expressions")

# ---- G3  the charitable repair, in accelerations ---------------------------------
a_rho = c * math.sqrt(G * rho_L)                                # m/s^2
a_Lam = c**2 * math.sqrt(Lam)                                   # m/s^2
gm = 0.5 * math.sqrt(a_rho * a_Lam)
print(f"\n  repair: a_rho = {a_rho:.4e}, a_Lambda = c^2 sqrt(L) = {a_Lam:.4e}, (1/2)sqrt(product) = {gm:.4e}")
check(abs(gm / a0 - (8 * math.pi) ** 0.25) < 1e-6,
      f"G3 redone with ACCELERATIONS, whose geometric mean is dimensionally legitimate, the construction gives "
      f"{gm:.4e} = {gm/a0:.4f} x a0 -- and that overshoot is exactly (8 pi)^(1/4) = {(8*math.pi)**0.25:.4f}, "
      f"pinned to 1e-6. So the repaired argument misses kappa = 1/2 by a factor 2.236, and misses it by a "
      f"FACTOR OF 8 pi TO A POWER, which is the tell for G4")

# ---- G4  the two scales are one scale -------------------------------------------
Lm, rL, cs, Gs = sp.symbols("Lambda rho_L c G", positive=True)
sub = {Lm: 8 * sp.pi * Gs * rL / cs**2}
ratio = sp.simplify((Gs * rL) / (cs**2 * Lm).subs(sub))
gmean = sp.simplify(sp.sqrt((Gs * rL) * (cs**2 * Lm).subs(sub)) / (cs**2 * Lm).subs(sub))
print(f"\n  omega_rho^2 / omega_Lambda^2 = {ratio}      geometric mean / omega_Lambda^2 = {gmean}")
check(sp.simplify(ratio - 1 / (8 * sp.pi)) == 0 and sp.simplify(gmean - 1 / sp.sqrt(8 * sp.pi)) == 0,
      f"G4 *** Lambda = 8 pi G rho_Lambda/c^2 IDENTICALLY, so omega_rho^2 = omega_Lambda^2/(8 pi) exactly: the "
      f"two 'distinct fundamental scales' are ONE scale differing by a pure number. Their geometric mean is just "
      f"omega_Lambda^2/sqrt(8 pi) -- no interference, no new content. The construction therefore CANNOT exclude "
      f"c H_Lambda, which is the same scale times sqrt(8 pi/3). This is the corpus's own kappa-linear "
      f"relabelling theorem: every member of the family relabels and none can FORCE kappa ***")

# ---- G5  the physical story, taken seriously ------------------------------------
rho_sn = 0.1 * 1.989e30 / (3.0857e16) ** 3     # ~0.1 Msun/pc^3, solar-neighbourhood baryons, kg/m^3
boost = math.sqrt(rho_sn / rho_L)
print(f"\n  rho_local (solar nbhd baryons) = {rho_sn:.3e} kg/m^3 = {rho_sn/rho_L:.3e} x rho_Lambda")
check(boost > 300,
      f"G5 the argument's own motivation is the DETECTOR's density -- 'a galactic baryonic core'. Taken "
      f"seriously, rho = rho_local makes a0 scale as sqrt(G rho_local), which is {boost:.0f}x too large in the "
      f"solar neighbourhood alone and would vary by orders between galaxies. Substituting rho = rho_Lambda "
      f"rescues the number but discards the very physical story that was meant to exclude c H_Lambda, leaving "
      f"G4's relabelling")

# ---- G6  the 1/2 lands on a0, not on the floor ----------------------------------
floor_needed = a0 / 2
check(abs(floor_needed / (0.25 * c * math.sqrt(G * rho_L)) - 1) < 1e-12
      and abs(a0 / floor_needed - 2) < 1e-12,
      f"G6 and the 1/2 is attached to the wrong object: Milgrom's balance takes the FLOOR, which for this "
      f"framework is a0/2 = (1/4) c sqrt(G rho_L) = {floor_needed:.4e}, not a0 = (1/2) c sqrt(G rho_L). So even "
      f"granting the rest, what would be derived is off by exactly 2 from what section 3.3 requires -- the same "
      f"Z-vs-2Z slip this corpus made earlier the same day, recurring independently")

print("\n" + "=" * 100)
n = sum(1 for c_, _ in ok if c_)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c_, m_ in ok:
        if not c_:
            print(f"    - {m_}")
    sys.exit(1)
print("  Exit 0. The zero-point interference argument does NOT derive kappa = 1/2: it is dimensionally")
print("  inconsistent (G1-G2), overshoots by (8 pi)^(1/4) when repaired (G3), rests on two scales that are one")
print("  scale so it cannot exclude c H_Lambda (G4), is falsified if rho really means the detector's own density")
print("  (G5), and attaches its 1/2 to a0 rather than the floor (G6). The INSTINCT -- that the floor should be a")
print("  matter-coupled local response rather than a bare-horizon property -- is section 3.3's open question")
print("  correctly identified, and remains OPEN. kappa = 1/2 remains FITTED, NOT DERIVED.")
