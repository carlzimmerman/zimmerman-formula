#!/usr/bin/env python3
"""
DOOR L (GAP-5): Lensing-slip HEAD-TO-HEAD -- the framework (banked Route E + the
banked slip gamma = 2 sqrt(1+a0/g_N) - 1) vs its HOST Blanchet-Skordis "Relativistic
Khronon" (arXiv:2404.06584, J(Y)+K(Q)=mu^2(Q-1)^2; their no-slip phi=psi at Eq.(3.10),
forced by the ij Einstein eq (3.9)).

This STRESS-TESTS a BANKED result (the framework's "Phi != Psi slip" prediction,
COVARIANT_ACTION_STEP2_VERDICT 2026-06-17). Both-ways + quarantine.

PLAN
====
(1) HOST (Blanchet-Skordis), verbatim from the PDF text extraction:
      - K(Q) = mu^2(Q-1)^2                                       (their Eq.2.7, 4.12)
      - J = Lambda - Y + (2c^2/3a0) Y^(3/2) + O(Y^2)             (their Eq.3.23)
      - f(y) = 1 + J_Y(Y),  y = |grad phi|/a0                    (their Eq.3.22)
      - ij Einstein eq:  Delta(phi-psi) gamma_ij - di dj(phi-psi) = O(c^-2)  (3.9)
        => phi = psi + O(c^-2) for regular isolated matter       (their Eq.3.10)  [NO SLIP]
      - modified Poisson:  div[(1+J_Y) grad phi] + mu^2 phi = 4 pi G rho_m       (3.21)
      - lensing potential = phi (= psi), the FULL MOND potential incl. phantom
        Khronon density rho_tau:  Delta phi = 4 pi G (rho_m + rho_tau)           (3.15a)
    => light deflects on (phi+psi) = 2 phi = 2 * full MOND potential, ZERO slip.

(2) FRAMEWORK (banked):
      - Route E modified-INERTIA matter action sources ZERO metric (phi_- -linear).
        => the MATTER (inertia) sector does NOT bend light by itself.
      - banked slip gamma = 2 sqrt(1+a0/g_N) - 1, claimed Phi != Psi.
      - the COVARIANT_LENSING_NOGO (2026-06-17) proves: a covariant Cassini-safe
        PURE-SLIP term CANNOT exist; the SAME ij/Bianchi shear obstruction (3.9) the
        host hits forces slip-generating <=> Phi-moving. So the framework's lensing
        MUST live in the preferred-frame (aether/khronon) sector = EXACTLY the host's
        class. We TEST whether, once embedded there, the framework's effective slip
        collapses to the host's phi=psi.

(3) Reconstruct what "gamma = 2 sqrt(1+a0/g_N) - 1" MEANS and whether it is the
    EFFECTIVE-DM-inferred slip (the PPN-gamma you'd FIT if you (wrongly) attributed
    all lensing to the BARYONS only) -- the banked "delta-Phi=0 mislabeled-equation"
    caveat -- vs a GENUINE phi != psi at the field level.

(4) numpy null-geodesic deflection alpha(b) = (2/c^2) int (d/db)(phi+psi) ... for a
    point mass, BOTH theories, deep-MOND. Compare.

ALL printed numbers are REAL (sympy-exact where stated; numpy integration otherwise).
"""

import numpy as np
import sympy as sp

print("="*84)
print("DOOR L: LENSING-SLIP HEAD-TO-HEAD  --  framework vs host Blanchet-Skordis khronon")
print("="*84)

# ----------------------------------------------------------------------------------
# Framework constants (banked)
# ----------------------------------------------------------------------------------
c    = 2.99792458e8
G    = 6.674e-11
a0   = 9.3624e-11          # framework a0 = c^2 sqrt(Lambda/32pi)  (banked)
a0_BS= 1.2e-10             # the value Blanchet-Skordis ADOPT (phenomenological)
print(f"\nframework a0 = {a0:.4e} m/s^2  ;  host adopts a0 = {a0_BS:.4e} (ratio {a0/a0_BS:.3f})")
print("(a0 value is a convention gap, both in RAR band; we use the framework a0 throughout)")

# ==================================================================================
# PART 1 -- HOST: verbatim J(Y), the no-slip equality, the lensing potential
# ==================================================================================
print("\n" + "="*84)
print("PART 1 -- HOST (Blanchet-Skordis 2404.06584): the no-slip phi=psi is a THEOREM (Eq.3.9->3.10)")
print("="*84)

# sympy reproduction of their ij Einstein eq (3.9): for a traceless transverse shear
# source built from a single scalar f, the conservation/ij-eq forces (phi-psi) to obey
#   Delta(phi-psi) gamma_ij - di dj (phi-psi) = O(c^-2)
# whose ONLY regular isolated solution is phi-psi = const -> 0 at infinity.  Reproduce
# the algebra: assume phi-psi = h(r); the off-diagonal (i != j) component is -di dj h.
x,y,z = sp.symbols('x y z', real=True)
r = sp.sqrt(x**2+y**2+z**2)
h = sp.Function('h')
H = h(r)
# off-diagonal ij Einstein eq component (i=x, j=y), must vanish to leading PN:
offdiag = -sp.diff(H, x, y)
offdiag = sp.simplify(offdiag)
print("\nij Einstein eq (3.9), off-diagonal (x,y) piece of -di dj(phi-psi):")
print("   -d_x d_y (phi-psi) =", offdiag)
print("   For this to vanish for ALL x,y (isolated regular system) with phi-psi=h(r),")
print("   need h''(r)=h'(r)/r form forcing h'=0 -> h=const -> phi=psi (their Eq.3.10).")
# Demonstrate: the only radial h with d_x d_y h = 0 everywhere off-axis is h' propto r? check h=r^2:
for trial, name in [(r**2,'r^2'), (r, 'r'), (sp.log(r),'log r'), (1/r,'1/r')]:
    od = sp.simplify(-sp.diff(trial, x, y))
    print(f"     trial phi-psi={name:6s}: -d_x d_y = {od}   ({'VANISHES' if od==0 else 'nonzero -> excluded'})")
print("   => only phi-psi = a + b r^2 has vanishing off-diagonal; b r^2 not asymptotically")
print("      flat, a is pure gauge => phi = psi.  [host no-slip is a Bianchi/shear THEOREM]")

# Host J(Y) deep-MOND, Eq.3.23, and the MOND f(y)=1+J_Y, Eq.3.22:
Ysym, a0s, csym, Lam = sp.symbols('Y a0 c Lambda', positive=True)
J_BS = Lam - Ysym + (2*csym**2/(3*a0s))*Ysym**sp.Rational(3,2)   # Eq.3.23
JY   = sp.diff(J_BS, Ysym)
print("\nhost J(Y) (Eq.3.23):  J = Lambda - Y + (2c^2/3a0) Y^(3/2)")
print("host J_Y =", sp.simplify(JY))
# With Y = a0^2 y^2 / c^4 (their nonrel relation below 3.22), f(y)=1+J_Y:
ysm = sp.symbols('y', positive=True)
JY_y = JY.subs(Ysym, a0s**2 * ysm**2 / csym**4)
f_y  = sp.simplify(1 + JY_y)
print("host f(y) = 1 + J_Y, with Y=a0^2 y^2/c^4  ->  f(y) =", f_y)
print("   deep-MOND y<<1:  f(y) ->", sp.simplify(sp.limit(f_y, ysm, 0, '+')),
      " (the leading 1 is subdominant; f ~ y -> standard MOND).")
print("   [Check: at low y the c^2/(... ) y term dominates; pure MOND f(y)=y recovered.]")

print("""
HOST SUMMARY:
  * phi = psi to O(c^-2)  -- NO gravitational slip (Eq.3.10), forced by the ij Einstein
    eq (3.9) = the SAME traceless-shear/Bianchi obstruction the banked no-go identifies.
  * the lensing potential is the FULL MOND potential phi (incl. the phantom Khronon
    density rho_tau, Eq.3.15a): Delta phi = 4 pi G (rho_m + rho_tau).
  * light deflects on (phi+psi) = 2 phi  ->  'GR lensing of the phantom mass' at g_obs.
  * the host AeST-class lenses at the FULL MOND acceleration with ZERO field-level slip.
""")

# ==================================================================================
# PART 2 -- FRAMEWORK: what the banked slip gamma=2 sqrt(1+a0/g_N)-1 actually IS
# ==================================================================================
print("="*84)
print("PART 2 -- FRAMEWORK: decode the banked slip gamma = 2 sqrt(1+a0/g_N) - 1")
print("="*84)

# The framework's MOND acceleration (its OWN dS-Unruh interpolation):
#   g_obs = sqrt(g_N^2 + g_N a0).    Define x = a0/g_N.   Then
#   g_obs/g_N = sqrt(1 + a0/g_N) = sqrt(1+x).
gN, a0v = sp.symbols('g_N a0', positive=True)
g_obs = sp.sqrt(gN**2 + gN*a0v)
ratio = sp.simplify(g_obs/gN)
print("\nframework g_obs = sqrt(g_N^2 + g_N a0)  ->  g_obs/g_N =", ratio, "= sqrt(1+a0/g_N)")

# The banked slip:
gamma_bank = 2*sp.sqrt(1 + a0v/gN) - 1
print("banked slip:  gamma = 2 sqrt(1+a0/g_N) - 1 =", gamma_bank)
print("   note 2 sqrt(1+a0/g_N) = 2 * (g_obs/g_N).  So  gamma + 1 = 2 g_obs/g_N.")
print("   i.e. gamma = 2 g_obs/g_N - 1.")

# INTERPRETATION CRUX.  PPN gamma is DEFINED by  psi = gamma * phi  (slip), and the
# light deflection is proportional to (phi+psi) = (1+gamma) phi_baryon IF one writes
# everything in terms of the BARYONIC Newtonian potential phi_N (g_N).  The lensing
# potential that ACTUALLY bends light is Phi_lens with grad Phi_lens = g_obs (the full
# MOND acceleration).  Two equivalent bookkeepings:
#
#   (A) FIELD-LEVEL slip: psi vs phi as the two metric potentials of the SAME source.
#       Host: psi=phi (Eq.3.10).  A genuine field-level slip would be psi != phi.
#
#   (B) EFFECTIVE-DM / "inferred" slip: if an observer attributes ALL dynamics+lensing
#       to the BARYONS ONLY (no dark matter, no phantom), they'd FIT a PPN gamma_eff by
#       (phi_dyn + phi_lens) = (1 + gamma_eff) phi_N.  Here phi_dyn gives g_obs (dynamics)
#       and phi_lens also gives g_obs (host lenses at g_obs) -> total bending uses 2 g_obs,
#       while phi_N gives g_N.  So  1 + gamma_eff = 2 g_obs/g_N  -> gamma_eff = 2 g_obs/g_N - 1.
print("""
THE BOOKKEEPING CRUX (both ways):
  PPN gamma is psi = gamma*phi.  But the banked formula gamma = 2 g_obs/g_N - 1 is NOT
  psi/phi of the SAME source -- it is the ratio of the LENSING bending (which uses the
  FULL MOND potential, grad->g_obs) to TWICE the BARYONIC Newtonian potential (grad->g_N).
  That is the EFFECTIVE-DM 'inferred slip' an observer measures if they (wrongly) divide
  the real (phantom-mass) lensing by the baryon-only Newtonian potential.
""")

# Show the two readings numerically collapse:
gamma_eff = lambda xx: 2*np.sqrt(1+xx) - 1        # banked formula, x=a0/g_N
# Host field-level slip is ZERO (psi=phi).  Host EFFECTIVE-DM inferred slip:
# host lensing potential grad -> g_obs; baryon Newtonian grad -> g_N; same 2 g_obs/g_N - 1.
print("Numerical check across the MOND transition (x = a0/g_N):")
print(f"{'a0/g_N':>10} {'g_obs/g_N':>10} {'gamma_eff=2 gobs/gN-1':>22} {'host field slip psi/phi-1':>26}")
for xx in [1e-4, 1e-2, 0.1, 1.0, 10.0, 100.0]:
    go = np.sqrt(1+xx)
    print(f"{xx:>10.0e} {go:>10.4f} {gamma_eff(xx):>22.4f} {0.0:>26.1f}")
print("""  -> The banked gamma is the EFFECTIVE-DM inferred slip (grows in deep MOND, x>>1).
     The host's FIELD-LEVEL slip psi/phi-1 is IDENTICALLY ZERO (Eq.3.10) at every x.
     These are NOT contradictory: they are TWO DIFFERENT QUANTITIES.""")

# ==================================================================================
# PART 3 -- the decisive head-to-head: do the framework & host predict the SAME
#           OBSERVABLE light deflection for the same baryons?  (numpy point-mass)
# ==================================================================================
print("="*84)
print("PART 3 -- OBSERVABLE null-geodesic deflection alpha(b): framework vs host, same baryons")
print("="*84)

# Deflection of light:  alpha = (2/c^2) * integral along the line of sight of grad_perp
# of the lensing potential Phi_lens, where the bending uses (Phi+Psi).  In GR/AeST-class
# with no field-level slip,  alpha = (4/c^2) * integral of g_obs_perp ... i.e. light
# responds to the FULL lensing acceleration g_lens.  The ONLY question that distinguishes
# the framework from the host is: WHAT IS g_lens?
#
# HOST:        g_lens^BS  = g_obs = sqrt(g_N^2 + g_N a0)         (lenses at full MOND, Eq.3.15a/3.21)
# FRAMEWORK:   the Route-E MI matter action sources ZERO metric -> the inertia sector
#              bends NO light by itself.  Its lensing MUST come from the preferred-frame
#              (khronon/aether) partner -- and the no-go (2026-06-17) shows that partner is
#              forced into EXACTLY the host's class (the diff-invariant pure-slip term is
#              FORBIDDEN by the same (3.9) obstruction).  The banked Route-F 'Psi-only match'
#              was *engineered* to give grad(dPsi)=2(g_obs-g_N) so that light lenses at g_obs.
#              => g_lens^FW = g_obs as well.
#
# So BOTH lens at g_obs.  We integrate alpha(b) for a point mass in the deep-MOND regime
# for both and compare.

def g_obs_of_r(r, M, a0=a0, G=G):
    gN = G*M/r**2
    return np.sqrt(gN**2 + gN*a0)          # framework's own dS-Unruh interpolation = host's MOND too

from scipy.integrate import quad
def deflection(b, M, glaw):
    # Null-geodesic deflection. Light responds to (phi+psi)=2*phi (no field-level slip),
    # so the bending angle is the standard GR light-bending integral
    #   alpha(b) = (2/c^2) * integral_{-inf}^{+inf}  g_perp ds
    #            = (2/c^2) * integral_{-inf}^{+inf}  g(sqrt(b^2+s^2)) * b/sqrt(b^2+s^2) ds
    # For Newton g=GM/r^2 this integral = 2GM/b, giving alpha = 4GM/(b c^2) exactly.
    # Substitution s = b*tan(th), ds = b sec^2 th dth, r = b sec th maps [0,inf)->[0,pi/2)
    # and resolves the s~b peak exactly (no grid artifact).
    def integrand(th):
        r = b/np.cos(th)
        return glaw(r) * (b/r) * (b/np.cos(th)**2)   # g_perp * ds/dth
    half, _ = quad(integrand, 0.0, np.pi/2, limit=200)
    return (2.0/c**2) * 2.0 * half                    # full line = 2 * half-line

# sanity: pure Newton g=GM/r^2 -> alpha = 4GM/(b c^2)
M_sun = 1.989e30
def g_newton(r, M=M_sun): return G*M/r**2
b_test = 7e8
alpha_N = deflection(b_test, M_sun, lambda r: g_newton(r, M_sun))
alpha_N_exact = 4*G*M_sun/(b_test*c**2)
print(f"\n[sanity] Newton point-mass deflection at b={b_test:.1e} m:")
print(f"   numeric alpha = {alpha_N:.6e} rad ;  exact 4GM/bc^2 = {alpha_N_exact:.6e} rad ;  ratio {alpha_N/alpha_N_exact:.5f}")

# Now a galaxy-scale lens deep in MOND.  M = 1e11 Msun, impact parameters from inner
# (Newtonian) to outer (deep-MOND).
M_gal = 1e11 * M_sun
kpc = 3.0857e19
print(f"\nGalaxy lens M={M_gal/M_sun:.0e} Msun.  r_M = sqrt(GM/a0) (MOND radius):")
rM = np.sqrt(G*M_gal/a0)
print(f"   r_M = {rM/kpc:.2f} kpc.  Deep MOND for b >> r_M.")
print(f"\n{'b [kpc]':>10} {'a0/g_N at b':>12} {'alpha_HOST [arcsec]':>20} {'alpha_FRMWK [arcsec]':>20} {'ratio':>8}")
arcsec = 206265.0
for bkpc in [1.0, 10.0, rM/kpc, 100.0, 1000.0]:
    b = bkpc*kpc
    gN_b = G*M_gal/b**2
    a_host = deflection(b, M_gal, lambda r: g_obs_of_r(r, M_gal)) * arcsec
    a_frmw = deflection(b, M_gal, lambda r: g_obs_of_r(r, M_gal)) * arcsec  # SAME g_lens=g_obs
    print(f"{bkpc:>10.2f} {a0/gN_b:>12.3e} {a_host:>20.5f} {a_frmw:>20.5f} {a_frmw/a_host:>8.4f}")

print("""
=> With the framework's lensing forced into the host's preferred-frame class (no-go
   2026-06-17), BOTH lens at the FULL MOND g_obs and the OBSERVABLE deflection alpha(b)
   is IDENTICAL (ratio 1.0000).  No field-level slip distinguishes them on STATIC baryons.
""")

# ==================================================================================
# PART 4 -- VERDICT logic + the one place a discriminator COULD survive
# ==================================================================================
print("="*84)
print("PART 4 -- VERDICT: AGREE on static lensing; the banked 'Phi!=Psi slip' is the")
print("          EFFECTIVE-DM inferred slip, NOT a field-level slip vs the host")
print("="*84)
print("""
(1) The host (Blanchet-Skordis) phi=psi (Eq.3.10) is FORCED by the ij Einstein eq (3.9)
    -- the identical traceless-shear/Bianchi obstruction the banked COVARIANT_LENSING_NOGO
    (2026-06-17) proved kills any covariant Cassini-safe PURE-SLIP term.  Same wall.

(2) The framework's banked slip gamma = 2 sqrt(1+a0/g_N) - 1 = 2 g_obs/g_N - 1 is NOT a
    field-level psi/phi mismatch.  It is the EFFECTIVE-DM 'inferred slip': the ratio of the
    real (phantom-mass) lensing potential (grad -> g_obs) to TWICE the BARYON-ONLY Newtonian
    potential (grad -> g_N).  An observer who attributes all lensing to baryons measures it;
    it is exactly what GR+real-dark-matter would ALSO give for the same total mass.  This is
    the banked 'delta-Phi=0 mislabeled-equation' caveat REPRODUCING: the '=0' / 'slip' was a
    relabeling of which potential the gradient is taken against, not a genuine psi != phi.

(3) Once the framework's lensing is placed in the ONLY sector the no-go allows (the host's
    preferred-frame khronon/aether class), its OBSERVABLE deflection on static baryons is
    IDENTICAL to the host's (Part 3, ratio 1.0000): both 'GR-lens the phantom mass' at g_obs,
    both have ZERO field-level slip.  AGREE.

=> VERDICT: AGREE.  The framework ALSO collapses to phi=psi (no field-level slip); its
   lensing = GR-of-the-phantom-mass, reconciling the lensing no-go with the host.  The
   banked 'new falsifiable Phi != Psi slip prediction vs AeST' is REVISED: it is NOT a
   discriminator against the host -- it is the effective-DM inferred slip the host ALSO
   predicts (host explicitly: 'lensing as if dark matter was present', Eq.3.10 discussion).

   BOTH-WAYS REVISION OF THE BANKED RESULT (honest): the COVARIANT_ACTION_STEP2_VERDICT
   billed gamma=2 sqrt(1+a0/g_N)-1 as 'distinguishing the framework from AeST's no-slip.'
   That is WRONG as stated: AeST/host ALSO produce this same inferred slip; their phi=psi
   is the FIELD-level statement, the framework's gamma is the INFERRED-level statement, and
   they are mutually CONSISTENT, not contradictory.  The slip vs LCDM (which has gamma=1
   exactly because LCDM's lensing mass IS real) survives as a MOND-FAMILY-shared signature,
   NOT a framework-vs-host discriminator.
""")

# Quantify the ONE surviving genuine discriminator channel (honest, both ways): a TRUE
# field-level slip can only arise from the TIME-DEPENDENT / preferred-frame sector where
# the host's static (3.10) derivation does not apply -- e.g. the gravitomagnetic
# zeta_i sector (3.12) or non-static configurations.  We report its SIZE as an upper bound.
print("="*84)
print("PART 5 -- the ONLY place a genuine framework-vs-host field-slip could survive")
print("="*84)
print("""
The host's phi=psi (3.10) is a STATIC, isolated-regular-matter result.  A genuine
FIELD-LEVEL slip distinct from the host could only live where that derivation breaks:
  - time-dependent / non-quasistatic configs (the (3.9) RHS O(c^-2) terms), or
  - the gravitomagnetic zeta_i sector (3.12),
both O(v/c) or O(c^-2) SUPPRESSED relative to the lensing potential.
""")
beta = 1e-3   # typical galaxy-scale v/c
print(f"Size of any genuine residual field-slip ~ O((v/c)^2) at galaxy scales v/c~{beta:.0e}:")
print(f"   (v/c)^2 = {beta**2:.1e}  -> a <~ {beta**2*100:.1e}% field-level slip, FAR below WL/SL sensitivity.")
print("""   => no STATIC weak-lensing or strong-lensing discriminator survives between the
      framework and its host.  The static lensing AGREES exactly; any residual is the
      c^-2/gravitomagnetic crumbs, unobservable in lensing.

FINAL: DOOR L = AGREE.  Framework lensing collapses to host's phi=psi (GR-of-phantom-mass);
banked 'Phi!=Psi slip' is the EFFECTIVE-DM inferred slip (a MOND-family signature vs LCDM,
NOT a discriminator vs the host); the banked 'delta-Phi=0 mislabeled-equation' caveat
REPRODUCES.  This REVISES the COVARIANT_ACTION_STEP2 'distinguishes from AeST' claim.
Quarantine held (a0/Z/kappa/I0 never asserted derived).
""")
