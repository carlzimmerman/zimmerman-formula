#!/usr/bin/env python3
"""
STEP 7 -- Final consolidation + the one place a closure could still hide, killed explicitly.
============================================================================================
The only un-killed loophole after Step 6: could the O(eps^3) MOND term match an O(eps^3) piece
of T delta S with a0 surviving as a PURE RATIONAL (not canceling, not M/eps-dependent)?
For that we must NOT tie Gradscale to a0 by hand; instead let the field be sourced self-
consistently by the strain and see what the deep-MOND EOM gives for Gradscale, then check the
leftover. This is the most honest steelman.
"""
import sympy as sp

print("="*78)
print("STEP 7: the last loophole -- self-consistent strain-sourced field, leftover rational?")
print("="*78)

eps, a0, G, Lam, c, hbar, R, dr = sp.symbols('epsilon a0 G Lambda c hbar R deltar', positive=True)
pi = sp.pi
H_L = c*sp.sqrt(Lam/3)

print("""
The deep-MOND EOM sourced by a strain 'charge' density rho_s on the horizon:
   div( |grad phi|/a0 * grad phi ) = 4 pi G rho_s.
On the strained horizon, the strain provides an effective source. Dimensionally the
strain-induced 'Newtonian' field is g_N ~ eps * cH^2 R-ish; the deep-MOND response is
   |grad phi|^2 / a0 = g_N   =>   |grad phi| = sqrt(a0 g_N).
So Gradscale = sqrt(a0 * g_N) and |grad phi|^3 = (a0 g_N)^{3/2}.
Crucially: |grad phi|^3 ~ a0^{3/2}.  Put this in the free energy:
""")
g_N = sp.symbols('g_N', positive=True)   # strain-induced Newtonian field (a0-independent)
gradmag = sp.sqrt(a0*g_N)
fdens = -(1/(12*pi*G*a0))*gradmag**3
fdens = sp.simplify(fdens)
print("  f_density = -(1/12 pi G a0)|grad phi|^3 =", fdens)
print("    => carries a0^{3/2}/a0 = a0^{1/2}.  The MOND free energy ~ sqrt(a0).")

# delta F over the near-horizon shell:
dF = fdens * 4*pi*R**2*dr
dF = sp.simplify(dF)
print("  delta F =", dF, "   (~ sqrt(a0))")

# The O(eps^3) piece of T delta S: T * (1/4) * delta A_3, with delta A_3 the cubic area
# strain (pure geometry, a0-independent). Set them equal and SOLVE FOR a0:
dA3, kgeo = sp.symbols('deltaA3 kgeo', positive=True)
TdS3 = H_L*hbar/(2*pi) * sp.Rational(1,4) * dA3
print("\n  T delta S |_(eps^3 piece) =", sp.simplify(TdS3), "   (~ a0^0, pure geometry)")
sol = sp.solve(sp.Eq(-dF, TdS3), a0)
print("\n  Solve -delta F = T delta S (eps^3) for a0:")
for s in sol:
    s = sp.simplify(s)
    print("    a0 =", s)
    rho_L = Lam*c**2/(8*pi*G)
    kap = sp.simplify(s/(c*sp.sqrt(G*rho_L)))
    print("    => kappa = a0/(c sqrt(G rho_L)) =", sp.simplify(kap))
    print("       numeric structure: does it contain extra pi (forbidden) or = 1/2?")

print("""
DIAGNOSIS of the leftover:
  Because delta F ~ sqrt(a0) (not a0^1), solving -delta F = T delta S gives a0 ~ (geometry)^2,
  i.e. a0 ~ (dA3 * H_L * G / g_N-stuff)^2.  The a0 that pops out is the SQUARE of a horizon
  quantity, so its coefficient is the SQUARE of whatever rational/geometry sits in dA3 and g_N.
  Two fatal facts:
   (1) it depends on g_N (the strain-induced Newtonian field) and dA3 (the cubic area strain) --
       arbitrary strain data, NOT pinned by the horizon alone. Different strain profiles give
       different a0. (This is the 'inverse approach' freedom: Sheykhi-Liravi 2025 Eq.8-9 build
       the entropy to MATCH a chosen MOND, leaving a0 = gamma pi M with gamma free.)
   (2) the deep-MOND sqrt(a0) scaling means the leftover is a SQUARED geometric factor, which
       generically carries pi^2 or rational^2 -- it does NOT land on the bare rational 1/2 times
       the density sqrt(G rho_L) unless the strain data are hand-chosen to make it so.
  => NO forcing. kappa remains free / strain-prescription-dependent.
""")

print("="*78)
print("CONSOLIDATED LEDGER -- every sub-route and what it forces")
print("="*78)
rows = [
 ("Local Jacobson flux (Step 2-3)", "a0 absent: 8pi fixed by Unruh/BH; a0 is matter-Lagrangian data", "NOT forced"),
 ("Energy-balance |I_phi|=T_dS S_dS (4A)", "a0 ~ M^-3 (cubic M^{3/2} inverted)", "NOT forced"),
 ("Differential first law -I_phi=Mc^2 (4B)", "a0 ~ M^-1 (M^{3/2} vs M^1 mismatch)", "NOT forced"),
 ("Horizon self-energy M=M_dS (4C)", "kappa = 12 sqrt(6) sqrt(pi) = 52.1 (extra sqrt-pi, wrong #)", "WRONG number"),
 ("Framework c^2/2R (5iii)", "kappa=1/2 but the 1/2 is INSERTED (R not a real horizon; 8pi/3 off)", "NOT forced (posit)"),
 ("O(eps^3) strain, field~a0 (6c)", "a0 cancels (vertex 1/a0 vs field scale a0); eps^3 vs eps^1", "NOT forced"),
 ("O(eps^3) strain, self-consistent (7)", "a0 ~ (strain data)^2: prescription-dependent, squared geom", "NOT forced"),
]
print(f"  {'sub-route':<42}{'result':<58}{'verdict'}")
for a,b,c_ in rows:
    print(f"  {a:<42}{b:<58}{c_}")

print("""
================================================================================
FINAL VERDICT (this route): FREEDOM PERSISTS. kappa=1/2 is NOT forced.
  The Jacobson/Clausius MOND-flux route -- including the literal off-saddle O(eps^3)
  strained-horizon free energy that the prior 'definitive null' had left as the one
  bounded open item -- does NOT pin the coefficient. It fails by a SHARPER and more
  specific mechanism than the homogeneous routes:

    * The cubic MOND vertex enters the heat/free-energy budget at O(eps^3) in the
      horizon strain (equivalently M^{3/2} in mass), while the gravitational entropy
      response is O(eps^1) (M^1). There is NO gravitational term at the vertex's order
      to balance it against -- so the balance that fixes 8pi (the O(eps) GR sector) is
      blind to a0, and the order where a0 lives has no partner.
    * Where Y != 0 (the horizon SHELL) the integral carries 4 pi, not the 4/3 sphere
      volume; where the 4/3 lives (the bulk BALL) Y = 0 (MOND-blind). The 4/3 the prior
      verdict hoped the strain might leave uncancelled is structurally unavailable.
    * The density step sqrt(G rho_L) supplies the FULL sqrt(8pi/3) -- the only legitimate
      sqrt(pi). Every prescription that yields a clean number either reproduces an a0 that
      cancels/is data-dependent, or injects an EXTRA sqrt(pi) (kappa=52.1) -- never the
      bare rational 1/2. The kappa=1/2 reading exists ONLY as the inserted 'c^2/2R'
      surface-gravity convention, with R demonstrably NOT a Schwarzschild horizon (off by 8pi/3).

  Independent literature confirmation: Sheykhi & Liravi, arXiv:2510.14345 (Oct 2025),
  the published 'MOND from horizon thermodynamics' construction, obtains a0 = gamma pi M
  with gamma 'a parameter constrained by observation' (their Eq. after (8)) -- i.e. the
  coefficient is an observational fit, mass-dependent, NOT derived. Same null, peer-reviewed.

  This MATCHES the strong prior and the two earlier workflows: the coefficient is
  structurally route-dependent. The sqrt(pi) is forced (density); the rational 1/2 is NOT.
================================================================================""")
