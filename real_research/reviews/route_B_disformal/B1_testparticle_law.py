"""
ROUTE B -- DISFORMAL MATTER COUPLING TO A PREFERRED FRAME.
B1: Can a disformal effective metric g~ = C g + D (acceleration structure) reproduce the
    dS-Unruh MODIFIED-INERTIA law in the test-particle limit?

THE FRAMEWORK LAW we must hit (test particle):
    m a mu_fw(|a|/a0) = F,    mu_fw(x) = (sqrt(1+4 x^2) - 1)/(2 x)
    g_obs = sqrt(g_N^2 + g_N a0)   [the on-shell inverse of the mu_fw gate]
    a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11

KEY PHYSICS (read agentC_covariance_memo d1, JOIN_VERDICT):
  - A *conformal* m_eff(I[g]) g coupling is a CONFORMAL COLLAPSE -> photons undeflected -> data-dead,
    and by Milgrom-94 a pointwise (local) coupling is NOT genuine MI.
  - So Route B must be DISFORMAL (a D-term along a preferred direction), and the D-term must depend
    on the worldline ACCELERATION relative to A^mu to encode mu_fw.

This script tests the TEST-PARTICLE limit ONLY (the field theory + ghost + lensing come in B2/B3).
The disformal action for a point particle coupling to g~:
    S_pp = -m c integral sqrt( -g~_munu dx^mu dx^nu )
We ask: what scalar D must multiply (A.u)^2 -- where A^mu is the preferred unit-timelike frame and
u^mu = dx/dtau the worldline 4-velocity -- so that the EOM is m a mu_fw(a/a0) = F?

We work in the NONRELATIVISTIC, quasi-static limit (the regime where MOND lives): weak field,
slow worldline, A^mu ~ the rest frame, the "acceleration relative to A" reduces to the ordinary
3-acceleration magnitude a = |d^2 x / dt^2|.
"""
import sympy as sp

print("="*78)
print("B1. DISFORMAL TEST-PARTICLE LIMIT -- can the D-term reproduce mu_fw?")
print("="*78)

# --- The target gate -------------------------------------------------------
x, a, a0 = sp.symbols('x a a0', positive=True)
mu_fw = (sp.sqrt(1+4*x**2) - 1)/(2*x)
print("\nTarget gate mu_fw(x) = (sqrt(1+4x^2)-1)/(2x), x=a/a0")
print("  limits: mu_fw(x->0) =", sp.limit(mu_fw, x, 0), " (deep-MOND: mu->x)")
# expand small x
print("  series small x:", sp.series(mu_fw, x, 0, 3))
print("  series large x:", sp.series(mu_fw.rewrite(sp.sqrt), x, sp.oo, 2) if False else "mu_fw(x->oo)->1 (check):",
      sp.limit(mu_fw, x, sp.oo))

# The on-shell relation: m a mu_fw(a/a0) = F = m g_N  (F per unit mass = g_N, the Newtonian field)
# => a mu_fw(a/a0) = g_N.  Solve for a(g_N): this is g_obs = a.
gN = sp.symbols('g_N', positive=True)
# a * mu_fw(a/a0) = gN.  Let a = g_obs. Substitute mu_fw:
#   a * (sqrt(1+4 a^2/a0^2)-1)/(2 a/a0) = gN
#   a0/2 * (sqrt(1+4 a^2/a0^2)-1) = gN
g_obs = sp.symbols('g_obs', positive=True)
lhs = a0/2*(sp.sqrt(1+4*g_obs**2/a0**2) - 1)
sol = sp.solve(sp.Eq(lhs, gN), g_obs)
print("\nOn-shell: solving  a*mu_fw(a/a0)=g_N  for a=g_obs:")
for s in sol:
    print("   g_obs =", sp.simplify(s))
# the physical (positive) root should be sqrt(gN^2 + gN a0)
target = sp.sqrt(gN**2 + gN*a0)
match = [sp.simplify(s - target) == 0 for s in sol]
print("   target framework g_obs = sqrt(g_N^2 + g_N a0)")
print("   ROOT MATCHES sqrt(g_N^2+g_N a0)?", any(match))

print("""
=> CONFIRMED: the gate mu_fw is EXACTLY the inverse of g_obs=sqrt(g_N^2+g_N a0).
   So any construction that yields  a*mu_fw(a/a0)=g_N  reproduces the framework law.
""")

# --- Now: the DISFORMAL point-particle action -----------------------------
# g~_munu = C(.) g_munu + D(.) A_mu A_nu, matter (the particle) couples to g~.
# In the NR rest-frame, the particle Lagrangian from S=-m c int sqrt(-g~ dx dx) is, to leading PN:
#   L = -m c^2 sqrt(C) sqrt(1 - (something)) ...
# The cleanest way to SEE whether a disformal D-term can encode an ACCELERATION-dependent inertia:
# write the *kinetic* term the particle action produces. For a static A^mu=(1,0,0,0) (rest frame),
# g~_00 = C g_00 + D A_0^2 = -(C + D) (with g_00=-1, A_0=1). The particle's inertial mass in the
# slow-motion KE (1/2) m_inertial v^2 is set by the *spatial* part g~_ij = C g_ij = C delta_ij,
# while the potential energy is set by g~_00.  A *conformal* C affects BOTH equally (=> conformal
# collapse). The disformal D affects ONLY g~_00 (the A_mu A_nu = time-time piece in the rest frame).
#
# THE STRUCTURAL PROBLEM (compute it, do not assert): a D(scalar) that depends on FIELD scalars
# (phi, X=(d phi)^2) -- the standard disformal -- does NOT depend on the worldline's own
# acceleration. To get mu_fw(|a|/a0) the D-term must depend on a = |du/dtau|, i.e. on the SECOND
# derivative of the worldline. Test whether that is (i) achievable and (ii) Ostrogradski-safe.

print("="*78)
print("B1b. Does a field-scalar D (phi, X) reproduce mu_fw?  -> NO (structural).")
print("="*78)
t = sp.symbols('t')
xpos = sp.Function('x')(t)
m, cc = sp.symbols('m c', positive=True)
# rest-frame disformal: g~_00 = -(C + D), g~_ij = C delta. NR point-particle Lagrangian to O(v^2):
#   S = -m c int dt sqrt( (C+D) c^2 - C v^2 ) ~ -m c^2 sqrt(C+D) + (1/2) m (C/sqrt(C+D)) v^2 + ...
C, D = sp.symbols('C D', positive=True)
v = sp.symbols('v')
Lrel = -m*cc*sp.sqrt((C+D)*cc**2 - C*v**2)
Lnr = sp.series(Lrel, v, 0, 4).removeO()
print("NR expansion of -m c sqrt((C+D)c^2 - C v^2):")
print("   ", sp.simplify(Lnr))
# the coefficient of (1/2) v^2 is the INERTIAL mass:
coeff_v2 = sp.simplify(Lnr.coeff(v,2))
m_inertial = sp.simplify(2*coeff_v2)   # since term is (1/2) m_inertial v^2 => coeff = m_inertial/2
print("   inertial mass m_inertial =", m_inertial, "  (times m)")
print("   rest energy coeff =", sp.simplify(Lrel.subs(v,0)))
print("""
READ-OFF: with field-scalar C,D the inertial mass is m * C/sqrt(C+D) -- a CONSTANT along the
worldline (C,D are field values, not functions of a). It cannot equal m*mu_fw(|a|/a0), which DEPENDS
on the worldline acceleration. So the standard (Bekenstein) disformal coupling to field scalars
gives a POSITION-DEPENDENT effective mass, NOT an ACCELERATION-DEPENDENT inertia. This is exactly
the 'pointwise = conformal/modified-gravity collapse' lemma (agentC d1) generalized to disformal:
a *local* (field-scalar) disformal coupling is modified GRAVITY (a fifth force / varying mass),
NOT modified inertia. To get mu_fw you MUST put the worldline acceleration a=|du/dtau| inside D.
""")
