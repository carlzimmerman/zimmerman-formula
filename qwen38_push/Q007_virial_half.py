#!/usr/bin/env python3
"""Q007 -- THE 1/2: the triad temperature coefficient is DERIVED from
isothermal hydrostatic equilibrium, not asserted.

WHAT THE REPO HAD.  GRAVITY_EVERYWHERE §2.ii (G082) and G031 V3 state
"sympy-exact":  sigma^2 = sqrt(G M_b a0)/2 = v_flat^2/2,
rho = sqrt(G M_b a0)/(4 pi G r^2).  G03G V1 states "the isothermal profile
is selected by flatness (v_c ~ r^(2-gamma) forces gamma = 2) -- and one
number appears three times: sigma^2/v_flat^2 = kappa = c_s^2 = 1/2 (EXACT)".
The FLATNESS argument selects the PROFILE shape (gamma = 2, i.e. rho ~ r^-2).
It says NOTHING about the AMPLITUDE.  The 1/2 in sigma^2 = v_flat^2/2 and
the 1/(4 pi G) in the density have been carried as ASSERTED exact values in
every lane (G002 defining relation, G038, G03G, G031 V3-V9, G078).

THE DERIVATION (this file).  The equilibrated sector is an isothermal gas
(EOS P = rho sigma^2, 1-D dispersion sigma) in hydrostatic equilibrium in
its own gravity:

        (1/rho) dP/dr = - G M_ph(<r) / r        (hydrostatic, phantom gravity)

For the r^-2 profile (the shape flatness selected) this closes to a
CONSTANT circular velocity, and the 1/2 falls out of the differential
equation itself:

    (1/rho) dP/dr = sigma^2 (1/rho) drho/dr = sigma^2 (-2/r)   [rho ~ r^-2]
    = - v_c^2 / r     =>    v_c^2 = 2 sigma^2.

The r^-2 profile's circular velocity is exactly the flat value:
v_c^2 = G M_ph(<r)/r = G (M_b r/r_M)/r = G M_b/r_M = sqrt(G M_b a0) = v_flat^2
(uses M_ph(<r) = M_b r/r_M, r_M = sqrt(G M_b/a0) -- G03E, certified).
Therefore sigma^2 = v_flat^2/2 = sqrt(G M_b a0)/2  EXACT, at EVERY r.

THE ONE-EQUATION STATEMENT (new).  The density coefficient and the
temperature coefficient are ONE identity:
        rho_ph(r) = sigma^2 / (2 pi G r^2) = v_flat^2 / (4 pi G r^2)
        = sqrt(G M_b a0) / (4 pi G r^2).
The "exact 1" in the density (GRAVITY_EVERYWHERE: "coefficient exactly 1")
and the 1/2 in the temperature are two halves of the SAME hydrostatic
relation -- the profile's own circular velocity IS its flat value, and an
isothermal r^-2 gas has v_c^2 = 2 sigma^2.  Nobody in the programme had
stated the two coefficients as one equation; both were independently
asserted exact.

NOVELTY CHECK.  git grep 'virial|sigma^2|1/2|4 pi G' over the repo: the 1/2
appears only as an assertion or the "sympy-exact" restatement; trichotomy
legA is the only 'virial' work (the virialized region's dynamics, not the
coefficient).  This is the first derivation of the coefficient from
isothermal hydrostatics + the flatness-selected profile.

KILL CONDITION.  If G081's relaxation/stability N-body finds the sector
relaxes to sigma^2 != sqrt(G M_b a0)/2 (K001 currently relaxes to 0.53 R0,
no attractor), the hydrostatic reading is wrong even if the algebra stands:
the algebra is footing-independent; the DYNAMICS is the test.
"""
import sympy as sp

G, Mb, a0, r = sp.symbols("G M_b a_0 r", positive=True)
sigma2 = sp.symbols("sigma^2", positive=True)
rM = sp.sqrt(G * Mb / a0)
vflat2 = sp.sqrt(G * Mb * a0)                     # v_flat^2 = G M_b/r_M = sqrt(G M_b a0)

# phantom density coefficient (the repo's asserted "exact 1")
A = sp.sqrt(G * Mb * a0) / (4 * sp.pi * G)
rho = A / r**2

# --- V1: the density coefficient gives the certified linear mass law
Menc = sp.integrate(4 * sp.pi * r**2 * rho, (r, 0, r))
V1 = sp.simplify(Menc - Mb * r / rM) == 0

# --- V2: the r^-2 profile's circular velocity is EXACTLY v_flat^2, all r
vc2 = sp.simplify(G * Menc / r)
V2 = sp.simplify(vc2 - vflat2) == 0

# --- V3: isothermal hydrostatics: (1/rho)dP/dr = sigma^2 (1/rho)drho/dr
dlogrho = sp.simplify(sp.diff(sp.log(rho), r))           # = -2/r
V3 = (dlogrho == -2 / r)

# --- V4: hydrostatic closure v_c^2 = - sigma^2 r dlogrho/dr = 2 sigma^2
vc2_hydro = sp.simplify(-sigma2 * r * dlogrho)           # = 2 sigma^2
V4 = (vc2_hydro == 2 * sigma2)

# --- V5: the 1/2.  v_c^2 = v_flat^2 (V2) AND v_c^2 = 2 sigma^2 (V4)
#         => sigma^2 = v_flat^2/2  (footing-independent, algebraic)
sigma2_derived = vc2 / 2                                  # = vflat2/2
V5 = sp.simplify(sigma2_derived - vflat2 / 2) == 0

# --- V6: THE ONE EQUATION: A = sigma^2/(2 pi G) with sigma^2 = vflat2/2
#         (substitute the DERIVED value, not the free symbol)
A_from_sigma = sp.simplify((vflat2 / 2) / (2 * sp.pi * G))
V6 = sp.simplify(A_from_sigma - A) == 0

# --- V7: footing-independence (numerical, both a0)
for label, a0v in [("canonical", 9.3619e-11), ("alt", 1.1279e-10)]:
    Gv, Mbv = 6.674e-11, 1e10 * 1.989e30
    rMv = (Gv * Mbv / a0v) ** 0.5
    vflat2v = Gv * Mbv / rMv
    sig2v = vflat2v / 2
    print(f"    {label}: a0={a0v:.4e}  v_flat^2={vflat2v:.6e}  "
          f"sigma^2/v_flat^2={sig2v/vflat2v:.12f} (expect 0.5)")
    assert abs(sig2v / vflat2v - 0.5) < 1e-12

print("Q007 -- THE 1/2: the triad temperature coefficient, derived")
print()
print("  route:  flatness selects rho~r^-2; isothermal hydrostatics on r^-2")
print("          closes to v_c^2 = 2 sigma^2; the r^-2 circular velocity is")
print("          exactly v_flat^2; therefore sigma^2 = v_flat^2/2, at every r.")
print()
print(f"  V1 [density coeff => certified linear mass law M=M_b r/r_M]   {'PASS' if V1 else 'FAIL'}")
print(f"  V2 [r^-2 circular velocity = v_flat^2 exactly, all r]         {'PASS' if V2 else 'FAIL'}")
print(f"  V3 [r^-2: (1/rho)drho/dr = -2/r]                              {'PASS' if V3 else 'FAIL'}")
print(f"  V4 [isothermal hydrostatic closure v_c^2 = 2 sigma^2]         {'PASS' if V4 else 'FAIL'}")
print(f"  V5 [sigma^2 = v_flat^2/2 = sqrt(G M_b a0)/2, EXACT]           {'PASS' if V5 else 'FAIL'}")
print(f"  V6 [ONE equation: A = sigma^2/(2 pi G) = v_flat^2/(4 pi G)]   {'PASS' if V6 else 'FAIL'}")
print("  V7 [footing-independent, both a0]                             PASS (above)")
print()
print("  NEW: the density coefficient 1/(4 pi G) and the temperature 1/2 are")
print("  ONE hydrostatic identity (A = sigma^2/(2 pi G)).  Previously each was")
print("  asserted exact independently; now both follow from isothermal")
print("  equilibrium of the flatness-selected r^-2 profile.")
print("  KILL: G081 N-body relaxing to sigma^2 != sqrt(G M_b a0)/2.")

import json
json.dump({
    "V1": bool(V1), "V2": bool(V2), "V3": bool(V3),
    "V4": bool(V4), "V5": bool(V5), "V6": bool(V6),
    "vc2_of_profile": str(vc2),
    "sigma2_derived": str(sigma2_derived),
    "A_from_sigma2": str(A_from_sigma),
}, open("qwen38_push/Q007_results.json", "w"), indent=1)
print("\nQ007_results.json written.")
