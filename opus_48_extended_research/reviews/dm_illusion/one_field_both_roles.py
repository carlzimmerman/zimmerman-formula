#!/usr/bin/env python3
"""
one_field_both_roles.py  (2026-06-19)

TASK (topic 'one_field_both_roles'):
  Does ONE dS-Unruh field give BOTH a0 (the J(Y) MOND/spatial term) AND the
  cold a^-3 clustering (the K(Q) dust = "dark matter")?

The AeST action (Skordis-Zlosnik 2021, arXiv:2007.00082 Eq.5), verbatim:
  S = int d^4x sqrt(-g)/(16 pi Gtilde) [ R - (K_B/2) F_munu F^munu
        + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q)
        - lambda (A_mu A^mu + 1) ] + S_m[g]
  with Q = A^mu grad_mu phi (TEMPORAL projection along the aether)
       Y = q^munu grad_mu phi grad_nu phi, q^munu = g^munu + A^mu A^nu (SPATIAL, orthogonal to A)

  ONE scalar phi, ONE aether A_mu, ONE free function F(Y,Q).

This script makes precise, both-ways, the three distinct senses of "one field both roles":
  (S1) FIELD-CONTENT sense: is it literally the same scalar phi in both terms?  -> test by inspection of Y,Q
  (S2) SHARED-ORIGIN/COUPLING sense: do a0 (Y-sector coeff) and the dust amplitude (Q-sector integration
       const I0) come from ONE coupling, so fixing one fixes the other?  -> the orthogonality test
  (S3) DERIVATION sense: does dS-Unruh DERIVE F(Y,Q) so BOTH modes have a SINGLE de Sitter origin?

We quantify each. No manufactured derivation; both-ways.
"""

import sympy as sp
import numpy as np

print("="*78)
print("ONE FIELD, BOTH ROLES?  --  a0 (Y-sector) vs cold dust (Q-sector) in AeST")
print("="*78)

# -----------------------------------------------------------------------------
# (S1) FIELD-CONTENT sense: same scalar, different projections of its gradient
# -----------------------------------------------------------------------------
print("\n--- (S1) FIELD-CONTENT: is it ONE scalar phi in both sectors? ---")
print("""
Y = q^munu d_mu phi d_nu phi  with q = g + A(x)A  -> SPATIAL gradient (perp to aether)
Q = A^mu d_mu phi                                 -> TEMPORAL gradient (along aether)

These are the two ALGEBRAICALLY INDEPENDENT scalar invariants you can build from
ONE gradient d_mu phi and ONE unit-timelike A_mu:
   (d phi)^2 = g^munu d_mu phi d_nu phi = Y - Q^2     (decomposition identity)
So {Y, Q} is a complete, orthogonal split of |grad phi|^2 by the aether.
""")
# Symbolic check of the decomposition identity Y - Q^2 = (grad phi)^2 in a local
# orthonormal frame where A = (1,0,0,0), metric = diag(-1,1,1,1).
t,x,y,z = sp.symbols('t x y z', real=True)
dphi = sp.Matrix(sp.symbols('p0 p1 p2 p3', real=True))   # d_mu phi (lower)
eta  = sp.diag(-1,1,1,1)
A_up = sp.Matrix([1,0,0,0])                              # A^mu  (A^0=1 in rest frame)
A_dn = eta*A_up                                          # A_mu = (-1,0,0,0)
# Q = A^mu d_mu phi
Q = (A_up.T * dphi)[0]
# q^munu = g^munu + A^mu A^nu  (upper)
g_up = eta.inv()
q_up = g_up + A_up*A_up.T
# Y = q^munu d_mu phi d_nu phi
Yv = (dphi.T * q_up * dphi)[0]
gphi2 = (dphi.T * g_up * dphi)[0]
identity = sp.simplify(Yv - Q**2 - gphi2)
print(f"  Q                = {sp.simplify(Q)}")
print(f"  Y                = {sp.simplify(Yv)}   (note: purely SPATIAL p1^2+p2^2+p3^2)")
print(f"  (grad phi)^2     = {sp.simplify(gphi2)}")
print(f"  Y - Q^2 - (grad phi)^2 = {identity}   (== 0 confirms the orthogonal split)")
assert identity == 0
print("""
VERDICT (S1): YES, literally ONE scalar field phi. a0 rides its SPATIAL gradient (Y),
the cold dust rides its TEMPORAL gradient (Q). Field-content unity is REAL and exact:
this is genuinely 'two modes of one field' at the level of degrees of freedom.
The aether A_mu does the splitting (Y perp A, Q along A).  <-- strongest sense the
illusion thesis can claim: no separate 'dark matter field' is added; the cluster/CMB
energy is a mode of the SAME gravitational-sector scalar that makes MOND.
""")

# -----------------------------------------------------------------------------
# (S2) SHARED-ORIGIN / COUPLING sense: does fixing a0 fix the dust amplitude?
# -----------------------------------------------------------------------------
print("--- (S2) SHARED-COUPLING: does the SAME number set a0 AND the dust amount? ---")
print("""
Background (FRW): A aligns with cosmic time => q^00 = 0 => Y = 0 IDENTICALLY on FRW.
  => the WHOLE a0 (Y^3/2) sector is INVISIBLE to the homogeneous background.
On FRW the action reduces to K(Qbar) = -1/2 F(0,Qbar), Qbar = phidot/N:
  K(Q) = -2 Lambda + K2 (Q - Q0)^2 + ...
Shift symmetry => conserved current => integrate the phi EOM ONCE:
  dK/dQ = I0 / a^3   ->   rho_dust-bar = rho0 / a^3 ,  with  8 pi Gtilde rho0 = Q0 * I0.
""")
# Symbolic: rho_dust amplitude vs Lambda and vs a0. a0 enters ONLY via the Y^3/2
# coefficient in F(Y,Q); the FRW dust amplitude is Q0*I0 with I0 an integration const.
Lam, a0, Z, K2, Q0, I0 = sp.symbols('Lambda a0 Z K2 Q0 I0', positive=True)
rho_dust0 = Q0*I0/(8*sp.pi)   # in units Gtilde=1; the load-bearing structure is the I0 dependence
print(f"  rho_dust0  (8piGtilde rho0 = Q0*I0)  ->  d/dLambda = {sp.diff(rho_dust0, Lam)}")
print(f"                                          d/d a0     = {sp.diff(rho_dust0, a0)}")
print(f"                                          d/d I0     = {sp.diff(rho_dust0, I0)}")
print("""
  d(rho_dust)/dLambda = 0  and  d(rho_dust)/d a0 = 0   STRUCTURALLY.
  The dust amplitude depends ONLY on Q0*I0; I0 is an INITIAL DATUM (integration constant
  of the shift-symmetric scalar), NOT an action coupling. Lambda enters K only as the
  additive '-2Lambda' (the CC), invisible to dK/dQ. a0 lives in the Y-sector, which is
  zero on FRW. So NOTHING that fixes a0 (or Lambda) reaches the dust amplitude.
""")

# Numerical 'why-now' coincidence check: does any dS/holographic combo of {Lambda,a0,Z,OmDE}
# land on Omega_dust/Omega_DE without a hand-tuned O(1)?
OmDE = 0.685
Om_dust = 0.265                      # ~Omega_cdm
target_ratio = Om_dust/OmDE          # ~0.387 "why-now"
Zval = np.sqrt(32*np.pi/3)           # 5.7888
cands = {
    "OmDE"            : OmDE,
    "1-OmDE (=OmM, circular)": 1-OmDE,
    "OmDE/Z"          : OmDE/Zval,
    "OmDE^(3/2)"      : OmDE**1.5,
    "1/Z"             : 1/Zval,
    "OmDE^2"          : OmDE**2,
    "(1-OmDE)/OmDE"   : (1-OmDE)/OmDE,
}
print(f"  Target why-now ratio Omega_dust/Omega_DE = {target_ratio:.3f}")
print("  Candidate dS/holographic dimensionless combos (need ~0.387, NO free O(1)):")
best = None
for k,v in cands.items():
    err = abs(v-target_ratio)/target_ratio
    flag = "  <-- closest" if (best is None or err < best[1]) else ""
    if best is None or err < best[1]: best = (k, err)
    print(f"     {k:26s} = {v:6.3f}   (off {err*100:5.1f}%)")
print(f"  Closest = {best[0]} at {best[1]*100:.0f}% off -- NONE lands without a tuned O(1).")
print("""
VERDICT (S2): NO. The two roles do NOT share a coupling. a0 (Y-sector) and the dust
amplitude I0 (Q-sector integration constant) are in PROVABLY ORTHOGONAL slots:
d(rho_dust)/d a0 = d(rho_dust)/dLambda = 0. Fixing a0 from Lambda leaves the dust
amount entirely free. 'One number for both' is FALSE -- it is one FIELD, two
INDEPENDENT data (one coupling a0, one initial constant I0). The Omega coincidence is
abundance, not unification.
""")

# -----------------------------------------------------------------------------
# Bridge-1 made explicit: a0 is absent from linear growth (so cannot source clustering)
# -----------------------------------------------------------------------------
print("--- Bridge-1 check: a0 absent from LINEAR growth (so a0-sector can't BE the dust) ---")
print("""
On the linear-perturbation level the clustering that builds the CMB 3rd peak and the
matter power spectrum is driven by delta(rho_dust) from the Q-sector. The Y^3/2 / a0
term is non-analytic in grad phi and vanishes at Y=0 (FRW) and to LINEAR order in
perturbations about Y=0 its contribution to the growth equation is higher order
(d/dY of Y^3/2 ~ Y^1/2 -> 0 as Y->0). Hence a0 'does not appear in the linear
cosmological regime' (Skordis-Zlosnik verbatim). So the a0-sector CANNOT, even in
principle, supply the linear clustering -- the dust must come from the SEPARATE
Q-sector amplitude. This is the structural reason the two roles are orthogonal.
""")
# Illustrate: derivative of Y^(3/2) at Y->0
Y = sp.symbols('Y', positive=True)
dJ = sp.diff(Y**sp.Rational(3,2), Y)
print(f"  d/dY [ Y^(3/2) ] = {dJ}  ->  limit Y->0 = {sp.limit(dJ, Y, 0)}  (vanishes: no linear a0 source)")

# -----------------------------------------------------------------------------
# (S3) DERIVATION sense: does dS-Unruh DERIVE F(Y,Q) so BOTH modes share a dS origin?
# -----------------------------------------------------------------------------
print("\n--- (S3) DERIVATION: does dS-Unruh DERIVE both modes of F(Y,Q)? ---")
print("""
What dS-Unruh DOES give (credit at full weight):
  * Y-sector: the deep-MOND limit J -> [2 lam_s/(3(1+lam_s) a0)] Y^3/2 -- the FORCED n=3/2
    sqrt-law -- matches the dS-Unruh inertia g_obs=sqrt(g_bar^2+g_bar a0). The a0 VALUE
    c^2 sqrt(Lambda/32pi) plugs into AeST's one a0 slot. (Z=cH_Lam/a0=sqrt(32pi/3)
    machine-exact.) The FORM of the Y-sector is dS-Unruh-motivated.
  * Q-sector: the dS vacuum NAMES the cosmic rest frame -> A_mu = u^mu satisfies all 3
    aether constraints. So dS-Unruh motivates the AETHER (the thing that DEFINES Q).

What dS-Unruh does NOT give (concede at full weight):
  * It does not DERIVE the Q-sector POTENTIAL K(Q) = -2Lambda + K2(Q-Q0)^2 + ... :
    the curvature K2 (the mass), the minimum Q0, and the amplitude I0 are FREE.
  * MI_KERNEL verdict: dS-Unruh does not even fix the Y-sector KERNEL theta(y) (wrong
    functional class: ratio-convolution vs absolute-scale derivative expansion; analytic
    memory, no sqrt(adot)). It pins the a0 PIECE and the deep-MOND endpoint, not the shape.
  * The aether is FOUNDED as a FRAME (non-dynamical u^mu), NOT as the dynamical FIELD A_mu
    (no kinetic term K_B, no propagating mode derived).
""")

print("="*78)
print("SUMMARY TABLE")
print("="*78)
rows = [
 ("S1 field-content: same scalar phi, two projections (Y perp A, Q along A)", "YES (exact)"),
 ("S2 shared coupling: one number sets a0 AND dust amount",                   "NO (orthogonal: d rho_dust/d a0=0)"),
 ("    -> a0 absent from linear growth (Bridge-1)",                           "TRUE (Y^3/2 derivative ->0 at FRW)"),
 ("    -> Omega_dust/Omega_DE from a dS identity",                            "NO (closest ~%d%% off)" % round(best[1]*100)),
 ("S3 derivation: dS-Unruh derives BOTH modes of F(Y,Q)",                     "PARTIAL form / NO amount+kernel"),
 ("    Y-sector FORM (sqrt-law) dS-Unruh motivated",                          "YES"),
 ("    Q-sector POTENTIAL K(Q) / amplitude I0 derived",                       "NO (free)"),
]
for a,b in rows:
    print(f"  {a:62s} {b}")

print("""
NET (both-ways):
  ONE FIELD, BOTH ROLES is TRUE in the FIELD-CONTENT sense (S1): the same gravitational-
  sector scalar phi (split by the dS-named aether into Y and Q) carries BOTH the MOND a0
  term and the cold clustering. No separate particle, no separate 'dark matter field' is
  added. THIS is the strong-illusion claim's real, defensible content: the cluster+CMB
  missing energy is a MODE of the framework's own field, not a new substance.

  But it is FALSE in the SHARED-ORIGIN sense (S2): the two modes are PROVABLY ORTHOGONAL
  -- a0 is an action coupling in the (FRW-invisible) Y-sector, the dust amount is a free
  integration constant I0 in the Q-sector; d(rho_dust)/d a0 = 0, a0 is absent from linear
  growth. Fixing a0 from Lambda does NOT fix how much 'dark matter' there is. They are two
  STRUCTURES of one field, not one structure doing two jobs.

  And only PARTIAL in the DERIVATION sense (S3): dS-Unruh motivates the Y-sector FORM and
  names the aether, but does not derive K(Q), I0, or the kernel.

  HONEST LINE held: the CMB 3rd peak still demands the Q-sector energy (CAMB-verified);
  the amount stays free; field != particle. 'Dark matter is a mode of the framework's own
  field' is the defensible illusion; 'one number / derived / pinned' is not.
""")
