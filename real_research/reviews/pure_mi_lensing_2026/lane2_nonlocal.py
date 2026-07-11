#!/usr/bin/env python3
"""
LANE 2 -- THE NONLOCAL LEAD.  Does Deffayet-Esposito-Farese-Woodard (DEW)
nonlocal-metric MOND, which lenses correctly from ONE metric, provide a
PURE-MI (no DM, no medium, GW-safe) lensing channel for the framework
(a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11, nu = sqrt(1+1/y))?

This script formalizes the load-bearing structural point:
  * Light deflection depends on the SUM of the two static potentials
    (temporal 'a' = -2 Psi  and spatial 'b' = 2 Phi):  bending ~ (Psi+Phi).
  * Orbital dynamics depends ONLY on the temporal potential gradient a'.
  * Pure MODIFIED INERTIA enhances the WORLDLINE response of MASSIVE bodies
    but leaves Einstein's equations sourced by the standard baryonic T_mu_nu
    -> BOTH metric potentials stay Newtonian-baryonic -> photons (geodesics)
    see only the baryonic potential -> UNDER-LENS by the full nu factor.
  * DEW nonlocal GRAVITY modifies the LEFT (geometric) side of the field
    equations so the SPATIAL potential b is enhanced and locked to the
    temporal one (their eq.10: a = k r b', k=1) -> one metric, correct lensing.
    But this is MODIFIED GRAVITY: matter is minimally coupled and geodesic;
    the MI worldline response is GONE.

Verdict computed here: the nonlocal channel EXISTS and is GW-safe and can HOST
the framework's a0/nu, but ONLY as nonlocal MG -- it is the honest
reclassification, NOT a pure-MI channel.  A pure-MI operator (nonlocality in
the MATTER kinetic sector, framework's K(Box_u) on rho_m u) provably cannot
enhance b, because b is fixed by the standard field equations with standard
source.  To lens you must touch curvature.

Papers (exact):
  Deffayet, Esposito-Farese, Woodard, "Nonlocal metric formulations of MOND
    with sufficient lensing", Phys.Rev.D 84, 124054 (2011), arXiv:1106.4984.
  Deffayet, Woodard, "The Case for Nonlocal Modifications of Gravity",
    Universe 4 (2018) 88, arXiv:1712.05463.
  Kim, Rahat, Sayeb, Tan, Woodard, Xu, "Determining cosmology for a nonlocal
    realization of MOND", Phys.Rev.D 94, 104009 (2016), arXiv:1608.07858.
  Deffayet, Woodard, "A Nonlocal Realization of MOND that Interpolates from
    Cosmology to Gravitationally Bound Systems", JCAP 04 (2026) 081,
    arXiv:2512.10513.
"""
import numpy as np
import sympy as sp

G = 6.674e-11
c = 2.998e8
a0 = 9.36e-11            # framework canonical, cH_Lambda/Z
def nu(y):               # framework interpolation nu(y)=sqrt(1+1/y), y=g_bar/a0
    return np.sqrt(1.0 + 1.0/y)

print("="*72)
print("LANE 2: nonlocal-gravity lensing vs pure modified inertia")
print("="*72)

# ---------------------------------------------------------------------------
# 1. TWO-POTENTIAL STRUCTURE  (DEW eqs 8-11, static spherical)
#    ds^2 = -B dt^2 + A dr^2 + r^2 dOmega^2 ;  a=lnB (temporal), b=lnA (spatial)
#    orbit:   r phi_dot^2  <-  (c^2/2) a'          (temporal gradient only)
#    lensing: deflection   <-  a'  +  b'/... i.e. (Psi + Phi), BOTH potentials
# DEW eq (11):  r B'/B = r b'  = 2 v^2 / c^2   (dynamics, temporal)
# DEW eq (10):  a(r) = r b'(r)                 (locks lensing pot to dynamics)
# ---------------------------------------------------------------------------
r, GM, ap, bp, k = sp.symbols('r GM a_p b_p k', positive=True)
# Newtonian/baryonic source (DEW eq 9):  r b' = 2 GM / (c^2 r)
rb_newt = 2*GM/(sp.Symbol('c')**2 * r)
# Deep-MOND source (DEW eq 12):          r b' -> 2 sqrt(a0 GM) / c^2
rb_mond = 2*sp.sqrt(sp.Symbol('a_0')*GM)/sp.Symbol('c')**2
print("\n[1] DEW field-equation source term  r*b'(r):")
print("    Newtonian/baryonic  (eq 9) :  r b' =", rb_newt)
print("    Deep-MOND enhanced  (eq 12):  r b' =", rb_mond)
print("    Ratio MOND/Newt = sqrt(a0/g_bar) enhancement  -> enhances BOTH")
print("    potentials a,b because eq(10) a=r b' locks them (k=1 => GR-halo lensing).")

# ---------------------------------------------------------------------------
# 2. THE UNDER-LENSING OF PURE MI, made quantitative.
#    Pure MI: Einstein eqs keep STANDARD source => r b' = 2GM/(c^2 r) (baryonic)
#             => lensing potential is BARYONIC.
#    Observed (halo/MOND) lensing needs r b' = 2 sqrt(a0 GM)/c^2.
#    Deficit ratio  =  baryonic / MOND-required  =  sqrt(g_bar/a0) = sqrt(y) .
#    (equivalently 1/nu-like in deep field; this reproduces the banked
#     'pure MI under-lenses' result from the potential structure alone.)
# ---------------------------------------------------------------------------
print("\n[2] Pure-MI lensing deficit (photons see baryonic potential only):")
print("    y=g_bar/a0   nu(y)      lensing_MI/lensing_needed = sqrt(g_bar/a0)")
for y in [1e2, 1.0, 1e-2, 1e-4]:
    gbar = y*a0
    deficit = np.sqrt(gbar/a0)          # = sqrt(y); <1 in deep field => under-lens
    print(f"    {y:7.1e}   {nu(y):6.3f}     {deficit:10.4e}")
print("    Deep-MOND (y<<1): deficit -> sqrt(y) << 1  => MI under-lenses; the")
print("    missing enhancement is exactly what DEW puts into the field eqs.")

# ---------------------------------------------------------------------------
# 3. WHY MI CANNOT SUPPLY IT (the mini-theorem).
#    Massive-body EOM in MI:   nu(|a|/a0) * a_worldline = -grad Phi_bar .
#    This modifies the RESPONSE (inertia) of MASSIVE test bodies; it does NOT
#    appear in G_mu_nu = 8piG T_mu_nu, whose source T is the standard baryonic
#    stress.  Photons are null geodesics of THAT metric: their bending is fixed
#    by (Psi_bar + Phi_bar), i.e. the baryonic potentials.  No choice of a
#    matter-kinetic nonlocal operator K(Box_u)[rho_m u] changes G_mu_nu's
#    source enhancement, because that operator lives in the matter action's
#    kinetic sector and (by the framework's own construction) leaves T_mu_nu
#    of the metric equal to standard baryonic stress up to MI corrections that
#    are ~10^7 too weak (banked source-side fork).  => pure MI cannot enhance b.
# ---------------------------------------------------------------------------
print("\n[3] Mini-theorem: to enhance the LENSING potential b you must modify")
print("    the geometric (LHS) field equations = touch CURVATURE.  DEW does")
print("    this via a nonlocal function of 1/Box acting on R_ab u^a u^b (their")
print("    Z[g]).  The framework's nonlocality acts on the MATTER current")
print("    rho_m u (K(Box_u/a0^2)); it modifies inertia, not G_mu_nu's source,")
print("    so it leaves b baryonic and cannot lens.  Migrating the operator")
print("    from matter->curvature IS the reclassification MI -> nonlocal MG.")

# ---------------------------------------------------------------------------
# 4. DEW solar-system screening (their eqs 77-82): exponential, e^{-y[g]},
#    y[g] = (c/3a0)|b'| ~ >10^4 in the solar system -> MOND term exp-suppressed.
#    Contrast AeST(=MG realization the framework inherits): power-law external
#    field -> the Desmond-Hees-Famaey / Park Q2 quadrupole is a 3-15sigma
#    tension.  Woodard's EXPONENTIAL screening is *plausibly* stronger on Q2,
#    but the paper only demonstrates scalar PN suppression; the quadrupole is
#    NOT verified here.  (Honest: potential advantage over Branch B, unproven.)
# ---------------------------------------------------------------------------
print("\n[4] DEW solar-system: y[g]=(c/3a0)|b'| in solar system:")
gN_sun_earth = G*1.989e30/(1.496e11)**2   # ~ Sun accel at 1 AU
y_ss = gN_sun_earth/a0
print(f"    g_N(1AU)/a0 ~ {y_ss:.2e}  -> MOND Lagrangian ~ e^(-y) ~ e^(-{y_ss:.1e})")
print("    => exponentially screened (DEW eq 82).  Q2 quadrupole NOT verified here.")

# ---------------------------------------------------------------------------
# 5. a0 / nu are FREE-FUNCTION inputs in nonlocal MG (Deffayet-Woodard:
#    'predict any amount of weak lensing by changing k'; f(Z) is chosen).
#    So the framework's a0=9.36e-11 and nu=sqrt(1+1/y) are ACCOMMODATABLE but
#    NOT PREDICTED by the nonlocal-gravity class.  No new derivation of a0.
# ---------------------------------------------------------------------------
print("\n[5] a0, nu enter nonlocal MG as FREE-FUNCTION choices (not derived).")
print("    Framework a0=%.3e can be imported; nonlocal MG does not FORCE it." % a0)

print("\n" + "="*72)
print("VERDICT: nonlocal channel EXISTS + GW-safe + one metric + correct")
print("lensing + can host a0/nu -- but ONLY as nonlocal MODIFIED GRAVITY.")
print("It is NOT a pure-MI lensing channel; it is the honest reclassification.")
print("Pure MI leaves G_mu_nu's source standard => cannot enhance the lensing")
print("potential b => under-lenses by sqrt(y).  To lens you must touch curvature.")
print("="*72)
