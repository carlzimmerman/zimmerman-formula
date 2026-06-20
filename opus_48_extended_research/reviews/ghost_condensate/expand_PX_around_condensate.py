#!/usr/bin/env python3
"""
evade_so41_gate -- part (a): does expanding P(X) around the condensate X0>0 (with
P'(X0)=0) genuinely produce the ghost-condensate kinetic structure -- a HEALTHY
time-kinetic term, a VANISHING ordinary (grad pi)^2 spatial term, and a k^4
dispersion -- WITHOUT requiring the *vacuum* to break SO(4,1)?

This is the technical heart of the gate-evasion claim. The SO(4,1) gate (banked
DARK_MATTER_ILLUSION wall-1 G2): a dS-INVARIANT vacuum's one-loop action can induce
only dS-invariant terms (Lambda, R), never a preferred-timelike kinetic term, because
the vacuum picks no frame. The ghost-condensate answer: the preferred frame and the
kinetic term come from expanding the (Lorentz-invariant) action P(X) around a
NON-VACUUM background <d_mu phi> = c delta_mu^0 (a matter solution), NOT from the
symmetric vacuum -> the symmetry theorem does not bind, because the term is generated
TREE-LEVEL by the background, not loop-induced by the vacuum.

We verify the ACLM (hep-th/0312099) structure with sympy, flat-space, P(X) with
X = -(d phi)^2 (signature -+++, so for a purely time-dependent background X = phidot^2 > 0).
We use the convention X = g^{mu nu} d_mu phi d_nu phi with mostly-plus metric; for a
homogeneous time background d_0 phi = c, X_bg = -c^2 < 0 ... conventions vary. To avoid a
sign-convention rabbit hole we use the ACLM-equivalent SCALAR variable
  P = P(X),  X := phidot^2 - (grad phi)^2     (so X>0 for the timelike condensate)
which is the standard ghost-condensate convention (X = (d_t phi)^2 - (nabla phi)^2).
Background: phi = c t  => X0 = c^2 > 0. Fluctuation: phi = c t + pi.
"""
import sympy as sp

print("="*78)
print("PART (a): expand P(X) around condensate X0>0, P'(X0)=0  -> ghost-cond kinetic")
print("="*78)

t, x, y, z = sp.symbols('t x y z', real=True)
c = sp.symbols('c', positive=True)          # condensate velocity <phidot> = c
# fluctuation field pi(t,x,y,z); we Taylor-expand to 2nd order in derivatives of pi
pi = sp.Function('pi')(t, x, y, z)

# X = (d_t phi)^2 - (grad phi)^2, phi = c t + pi
phidot = c + sp.diff(pi, t)
gx = sp.diff(pi, x); gy = sp.diff(pi, y); gz = sp.diff(pi, z)
X = phidot**2 - (gx**2 + gy**2 + gz**2)
X0 = c**2

# P(X): general smooth function. Expand P(X) = P(X0) + P'(X0)(X-X0) + 1/2 P''(X0)(X-X0)^2
P0, P1, P2 = sp.symbols("P0 P1 P2", real=True)   # P(X0), P'(X0), P''(X0)
dX = sp.expand(X - X0)
# Lagrangian density (flat space, the P(X) sector):
Lden = P0 + P1*dX + sp.Rational(1,2)*P2*dX**2

# Keep terms up to QUADRATIC order in pi (drop cubic+). Expand and collect.
Lden = sp.expand(Lden)

# Quadratic-in-pi part: collect by counting pi-derivative factors.
# pidot := d_t pi, gi := d_i pi. dX = 2 c pidot + pidot^2 - (gx^2+gy^2+gz^2).
# So:
#   linear in pi-deriv:  P1 * 2 c pidot   (total derivative -> drops from EOM / boundary)
#   quadratic:           P1*(pidot^2 - grad^2) + 1/2 P2 (2 c pidot)^2
#                      = P1*pidot^2 - P1*grad^2 + 2 P2 c^2 pidot^2
# => time-kinetic coeff  = P1 + 2 c^2 P2 = P'(X0) + 2 X0 P''(X0)
#    spatial-grad coeff   = -P1 = -P'(X0)
pidot = sp.diff(pi, t)
# substitute: treat the four first-derivatives of pi as independent symbols.
pd, Gx, Gy, Gz = sp.symbols('pd Gx Gy Gz', real=True)
Lsym = sp.expand(Lden).subs(
    {pidot: pd, sp.diff(pi,x): Gx, sp.diff(pi,y): Gy, sp.diff(pi,z): Gz})
Lsym = sp.expand(Lsym)
# Keep ONLY terms exactly BILINEAR in {pd,Gx,Gy,Gz} (total degree 2) -- these are the
# quadratic-fluctuation Lagrangian. Higher-degree = cubic/quartic interactions (drop);
# degree<2 = constant/total-derivative (drop). This is the standard quadratic action.
flucts = (pd, Gx, Gy, Gz)
def total_deg(term):
    return sum(sp.degree(term, gen=v) if term.has(v) else 0 for v in flucts)
Lquad2 = sp.Add(*[term for term in Lsym.as_ordered_terms() if total_deg(term) == 2])
Lquad2 = sp.expand(Lquad2)
print("\nQuadratic-fluctuation Lagrangian (bilinear part) =", Lquad2)
coeff_pd2 = Lquad2.coeff(pd, 2)
coeff_Gx2 = Lquad2.coeff(Gx, 2)

print("\nTime-kinetic coefficient  (coeff of pidot^2) =", sp.simplify(coeff_pd2))
print("   expected:  P'(X0) + 2 X0 P''(X0) = P1 + 2 c^2 P2 =", sp.simplify(P1 + 2*c**2*P2))
print("Spatial-grad coefficient  (coeff of (d_x pi)^2) =", sp.simplify(coeff_Gx2))
print("   expected: -P'(X0) = -P1 =", sp.simplify(-P1))

assert sp.simplify(coeff_pd2 - (P1 + 2*c**2*P2)) == 0
assert sp.simplify(coeff_Gx2 - (-P1)) == 0
print("\n[OK] coefficients match ACLM: time = P'+2X0 P'',  space = -P'  (mostly-minus X conv).")

print("\n--- Impose the CONDENSATE condition P'(X0)=0  (the extremum/minimum of P) ---")
sub_cond = {P1: 0}
tk = sp.simplify(coeff_pd2.subs(sub_cond))   # = 2 c^2 P2
sk = sp.simplify(coeff_Gx2.subs(sub_cond))   # = 0
print("time-kinetic coeff at P'=0:  2 X0 P''(X0) = 2 c^2 P2 =", tk)
print("spatial-grad coeff at P'=0:  -P'(X0)             =", sk)
print("""
RESULT (a): At the condensate point P'(X0)=0:
  * the ORDINARY spatial (grad pi)^2 term VANISHES identically (coeff = -P' = 0);
  * the time-kinetic term SURVIVES with coeff 2 X0 P''(X0); it is HEALTHY (no ghost,
    not infinitely strongly coupled) iff P''(X0) > 0  -> a genuine MINIMUM of P, not
    a maximum. (This is the no-ghost condition for the pi time-kinetic term.)
With (grad pi)^2 gone, the leading spatial operator is the higher-derivative
(nabla^2 pi)^2 / M^2 piece (an INDEPENDENT term in the EFT, generic & Lorentz-
breaking-allowed once the background is chosen) giving the dispersion
        omega^2 = (alpha / M^2) k^4     [ACLM ghost-condensate dispersion].
""")

print("="*78)
print("KEY LOGICAL POINT for the gate (does this need the VACUUM to break SO(4,1)?)")
print("="*78)
print("""
The preferred-frame kinetic structure above is generated at TREE LEVEL by expanding
the manifestly Lorentz-invariant action P(X) around the BACKGROUND <d_mu phi> = c
delta_mu^0. The background is a SOLUTION of the EOM (d/dt[a^3 P'(X) phidot]=0 admits
phidot=c=const), i.e. a STATE, not a property of the vacuum action.

The SO(4,1) gate G2 is a statement about what a *symmetric vacuum's one-loop action*
can INDUCE. It says: integrating out fluctuations in the dS-invariant vacuum yields
only dS-invariant local terms. The ghost-condensate kinetic term is NOT obtained that
way -- it is the SECOND VARIATION of a CLASSICAL action around a NON-INVARIANT
background. Spontaneous symmetry breaking by a background is the textbook way a
Lorentz-invariant action yields a frame-dependent spectrum (cf. a ferromagnet:
rotation-invariant Heisenberg Hamiltonian, magnetized ground state picks a direction,
magnons have a frame-dependent omega ~ k^2 dispersion). The symmetry theorem that
forbids the VACUUM from inducing the term does NOT forbid a BACKGROUND from
spontaneously generating it. So the gate, AS A SYMMETRY THEOREM ABOUT THE VACUUM,
is structurally EVADED by the condensate route.
""")
print("[a] VERIFIED: expansion of P(X) about X0 with P'=0 gives the GC kinetic structure")
print("    (healthy time-kinetic + vanishing ordinary grad term) at TREE level from a")
print("    BACKGROUND -- not from a vacuum one-loop induction. The G2 symmetry theorem")
print("    (about the VACUUM) does not bind this mechanism.")
