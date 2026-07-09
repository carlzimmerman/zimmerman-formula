#!/usr/bin/env python3
"""
mi_oneloop_desitter.py — CAPSTONE of the one-loop dS radiative check (merged + honest).

HISTORY: v1 of this file (Gemini) had the right skeleton — the ULTRALOCALITY of Box_u
(no spatial derivatives -> 1D heat kernel x spatial delta) and the dS friction gap
-9H^2/4 — but its decisive check was a hard-coded `True`, its positivity section
tested a manifestly-positive function, and its resolvent formula silently assumed
t inside the gap. This rewrite keeps the correct skeleton and makes every PASS earned,
with the FULL computations in three committed companion scripts (all exit 0, all
adversarially verified UPHELD by independent re-derivation):
  oneloop_laneA_divergences.py  — complete Seeley-DeWitt a1/a2 divergence list on dS via
                                  the exact Herglotz measure (rho_m = m^2 phi^2 proxy)
  oneloop_laneB_mixing.py       — graviton-frame mixing with the exact dS curvature
                                  commutators (the channel flat selection rules miss)
  oneloop_laneC_positivity.py   — dressed KL positivity: real KMS convolution of the
                                  exact cut density, branch points resolved, ghost control
"""
import sympy as sp
import numpy as np
import sys

def section(t): print("\n" + "="*80 + f"\n {t}\n" + "="*80)
def check(name, cond):
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: sys.exit(1)

# ------------------------------------------------------------------ 1
section("1. SKELETON (kept from v1, verified): Box_u on dS is spatially ULTRALOCAL")
s_, H = sp.symbols('s H', positive=True)
print(" Box_u (self-adjoint realization on the dS measure) = d^2/dtau^2 + 3H d/dtau;")
print(" NO spatial derivatives -> heat kernel = K_1D(tau,tau';s) x delta^3(x-x')/sqrt(gamma).")
# similarity transform f = e^(-3H tau/2) g removes the friction: D -> d^2/dtau^2 - 9H^2/4
a = sp.symbols('alpha'); tau = sp.symbols('tau'); g = sp.Function('g')
Df = sp.exp(a*tau)*(sp.diff(g(tau),tau,2) + (2*a+3*H)*sp.diff(g(tau),tau) + (a**2+3*H*a)*g(tau))
gap = sp.simplify((a**2 + 3*H*a).subs(a, -3*H/2))
check("similarity transform kills the friction term (2a+3H=0 at a=-3H/2)", sp.simplify((2*a+3*H).subs(a,-3*H/2))==0)
check(f"spectral gap = {gap} = -9H^2/4 (dS friction GAPS the 1D operator)", gap == -sp.Rational(9,4)*H**2)
print(" => coincident 1D kernel (4 pi s)^(-1/2) e^(-9H^2 s/4): positive, convergent.")
print(" CAVEAT fixed from v1: the proper-time resolvent formula holds only for spectral")
print(" parameter above the gap; the rest of the Herglotz support uses the retarded/normal")
print(" prescription (operator_definition.py) — handled correctly in laneA via the measure.")

# ------------------------------------------------------------------ 2
section("2. a0 IS NOT RENORMALIZED (exact-measure level, not just the naive series)")
z, t = sp.symbols('z t', positive=True)
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
check("no z^0 tadpole in K (series starts at sqrt(z))", sp.series(K, z, 0, 2).removeO().coeff(z,0)==0)
# the NEW sum rule (laneA, verified to 1e-12): INT dmu/|t| = K(inf)-K(0) = 1 (unit resolvent
# weight — the superposition has no spare weight to feed a tadpole). Reproduce numerically:
from scipy import integrate as si
rhoA = lambda u: (1-np.sqrt(1-4*abs(u)))/(2*np.pi*np.sqrt(abs(u)))   # -1/4<t<0
rhoB = lambda u: 1/(2*np.pi*np.sqrt(abs(u)))                          # t<-1/4
M1  = si.quad(lambda u: rhoA(-u)/u, 1e-12, 0.25, points=[0.25], limit=400)[0] \
    + si.quad(lambda u: rhoB(-u)/u, 0.25, np.inf, limit=400)[0]
print(f"   sum rule INT dmu(t)/|t| = {M1:.6f}  (exact value 1: unit resolvent weight)")
check("sum rule M_-1 = 1 to <1e-3 (laneA/mpmath: 1e-12)", abs(M1-1) < 1e-3)
print(" => divergences are polynomial in W=u.K u with a0 only inside W's argument:")
print("    a0 is neither additively nor multiplicatively renormalized (matter loop, proxy).")

# ------------------------------------------------------------------ 3
section("3. NO TRANSVERSE (grad u)^2 COUNTERTERM — the v1 hard-coded check, now EARNED")
print(" (a) THEOREM (replaces v1's `check(True)`): on dS the linear delta-u vertex vanishes")
print("     at EVERY resolvent order, via the geodesy identity u.(u.grad)^n V = (u.grad)^n(u.V).")
# verify the identity symbolically in a 1+1 flat-slicing dS model (n=1,2):
tt, xx = sp.symbols('t x'); Hs = sp.symbols('H', positive=True)
asc = sp.exp(Hs*tt)                          # scale factor
gdn = sp.diag(-1, asc**2)                    # metric
gup = gdn.inv()
# Christoffels
def Gamma(l,m,n):
    return sum(gup[l,r]*(sp.diff(gdn[r,m],[tt,xx][n]) + sp.diff(gdn[r,n],[tt,xx][m]) - sp.diff(gdn[m,n],[tt,xx][r]))/2 for r in range(2))
u_up = sp.Matrix([1,0])                      # comoving frame (geodesic on dS)
V0, V1 = sp.Function('V0')(tt,xx), sp.Function('V1')(tt,xx)
V = sp.Matrix([V0, V1])
def udotgrad_vec(W):                        # (u.grad) of a vector field
    out = sp.zeros(2,1)
    for l in range(2):
        out[l] = sp.diff(W[l], tt) + sum(Gamma(l,0,n)*W[n] for n in range(2))
    return sp.simplify(out)
u_dn = gdn*u_up
lhs1 = sp.simplify((u_dn.T*udotgrad_vec(V))[0])                 # u.( (u.grad)V )
rhs1 = sp.simplify(sp.diff((u_dn.T*V)[0], tt))                  # (u.grad)(u.V)
check("geodesy identity u.(u.grad)V = (u.grad)(u.V)  [n=1, exact]", sp.simplify(lhs1-rhs1)==0)
lhs2 = sp.simplify((u_dn.T*udotgrad_vec(udotgrad_vec(V)))[0])
rhs2 = sp.simplify(sp.diff((u_dn.T*V)[0], tt, 2))
check("geodesy identity at n=2 (exact)", sp.simplify(lhs2-rhs2)==0)
print("     => sandwiching on u_mu makes the linear vertex a total (u.grad)-chain on (u.V):")
print("        with delta_u.u=0 (unit norm) it vanishes identically — ALL resolvent orders.")
print(" (b) QUADRATIC order (laneA + verifier, incl. the cross-chain + du2 pieces the first")
print("     scan missed): every structure is nonzero but LONGITUDINAL-only; the (du.grad)(du.grad)")
print("     sandwich collapses to the algebraic mass term -H^2 a^2 psi^2. No (grad_perp u)^2.")
print(" (c) CURVATURE CHANNEL (laneB): R_{mu a nu b} u^a u^b = -H^2 P_perp — curvature DOES make")
print("     transverse structure, but commutator insertions are ALGEBRAIC (k0^2 -> H^2, never")
print("     kperp^2): all characteristic roots k-INDEPENDENT (n=2: {0, ±sqrt7 H}), NO wave cone;")
print("     the khronon kperp^2 overall factor survives on dS; k^3/k^4 terms identically absent.")
print(" (d) GRAVITON LINE (laneB verifier): the TT-graviton x delta_u_perp vertex is EXACTLY ZERO")
print("     (CAS, n=1,2, both polarizations; the constrained h_0i control vertex is nonzero, so")
print("     the probe is not vacuous). Only instantaneous constrained mixing survives (no cone).")

# ------------------------------------------------------------------ 4
section("4. WHAT *IS* GENERATED (reported, not waved away) — coefficients per 1/(16 pi^2 eps)")
print("   O_W  = s m^4 W          : vacuum energy renormalizes the SOURCE rho_m through the")
print("                             framework's own form factor (a0, s, K untouched)")
print("   O_WW = (s^2 m^4/2) W^2  : new, longitudinal-only, starts O(du^4) on dS")
print("   O_RW = -(s/6) m^2 R W   : curvature-cross term; O_RW/O_W = 2H^2/m^2 ~ 3e-84 (proton)")
print("   O_BoxW                  : total derivative (no bulk term)")
print("   NOT generated: any a0-dependent counterterm; any transverse (grad_perp u)^2 term.")

# ------------------------------------------------------------------ 5
section("5. DRESSED KL POSITIVITY (v1's decorative check replaced by the real convolution)")
print(" laneC computes the ACTUAL one-loop KMS convolution of the exact Herglotz cut density")
print(" (T = H/2pi, branch points resolved to 1e-6 offsets, adaptive quadrature 1e-10):")
print("   rho_dressed(w) >= 0 EVERYWHERE, both footings; KMS detailed balance to 4e-12;")
print("   UV: dressed continuum sign-definite, linear growth verified to 0.14% vs analytic;")
print("   GHOST CONTROL: an O(1) injected negative line IS flagged (threshold measured:")
print("   integrated weight ~0.15 is the blind spot -> positivity is necessary, NOT sufficient).")
mini = si.quad(lambda u: rhoA(-u), 1e-12, 0.25)[0]
check(f"cut density integrable at the branch point (INT rho_A = {mini:.4f} > 0)", 0 < mini < 1)

# ------------------------------------------------------------------ 6
section("CONCLUSION (scoped — the phrase 'the loop edge is closed' from v1 is RETRACTED)")
print("""
 One-loop dS radiative structure: SUBSTANTIALLY CLOSED at the DIVERGENCE level.
   COMPUTED: complete matter-loop divergence list (Gilkey a1/a2, exact under the stated
   rho_m = m^2 phi^2 proxy); a0 unrenormalized (exact measure, unit resolvent weight);
   linear vertex zero at all orders (theorem); no transverse aether kinetic term; the
   graviton-frame mixing channel closed (algebraic commutators, k-free roots, TT vertex
   zero); dressed KL positivity + detailed balance preserved. Both footings; nothing flips.
   STILL OPEN (named): the T_uu/disformal rho_m variant (argued, not computed); one-loop
   FINITE nonlocal parts + light-field IR on dS; all-n TT-vertex proof (CAS n=1,2);
   pure-graviton diagrams beyond selection-rule coverage; two loops; sub-threshold-ghost
   blind spot. Sign s=-1, a0, Z remain INPUTS. NOT 'theory closed'.
""")
print("exit 0"); sys.exit(0)
