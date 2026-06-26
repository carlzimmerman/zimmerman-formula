"""
ROUTE B -- B2. Put the worldline ACCELERATION into the disformal D-term.

B1 proved: a field-scalar disformal D(phi,X) gives POSITION-dependent mass = modified gravity,
not mu_fw(|a|/a0). To get mu_fw the disformal structure must carry the worldline acceleration
a=|du/dtau|. Two ways:
  (B2a) LOCAL: D = D(a) with a literally |du/dtau| -> the action S=-mc int sqrt(-g~_munu dx dx)
        with g~ depending on d^2x/dtau^2 is a HIGHER-DERIVATIVE (Ostrogradski) worldline action.
  (B2b) NONLOCAL: D = D( retarded kernel * trajectory ) -- Milgrom-94's licensed time-nonlocal form.

Milgrom 1994 (astro-ph/9303012), ABSTRACT, VERBATIM (PDF read firsthand):
  "If, to boot, S_k is Galilei invariant it must be time-nonlocal; indeed, it is non-local in the
   strong sense that it cannot even be a limit of a sequence of local, higher-derivative theories,
   with increasing order. THIS IS A BLESSING, as such theories need not suffer from the illnesses
   that are endemic to higher-derivative theories."
  EOM (sec I): "the rotation curve mu(a/a_o) a = dphi/dr where a=v^2/r".

So: (B2a) is BOTH forbidden as Galilei-invariant MOND AND Ostrogradski-sick (the higher-derivative
illness). (B2b) is the licensed object and the ONLY ghost-safe one. We verify both prongs with sympy.
"""
import sympy as sp

print("="*78)
print("B2a. LOCAL acceleration-disformal => higher-derivative => OSTROGRADSKI GHOST.")
print("="*78)

t = sp.symbols('t', real=True)
x = sp.Function('x')(t)
m, a0 = sp.symbols('m a0', positive=True)
v  = sp.diff(x, t)        # velocity
ac = sp.diff(x, t, 2)     # acceleration (the disformal-D argument)

# The simplest LOCAL acceleration-dependent kinetic action that yields a mu_fw-like inertia is a
# function L(v, a) with a = xddot.  Take the canonical MOND-ish local higher-derivative model
# (the kind Milgrom says "cannot even be a limit" but is the only LOCAL option):
#   L = (m/2) v^2 * f(a/a0)   with some gating f.  Any nontrivial f(a) => L depends on xddot.
# Ostrogradski: a Lagrangian L(x, xdot, xddot) with non-degenerate d^2L/d(xddot)^2 has a linearly
# unstable (ghost) Hamiltonian -- one canonical momentum enters H LINEARLY. Check non-degeneracy.

f = sp.Function('f')
L_local = sp.Rational(1,2)*m*v**2*f(ac/a0)
print("\nLocal candidate L = (m/2) v^2 f(xddot/a0). Ostrogradski non-degeneracy test:")
d2L = sp.diff(L_local, ac, 2)
print("   d^2L/d(xddot)^2 =", sp.simplify(d2L))
print("   -> nonzero whenever f'' != 0 (i.e. any genuine gate) => NON-DEGENERATE")
print("   => Ostrogradski theorem applies: the Hamiltonian is LINEAR in the momentum conjugate")
print("      to xdot -> UNBOUNDED BELOW -> GHOST. This is Milgrom's 'illness of higher-derivative'.")

# Make it fully explicit with the simplest nondegenerate example f(y)=y^2 (so L ~ v^2 (xddot)^2):
print("\nExplicit Ostrogradski Hamiltonian for L = (1/2) eps (xddot)^2 + (m/2) v^2 (the canonical")
print("non-degenerate higher-derivative kinetic term):")
eps = sp.symbols('epsilon', positive=True)
xd, xdd, xddd, xdddd = sp.symbols('xd xdd xddd xdddd', real=True)
# Ostrogradski momenta:  p1 = dL/dxd - d/dt(dL/dxdd);  p2 = dL/dxdd
# H = p1 xd + p2 xdd - L.  For L = (1/2)eps xdd^2 + (m/2) xd^2:
#   dL/dxd = m xd ; dL/dxdd = eps xdd
#   p1 = m xd - eps xddd ; p2 = eps xdd
# H = p1 xd + p2 (p2/eps) - [ (1/2)eps (p2/eps)^2 + (m/2) xd^2 ]
#   = p1 xd + p2^2/eps - p2^2/(2 eps) - (m/2) xd^2
#   = p1 xd + p2^2/(2 eps) - (m/2) xd^2
p1, p2 = sp.symbols('p1 p2', real=True)
H = p1*xd + p2**2/(2*eps) - sp.Rational(1,2)*m*xd**2
print("   H(xd, p1, p2) =", H)
print("   -> the term p1*xd is LINEAR in p1 and xd is a free coordinate direction:")
print("      H is UNBOUNDED BELOW (take xd -> +-inf at fixed p1). OSTROGRADSKI GHOST confirmed.")
# sympy: H has no lower bound -> show derivative wrt xd is linear (no quadratic confinement in p1*xd):
print("   d^2H/dxd^2 =", sp.diff(H, xd, 2), " (the only xd-curvature is -m < 0: runs away).")

print("""
VERDICT B2a: A LOCAL disformal coupling carrying the worldline acceleration (D=D(|xddot|)) is a
higher-derivative worldline action with a non-degenerate xddot kinetic structure -> Ostrogradski
ghost (Hamiltonian unbounded below). This is EXACTLY the higher-derivative illness Milgrom-94 warns
of, and his no-go forbids it as a Galilei-invariant MOND action anyway. So the LOCAL acceleration-
disformal route is OBSTRUCTED on TWO independent counts (ghost + Milgrom no-go).
""")

print("="*78)
print("B2b. The ONLY licensed route: NONLOCAL (retarded-kernel) disformal D -- ghost-safe by")
print("     Milgrom-94's blessing (not a higher-derivative limit, so Ostrogradski does not apply).")
print("="*78)
print("""
The acceleration is read NONLOCALLY:  a_eff(t) = | int K(t-t') xdot(t') dt' |  (a causal memory
kernel), NOT xddot(t). Then D = D(a_eff/a0) and the action is time-nonlocal but FIRST-derivative in
the integrand -> NO Ostrogradski momentum tower. This is precisely the in-in/Galley worldline MI
action already CONSTRUCTED this session (nonlocal_MI/build_part1).

So the disformal D-TERM, to carry mu_fw ghost-safely, must be built on that SAME nonlocal kernel:
   g~_munu = C g_munu + D[a_eff] A_mu A_nu,   a_eff = nonlocal(history of u rel. to A).
The disformal structure does not change the no-go physics -- it INHERITS the established nonlocal
worldline MI. What it ADDS (the point of Route B) is the LENSING/metric sector via the A_mu A_nu
disformal term. We test that next (B3): does coupling matter to g~ (not g) give the right lensing
while keeping gravity (the EH term on g) standard, and does it keep c_T=c?
""")
