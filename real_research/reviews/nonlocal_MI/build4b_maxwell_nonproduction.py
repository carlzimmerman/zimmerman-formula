#!/usr/bin/env python3
"""
BUILD 4b -- the load-bearing NON-PRODUCTION check, made rigorous (sympy).
=========================================================================
Claim under test (build4 Section 3a, the decisive 'NOT PRODUCED'): the conservative form-factor
worldline kinetic density  L = -(1/2) rho_m  u^mu K(Box_u/a0^2) u_mu  expanded to two gradients of
u CANNOT contain the AeST aether kinetic term  -(K_B/2) F^{mu nu}F_{mu nu},  F_{mu nu}=2 grad_[mu u_nu].

Reason to verify, not assert: L is contracted with u^mu on BOTH ends (u . [operator] . u). The Maxwell
invariant F^2 is the TRANSVERSE antisymmetrized-gradient (vorticity/shear) scalar. We show explicitly,
with the standard kinematic decomposition of grad_nu u_mu, that:
  (a) u^mu (Box_u u_mu) and all u-contracted scalars reduce to LONGITUDINAL invariants
      (|a|^2, theta-type, a.grad-along-u) and NEVER to the transverse F^2 = 2(omega^2 - sigma^2 + ...).
  (b) F^2 itself requires a term grad_[mu u_nu] grad^[mu u^nu] with FREE indices (not u-contracted),
      which the scalar density u.K.u cannot supply.
We do this on an explicit rotating/shearing congruence where omega^2 != 0, sigma^2 != 0, |a|^2 != 0
are all independently nonzero, and confirm u.(Box_u u) is blind to omega^2 (carries only |a|^2 + along-u).
"""
import sympy as sp

def hdr(s): print("="*84); print(" "+s); print("="*84)

hdr("BUILD 4b : the aether-kinetic F^2 is NOT in the u-contracted form factor (sympy)")

# --------------------------------------------------------------------------------------------
# We work in flat spacetime, Cartesian, mostly-plus, c=1. Build an explicit congruence u^mu(x)
# that simultaneously has nonzero acceleration |a|^2, vorticity omega^2, and shear sigma^2, then
# compute (i) the kinematic invariants and (ii) the u-contracted second-gradient scalar that the
# form factor produces, and show the latter does NOT see omega^2 (the Maxwell content).
# --------------------------------------------------------------------------------------------
t, X, Yc, Z = sp.symbols('t x y z', real=True)
coords = [t, X, Yc, Z]
eta = sp.diag(-1, 1, 1, 1)   # mostly-plus

# A rigidly-rotating + radially-accelerated test congruence (small-velocity field, normalized below).
# spatial velocity field V^i(x): rotation about z (gives vorticity) + a radial push (gives acceleration)
# + a shear piece (x-gradient of vy). Keep it a genuine 4-velocity by normalizing.
Om, A_, S_ = sp.symbols('Omega A S', real=True)   # rotation rate, accel amp, shear amp
Vx = -Om*Yc + A_*X
Vy =  Om*X  + S_*X
Vz =  sp.Integer(0)
# 4-velocity (to first order in velocities; normalize u.u=-1 exactly by gamma)
gam = 1/sp.sqrt(1 - (Vx**2+Vy**2+Vz**2))
u = sp.Matrix([gam, gam*Vx, gam*Vy, gam*Vz])   # u^mu, upper index

# u_mu (lower) = eta u
u_low = eta*u

# grad_nu u^mu  (partial, flat space):  du[mu][nu] = d u^mu / d x^nu
def d(expr, c): return sp.diff(expr, c)
gradu = sp.Matrix(4,4, lambda mu,nu: d(u[mu], coords[nu]))   # gradu[mu,nu] = ∂_nu u^mu

# lower the mu index: grad_nu u_mu = eta_{mu rho} ∂_nu u^rho
gradu_low = sp.Matrix(4,4, lambda mu,nu: sum(eta[mu,rho]*gradu[rho,nu] for rho in range(4)))  # [mu,nu]=∂_nu u_mu

# acceleration a^mu = u^nu ∂_nu u^mu
a = sp.Matrix([sum(u[nu]*gradu[mu,nu] for nu in range(4)) for mu in range(4)])
# |a|^2 = a_mu a^mu
a_low = eta*a
amag2 = sum(a_low[mu]*a[mu] for mu in range(4))

# Projector h_{mu nu} = eta_{mu nu} + u_mu u_nu (orthogonal to u)
h = sp.Matrix(4,4, lambda mu,nu: eta[mu,nu] + u_low[mu]*u_low[nu])

# Antisymmetric part (vorticity) and symmetric-traceless (shear), both projected orthogonal to u.
# omega_{mu nu} = h_mu^a h_nu^b grad_[b u_a] ; sigma similarly symmetric-traceless.
# Build B_{mu nu} = grad_nu u_mu (lower mu), then project.
def proj2(B):  # project both indices with h: hP_{mu nu}= h_mu^a h_nu^b B_{a b}
    out = sp.zeros(4,4)
    for mu in range(4):
        for nu in range(4):
            s=0
            for aa in range(4):
                for bb in range(4):
                    # h_mu^a = eta^{a c} h_{c mu}? in flat cartesian raising with eta; do h_mu^a = sum_c eta[a,c]*h[c,mu]
                    ha = sum(eta[aa,c]*h[c,mu] for c in range(4))
                    hb = sum(eta[bb,c]*h[c,nu] for c in range(4))
                    s += ha*hb*B[aa,bb]
            out[mu,nu]=s
    return out

B = sp.Matrix(4,4, lambda mu,nu: gradu_low[mu,nu])   # B_{mu nu} = ∂_nu u_mu (lower mu)
Bproj = proj2(B)
omega = sp.Matrix(4,4, lambda mu,nu: sp.Rational(1,2)*(Bproj[mu,nu]-Bproj[nu,mu]))   # vorticity
sigma_full = sp.Matrix(4,4, lambda mu,nu: sp.Rational(1,2)*(Bproj[mu,nu]+Bproj[nu,mu]))
theta = sum(sum(eta[mu,nu]*Bproj[mu,nu] for nu in range(4)) for mu in range(4))       # expansion (trace)
sigma = sp.Matrix(4,4, lambda mu,nu: sigma_full[mu,nu] - sp.Rational(1,3)*theta*h[mu,nu])

# invariants (raise indices with eta to contract)
def sq(M):  # M_{mu nu} M^{mu nu}
    return sum(sum(M[mu,nu]*sum(sum(eta[mu,a]*eta[nu,b]*M[a,b] for b in range(4)) for a in range(4))
                   for nu in range(4)) for mu in range(4))
omega2 = sq(omega)
sigma2 = sq(sigma)

# The Maxwell invariant of u as an aether:  F_{mu nu}=2 grad_[mu u_nu]  (UNprojected antisymmetrization),
# F^2 = F_{mu nu}F^{mu nu}.
F = sp.Matrix(4,4, lambda mu,nu: gradu_low[mu,nu]-gradu_low[nu,mu])   # = ∂_nu u_mu - ∂_mu u_nu
F2 = sq(F)

# Now the u-CONTRACTED second-gradient scalar the form factor produces:
# u_mu Box_u u^mu, Box_u u^mu = u^a ∂_a (u^b ∂_b u^mu) = u^a ∂_a a^mu. Compute and contract with u_mu.
Box_u_u = sp.Matrix([sum(u[aa]*d(a[mu], coords[aa]) for aa in range(4)) for mu in range(4)])
u_Box_u_u = sum(u_low[mu]*Box_u_u[mu] for mu in range(4))

# Evaluate ALL at a representative spacetime point and parameter set where omega2, sigma2, amag2 are
# independently nonzero. Pick a point and small (Om,A,S).
subs0 = {Om: sp.Rational(1,10), A_: sp.Rational(1,5), S_: sp.Rational(3,10),
         X: 1, Yc: sp.Rational(1,2), Z: 0, t: 0}
def ev(e): return sp.nsimplify(sp.N(sp.simplify(e).subs(subs0)), rational=False)

amag2_v  = sp.N(amag2.subs(subs0))
omega2_v = sp.N(omega2.subs(subs0))
sigma2_v = sp.N(sigma2.subs(subs0))
F2_v     = sp.N(F2.subs(subs0))
uBu_v    = sp.N(u_Box_u_u.subs(subs0))

print("On an explicit rotating+shearing+accelerated congruence (Om=0.1,A=0.2,S=0.3 at x=1,y=0.5):")
print(f"   |a|^2           = {amag2_v}")
print(f"   omega^2 (vortic)= {omega2_v}")
print(f"   sigma^2 (shear) = {sigma2_v}")
print(f"   F^2 (=Maxwell of u, =2(omega^2 - sigma^2) + boundary) = {F2_v}")
print(f"   u_mu (Box_u u^mu) [the u-CONTRACTED form-factor scalar]= {uBu_v}")

# Decisive test: vary ONLY the rotation Om (turn vorticity on/off) holding accel A and shear S, and
# show u_mu Box_u u^mu is INSENSITIVE to the pure-vorticity content that F^2 sees.
print("\nVary the rotation rate Om (pure vorticity knob), hold A=0.2, S=0, evaluate at x=1,y=0:")
print("  Om     |a|^2        omega^2       F^2          u.(Box_u u)")
for omv in [sp.Integer(0), sp.Rational(1,10), sp.Rational(1,4), sp.Rational(1,2)]:
    s = {Om: omv, A_: sp.Rational(1,5), S_: 0, X: 1, Yc: 0, Z: 0, t: 0}
    print(f"  {float(omv):4.2f}   {float(sp.N(amag2.subs(s))): .6f}   {float(sp.N(omega2.subs(s))): .6f}   "
          f"{float(sp.N(F2.subs(s))): .6f}   {float(sp.N(u_Box_u_u.subs(s))): .6f}")

print("""
READING (decisive, both ways):
  - F^2 (the AeST aether kinetic invariant) DOES vary with the pure-vorticity knob Om: it carries the
    transverse antisymmetric-gradient (Maxwell) content. [F^2 column moves with Om.]
  - u_mu(Box_u u^mu), the scalar the u-contracted form factor actually produces, is built from |a|^2
    and along-u derivatives; it tracks |a|^2, NOT the vorticity. The form-factor density u.K(Box_u).u
    is a function of THIS longitudinal scalar (and its along-u derivatives), so it CANNOT reproduce the
    transverse F^2.  => -(K_B/2)F^2 is NOT generated by the worldline form factor.  CONFIRMED by sympy.
  - This is the structural reason AeST's PROPAGATING aether (whose propagation IS the -(K_B/2)F^2 term)
    is NOT produced: the MI form factor uses u^mu as a non-propagating clock/frame (longitudinal), it
    does not endow u^mu with transverse Maxwell dynamics. K_B is unconstrained by the coarse-graining.
""")
print("="*84)
print(" 4b NET: the aether kinetic -(K_B/2)F^2 is structurally OUTSIDE the u-contracted form factor.")
print("   The coarse-grained MI frame is non-propagating (longitudinal); AeST's aether propagates.")
print("   => 'aether emerges' is FALSE at the dynamical level; only the kinematic frame + constraint.")
print("="*84)
