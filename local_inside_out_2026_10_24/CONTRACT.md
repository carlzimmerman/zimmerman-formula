# LIO-1: local inside-out formation with interface energy

Base revision f19bcf139fd7e3a219d429bdfa665ffceefd045d. Continue FT-I,
not the rejected uniform-phase pumping scans. Goal: form and preserve the
baryonic galaxy law with local conversion and a freely gravitating exterior.
Use the inherited canonical a0, beta20 and phase energy
Egrad=a0² ell²/(2G) integral r² (dx/dr)² dr, qT=sin²(pi x/2).
The inherited protection example used ell=30 kpc. Do not silently reduce it.

## Routes and decisive tests

1. Interface capacity: derive the minimum gradient energy for qT>=.95 at
   r=Rin and qT<=.05 at Rout, allowing the cheapest smooth spherical profile.
   Rout=infinity is the most favorable exterior. Test Rin=.5b,2b,5b for
   the four numeric parent mass/size profiles. Compare to declared binding
   energy proxies; those proxies are not universal bounds on arbitrary
   energy sources or arbitrarily compact baryonic collapse.
2. Protection/formation compatibility: compute the minimum ell needed for
   linear stability of the prepared parent T state at f=.95,beta20 using
   its actual nonuniform phase Hessian. Compare to the energy-admissible
   ell interval, preserving the local/global distinction. Granting the
   parent law density here is a necessary end-state test, not formation.
3. Local-interface dynamics and force: only after the cost is known,
   construct and test a finite local bubble with free exterior, including
   field mass, gradient pressure and reciprocal work. Measure the actual
   acceleration against the baryon-only law; phase formation alone is not
   success. Do not assume the old protected uniform endpoint survives a wall.

## First finite computation

Parent profiles; Rin/b=.5,2,5; qin=.95,qout=.05. Compute the exact analytic
capacity bound, independent SI normalization check, and the parent prepared
state stability threshold at n64,128,256 using its inherited uniform radial
mesh. Sample ell from1e-6 to1e4 kpc then bracket the zero eigenvalue; preserve
the case of no stable ell rather than assuming stiffness can stabilize all
profiles. Beta20, f=.95. No parameter is selected using an observational fit.

Energy proxies in G Mb²/b: 1,10,100, plus the initial shell energy magnitude
about1.29 from FT-I. They are explicitly hypothetical assembly work budgets.
A capacity violation against these does not prove all real formation
impossible. Compute the minimum required work rather than hiding the budget.

Checks: Cauchy-Schwarz equality profile x=a+b/r, its quadrature energy and
boundary values; SI-to-galactic units; stability eigenvalue signs bracketed;
refinement of thresholds. Source snapshots are hashed. Review is self-review.
No cosmological initial-state, 3D stability, thermal lifetime or microscopic
derivation is claimed. A local open exterior differs from the parent's
no-flux uniform T stability problem; compare them, do not equate them.
