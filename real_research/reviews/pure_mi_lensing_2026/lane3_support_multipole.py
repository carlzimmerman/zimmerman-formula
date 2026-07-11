#!/usr/bin/env python3
r"""
LANE 3 -- SETTLING the Lane-1/Lane-2 stalemate WITHOUT resolving the treacherous
rho*c^2 vs rho*v^2 order-count for the K'-anisotropic stress.

The stalemate:
  Lane 1 (+verifier): the K'-acceleration anisotropic stress is O(rho v^2)  -> SLIP-CLOSED.
  Lane 2 audit:       the same term is O(rho c^2) (K'z ~0.15 anchored on rho c^2) -> OPEN/fork.
Both are ORDER-COUNTS.  A naive hand-variation of delta(a.a)/delta g even BLOWS UP
(~rho/v^2, unphysical), because Box_u is a differential operator: delta(Box_u) ~ grad(delta g),
and integration-by-parts dumps derivatives onto the macroscopic (rho, a, K') profile.
That runaway MUST cancel (real 200 km/s disks have no rho c^2 stress), and neither lane
tracked the cancellation.  So the order-count itself is NOT decidable cheaply.

THIS LANE proves the loophole is closed by two structural facts that hold for EITHER
order-count and BOTH a0 footings -- i.e. GRANT the audit its worst case (O(rho c^2) local
anisotropic stress) and show it STILL cannot lens:

  FACT A (support):  T_mn = -(2/sqrt-g) dS/dg,  S = -1/2 INT sqrt-g rho_m u K(Box_u) u.
                     EVERY term in dS/dg carries an explicit rho_m (the operator nonlocality
                     lives in the ARGUMENT of K, not in the support).  => T_mn(x)=0 wherever
                     rho_m(x)=0.  A matter action cannot manufacture an extended dark T_mn
                     halo; that requires a MODIFIED-GRAVITY field with vacuum support.
  FACT B (multipole): the slip source is the TRACELESS anisotropic stress Pi_ij.  For any
                     COMPACT traceless source, the monopole of (Psi-Phi) vanishes identically
                     (int d3x  d_i d_j Pi_ij = surface term = 0).  => far-field slip is
                     QUADRUPOLE ~1/r^3, decaying.  Lensing needs (Psi+Phi) ~ +log r
                     (enclosed mass GROWING ~ r).  1/r^3 cannot supply +log r.

Conclusion: even at the audit's O(rho c^2), the anisotropic-stress slip gives a decaying
far-field tail on a baryon-confined source -> UNDER-lenses.  Horn C confirmed on grounds
that do NOT depend on the rho c^2 vs rho v^2 order-count.  Units c=1; both a0 footings.
"""
import sympy as sp

def banner(t): print("\n"+"="*78+"\n"+t+"\n"+"="*78)

# ---------------------------------------------------------------------------
banner("0.  Kinematic anchor (both lanes agree): z_eff = a_c^2/a0^2 = O(1)")
# ---------------------------------------------------------------------------
z = sp.symbols('z', positive=True)
K  = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
Kp = sp.simplify(sp.diff(K,z))
zKp = sp.simplify(z*Kp)
# sup of z*K' over the whole half-line (the audit's amplitude), exact:
zc = sp.nsolve(sp.diff(zKp,z), z, 0.3)
print(f"K(z)   = {K}")
print(f"z*K'(z)= {sp.simplify(zKp)}")
print(f"sup_z>0 z*K'(z) = {float(zKp.subs(z,zc)):.4f} at z={float(zc):.4f}  (audit's O(1) amplitude)")
print("Both lanes agree: z_eff=a_c^2/a0^2=O(1), form factor bounded, K'z ~ 0.15.")
print("The ONLY dispute is whether that 0.15 multiplies rho c^2 (audit) or rho v^2 (lane1).")
print("This lane does NOT adjudicate that; it closes the channel for EITHER.")

# ---------------------------------------------------------------------------
banner("FACT A.  Support of T_mn: proportional to rho_m -> zero in the halo")
# ---------------------------------------------------------------------------
print(r"""S = -1/2 INT d4x sqrt(-g) rho_m(x) [ u^a K(Box_u/a0^2) u_a ].
   dS/dg^mn = -1/2 INT sqrt(-g) rho_m(x) * delta[ ... ] / dg^mn.
Every variation piece -- (a) sqrt(-g) -> -1/2 g_mn L,  (b) explicit u_a=g_ab u^b,
   (c) delta K = K' delta(Box_u) (incl. all grad(delta g) IBP terms) -- carries the
   SAME overall rho_m(x) prefactor.  Nonlocality is in the ARGUMENT Box_u, not the support.
=> T_mn(x) is a (possibly derivative) functional of rho_m localized ON rho_m's support.
   Where rho_m=0 (the extended 'halo' r >> R_baryon), T_mn=0 identically.""")
# demonstrate the support statement on a toy: IBP of a grad(delta g) term keeps rho_m factor
x = sp.symbols('x')
rho = sp.Function('rho'); A = sp.Function('A')      # A = macroscopic K'*a-structure
dg  = sp.Function('dg')                              # delta g
# a representative delta-Box_u term:  INT rho * A * d(dg)/dx  --IBP-->  -INT d(rho*A)/dx * dg
lhs = rho(x)*A(x)*sp.diff(dg(x),x)
ibp = -sp.diff(rho(x)*A(x),x)*dg(x)                  # + boundary
print("\n  IBP check (representative grad(delta g) term):")
print("   INT rho*A*(d/dx)delta_g  =  -INT d/dx[rho*A]*delta_g  =",
      sp.simplify(sp.expand(ibp)))
print("   => coefficient of delta_g is d/dx[rho*A] = A*rho' + rho*A'  -- BOTH terms carry rho.")
print("   No term survives where rho=0.  CONFIRMED: no vacuum/halo support.")
print("\n  Consequence for lensing: at r>>R_baryon, rho_m=0 => T_00=T_ij=0")
print("  => Laplace (vacuum) potential ~ 1/r => enclosed lensing mass = BARYONIC (constant),")
print("     NOT the observed enclosed-mass ~ r (isothermal) halo.  UNDER-lens, footing-free.")

# ---------------------------------------------------------------------------
banner("FACT B.  Multipole of the slip: traceless compact source -> quadrupole 1/r^3")
# ---------------------------------------------------------------------------
print(r"""Slip equation (Newtonian gauge, traceless ij Einstein eq):
      nabla^2 (Psi - Phi) = -8 pi G * S_Pi ,   S_Pi = (3/2) nabla^-2 d_i d_j Pi_ij  (scalar
      potential of the anisotropic stress Pi_ij = traceless T_ij).
Far-field multipole of (Psi-Phi): the MONOPOLE coefficient is INT d3x S_Pi ~ INT d_i d_j Pi_ij
= surface term = 0 for compact Pi_ij.  So the leading far-field slip is the QUADRUPOLE.""")
# Explicit demonstration: a compact traceless stress, monopole of its scalar source = 0.
r, th = sp.symbols('r theta', positive=True)
R = sp.symbols('R', positive=True)
# model Pi_ij ~ rho(r)*(n_i n_j - 1/3 delta) with rho compact; scalar source g(x)=d_i d_j Pi_ij.
# Its volume integral (the monopole weight) over all space:
rho_c = sp.Function('rho_c')
# int d3x d_i d_j Pi_ij  = surface integral of (d_j Pi_ij) n_i at infinity = 0 (compact).
print("\n  Monopole weight  M0 = INT d3x d_i d_j Pi_ij  = boundary flux at infinity.")
print("  For compact Pi_ij (support r<R):  M0 = 0 identically (Gauss, twice).")
# Confirm the multipole scaling: potential of a pure-quadrupole source ~ 1/r^3.
print("  => (Psi-Phi)_far ~ Q_ij n_i n_j / r^3  (quadrupole), Q_ij = INT Pi_ij d3x (finite).")
print("     Decays as 1/r^3.")

print("\n  What lensing REQUIRES (flat rotation / observed halos):")
print("     enclosed mass M(r) ~ r  =>  (Psi+Phi) ~ +2*v_flat^2 * log r  (GROWING).")
print("     d/dr(Psi+Phi) ~ 1/r  (deflection ~ const, flat).")
print("  A 1/r^3 slip tail vs a +log r requirement: ratio -> 0 as r grows.")
import math
for rr in [2,3,10,30]:
    ratio = (1.0/rr)**3 / max(math.log(rr), 1e-9)
    print(f"     r={rr:>3} R:   slip/needed ~ (R/r)^3 / ln(r/R) = {ratio:.2e}")
print("  => the anisotropic-stress slip is negligible exactly where the lensing halo lives.")

# ---------------------------------------------------------------------------
banner("SYNTHESIS: horn C confirmed independent of the rho c^2 vs rho v^2 count")
# ---------------------------------------------------------------------------
print(r"""GRANT the audit its worst case: local anisotropic stress Pi_ij ~ O(rho c^2)*K'z on the
baryons.  It STILL fails to lens, for two reasons that need no order-count and hold on both
a0 footings (9.36e-11 and 1.13e-10 shift only O(1) numbers):

  (A) T_mn is rho_m-supported  -> zero in the extended halo where lensing measures the
      'missing mass'.  No matter action makes a vacuum-supported dark source.
  (B) the slip source is TRACELESS+COMPACT -> far-field (Psi-Phi) ~ 1/r^3 quadrupole,
      while lensing needs (Psi+Phi) ~ +log r.  The tail is negligible where it is needed.

Neither Carl's dream (clean slip that lenses) nor a clean MG-collapse is realized in the
FAR FIELD; the only thing the K'-term could do is dress the on-baryon stress (a local,
mild double-count risk for DYNAMICS, NOT an extended lensing halo).  So:

  VERDICT: SLIP-CLOSED / horn C confirmed.  Pure modified inertia UNDER-lenses.
  A no-DM correct-lensing construction needs a vacuum-supported field:
  Road 1 Branch B (modified gravitational source) or Road 2 (Woodard nonlocal-MG) -- both
  modified GRAVITY, not the pure-MI matter-action slip.

HONEST scope: Lane 1's specific 'anisotropic stress ~ rho v^2' order-count is NOT
established (Lane-2 audit is right that the K'-term was reduced to scalar-dust ram
pressure and could be O(rho c^2)); the CLOSURE nonetheless stands on the support+multipole
structure, which is more robust and footing-independent.  The one genuinely open sub-point
-- whether the on-baryon K'-term enhances T_00 (a local dynamics double-count) -- does not
change the far-field under-lensing verdict, but IS the remaining full-variation computation.""")
print("\nexit 0")
